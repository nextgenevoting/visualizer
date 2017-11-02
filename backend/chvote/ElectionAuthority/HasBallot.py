import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from chvote.Utils.Utils           import AssertInt, AssertList, AssertClass

def HasBallot(v, B_bold, secparams):
    """
    Algorithm 7.23: Checks if the ballot list B contains an entry for v.

    Args:
        v (int):                            Voter index
        B_bold (list):                      Ballot list
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        bool
    """

    AssertInt(v)
    AssertList(B_bold)
    AssertClass(secparams, SecurityParams)

    for j in range(len(B_bold)):
        # (v_j, alpha, r) = B_bold[j]
        if v == B_bold[j].voterId:
            return True

    return False

class HasBallotTest(unittest.TestCase):
    def testCheckBallot(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
