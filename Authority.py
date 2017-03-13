import multiprocessing as mp

from Crypto.SecurityParams                  import secparams_default
from ElectionAuthority.GenElectorateData    import GenElectorateData
from ElectionAuthority.GetPublicCredentials import GetPublicCredentials

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

    def __init__(self, name):
        self.name = name

    def PerformGenElectorateData(self, n, k, E, N, t, secparams = secparams_default):
        """
        (Protocol 6.1) Every authority j in {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
        the public election parameters for all voters.

        Args:
            n (list): List with number of candidates n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j
            E ([int][int]): Eligibility matrix [N][t] containing a bool value (1 = eligible, 0 = not eligible)

        Returns:
            list:       d_hat_j, a list of public data of all voters, calculated by authority j

        """
        self.d_j, self.d_hat_j, self.P_j, self.K = GenElectorateData(False, None, None, n, k, E, N, t, secparams)
        return self.d_hat_j

    def PerformGetPublicCredentials(self, D_hat, N, secparams = secparams_default):
        """
        (Protocol 6.1) Every authority j in {1,...,s} calls GetPublicCredentials upon knowing the public data of the whole electorate D_hat.
        This algorithm outputs the two lists x_hat and y_hat of all public credentials, which are used to identify the voters during the vote casting and vote confirmation phases

        Args:
           D_hat (list):        The public data of the whole electorate
           N (int):         The number of voters
        """
        self.x_hat, self.y_hat = GetPublicCredentials(D_hat, N, secparams)

    #def PerformParallelGenElectorateData(self, n, k, E, N, t, secparams = secparams_default):
    #    """
    #    Every authority j in {1,...,s} calls GenElectorateData with n, k, E in order to (independently) generate
    #    the public election parameters for all voters

    #    @type   n:  list
    #    @param  n:  List with number of candidates n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j

    #    @type   k:  list
    #    @type   k:  Number of selections k = (k_1, ..., k_t), 0 <= kj <= nj, kj = 0 means ineligible

    #    @type   E:  [int][int]
    #    @type   E:  Eligibility matrix [N][t]
    #    """

    #    # Set up parallel GenElectorateData call
    #    output = mp.Queue()
    #    processes = [mp.Process(target=GenElectorateData, args=(True, x, output, n, [1,1], E, N, t,)) for x in range(mp.cpu_count())]
    #    # Run processes
    #    for p in processes:
    #        p.start()
    #    # Get results
    #    results = [output.get() for p in processes]

    #    # Wait for the processs to complete
    #    for p in processes:
    #        p.join()

    #    reassembledResult = []
