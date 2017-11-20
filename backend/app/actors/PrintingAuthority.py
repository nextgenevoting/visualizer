from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.PrintingAuthority.GetVotingCards import GetVotingCards
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz

from app.actors.Actor import Actor

class PrintingAuthority(Actor):
    """
    The Printing Authority class represents the printing authority in the CHVote protocol
    """
    def __init__(self, collection, electionID):
        Actor.__init__(self, collection, electionID)

    @property
    def privateCredentials(self):
        return self.state.privateCredentials

    @privateCredentials.setter
    def privateCredentials(self, value):
        AssertList(value)
        self.state.privateCredentials = value

    @property
    def votingCards(self):
        return self.state.votingCards

    @votingCards.setter
    def votingCards(self, value):
        AssertList(value)
        self.state.votingCards = value


    def PrintVotingCards(self, bulletinBoard, secparams):
        """
        (Protocol 6.2) Printing of voting sheets

        """

        votingCardStrings, rawVotingCards = GetVotingCards(bulletinBoard.voters, bulletinBoard.countingCircles, bulletinBoard.candidates, bulletinBoard.numberOfCandidates, bulletinBoard.numberOfSelections, bulletinBoard.eligibilityMatrix, self.privateCredentials, secparams)
        self.votingCards = rawVotingCards

        return self.votingCards