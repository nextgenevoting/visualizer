from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from app.actors.Actor import Actor
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz, AssertClass
from chvote.Types import VerificationResult

class BulletinBoard(Actor):

    def __init__(self, collection, electionID):
        Actor.__init__(self, collection, electionID)

    @property
    def securityLevel(self):
        return self.state.securityLevel

    @securityLevel.setter
    def securityLevel(self, value):
        AssertInt(value)
        self.state.securityLevel = value

    @property
    def voters(self):
        return self.state.voters

    @voters.setter
    def voters(self, value):
        AssertList(value)
        self.state.voters = value


    @property
    def titles(self):
        return self.state.titles

    @titles.setter
    def titles(self, value):
        AssertList(value)
        self.state.titles = value


    @property
    def countingCircles(self):
        return self.state.countingCircles

    @countingCircles.setter
    def countingCircles(self, value):
        AssertList(value)
        self.state.countingCircles = value

    @property
    def candidates(self):
        return self.state.candidates

    @candidates.setter
    def candidates(self, value):
        AssertList(value)
        self.state.candidates = value

    @property
    def numberOfCandidates(self):
        return self.state.numberOfCandidates

    @numberOfCandidates.setter
    def numberOfCandidates(self, value):
        AssertList(value)
        self.state.numberOfCandidates = value

    @property
    def numberOfSelections(self):
        return self.state.numberOfSelections

    @numberOfSelections.setter
    def numberOfSelections(self, value):
        AssertList(value)
        self.state.numberOfSelections = value

    @property
    def numberOfParallelElections(self):
        return self.state.numberOfParallelElections

    @numberOfParallelElections.setter
    def numberOfParallelElections(self, value):
        AssertInt(value)
        self.state.numberOfParallelElections = value

    @property
    def eligibilityMatrix(self):
        return self.state.eligibilityMatrix

    def generateEligibilityMatrix(self):
        self.state.eligibilityMatrix = [[True for el in range(self.numberOfParallelElections)] for i in range(len(self.voters))]

    @property
    def partialPublicVotingCredentials(self):
        return self.state.partialPublicVotingCredentials

    @partialPublicVotingCredentials.setter
    def partialPublicVotingCredentials(self, value):
        AssertList(value)
        self.state.partialPublicVotingCredentials = value

    @property
    def ballots(self):
        return self.state.ballots

    @ballots.setter
    def ballots(self, value):
        AssertList(value)
        self.state.ballots = value

    @property
    def confirmations(self):
        return self.state.confirmations

    @confirmations.setter
    def confirmations(self, value):
        AssertList(value)
        self.state.confirmations = value

    @property
    def publicKeyShares(self):
        return self.state.publicKeyShares

    @publicKeyShares.setter
    def publicKeyShares(self, value):
        AssertList(value)
        self.state.publicKeyShares = value

    @property
    def publicKey(self):
        return self.state.publicKey

    @publicKey.setter
    def publicKey(self, value):
        AssertMpz(value)
        self.state.publicKey = value

    @property
    def encryptions(self):
        return self.state.encryptions

    @encryptions.setter
    def encryptions(self, value):
        AssertList(value)
        self.state.encryptions = value

    @property
    def shuffleProofs(self):
        return self.state.shuffleProofs

    @shuffleProofs.setter
    def shuffleProofs(self, value):
        AssertList(value)
        self.state.shuffleProofs = value

    @property
    def decryptions(self):
        return self.state.decryptions

    @decryptions.setter
    def decryptions(self, value):
        AssertList(value)
        self.state.decryptions = value


    @property
    def decryptionProofs(self):
        return self.state.decryptionProofs

    @decryptionProofs.setter
    def decryptionProofs(self, value):
        AssertList(value)
        self.state.decryptionProofs = value

    @property
    def verificationResult(self):
        return self.state.verificationResult

    @verificationResult.setter
    def verificationResult(self, value):
        AssertClass(value, VerificationResult)
        self.state.verificationResult = value


    def getBallotById(self, ballotId):
        for ballot in self.ballots:
            if ballot.id == ballotId:
                return ballot
        return None


    def getConfirmationById(self, confirmationId):
        for confirmation in self.confirmations:
            if confirmation.id == confirmationId:
                return confirmation
        return None