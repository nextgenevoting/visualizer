import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from Utils.Utils           import AssertInt, AssertList, AssertClass

def HasBallot(i, B_bold, secparams):
    """
    Algorithm 7.23: Checks if the ballot list B contains an entry for i.

    Args:
        i (int):            Voter index
        B_bold (list):      Ballot list

    Returns:
        bool
    """

    AssertInt(i)
    AssertList(B_bold)
    AssertClass(secparams, SecurityParams)

    for j in range(len(B_bold)):
        (i_j, alpha, r) = B_bold[j]
        if i == i_j:
            return True

    return False

class HasBallotTest(unittest.TestCase):
    def testCheckBallot(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
