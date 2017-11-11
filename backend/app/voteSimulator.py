from chvote.Common.SecurityParams import secparams_l1
from app.models.electionAuthorityState import ElectionAuthorityState
from app.models.voterState import VoterState
from app.parties.ElectionAuthority import ElectionAuthority
from app.database import db, serializeState
from app.parties.BulletinBoard import BulletinBoard
from app.parties.PrintingAuthority import PrintingAuthority
from app.parties.Voter import Voter
from app.parties.ElectionAdministrator import ElectionAdministrator
from bson.objectid import ObjectId
from app.main.syncService import syncElectionStatus, SyncType
from chvote.VotingClient.GenBallot import GenBallot
from chvote.Types import *
from chvote.VotingClient.GetPointMatrix import GetPointMatrix
from chvote.VotingClient.GetReturnCodes import GetReturnCodes
from chvote.VotingClient.GetFinalizationCode import GetFinalizationCode
from chvote.VotingClient.GenConfirmation import GenConfirmation

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

        # load election administrator
        self.electionAdministrator = ElectionAdministrator(db.electionAdministratorStates, electionID)


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
        self.electionAdministrator.persist()
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
            publicKeyShare = authority.genKey(self.bulletinBoard, self.secparams)
            self.bulletinBoard.publicKeyShares.append(publicKeyShare)
        for authority in self.authorities:
            pk = authority.getPublicKey(self.bulletinBoard, self.secparams)
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
        voter.points = []
        voter.responses = []

        # create a new checkBallotTask (a temporary ballot that will be passed to the authorities for checking)
        (alpha, r) = GenBallot(votingCode, selection, self.bulletinBoard.publicKey, self.secparams)
        # pass it to the first authority
        checkBallotTask = CheckBallotTask(voterId, alpha)
        checkBallotTask.checkResults = [None] * self.secparams.s
        self.authorities[0].checkBallotTasks.append(checkBallotTask)

        voter.selection = selection
        voter.randomizations = r

        # if the first authority is set to autoCheck = true, check ballot and reply automatically, otherwise checkVote will be called by the user through the webapp later
        if(self.authorities[0].autoCheck): self.checkVote(voterId, 0)



    def confirmVote(self, voterId, confirmationCode):
        # 6.6 Vote Confirmation
        voter = self.voters[voterId]

        # reset previous confirmation data
        # TODO

        # create a new checkConfirmationTask (a temporary confirmation that will be passed to the authorities for checking)
        gamma = GenConfirmation(confirmationCode, voter.points, self.secparams)
        # pass it to the first authority
        checkConfirmationTask = CheckConfirmationTask(voterId, gamma)
        checkConfirmationTask.checkResults = [None] * self.secparams.s
        self.authorities[0].checkConfirmationTasks.append(checkConfirmationTask)

        # if the first authority is set to autoCheck = true, check ballot and reply automatically, otherwise checkVote will be called by the user through the webapp later
        if(self.authorities[0].autoCheck): self.checkConfirmation(voterId, 0)

    def checkVote(self, voterId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        checkResult = authority.checkBallot(voterId, self.bulletinBoard, self.secparams)

        if authority.autoCheck:
            if checkResult:
                self.respond(voterId, authorityId)
            else:
                self.discardBallot(voterId, authorityId)

    def respond(self, voterId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        (checkBallotTask, response) = authority.respond(voterId, self.bulletinBoard, self.secparams)
        voter.responses.append(response)

        # pass checkBallotTask to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].checkBallotTasks.append(checkBallotTask)
            if (self.authorities[authorityId + 1].autoCheck):
                self.checkVote(voterId, authorityId + 1)
        else:
            # this was the last authority to check the ballot
            # Generate return codes
            if all(checkResult for checkResult in checkBallotTask.checkResults):
                self.getReturnCodes(voter)

    def discardBallot(self, voterId, authorityId):
        # 6.5 Vote Casting
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        authority.discardBallot(voterId, self.bulletinBoard, self.secparams)

    def getReturnCodes(self, voter):
        P_s = GetPointMatrix(voter.responses, voter.selection, voter.randomizations, self.secparams)
        voter.points = P_s
        voter.verificationCodes = GetReturnCodes(voter.selection, P_s, self.secparams)
        voter.status = 1

    def checkConfirmation(self, voterId, authorityId):
        # 6.6 Vote Confirmation
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        authority.checkConfirmation(voterId, self.bulletinBoard, self.secparams)

        if authority.autoCheck: self.finalize(voterId, authorityId)


    def finalize(self, voterId, authorityId):
        # 6.6 Vote Confirmation
        authority = self.authorities[authorityId]
        voter = self.voters[voterId]

        (checkConfirmationTask, finalization) = authority.finalize(voterId, self.bulletinBoard, self.secparams)
        voter.finalizations.append(finalization)

        # pass checkConfirmationTask to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].checkConfirmationTasks.append(checkConfirmationTask)
            if (self.authorities[authorityId + 1].autoCheck):
                self.checkConfirmation(voterId, authorityId + 1)
        else:
            # this was the last authority to check the confirmation
            # Generate finalizationCode codes
            if all(checkResult for checkResult in checkConfirmationTask.checkResults):
                self.getFinalizationCode(voter)

    def getFinalizationCode(self, voter):
        voter.finalizationCode = GetFinalizationCode(voter.finalizations, self.secparams)
        voter.status = 2

# *********************************
#  POST ELECTION PHASE
# *********************************
    def startMixing(self):
        # the first election authority must extract the encryptions from the ballot-list
        numOfEncryptions = self.authorities[0].getEncryptions(self.bulletinBoard, self.secparams)

        # set the permutation to 1,2,3,...,len(encryptions) inititially for the shuffle transition / animation
        permutation = [i for i in range(numOfEncryptions)]

        for electionAuthority in self.authorities:
            electionAuthority.permutation = permutation

        if (self.authorities[0].autoCheck):
                self.mix(0)

    def mix(self, authorityId):
        if len(self.authorities[authorityId].encryptions) == 0:
            raise RuntimeError("This authority requires the encryptions of the previous authority!")

        e_shuffled = self.authorities[authorityId].mix(self.bulletinBoard, self.secparams)

        # pass e_shuffled to the next authority
        if authorityId < self.secparams.s - 1:
            self.authorities[authorityId + 1].encryptions = e_shuffled
            if (self.authorities[authorityId + 1].autoCheck):
                self.mix(authorityId + 1)
        else:
            # this was the last authority to mix
            pass


    def decrypt(self, authorityId):
        authority = self.authorities[authorityId]

        shuffleProofCheck = authority.decrypt(self.bulletinBoard, self.secparams)
        if not shuffleProofCheck:
            raise RuntimeError("Shuffle proof check failed!")

        if authorityId < self.secparams.s - 1:
            if (self.authorities[authorityId + 1].autoCheck):
                self.decrypt(authorityId+1)
        else:
            # this was the last authority to decrypt
            self.updateStatus(6)

    def tally(self):
        self.electionAdministrator.tally(self.bulletinBoard, self.secparams)