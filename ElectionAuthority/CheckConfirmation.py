import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams                    import SecurityParams, secparams_default, secparams_l0, secparams_l3
from Utils.Utils                              import AssertClass, AssertNumeric
from ElectionAuthority.CheckConfirmationProof import CheckConfirmationProof

def CheckConfirmation(i, gamma, y_hat, B, C, secparams=secparams_default):
    """
    Algorithm 7.34: Checks if a confirmation γ obtained from voter i is valid. For
    this, voter i must have submitted a valid ballot before, but not a valid
    confirmation. The check then succeeds if π is valid and if y_hat is the public
    confirmation credential of voter i.

    Args:
        i (int):        Voter index
        gamma:          Confirmation
        y_hat (list):   Public confirmation credentials
        B (list):       Ballot list
        C (list):       Confirmation list

    Returns:
        bool            True if the goven confirmation is valid, False otherwise.
    """

    AssertNumeric(i)
    # TODO check type of gamma
    AssertList(y_hat)
    AssertList(B)
    AssertList(C)
    AssertClass(secparams, SecurityParams)

    (y_hat_, pi) = gamma

    if HasBallot(i, B) and not HasConfirmation(i, C) and y_hat_ == y_hat[i]:
        if CheckConfirmationProof(pi, y_hat):
            return True

    return False

class CheckConfirmationTest(unittest.TestCase):
    def testCheckConfirmation(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()