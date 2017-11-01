from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.ElectionAuthority.GenKeyPair import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey import GetPublicKey
from app.parties.Party import Party
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz, AssertTuple
from chvote.ElectionAuthority.CheckBallot import CheckBallot
from chvote.ElectionAuthority.GetPublicCredentials import GetPublicCredentials
from chvote.ElectionAuthority.GenResponse import GenResponse
from chvote.Types import BallotWithRandomizations

class ElectionAuthority(Party):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    def __init__(self, collection, electionID, authorityID):
        Party.__init__(self, collection, electionID, {'authorityID' : authorityID})

    @property
    def id(self):
        return self.state.id

    @id.setter
    def id(self, value):
        AssertInt(value)
        self.state.id = value

    @property
    def autoCheck(self):
        return self.state.autoCheck

    @autoCheck.setter
    def autoCheck(self, value):
        self.state.autoCheck = value

    @property
    def partialPublicVotingCredentials(self):
        return self.state.partialPublicVotingCredentials

    @partialPublicVotingCredentials.setter
    def partialPublicVotingCredentials(self, value):
        AssertList(value)
        self.state.partialPublicVotingCredentials = value

    @property
    def partialSecretVotingCredentials(self):
        return self.state.partialSecretVotingCredentials

    @partialSecretVotingCredentials.setter
    def partialSecretVotingCredentials(self, value):
        AssertList(value)
        self.state.partialSecretVotingCredentials = value

    @property
    def publicVotingCredentials(self):
        return self.state.publicVotingCredentials

    @publicVotingCredentials.setter
    def publicVotingCredentials(self, value):
        AssertTuple(value)
        self.state.publicVotingCredentials = value


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

    @property
    def voterBallots(self):
        return self.state.voterBallots

    @voterBallots.setter
    def voterBallots(self, value):
        AssertList(value)
        self.state.voterBallots = value

    @property
    def ballots(self):
        return self.state.ballots

    @ballots.setter
    def ballots(self, value):
        AssertList(value)
        self.state.ballots = value



    def GenElectionData(self, bulletinBoard, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        """

        self.partialSecretVotingCredentials, self.partialPublicVotingCredentials, self.points = GenElectorateData(bulletinBoard.numberOfCandidates, bulletinBoard.numberOfSelections, bulletinBoard.eligibilityMatrix, secparams)

        return self.partialPublicVotingCredentials


    def GetPublicCredentials(self, bulletinBoard, secparams):
        self.publicVotingCredentials = GetPublicCredentials(bulletinBoard.partialPublicVotingCredentials, secparams)
        return self.publicVotingCredentials



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

    def checkBallot(self, voterId, bulletinBoard, secparams):
        """
        (Protocol 6.4) Every authority j ∈ {1,...,s} checks the ballot and responds to it
        """

        voterBallot = None
        for v in self.voterBallots:
            if v.voterId == voterId:
                voterBallot = v


        if voterBallot == None:
            raise RuntimeError("voterBallot not found on election authority")

        checkResult = CheckBallot(voterId-1, voterBallot.ballot, self.publicKey, bulletinBoard.numberOfSelections, bulletinBoard.eligibilityMatrix, self.publicVotingCredentials[0], self.ballots, secparams)
        if checkResult:
            (beta_j, z) = GenResponse(voterId-1, voterBallot.ballot.a_bold, self.publicKey, bulletinBoard.numberOfCandidates, bulletinBoard.numberOfSelections, bulletinBoard.eligibilityMatrix, self.points, secparams)
            self.ballots.append(BallotWithRandomizations(voterId, voterBallot.ballot, z))
        else:
            # abort
            beta_j = None
            pass

        # remove the voterBallot from this elections voterBallot list (it will be moved to the next authority that's why we have to return the voterBallot)
        self.voterBallots.remove(voterBallot)

        return (voterBallot, checkResult, beta_j)