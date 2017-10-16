from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from app.parties.Party import Party

class ElectionAuthority(Party):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    def __init__(self, collection, electionID, authorityID):
        Party.__init__(self, collection, electionID, {'authorityID' : authorityID})


    def GenElectionData(self, bulletinBoard, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        Args:

        Returns:
            list:                   d_hat_j, a list of public data of all voters, calculated by authority j

        """

        self.state.secretVoterData, self.state.publicVoterData, self.state.points = GenElectorateData(bulletinBoard.numberOfCandidates, bulletinBoard.numberOfSelections, bulletinBoard.elegibilityMatrix, secparams)

        bulletinBoard.publicCredentials = []
        bulletinBoard.publicCredentials.append(self.state.publicVoterData)
        return bulletinBoard