import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Common.SecurityParams                      import SecurityParams, secparams_l0, secparams_l3
from Utils.Utils                                import AssertClass, AssertNumeric, AssertList
from ElectionAuthority.CheckConfirmationProof   import CheckConfirmationProof
from ElectionAuthority.HasConfirmation          import HasConfirmation
from ElectionAuthority.HasBallot                import HasBallot

def CheckConfirmation(v, gamma, y_hat_bold, B, C, secparams):
    """
    Algorithm 7.33: Checks if a confirmation γ obtained from voter v is valid. For
    this, voter v must have submitted a valid ballot before, but not a valid
    confirmation. The check then succeeds if π is valid and if y_hat is the public
    confirmation credential of voter v.

    Args:
        v (int):                             Voter index
        gamma:                               Confirmation
        y_hat_bold (list):                   Public confirmation credentials
        B (list):                            Ballot list
        C (list):                            Confirmation list
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        bool                                 True if the given confirmation is valid, False otherwise.
    """

    AssertNumeric(v)
    AssertList(y_hat_bold)
    AssertList(B)
    AssertList(C)
    AssertClass(secparams, SecurityParams)

    (y_hat_, pi) = gamma

    if HasBallot(v, B, secparams) and not HasConfirmation(v, C, secparams) and y_hat_ == y_hat_bold[v]:
        if CheckConfirmationProof(pi, y_hat_, secparams):
            return True

    return False

class CheckConfirmationTest(unittest.TestCase):
    def testCheckConfirmation(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
