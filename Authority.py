import multiprocessing as mp

from Crypto.SecurityParams                  import secparams_default
from ElectionAuthority.GenElectorateData    import GenElectorateData
from ElectionAuthority.GetPublicCredentials import GetPublicCredentials
from ElectionAuthority.GenKeyPair           import GenKeyPair
from ElectionAuthority.GetPublicKey         import GetPublicKey
from ElectionAuthority.CheckBallot          import CheckBallot

class Authority(object):
    """
    The Authority class represents a single election authority which performs several algorithms according
    to the protocol diagrams in chapter 6 of the specification document
    """
    name = ""

    # The election authority knows:
    d_j = None
    d_hat_j = None
    P_j = None
    K = None

    x_hat = []
    y_hat = []

    pk = None
    B = []

    def __init__(self, name):
        self.name = name

    def PerformGenElectorateData(self, n, k, E, secparams = secparams_default):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        Args:
            n (list):           A list containing the number of candidates: (n_1, ... , n_t)
            k (list):           A list containing the number of possible selections per election: (k_1, ... , k_t)
            E ([[]]):           Eligibility matrix [N][t], 1 means eligible

        Returns:
            list:               d_hat_j, a list of public data of all voters, calculated by authority j

        """
        self.d_j, self.d_hat_j, self.P_j, self.K = GenElectorateData(n, k, E, secparams)
        return self.d_hat_j

    def PerformGetPublicCredentials(self, D_hat, secparams = secparams_default):
        """
        (Protocol 6.1) Every authority j ∈ {1,...,s} calls GetPublicCredentials upon knowing the public data of the whole electorate D_hat.
        This algorithm outputs the two lists x_hat and y_hat of all public credentials, which are used to identify the voters during the vote casting and vote confirmation phases

        Args:
           D_hat (list):        The public data of the whole electorate
           N (int):             The number of voters
        """
        self.x_hat, self.y_hat = GetPublicCredentials(D_hat, secparams)


    def PerformKeyGeneration(self, secparams = secparams_default):
        """
        (Protocol 6.3) Key Generation: In the last step of the election preparation, a public ElGamal encryption key pk ∈ G_q is
        generated jointly by the election authorities.

        Returns:
            mpz:                pk
        """
        (sk_j, pk_j) = GenKeyPair(secparams)
        return pk_j


    def PerformGetPublicKey(self, pk, secparams = secparams_default):
        """
        (Protocol 6.3) GetPublicKey: Combining the s key shares of all authorities

        Args:
            pk (list):          Public Key Shares pk = (pk_1, ... , pk_s)

        Returns:
            mpz:                pk
        """
        self.pk = GetPublicKey(pk)
        return self.pk


    def PerformCheckBallot(self, i, ballot, secparams = secparams_default):
        """
        (Protocol 6.5) PerformCheckBallot: Receives the ballot from the client and checks its validity

        Args:
            i (int):            Voter index
            alpha (Ballot):     Ballot

        Returns:
            bool
        """
        return CheckBallot(i, ballot, self.pk, self.K, self.x_hat, self.B, secparams)
