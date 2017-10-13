from chvote.ElectionAuthority.GenElectorateData import GenElectorateData

class ElectionAuthority(object):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    state = None


    def __init__(self, electionAuthorityState):
        self.state = electionAuthorityState


    def loadState(self, electionAuthorityState):
        self.state = electionAuthorityState


    def GenElectionData(self, bulletinBoardState, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        Args:

        Returns:
            list:                   d_hat_j, a list of public data of all voters, calculated by authority j

        """

        self.state.secretVoterData, self.state.publicVoterData, self.state.points = GenElectorateData(bulletinBoardState.numberOfCandidates, bulletinBoardState.numberOfSelections, bulletinBoardState.elegibilityMatrix, secparams)

        bulletinBoardState.publicCredentials.append(self.state.publicVoterData)
        return bulletinBoardState