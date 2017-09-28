import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from Utils.Utils           import AssertList, AssertClass, AssertNumeric
from Types                 import *

def HasConfirmation(v, C, secparams):
    """
    Algorithm 7.34: Checks if the confirmation list C contains an entry for v.

    Args:
        v (int):                           Voter Index v in N
        C (list of Confirmation):          Confirmation list C
        secparams (SecurityParams):        Collection of public security parameters

    Returns:
        bool:                              True if the list C contains a Confirmation of voter i
    """

    AssertNumeric(v)
    AssertList(C)
    AssertClass(secparams, SecurityParams)

    for j in range(len(C)):
        (v_j, epsilon_j) = C[j]
        if v == v_j:
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