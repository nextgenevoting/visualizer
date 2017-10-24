from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from app.parties.Party import Party
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz

class BulletinBoard(Party):

    def __init__(self, collection, electionID):
        Party.__init__(self, collection, electionID)

    @property
    def voters(self):
        return self.state.voters

    @voters.setter
    def voters(self, value):
        AssertList(value)
        self.state.voters = value

        self.generateElegibilityMatrix()

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
        # number of parallel elections
        self.state.t = len(value)
        self.generateElegibilityMatrix()

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
        return self.state.t

    @property
    def elegibilityMatrix(self):
        return self.state.elegibilityMatrix

    def generateElegibilityMatrix(self):
        self.state.elegibilityMatrix = [[True for el in range(self.numberOfParallelElections)] for i in range(len(self.voters))]

    @property
    def publicCredentials(self):
        return self.state.publicCredentials

    @publicCredentials.setter
    def publicCredentials(self, value):
        AssertList(value)
        self.state.publicCredentials = value

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