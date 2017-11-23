import multiprocessing as mp

from chvote.ElectionAuthority.GenElectorateData     import GenElectorateData
from chvote.ElectionAuthority.GetPublicCredentials  import GetPublicCredentials
from chvote.ElectionAuthority.GenKeyPair            import GenKeyPair
from chvote.ElectionAuthority.GetPublicKey          import GetPublicKey
from chvote.ElectionAuthority.CheckBallot           import CheckBallot
from chvote.ElectionAuthority.GenResponse           import GenResponse
from chvote.ElectionAuthority.CheckConfirmation     import CheckConfirmation
from chvote.ElectionAuthority.GetEncryptions        import GetEncryptions
from chvote.ElectionAuthority.GenShuffle            import GenShuffle
from chvote.ElectionAuthority.GenShuffleProof       import GenShuffleProof
from chvote.ElectionAuthority.GetPartialDecryptions import GetPartialDecryptions
from chvote.ElectionAuthority.CheckShuffleProofs    import CheckShuffleProofs
from chvote.ElectionAuthority.GenDecryptionProof    import GenDecryptionProof
from chvote.ElectionAuthority.GetFinalization       import GetFinalization
from chvote.Types                                   import *

class Authority(object):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """

    def __init__(self, j, bulletinBoard):
        self.name = "S%d" % j
        self.j = j
        self.bulletinBoard = bulletinBoard

        # The election authority knows:
        self.n_bold = None
        self.d_j_bold = None
        self.d_hat_j_bold = None
        self.K_bold = None
        self.E_bold = None
        self.P_bold_j = None

        self.x_hat_bold = []
        self.y_hat_bold = []

        self.pk_j = None
        self.sk_j = None
        self.pk = None
        self.B_j = []
        self.C_j = []


    def GenElectionData(self, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        Args:

        Returns:
            list:                   d_hat_j, a list of public data of all voters, calculated by authority j

        """

        self.n_bold = self.bulletinBoard.n_bold
        self.d_j_bold, self.d_hat_j_bold, self.P_bold_j = GenElectorateData(self.n_bold, self.bulletinBoard.k_bold, self.bulletinBoard.E_bold, secparams)

        self.bulletinBoard.D_hat_bold.append(self.d_hat_j_bold)
        return self.d_hat_j_bold

    def GetPublicCredentials(self, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GetPublicCredentials upon knowing the public data of the whole electorate D_hat.
        This algorithm outputs the two lists x_hat and y_hat of all public credentials, which are used to identify the voters during the vote casting and vote confirmation phases

        Args:
        """

        self.x_hat, self.y_hat = GetPublicCredentials(self.bulletinBoard.D_hat_bold, secparams)

    def GenKeyPair(self, secparams):
        """
        (Protocol 6.3) Key Generation: In the last step of the election preparation, a public ElGamal encryption key pk ∈ G_q is
        generated jointly by the election authorities.

        Returns:
            mpz:                pk
        """

        self.sk_j, self.pk_j = GenKeyPair(secparams)
        self.bulletinBoard.pk_bold.append(self.pk_j)
        return self.pk_j

    def getPublicKey(self, secparams):
        """
        (Protocol 6.3) GetPublicKey: Combining the s key shares of all authorities

        Args:

        Returns:
            mpz:                pk
        """

        self.pk = GetPublicKey(self.bulletinBoard.pk_bold, secparams)
        return self.pk

    def runCheckBallot(self, v, alpha, secparams):
        """
        (Protocol 6.5) PerformCheckBallot: Receives the ballot from the client and checks its validity

        Args:
            v (int):            Voter index
            alpha (Ballot):     Ballot

        Returns:
            bool
        """

        return CheckBallot(v, alpha, self.pk, self.bulletinBoard.k_bold, self.bulletinBoard.E_bold, self.x_hat, self.B_j, secparams)

    def genResponse(self, v, a_bold, alpha, secparams):
        """
        (Protocol 6.5) genResponse: Generates a response for the OT query a

        Args:
            v (int):            Voter index
            a_bold (list):      Queries

        Returns:
            tuple:              (v, beta_j)
        """
        (beta_j, r_bold) = GenResponse(v, a_bold, self.pk, self.n_bold, self.bulletinBoard.k_bold, self.bulletinBoard.E_bold, self.P_bold_j, secparams)
        self.B_j.append(VoterBallot(v, alpha, r_bold))
        return (beta_j, r_bold)

    def printPoints(self):
        print("Points of Authority %s:" % self.name)
        print(self.P_bold_j)


    def checkConfirmation(self, v, gamma, secparams):
        """
        (Protocol 6.6) checkConfirmation()

        Args:
           v (int):            Voter index
           gamma (tuple):      Confirmation

        Returns:
           bool
        """
        if CheckConfirmation(v, gamma, self.y_hat, self.B_j, self.C_j, secparams):
            self.C_j.append(VoterConfirmation(v, gamma, 1))

            self.bulletinBoard.delta_bold[v][self.j] = GetFinalization(v, self.P_bold_j, self.B_j, secparams)

            return True
        else:
            return False

    def shuffle(self, secparams):
        """
       (Protocol 6.7) shuffle()

       Args:

       Returns:
          None
       """
        if self.j == 0:
            if len(self.B_j) == 0 or len(self.C_j) == 0:
                raise RuntimeError('Shuffle called without any valid ballots!')

            # the following steps are only performed by the first election authority
            e_bold_0 = GetEncryptions(self.B_j, self.C_j, self.n_bold, self.bulletinBoard.w_bold, secparams)
            (e_bold_1, r_bold_1, psi_1) = GenShuffle(e_bold_0, self.pk, secparams)
            pi_1 = GenShuffleProof(e_bold_0, e_bold_1, r_bold_1, psi_1, self.pk, secparams)

            self.bulletinBoard.EN_bold.append(e_bold_1)
            self.bulletinBoard.pi_bold.append(pi_1)
        else:
            # executed by election authorities 1..s
            e_bold_j_minus_1 = self.bulletinBoard.EN_bold[self.j-1]
            (e_bold_j, r_bold_j, psi_j) = GenShuffle(e_bold_j_minus_1, self.pk, secparams)
            pi_j = GenShuffleProof(e_bold_j_minus_1, e_bold_j, r_bold_j, psi_j, self.pk, secparams)

            self.bulletinBoard.EN_bold.append(e_bold_j)
            self.bulletinBoard.pi_bold.append(pi_j)

    def decrypt(self, secparams):
        """
        (Protocol 6.8) decrypt()

        Args:

        Returns:
          None
        """
        e_0 = GetEncryptions(self.B_j, self.C_j, self.n_bold, self.bulletinBoard.w_bold, secparams)
        if not CheckShuffleProofs(self.bulletinBoard.pi_bold, e_0, self.bulletinBoard.EN_bold, self.pk, self.j, secparams):
            return False
        b_prime_j = GetPartialDecryptions(self.bulletinBoard.EN_bold[-1], self.sk_j, secparams)
        pi_prime_j = GenDecryptionProof(self.sk_j, self.pk_j, self.bulletinBoard.EN_bold[-1], b_prime_j, secparams)

        self.bulletinBoard.B_prime_bold.append(b_prime_j)
        self.bulletinBoard.pi_prime_bold.append(pi_prime_j)

        return True
