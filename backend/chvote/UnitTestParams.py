from gmpy2 import mpz

from chvote.Types import *

from chvote.Common.SecurityParams import secparams_l0


class UnitTestParams(object):
    """
    This class holds some complex objects (BulletProofs etc.) for testing purposes
    """

    def __init__(self):
        # Set up a test election event
        secparams = secparams_l0

        self.n_total = 6    # 6 total candidates
        self.c = ["Hillary Clinton", "Donald Trump", "Vladimir Putin", "Yes", "No", "Empty"]
        self.n = [3,3]      # 3 candidates per election
        self.t = 2          # 2 sim. elections
        self.N_E = 2          # 2 Voters
        self.k = [1,1]      # 1 selection per election

        self.E = [[True for el in range(self.t)] for v in range(self.N_E)]
        self.K = [[1,1],[1,1]]      # 1 selection per election

        self.pk = mpz(4096)
        self.X = 'AG'     # Voting Code

        self.P = [[Point(mpz(2), mpz(2)) for cand in range(self.n_total)] for v in range(self.N_E)]

        self.x_hat = mpz(607)
        self.a = mpz(546)
        self.b = mpz(256)
        self.pk = mpz(4096)

unittestparams = UnitTestParams()