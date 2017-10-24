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
