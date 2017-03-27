import unittest
import os, sys
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz, AssertClass
from Utils.ToInteger        import ToInteger
from Utils.RecHash          import RecHash
from Crypto.SecurityParams  import secparams_default, secparams_l0, secparams_l3, SecurityParams
from Types                  import PublicCommitment, PublicValue

def GetNIZKPChallenge(y, t, q, secparams=secparams_default):
    """
    Algorithm 7.4: Computes a NIZKP challenge c ∈ Z_q for a given public value
    y and a public commitment t. The domains Y and T of the input values are
    unspecified.

    Args:
        y (mpz);    Public value
        t (mpz):    Commitment
        q (mpz):    Upper bound of challenge (q >= 2)

    Returns:
        c (mpz):    The NIZKP challenge
    """

    AssertClass(y, PublicValue)
    AssertClass(t, PublicCommitment)
    AssertMpz(q)
    assert q >= 2
    AssertClass(secparams, SecurityParams)


    c = mpz(ToInteger(RecHash([y, t], secparams)) % q)

    return c

class GetNIZKPChallengeTest(unittest.TestCase):
    def test(self):
        self.assertTrue(False) # TODO

if __name__ == '__main__':
    unittest.main()
