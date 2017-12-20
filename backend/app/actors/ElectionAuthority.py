from chvote.ElectionAuthority.GenElectorateData import GenElectorateData
from chvote.ElectionAuthority.GenKeyPair import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey import GetPublicKey
from app.actors.Actor import Actor
from chvote.Utils.Utils import AssertList, AssertInt, AssertMpz, AssertTuple
from chvote.ElectionAuthority.CheckBallot import CheckBallot
from chvote.ElectionAuthority.GetPublicCredentials import GetPublicCredentials
from chvote.ElectionAuthority.GenResponse import GenResponse
from chvote.Types import *
from chvote.ElectionAuthority.CheckConfirmation import CheckConfirmation
from chvote.ElectionAuthority.GetFinalization import GetFinalization
from chvote.ElectionAuthority.GetEncryptions import GetEncryptions
from chvote.ElectionAuthority.GenShuffle import GenShuffle
from chvote.ElectionAuthority.GenShuffleProof import GenShuffleProof
from chvote.ElectionAuthority.CheckShuffleProofs import CheckShuffleProofs
from chvote.ElectionAuthority.GetPartialDecryptions import GetPartialDecryptions
from chvote.ElectionAuthority.GenDecryptionProof import GenDecryptionProof

class ElectionAuthority(Actor):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    def __init__(self, collection, electionID, authorityID):
        Actor.__init__(self, collection, electionID, {'authorityID' : authorityID})

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
    def checkBallotTasks(self):
        return self.state.checkBallotTasks

    @checkBallotTasks.setter
    def checkBallotTasks(self, value):
        AssertList(value)
        self.state.checkBallotTasks = value

    @property
    def ballots(self):
        return self.state.ballots

    @ballots.setter
    def ballots(self, value):
        AssertList(value)
        self.state.ballots = value


    @property
    def checkConfirmationTasks(self):
        return self.state.checkConfirmationTasks

    @checkConfirmationTasks.setter
    def checkConfirmationTasks(self, value):
        AssertList(value)
        self.state.checkConfirmationTasks = value

    @property
    def confirmations(self):
        return self.state.confirmations

    @confirmations.setter
    def confirmations(self, value):
        AssertList(value)
        self.state.confirmations = value


    @property
    def encryptions(self):
        return self.state.encryptions

    @encryptions.setter
    def encryptions(self, value):
        AssertList(value)
        self.state.encryptions = value


    @property
    def encryptionsShuffled(self):
        return self.state.encryptionsShuffled

    @encryptionsShuffled.setter
    def encryptionsShuffled(self, value):
        AssertList(value)
        self.state.encryptionsShuffled = value


    @property
    def permutation(self):
        return self.state.permutation

    @permutation.setter
    def permutation(self, value):
        AssertList(value)
        self.state.permutation = value

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



    def genKey(self, bulletinBoard, secparams):
        """
        (Protocol 6.3) Every authority j ∈ {1,...,s} calls GenKeyPair() in order to (independently) generate
        a key pair

        """

        self.secretKeyShare, self.publicKeyShare = GenKeyPair(secparams)

        return self.publicKeyShare

    def getPublicKey(self, bulletinBoard, secparams):
        """
        (Protocol 6.3) Every authority j ∈ {1,...,s} calls GetPublicKey() to combine the s public key shares into one public key

        """
        self.publicKey = GetPublicKey(bulletinBoard.publicKeyShares, secparams)
        return self.publicKey

    def checkBallot(self, ballotId, bulletinBoard, secparams):
        """
        (Protocol 6.4) Every authority j ∈ {1,...,s} checks the ballot and responds to it
        """

        checkBallotTask = None
        for v in self.checkBallotTasks:
            if v.ballotId == ballotId:
                checkBallotTask = v

        if checkBallotTask == None:
            raise RuntimeError("checkBallotTask not found on election authority")

        # find ballot
        ballot = bulletinBoard.getBallotById(ballotId)

        (checkResult, checks) = CheckBallot(ballot.voterId, ballot.ballot, self.publicKey, bulletinBoard.numberOfSelections, bulletinBoard.eligibilityMatrix, self.publicVotingCredentials[0], self.ballots, secparams)

        if(checkResult):
            ballot.validity = 1
        else:
            if checks[0] == False:
                ballot.validity = 2 # ballot proof failed
            if checks[1] == True:
                ballot.validity = 3  # alreadyHasBallot
            if checks[2] == False:
                ballot.validity = 4  # credential check failed
            if checks[3] == False:
                ballot.validity = 5  # query length failed

        checkBallotTask.checkResults[self.id] = ballot.validity

        return checkResult

    def respond(self, ballotId, bulletinBoard, secparams):
        checkBallotTask = None
        for v in self.checkBallotTasks:
            if v.ballotId == ballotId:
                checkBallotTask = v

        if checkBallotTask == None:
            raise RuntimeError("checkBallotTask not found on election authority")

        ballot = bulletinBoard.getBallotById(ballotId)

        (beta_j, z) = GenResponse(ballot.voterId, ballot.ballot.a_bold, self.publicKey, bulletinBoard.numberOfCandidates,
                                  bulletinBoard.numberOfSelections, bulletinBoard.eligibilityMatrix, self.points,
                                  secparams)
        ballot.responses[self.id] = beta_j
        ballot.randomizations = z
        self.ballots.append(ballot)

        # remove the checkBallotTask from this elections checkBallotTask list (it will be moved to the next authority that's why we have to return the voterBallot)
        self.checkBallotTasks.remove(checkBallotTask)

        return (checkBallotTask, beta_j)

    def discardBallot(self, ballotId, bulletinBoard, secparams):
        checkBallotTask = None
        for v in self.checkBallotTasks:
            if v.ballotId == ballotId:
                checkBallotTask = v

        if checkBallotTask == None:
            raise RuntimeError("checkBallotTask not found on election authority")

        self.checkBallotTasks.remove(checkBallotTask)

        from app.api.syncService import pushVoterMessage
        pushVoterMessage(bulletinBoard.electionID, checkBallotTask.voterId, "Ballot is not valid!")

        return checkBallotTask.voterId

    def checkConfirmation(self, confirmationId, bulletinBoard, secparams):
        """
        (Protocol 6.6) Every authority j ∈ {1,...,s} checks the confirmation
        """

        checkConfirmationTask = None
        for v in self.checkConfirmationTasks:
            if v.confirmationId == confirmationId:
                checkConfirmationTask = v

        if checkConfirmationTask == None:
            raise RuntimeError("checkConfirmationTask not found on election authority")

        # find confirmation
        confirmation = bulletinBoard.getConfirmationById(confirmationId)

        (checkResult, checks) = CheckConfirmation(checkConfirmationTask.voterId, confirmation.confirmation, self.publicVotingCredentials[1], self.ballots, self.confirmations, secparams)

        if (checkResult):
            confirmation.validity = 1
        else:
            if checks[0] == False:
                confirmation.validity = 2  # confirmation proof failed
            if checks[1] == False:
                confirmation.validity = 3  # hasBallot
            if checks[2] == True:
                confirmation.validity = 4  # already has confirmation
            if checks[3] == False:
                confirmation.validity = 5  # credential check failed

        checkConfirmationTask.checkResults[self.id] = confirmation.validity

        return checkResult

    def discardConfirmation(self, confirmationId, bulletinBoard, secparams):
        checkConfirmationTask = None
        for v in self.checkConfirmationTasks:
            if v.confirmationId == confirmationId:
                checkConfirmationTask = v

        if checkConfirmationTask == None:
            raise RuntimeError("checkConfirmationTask not found on election authority")

        self.checkConfirmationTasks.remove(checkConfirmationTask)
        from app.api.syncService import pushVoterMessage
        pushVoterMessage(bulletinBoard.electionID, checkConfirmationTask.voterId, "Confirmation is not valid!")
        return checkConfirmationTask.voterId

    def finalize(self, confirmationId, bulletinBoard, secparams):
        checkConfirmationTask = None
        for v in self.checkConfirmationTasks:
            if v.confirmationId == confirmationId:
                checkConfirmationTask = v

        if checkConfirmationTask == None:
            raise RuntimeError("checkConfirmationTask not found on election authority")

        confirmation = bulletinBoard.getConfirmationById(confirmationId)

        delta_j = GetFinalization(checkConfirmationTask.voterId, self.points, self.ballots, secparams)

        confirmation.finalizations[self.id] = delta_j

        self.confirmations.append(confirmation)

        # remove the voterBallot from this elections voterBallot list (it will be moved to the next authority that's why we have to return the voterBallot)
        self.checkConfirmationTasks.remove(checkConfirmationTask)

        return (checkConfirmationTask, delta_j)

    # *********************************
    #  POST ELECTION PHASE
    # *********************************

    def getEncryptions(self, bulletinBoard, secparams):
        encryptions = GetEncryptions(self.ballots, self.confirmations, bulletinBoard.numberOfCandidates, bulletinBoard.countingCircles, secparams)
        self.encryptions = encryptions
        return len(encryptions)


    def mix(self, bulletinBoard, secparams):
        e_orig = self.encryptions
        (e_shuffled, r, psi) = GenShuffle(e_orig, self.publicKey, secparams)
        pi = GenShuffleProof(e_orig, e_shuffled, r, psi, self.publicKey, secparams)
        self.encryptionsShuffled = e_shuffled
        self.permutation = psi
        bulletinBoard.encryptions.append(e_shuffled)
        bulletinBoard.shuffleProofs.append(pi)
        return e_shuffled

    def decrypt(self, bulletinBoard, secparams):

        e_0 = GetEncryptions(self.ballots, self.confirmations, bulletinBoard.numberOfCandidates, bulletinBoard.countingCircles, secparams)
        if not CheckShuffleProofs(bulletinBoard.shuffleProofs, e_0, bulletinBoard.encryptions, self.publicKey, self.id, secparams):
            return False
        partialDecryptions = GetPartialDecryptions(bulletinBoard.encryptions[-1], self.secretKeyShare, secparams)
        decryptionProofs = GenDecryptionProof(self.secretKeyShare, self.publicKeyShare, bulletinBoard.encryptions[-1], partialDecryptions, secparams)

        bulletinBoard.decryptions.append(partialDecryptions)
        bulletinBoard.decryptionProofs.append(decryptionProofs)

        return True