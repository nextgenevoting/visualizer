from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.PrintingAuthority.GetVotingCards import GetVotingCards
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz

from app.actors.Actor import Actor
from chvote.ElectionAdministrator.GetVotes import GetVotes
from chvote.ElectionAuthority.GetDecryptions import GetDecryptions
from chvote.ElectionAuthority.CheckDecryptionProofs import CheckDecryptionProofs

class ElectionAdministrator(Actor):
    """
    The Election Administrator class represents the election Admin in the CHVote protocol
    """
    def __init__(self, collection, electionID):
        Actor.__init__(self, collection, electionID)

    @property
    def votes(self):
        return self.state.votes

    @votes.setter
    def votes(self, value):
        AssertList(value)
        self.state.votes = value


    @property
    def w_bold(self):
        return self.state.w_bold


    @w_bold.setter
    def w_bold(self, value):
        AssertList(value)
        self.state.w_bold = value


    @property
    def finalResults(self):
        return self.state.finalResults


    @finalResults.setter
    def finalResults(self, value):
        AssertList(value)
        self.state.finalResults = value

    def tally(self, bulletinBoard, secparams):
        decryptionProofCheck = CheckDecryptionProofs(bulletinBoard.decryptionProofs, bulletinBoard.publicKeyShares, bulletinBoard.encryptions[-1], bulletinBoard.decryptions, secparams )
        if not decryptionProofCheck:
            raise RuntimeError("Decryption proof check failed!")

        m_bold = GetDecryptions(bulletinBoard.encryptions[-1], bulletinBoard.decryptions, secparams)
        self.votes, self.w_bold = GetVotes(m_bold, bulletinBoard.numberOfCandidates, bulletinBoard.countingCircles, secparams)

        candidateVotes = [0] * sum(bulletinBoard.numberOfCandidates)
        for c in range(len(bulletinBoard.candidates)):
            for votes in self.votes:
                if votes[c] == 1:
                    candidateVotes[c] += 1

        j = 0
        finalVotes = []
        for c in bulletinBoard.numberOfCandidates:
            electionEventResults = []
            for i in range(c):
                electionEventResults.append(candidateVotes[j])
                j = j+1
            finalVotes.append(electionEventResults)

        self.finalResults = finalVotes