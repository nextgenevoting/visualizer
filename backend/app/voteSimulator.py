from chvote.Common.SecurityParams import secparams_l1
from app.models.electionAuthorityState import ElectionAuthorityState
from app.models.voterState import VoterState
from app.parties.ElectionAuthority import ElectionAuthority
from app.database import db, serializeState
from app.parties.BulletinBoard import BulletinBoard
from app.parties.PrintingAuthority import PrintingAuthority
from app.parties.Voter import Voter
from bson.objectid import ObjectId
from app.main.syncService import syncElectionStatus, SyncType

class VoteSimulator(object):

    def __init__(self, election):
        self.electionID = election
        self.secparams = secparams_l1

        # Parties
        self.authorities = [None] * self.secparams.s
        self.bulletinBoard = BulletinBoard(db.bulletinBoardStates, election)
        self.printingAuthority = PrintingAuthority(db.printingAuthorityStates, election)
        self.voters = []

        # create new election authorities
        for j in range(self.secparams.s):
            self.authorities[j] = ElectionAuthority(db.electionAuthorityStates, election, j)

        # create voters
        for i in range(len(self.bulletinBoard.voters)):
            self.voters.append(Voter(db.voterStates, election, i))

        print("init sim done")

    def persist(self):
        self.bulletinBoard.persist()
        for authority in self.authorities:
            authority.persist()

        self.printingAuthority.persist()

        for voter in self.voters:
            voter.persist()

    def updateStatus(self, newStatus):
        assert isinstance(newStatus, int), "status must be a number"
        # update election status
        db.elections.update_one({'_id': ObjectId(self.electionID)}, {"$set": {"status" : newStatus}}, upsert=False)
        syncElectionStatus(self.electionID, SyncType.ROOM)

    def setupElection(self, numberOfVoters, w_bold, c_bold, n_bold, k_bold):
        self.bulletinBoard.countingCircles = w_bold
        self.bulletinBoard.candidates = c_bold
        self.bulletinBoard.numberOfCandidates = n_bold
        self.bulletinBoard.numberOfSelections = k_bold

        voters = []
        for v in range(numberOfVoters):
            newVoter = VoterState(v+1)
            newVoter.countingCircle = w_bold[v]
            db.voterStates.insert({'election': self.electionID, 'voterID': v, 'state': serializeState(newVoter)})
            voters.append(newVoter.name)
        self.bulletinBoard.voters = voters

        # 7.1 Generation of electorate data
        for authority in self.authorities:
            authority.GenElectionData(self.bulletinBoard, self.secparams)


        # 7.3 Key generation
        self.bulletinBoard.publicKeyShares = []

        for authority in self.authorities:
            publicKeyShare = authority.GenKey(self.bulletinBoard, self.secparams)
            self.bulletinBoard.publicKeyShares.append(publicKeyShare)
        for authority in self.authorities:
            pk = authority.GetPublicKey(self.bulletinBoard, self.secparams)
        self.bulletinBoard.publicKey = pk

        # 7.2 Send secret voter data to the printing authority (this is typically done in the printVotingCards(), but since we want to show the secret voter data before printing the cards, we do it here)
        privateCredentials = []
        for authority in self.authorities:
            privateCredentials.append(authority.secretVotingCredentials)
            self.printingAuthority.privateCredentials = privateCredentials


    def printVotingCards(self):
        # 7.2 Printing of voting cards
        self.printingAuthority.PrintVotingCards(self.bulletinBoard, self.secparams)

    def sendVotingCards(self):
        # 7.2 Printing of voting cards contd.
        for voter in self.voters:
            voter.votingCard = self.printingAuthority.votingCards[voter.id-1]   # id = index + 1  --> (1,2,3...)