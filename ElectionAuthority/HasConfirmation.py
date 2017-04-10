import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0, secparams_l3
from Utils.Utils           import AssertList, AssertClass, AssertNumeric
from Types                 import *

def HasConfirmation(i, C, secparams=secparams_default):
    """
    Algorithm 7.35: Checks if the confirmation list C contains an entry for i.

    Args:
        i (int):            Voter Index i in N
        C (list):           Confirmation list C

    Returns:
        bool
    """

    AssertNumeric(i)
    AssertList(C)
    AssertClass(secparams, SecurityParams)

    for j in range(len(C)):
        (i_j, epsilon_j) = C[j]
        if i == i_j:
            return True

    return False

class HasConfirmationTest(unittest.TestCase):
    def testHasConfirmation(self):
        C = [(0, 123), (1, 123), (2, 123)]

        self.assertTrue(HasConfirmation(0, C))
        self.assertTrue(HasConfirmation(1, C))
        self.assertTrue(HasConfirmation(2, C))
        self.assertFalse(HasConfirmation(3, C))

if __name__ == '__main__':
    unittest.main()
