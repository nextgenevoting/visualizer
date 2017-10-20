from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.ElectionAuthority.GenKeyPair import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey import GetPublicKey
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

        """

        self.state.secretVoterData, self.state.publicVoterData, self.state.points = GenElectorateData(bulletinBoard.numberOfCandidates, bulletinBoard.numberOfSelections, bulletinBoard.elegibilityMatrix, secparams)

        bulletinBoard.publicCredentials = []
        bulletinBoard.publicCredentials.append(self.state.publicVoterData)
        return True

    def GenKey(self, bulletinBoard, secparams):
        """
        (Protocol 6.3) Every authority j ∈ {1,...,s} calls GenKeyPair() in order to (independently) generate
        a key pair

        """

        self.state.secretKeyShare, self.state.publicKeyShare = GenKeyPair(secparams)

        bulletinBoard.publicKeyShares.append(self.state.secretKeyShare)
        return True

    def GetPublicKey(self, bulletinBoard, secparams):
        """
        (Protocol 6.3) Every authority j ∈ {1,...,s} calls GetPublicKey() to combine the s public key shares into one public key

        """
        self.state.publicKey = GetPublicKey(bulletinBoard.publicKeyShares, secparams)
        return self.state.publicKey