from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.ElectionAuthority.GenKeyPair import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey import GetPublicKey
from app.actors.Actor import Actor
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz, AssertClass, AssertString
from chvote.Types import VotingCard

class Voter(Actor):
    """
    The Voter class represents a single voter participating in the CHVote protocol
    """
    def __init__(self, collection, electionID, voterID, state=None):
        Actor.__init__(self, collection, electionID, {'voterID' : voterID}, state)

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
    def invalidBallot(self):
        return self.state.invalidBallot

    @invalidBallot.setter
    def invalidBallot(self, value):
        self.state.invalidBallot = value

    @property
    def invalidConfirmation(self):
        return self.state.invalidConfirmation

    @invalidConfirmation.setter
    def invalidConfirmation(self, value):
        self.state.invalidConfirmation = value

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

    @property
    def votingCodeRevealed(self):
        return self.state.votingCodeRevealed

    @votingCodeRevealed.setter
    def votingCodeRevealed(self, value):
        self.state.votingCodeRevealed = value

    @property
    def confirmationCodeRevealed(self):
        return self.state.confirmationCodeRevealed

    @confirmationCodeRevealed.setter
    def confirmationCodeRevealed(self, value):
        self.state.confirmationCodeRevealed = value

