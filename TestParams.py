import hashlib
import gmpy2
from gmpy2 import mpz
from math import ceil, log2

from Election               import Election
from Candidate              import Candidate
from Crypto.SecurityParams  import secparams_l0
from Types                  import *

class TestParams(object):
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
        self.N = 2          # 2 Voters
        self.k = [1,1]      # 1 selection per election

        self.E = [[True for el in range(self.t)] for v in range(self.N)]
        self.K = [[1,1],[1,1]]      # 1 selection per election

        self.pk = mpz(4096)
        self.X = b'\xff\xee\xdd\xcc\xbb\xaa'     # Voting Code

        self.P = [[Point(mpz(2), mpz(2)) for cand in range(self.n_total)] for v in range(self.N)]

        """
        ballotProof test values: These values have been generate by GenBallot:
        (alpha, r) = GenBallot(testparams.X, [1,4], testparams.pk, secparams_l0)
        ballotProof = alpha[3]
        """
        self.ballotProof = ((mpz(161), mpz(195), mpz(16)), (mpz(79), mpz(137), mpz(157)))
        self.x_hat = mpz(252)
        self.a = mpz(546)
        self.b = mpz(256)

testparams = TestParams()