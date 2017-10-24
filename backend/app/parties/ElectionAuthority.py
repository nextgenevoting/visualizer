from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.ElectionAuthority.GenKeyPair import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey import GetPublicKey
from app.parties.Party import Party
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz

class ElectionAuthority(Party):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    def __init__(self, collection, electionID, authorityID):
        Party.__init__(self, collection, electionID, {'authorityID' : authorityID})

    @property
    def publicVotingCredentials(self):
        return self.state.publicVotingCredentials

    @publicVotingCredentials.setter
    def publicVotingCredentials(self, value):
        AssertList(value)
        self.state.publicVotingCredentials = value

    @property
    def secretVotingCredentials(self):
        return self.state.secretVotingCredentials

    @secretVotingCredentials.setter
    def secretVotingCredentials(self, value):
        AssertList(value)
        self.state.secretVotingCredentials = value


    @property
    def points(self):
        return self.state.points

    @points.setter
    def points(self, value):
        AssertList(value)
        self.state.points = value

    @property
    def secretKeyShare(self):
        return self.state.secretKeyShare

    @secretKeyShare.setter
    def secretKeyShare(self, value):
        AssertMpz(value)
        self.state.secretKeyShare = value

    @property
    def publicKeyShare(self):
        return self.state.publicKeyShare

    @publicKeyShare.setter
    def publicKeyShare(self, value):
        AssertMpz(value)
        self.state.publicKeyShare = value

    @property
    def publicKey(self):
        return self.state.publicKey

    @publicKey.setter
    def publicKey(self, value):
        AssertMpz(value)
        self.state.publicKey = value

    def GenElectionData(self, bulletinBoard, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        """

        self.secretVotingCredentials, self.publicVotingCredentials, self.points = GenElectorateData(bulletinBoard.numberOfCandidates, bulletinBoard.numberOfSelections, bulletinBoard.elegibilityMatrix, secparams)

        bulletinBoard.publicCredentials = self.publicVotingCredentials
        return True

    def GenKey(self, bulletinBoard, secparams):
        """
        (Protocol 6.3) Every authority j ∈ {1,...,s} calls GenKeyPair() in order to (independently) generate
        a key pair

        """

        self.secretKeyShare, self.publicKeyShare = GenKeyPair(secparams)

        return self.publicKeyShare

    def GetPublicKey(self, bulletinBoard, secparams):
        """
        (Protocol 6.3) Every authority j ∈ {1,...,s} calls GetPublicKey() to combine the s public key shares into one public key

        """
        self.publicKey = GetPublicKey(bulletinBoard.publicKeyShares, secparams)
        return self.publicKey