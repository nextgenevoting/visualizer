import unittest
import os, sys
from gmpy2 import mpz
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from SecurityParams import secparams_default, secparams_l0, secparams_l3
from Utils import AssertMpz, ToInteger
from RecHash import RecHash

def GetNIZKPChallenge(y, t, q, secparams=secparams_default):
    """
    Algorithm 7.4: Computes a NIZKP challenge c ϵ Z_q for a given public value
    y and a public commitment t. The domains Y and T of the input values are
    unspecified.

    Args:
        y (int);    Public value
        t (int):    Commitment
        q (int):    Upper bound of challenge (q >= 2)

    Returns:
        c (int):    the NIZKP challenge
    """

    AssertMpz(y)
    AssertMpz(t)
    AssertMpz(q)
    assert(q >= 2)

    c = mpz(ToInteger(RecHash([y, t], secparams)) % q)

    return c

class GetNIZKPChallengeTest(unittest.TestCase):
    def test(self):
        self.AssertTrue(False) # TODO

if __name__ == '__main__':
    unittest.main()
