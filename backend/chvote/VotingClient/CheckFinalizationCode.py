import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0
from chvote.Utils.Utils           import AssertList, AssertClass, AssertInt
from chvote.Types                 import *


def CheckFinalizationCode(FC, FC_prime, secparams):
    """
    Algorithm 7.39: Checks if the displayed finalization code FC1 matches with the finalization
    code FC from the voting card. Note that this algorithm is executed by humans.

    Args:
        FC (string):                         Printed finalization code
        FC_prime (string):                   Displayed finalization code
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        bool:                                FC == FC_prime
    """

    AssertClass(secparams, SecurityParams)

    return FC == FC_prime

class CheckFinalizationCodeTest(unittest.TestCase):
    def testCheckFinalizationCode(self):

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
