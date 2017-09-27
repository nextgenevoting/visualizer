import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                       import AssertClass, AssertList
from Utils.ToInteger                   import ToInteger
from Utils.StringToInteger             import StringToInteger
from Utils.RecHash                     import RecHash
from Common.SecurityParams             import SecurityParams
from Types                             import *
from VotingClient.GetValues            import GetValues
from VotingClient.GenConfirmationProof import GenConfirmationProof

def GenConfirmation(Y, P_bold, secparams):
    """
    Algorithm 7.30: Generates the confirmation gamma, which consists of the
    public confirmation credential y_hat and a NIZKP of knowledge pi of the secret
    confirmation and validity credentials y and y_prime.

    Args:
        Y:                                   Confirmation code
        P_bold (list of points):             Points
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        gamma:                               Confirmation
    """

    AssertList(P_bold)
    AssertClass(secparams, SecurityParams)

    for i in range(secparams.s):
        p_bold_i = [ P_bold[i][k_i] for k_i in range(len(P_bold)) ]
        y_prime_i = GetValues(p_bold_i, secparams)

    y = StringToInteger(Y, secparams.A_Y) % secparams.q_hat
    y_hat = gmpy2.powmod(secparams.g_hat, y + y_prime, secparams.p_hat)
    pi = GenConfirmationProof(y, y_prime, y_hat, secparams)
    gamma = Confirmation(y_hat, pi)

    return gamma

class GenConfirmationTest(unittest.TestCase):
    def testGenConfirmation(self):
        P_ = [ [ Point(1, 3), Point(5, 7), Point( 9, 11) ]
             , [ Point(2, 4), Point(6, 8), Point(10, 12) ]
             , [ Point(7, 9), Point(3, 5), Point( 1, 13) ]
             ]

        print(GenConfirmation([1, 2, 3, 4], P_, [1, 2]))

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
