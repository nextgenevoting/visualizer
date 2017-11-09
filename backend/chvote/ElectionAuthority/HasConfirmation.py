import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from chvote.Utils.Utils           import AssertList, AssertClass, AssertNumeric

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

    for voterConfirmation in C:
        if v == voterConfirmation.voterId:
            return True

    return False

class HasConfirmationTest(unittest.TestCase):
    def testHasConfirmation(self):
        C = [(0, 123), (1, 123), (2, 123)]

        self.assertTrue(HasConfirmation(0, C, secparams_l0))
        self.assertTrue(HasConfirmation(1, C, secparams_l0))
        self.assertTrue(HasConfirmation(2, C, secparams_l0))
        self.assertFalse(HasConfirmation(3, C, secparams_l0))

if __name__ == '__main__':
    unittest.main()
