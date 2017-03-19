import unittest
import os, sys
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz, AssertInt
from Utils.ToInteger        import ToInteger
from Utils.RecHash          import RecHash
from Crypto.SecurityParams  import secparams_default, secparams_l0, secparams_l3

def GetChallenges(n, y, q, secparams=secparams_default):
    """
    Algorithm 7.5: Computes n challenges c ∈ Z_q for a given of public value y. The domain
    Y of the input value is unspecified. The results in c = (c_1, ..., c_n) are identical to
    c_i = RecHash(y, i), but precomputing H makes the algorithm more efficient.

    Args:
        n (int):    Number of challenges to compute
        y (mpz):    Public value
        q (mpz):    Upper bound of challenge (q >= 2)

    Retuns:
        c (list):   List containing n computed challenges
    """

    AssertInt(n)
    AssertMpz(y)
    AssertMpz(q)
    assert(q >= 2)

    H = RecHash(y, secparams)
    c = []

    for i in range(1, n + 1):
        I = RecHash(i)
        c.append(mpz(ToInteger(secparams.hash(H + I)) % q))

    return c

class GetChallengesTest(unittest.TestCase):
    def test(self):
        # The results in c should be identical to c_i = ToInteger(RecHash(y,i)):
        c = GetChallenges(50, mpz(1234), mpz(2 ** 1024))
        for i in range(1, len(c)+1):
            self.assertEqual(c[i-1], ToInteger(RecHash([mpz(1234), i]))%mpz(2**1024))

if __name__ == '__main__':
    unittest.main()
