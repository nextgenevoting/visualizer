import os
import sys
import unittest
from math import floor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                 import Truncate, AssertList, AssertClass
from chvote.Utils.Random                import randomMpz
from chvote.Utils.RecHash               import RecHash
from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from chvote.ElectionAuthority.GenPoints import GenPoints
from chvote.UnitTestParams              import unittestparams
from chvote.Types                       import *

def GenSecretVoterData(p_bold, secparams):
    """
    Algorithm 7.10: Generates the secret data for a single voter, which is sent to the voter prior to an election event via the printing authority.

    Args:
       p_bold (list):                      A list of n points = (p_1, ... , p_n) in Z_p'
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
       tuple:                              Secret voter data (x,y,F,r)
    """

    AssertList(p_bold)
    AssertClass(secparams, SecurityParams)

    q_hat_apos_x = floor(secparams.q_hat_X // secparams.s)
    q_hat_apos_y = floor(secparams.q_hat_Y // secparams.s)
    x = randomMpz(q_hat_apos_x, secparams)
    y = randomMpz(q_hat_apos_y, secparams)

    F = Truncate(RecHash(p_bold, secparams),secparams.L_F) # Finalization code
    r_bold = []                                            # Return codes

    n = len(p_bold)
    for i in range(n):
        r_bold.append(Truncate(RecHash(p_bold[i], secparams), secparams.L_R))

    return SecretVoterData(x,y,F,r_bold)

class GenSecretVoterDataTest(unittest.TestCase):
    def testGenSecretVoterData(self):
        # generate some points for 10 candidates [5 per election]
        points, yvalues = GenPoints([5,5], [3,2], secparams_l0)
        x,y,F,r = GenSecretVoterData(points, secparams_l3)

        # check that x and y are of type MPZ
        self.assertTrue(x.__class__.__name__ == 'mpz' and y.__class__.__name__ == 'mpz')

        # check that F is a byte array (bytes)
        self.assertTrue(isinstance(F, bytes))

        # check that r is a list of n return codes
        self.assertTrue(isinstance(r, list) and len(r) == 10)

    def testGenSecretVoterDataL0(self):
        # generate some points for 6 candidates [3 per election], 1 selection per election, 2 simult. elections,
        points, yvalues = GenPoints(unittestparams.n, unittestparams.k, secparams_l0)

        # points contains 6x (mpz(2), mpz(2))
        x, y, F, r = GenSecretVoterData(points, secparams_l0)

        # q_hat_apos_x = 43
        # q_hat_apos_y = 43
        self.assertEqual(x, 2)  # deterministic randomMpz(43) == 2
        self.assertEqual(y, 2)  # deterministic randomMpz(43) == 2

        # RecHash([(mpz(2),mpz(2)),(mpz(2),mpz(2)),(mpz(2),mpz(2)),(mpz(2),mpz(2)),(mpz(2),mpz(2)),(mpz(2),mpz(2))], secparams)
        # --> b'\xa9'
        self.assertEqual(F, b'\xa9')

if __name__ == '__main__':
    unittest.main()
