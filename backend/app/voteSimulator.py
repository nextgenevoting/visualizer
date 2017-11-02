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
from chvote.VotingClient.GenBallot import GenBallot
from chvote.Types import *
from chvote.VotingClient.GetPointMatrix import GetPointMatrix
from chvote.VotingClient.GetReturnCodes import GetReturnCodes

class VoteSimulator(object):

    # *************************************************************************************
    # *** Internal methods for loading/saving the states
    # *************************************************************************************

    # Constructor:
    # Set up the voteSim instance by instantiating all parties and loading the corresponding states from the database
    def __init__(self, electionID):
        self.electionID = electionID
        self.secparams = secparams_l1

        # load bulletinBoard
        self.bulletinBoard = BulletinBoard(db.bulletinBoardStates, electionID)

        # load printing authority
        self.printingAuthority = PrintingAuthority(db.printingAuthorityStates, electionID)

        # load election authorities
        self.authorities = [None] * self.secparams.s
        for j in range(self.secparams.s):
            self.authorities[j] = ElectionAuthority(db.electionAuthorityStates, electionID, j)

        # load voters
        self.voters = []
        for i in range(len(self.bulletinBoard.voters)):
            self.voters.append(Voter(db.voterStates, electionID, i))

    # persist()
    # Save the state of all parties to the database
    def persist(self):
        self.bulletinBoard.persist()
        self.printingAuthority.persist()
        for authority in self.authorities: authority.persist()
        for voter in self.voters: voter.persist()

    # updateStatus()
    # Helper function to update the status of an election
    def updateStatus(self, newStatus):
        assert isinstance(newStatus, int), "status must be a number"
        db.elections.update_one({'_id': ObjectId(self.electionID)}, {"$set": {"status" : newStatus}}, upsert=False)
        syncElectionStatus(self.electionID, SyncType.ROOM)


    # *************************************************************************************
    # The following functions implement the chVote protocol
    # *************************************************************************************

    # setupElection()
    # Set the pre-election parameters and generate electorate data
    def setupElection(self, numberOfVoters, w_bold, c_bold, n_bold, k_bold):
        self.bulletinBoard.countingCircles = w_bold
        self.bulletinBoard.candidates = c_bold
        self.bulletinBoard.numberOfCandidates = n_bold
        self.bulletinBoard.numberOfSelections = k_bold
        self.bulletinBoard.numberOfParallelElections = len(k_bold)

        voters = []
        for v in range(numberOfVoters):
            newVoter = VoterState(v)
            newVoter.countingCircle = w_bold[v]
            db.voterStates.insert({'election': self.electionID, 'voterID': v, 'state': serializeState(newVoter)})
            voters.append(newVoter.name)
        self.bulletinBoard.voters = voters

        self.bulletinBoard.generateEligibilityMatrix()

        # 6.1 Generation of electorate data
        for authority in self.authorities:
            self.bulletinBoard.partialPublicVotingCredentials.append(authority.GenElectionData(self.bulletinBoard, self.secparams))
        for authority in self.authorities:
            authority.GetPublicCredentials(self.bulletinBoard, self.secparams)

        # 6.3 Key generation
        self.bulletinBoard.publicKeyShares = []

        for authority in self.authorities:
            publicKeyShare = authority.GenKey(self.bulletinBoard, self.secparams)
            self.bulletinBoard.publicKeyShares.append(publicKeyShare)
        for authority in self.authorities:
            pk = authority.GetPublicKey(self.bulletinBoard, self.secparams)
        self.bulletinBoard.publicKey = pk

        # 6.2 Send secret voter data to the printing authority (this is typically done in the printVotingCards(), but since we want to show the secret voter data before printing the cards, we do it here)
        secretCredentials = [auth.partialSecretVotingCredentials for auth in self.authorities]
        self.printingAuthority.privateCredentials = secretCredentials


    def printVotingCards(self):
        # 6.2 Printing of voting cards
        self.printingAuthority.PrintVotingCards(self.bulletinBoard, self.secparams)

    def sendVotingCards(self):
        # 6.2 Printing of voting cards contd.
        for voter in self.voters:
            voter.votingCard = self.printingAuthority.votingCards[voter.id]   # id = index + 1  --> (1,2,3...)


    def castVote(self, voterId, selection, votingCode):
        # 6.5 Vote Casting
        voter = self.voters[voterId]

        # reset previous votecasting data
        voter.responses = []
        voter.checkResults = []

        # create a new VoterBallot (a temporary ballot that will be passed to the authorities for checking)
        (alpha, r) = GenBallot(votingCode, selection, self.bulletinBoard.publicKey, self.secparams)
        # pass it to the first authority
        voterBallot = VoterBallot(voterId, alpha)
        voterBallot.checkResults = [None] * self.secparams.s
        self.authorities[0].voterBallots.append(voterBallot)

        voter.selection = selection
        voter.randomizations = r

        # if the first authority is set to autoCheck = true, check ballot and reply automatically, otherwise checkVote will be called by the user through the webapp later
        if(self.authorities[0].autoCheck): self.checkVote(voterId, 0)

    def checkVote(self, voterId, authorityId):
        # 6.5 Vote Casting
        #for j in range(authorityId, self.secparams.s):
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        authority.checkBallot(voterId, self.bulletinBoard, self.secparams)

        if authority.autoCheck: self.respond(voterId, authorityId)

    def respond(self, voterId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        (voterBallot, response) = authority.respond(voterId, self.bulletinBoard, self.secparams)
        voter.responses.append(response)

        # pass voterBallot to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].voterBallots.append(voterBallot)
            if (self.authorities[authorityId + 1].autoCheck):
                self.checkVote(voterId, authorityId + 1)
        else:
            # this was the last authority to check the ballot
            # Generate return codes
            if all(checkResult for checkResult in voterBallot.checkResults):
                self.getReturnCodes(voter)

    def discardBallot(self, voterId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        authority.discardBallot(voterId, self.bulletinBoard, self.secparams)


    def getReturnCodes(self, voter):
        P_s = GetPointMatrix(voter.responses, voter.selection, voter.randomizations, self.secparams)
        voter.verificationCodes = GetReturnCodes(voter.selection, P_s, self.secparams)
        voter.status = 1
