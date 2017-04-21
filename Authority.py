import multiprocessing as mp

from ElectionAuthority.GenElectorateData    import GenElectorateData
from ElectionAuthority.GetPublicCredentials import GetPublicCredentials
from ElectionAuthority.GenKeyPair           import GenKeyPair
from ElectionAuthority.GetPublicKey         import GetPublicKey
from ElectionAuthority.CheckBallot          import CheckBallot
from ElectionAuthority.GenResponse          import GenResponse
from ElectionAuthority.CheckConfirmation    import CheckConfirmation

class Authority(object):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    j = None
    name = None
    bulletinBoard = None

    # The election authority knows:
    n_bold = None
    d_j_bold = None
    d_hat_j_bold = None
    P_j_bold = None
    K_bold = None

    x_hat_bold = []
    y_hat_bold = []

    pk = None
    B_j = []
    C_j = []

    def __init__(self, j, bulletinBoard):
        self.name = "S%d" % j
        self.j = j
        self.bulletinBoard = bulletinBoard

    def GenElectionData(self, n_bold, k_bold, E_bold, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        Args:
            n_bold (list):           A list containing the number of candidates: (n_1, ... , n_t)
            k_bold (list):           A list containing the number of possible selections per election: (k_1, ... , k_t)
            E_bold (list):           Eligibility matrix [N][t], 1 means eligible

        Returns:
            list:                   d_hat_j, a list of public data of all voters, calculated by authority j

        """

        self.n_bold = n_bold
        self.d_j_bold, self.d_hat_j_bold, self.P_j_bold, self.K_bold = GenElectorateData(n_bold, k_bold, E_bold, secparams)

        self.bulletinBoard.D_hat_bold.append(self.d_hat_j_bold)
        return self.d_hat_j_bold

    def GetPublicCredentials(self, D_hat_bold, secparams):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GetPublicCredentials upon knowing the public data of the whole electorate D_hat.
        This algorithm outputs the two lists x_hat and y_hat of all public credentials, which are used to identify the voters during the vote casting and vote confirmation phases

        Args:
           D_hat_bold (list):        The public data of the whole electorate
        """

        self.x_hat, self.y_hat = GetPublicCredentials(D_hat_bold, secparams)

    def GenKeyPair(self, secparams):
        """
        (Protocol 6.3) Key Generation: In the last step of the election preparation, a public ElGamal encryption key pk ∈ G_q is
        generated jointly by the election authorities.

        Returns:
            mpz:                pk
        """

        (sk_j, pk_j) = GenKeyPair(secparams)
        return pk_j

    def getPublicKey(self, pk, secparams):
        """
        (Protocol 6.3) GetPublicKey: Combining the s key shares of all authorities

        Args:
            pk (list):          Public Key Shares pk = (pk_1, ... , pk_s)

        Returns:
            mpz:                pk
        """

        self.pk = GetPublicKey(pk, secparams)
        return self.pk

    def runCheckBallot(self, i, ballot, secparams):
        """
        (Protocol 6.5) PerformCheckBallot: Receives the ballot from the client and checks its validity

        Args:
            i (int):            Voter index
            alpha (Ballot):     Ballot

        Returns:
            bool
        """

        return CheckBallot(i, ballot, self.pk, self.K_bold, self.x_hat, self.B_j, secparams)

    def genResponse(self, i, alpha, secparams):
        """
        (Protocol 6.5) genResponse: Generates a response for the OT query a

        Args:
            i (int):            Voter index
            a (list):           Queries

        Returns:
            tuple:              (i, beta_j)
        """
        (beta_j, r_bold) = GenResponse(i, alpha, self.pk, self.n_bold, self.K_bold, self.P_j_bold, secparams)
        self.B_j.append((i,alpha, r_bold))
        return (beta_j, r_bold)

    def printPoints(self):
        print("Points of Authority %s:" % self.name)
        print(self.P_j_bold)


    def checkConfirmation(self, i, gamma, secparams):
        return CheckConfirmation(i,gamma, self.y_hat, self.B_j, self.C_j, secparams)