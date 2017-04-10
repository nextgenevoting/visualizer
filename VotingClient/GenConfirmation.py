import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                       import AssertClass, AssertList
from Utils.ToInteger                   import ToInteger
from Utils.RecHash                     import RecHash
from Crypto.SecurityParams             import SecurityParams, secparams_default, secparams_l0
from Types                             import Point
from VotingClient.GetValues            import GetValues
from VotingClient.GenConfirmationProof import GenConfirmationProof

def GenConfirmation(Y, P_, k, secparams=secparams_default):
    """
    Algorithm 7.30: Generates the confirmation gamma, which consists of the public
    confirmation credential y_hat and a NIZKP of knowledge pi of the secret
    confirmation credential y.

    Args:
        Y: Confirmation code
        P_ (list of points): Points
        k: Number of selections

    Returns:
        gamma: Confirmation
    """

    AssertList(P_)
    AssertClass(secparams, SecurityParams)

    s = len(P_)
    h = [None] * s

    for j in range(s):
        p_j = [P_[k_][j] for k_ in range(sum(k))]
        y_j = GetValues(p_j, k)
        h[j] = ToInteger(RecHash(y_j)) % secparams.q_hat

    y = (ToInteger(Y) + sum(h)) % secparams.q_hat
    y_hat = gmpy2.powmod(secparams.g_hat, y, secparams.p_hat)
    pi = GenConfirmationProof(y, y_hat)
    gamma = (y_hat, pi)

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
