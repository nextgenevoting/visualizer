from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.ElectionAuthority.GenKeyPair import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey import GetPublicKey
from app.parties.Party import Party
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz, AssertClass, AssertString
from chvote.Types import VotingCard

class Voter(Party):
    """
    The Voter class represents a single voter participating in the CHVote protocol
    """
    def __init__(self, collection, electionID, voterID):
        Party.__init__(self, collection, electionID, {'voterID' : voterID})

    @property
    def id(self):
        return self.state.id

    @id.setter
    def id(self, value):
        AssertInt(value)
        self.state.id = value

    @property
    def name(self):
        return self.state.name

    @name.setter
    def name(self, value):
        AssertString(value)
        self.state.name = value

    @property
    def votingCard(self):
        return self.state.votingCard

    @votingCard.setter
    def votingCard(self, value):
        AssertClass(value, VotingCard)
        self.state.votingCard = value


    @property
    def countingCircle(self):
        return self.state.countingCircle

    @countingCircle.setter
    def countingCircle(self, value):
        AssertInt(value)
        self.state.countingCircle = value

    # Votingclient Properties

    @property
    def selection(self):
        return self.state.selection

    @selection.setter
    def selection(self, value):
        AssertList(value)
        self.state.selection = value

    @property
    def randomizations(self):
        return self.state.randomizations

    @randomizations.setter
    def randomizations(self, value):
        AssertList(value)
        self.state.randomizations = value


    @property
    def validBallot(self):
        return self.state.validBallot

    @validBallot.setter
    def validBallot(self, value):
        AssertString(value)
        self.state.validBallot = value

    @property
    def points(self):
        return self.state.points

    @points.setter
    def points(self, value):
        AssertList(value)
        self.state.points = value

    @property
    def verificationCodes(self):
        return self.state.verificationCodes

    @verificationCodes.setter
    def verificationCodes(self, value):
        AssertList(value)
        self.state.verificationCodes = value

    @property
    def finalizations(self):
        return self.state.finalizations

    @finalizations.setter
    def finalizations(self, value):
        AssertList(value)
        self.state.finalizations = value


    @property
    def finalizationCode(self):
        return self.state.finalizationCode

    @finalizationCode.setter
    def finalizationCode(self, value):
        AssertString(value)
        self.state.finalizationCode = value

    @property
    def status(self):
        return self.state.status

    @status.setter
    def status(self, value):
        AssertInt(value)
        self.state.status = value