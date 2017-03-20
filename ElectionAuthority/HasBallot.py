import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Crypto.SecurityParams  import SecurityParams, secparams_default, secparams_l0, secparams_l3
from Utils.Utils            import AssertInt, AssertList, AssertClass

def HasBallot(i, B, secparams=secparams_default):
    """
    Algorithm 7.23: Checks if the ballot list B contains an entry for i.

    Args:
        i (int):            Voter index
        B (list):           Ballot list

    Returns:
        bool
    """
    AssertInt(i)
    AssertList(B)
    AssertClass(secparams, SecurityParams)

    for j in range(len(B)):
        (i_j,alpha,r) = B[j]
        if(i == i_j): return True;
    return False;


class HasBallotTest(unittest.TestCase):
    def testCheckBallot(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
