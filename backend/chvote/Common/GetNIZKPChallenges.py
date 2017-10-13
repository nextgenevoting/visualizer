import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertInt, AssertClass
from chvote.Utils.ToInteger       import ToInteger
from chvote.Utils.RecHash         import RecHash
from chvote.Common.SecurityParams import secparams_l3, SecurityParams

def GetNIZKPChallenges(n, y, kappa, secparams):
    """
    Algorithm 7.5: Computes n challenges c ∈ Z_q for a given of public value y. The domain
    Y of the input value is unspecified. The results in c = (c_1, ..., c_n) are identical to
    c_i = RecHash(y, i), but precomputing H makes the algorithm more efficient.

    Args:
        y (unspecified):                    Public value
        t (unspecified):                    Commitment
        kappa (int):                        Soundness strength 1 <= kappa <= 8L
        secparams (SecurityParams):         Collection of public security parameters

    Retuns:
        list of mpz:                        List containing n computed challenges (mpz)
    """

    AssertInt(n)
    AssertInt(kappa)
    assert kappa >= 1 and kappa <= 8 * secparams.L, "Constraint for kappa: 1 <= kappa <= 8L"
    AssertClass(secparams, SecurityParams)

    H = RecHash(y, secparams)
    c = []

    for i in range(1, n + 1):
        I = RecHash(i, secparams)
        c.append(mpz(ToInteger(secparams.hash(H + I)) % 2^kappa))

    return c

class GetGetNIZKPChallengesTest(unittest.TestCase):
    def testGetNIZKPChallenges(self):
        # The results in c should be identical to c_i = ToInteger(RecHash(y,i)):
        c = GetNIZKPChallenges(50, mpz(1234), secparams_l3.tau, secparams_l3)
        self.assertEqual(len(c), 50)
        for i in range(1, len(c)+1):
            self.assertEqual(c[i-1], ToInteger(RecHash([mpz(1234), i], secparams_l3))% 2^secparams_l3.tau)

if __name__ == '__main__':
    unittest.main()
