import unittest
import os, sys
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertInt, AssertMpz, AssertClass
from chvote.Utils.ToInteger       import ToInteger
from chvote.Utils.RecHash         import RecHash
from chvote.Common.SecurityParams import secparams_l0, secparams_l3, SecurityParams

def GetNIZKPChallenge(y, t, kappa, secparams):
    """
    Algorithm 7.4: Computes a NIZKP challenge c ∈ Z_q for a given public value
    y and a public commitment t. The domains Y and T of the input values are
    unspecified.

    Args:
        y (unspecified):                    Public value
        t (unspecified):                    Commitment
        kappa (int):                        Soundness strength 1 <= kappa <= 8L
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        mpz:                                The NIZKP challenge
    """

    AssertInt(kappa)
    assert kappa >= 1 and kappa <= 8 * secparams.L, "Constraint for kappa: 1 <= kappa <= 8L"
    AssertClass(secparams, SecurityParams)

    c = mpz(ToInteger(RecHash([y, t], secparams)) % 2^kappa)

    return c

class GetNIZKPChallengeTest(unittest.TestCase):
    def testGetNIZKPChallenge(self):
        for i in range (100):
            c = GetNIZKPChallenge("Test", "chvote", secparams_l3.tau, secparams_l3)
            AssertMpz(c)
            assert c >= 0 and c <= 2^secparams_l3.tau

if __name__ == '__main__':
    unittest.main()
