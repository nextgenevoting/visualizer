import unittest
import os, sys
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertInt, AssertClass
from Utils.ToInteger       import ToInteger
from Utils.RecHash         import RecHash
from Crypto.SecurityParams import secparams_l0, secparams_l3, SecurityParams

def GetNIZKPChallenges(n, y, kappa, secparams):
    """
    Algorithm 7.5: Computes n challenges c ∈ Z_q for a given of public value y. The domain
    Y of the input value is unspecified. The results in c = (c_1, ..., c_n) are identical to
    c_i = RecHash(y, i), but precomputing H makes the algorithm more efficient.

    Args:
        n (int):        Number of challenges to compute
        y (mpz):        Public value
        kappa (mpz):    Soundness strength 1 <= kappa <= 8L

    Retuns:
        c (list):   List containing n computed challenges (mpz)
    """

    AssertInt(n)
    AssertMpz(y)
    AssertMpz(kappa)
    assert(kappa >= 2)
    AssertClass(secparams, SecurityParams)

    H = RecHash(y, secparams)
    c = []

    for i in range(1, n + 1):
        I = RecHash(i)
        c.append(mpz(ToInteger(secparams.hash(H + I)) % 2^kappa))

    return c

class GetGetNIZKPChallengesTest(unittest.TestCase):
    def test(self):
        # The results in c should be identical to c_i = ToInteger(RecHash(y,i)):
        c = GetNIZKPChallenges(50, mpz(1234), mpz(1024))
        for i in range(1, len(c)+1):
            self.assertEqual(c[i-1], ToInteger(RecHash([mpz(1234), i]))%mpz(1024))

if __name__ == '__main__':
    unittest.main()
