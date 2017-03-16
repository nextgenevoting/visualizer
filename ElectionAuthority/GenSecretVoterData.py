import unittest
import os, sys
import gmpy2
from gmpy2 import mpz
from math import floor

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                    import Truncate, AssertList
from Utils.Random                   import randomMpz
from Utils.RecHash                  import RecHash
from Crypto.SecurityParams          import secparams_default, secparams_l0, secparams_l3
from ElectionAuthority.GenPoints    import GenPoints
from TestParams                     import testparams

def GenSecretVoterData(p, secparams = secparams_default):
    """
    Algorithm 7.10: Generates the secret data for a single voter, which is sent to the voter prior to an election event via the printing authority.

    Args:
       p (list):    A list of n points = (p_1, ... , p_n) in Z_p'

    Returns:
       tuple:   Secret voter data (x,y,F,r)
    """
    AssertList(p)

    q_hat_apos_x = floor(secparams.q_hat_X // secparams.s)
    q_hat_apos_y = floor(secparams.q_hat_Y // secparams.s)
    x = randomMpz(q_hat_apos_x, secparams)
    y = randomMpz(q_hat_apos_y, secparams)

    F = Truncate(RecHash(p, secparams),secparams.L_F)        # Finalization code
    r = []                                                   # Return codes
    for i in range(0, len(p)):
        r.append(Truncate(RecHash(p[i], secparams), secparams.L_R))

    return (x,y,F,r)

# Unit Tests
class GenSecretVoterDataTest(unittest.TestCase):

    def testGenSecretVoterData(self):

        # generate some points for 10 candidates [5 per election]
        points, yvalues = GenPoints([5,5], [3,2], 2)
        x,y,F,r = GenSecretVoterData(points, secparams_l3)

        # check that x and y are of type MPZ
        self.assertTrue(x.__class__.__name__ == 'mpz' and y.__class__.__name__ == 'mpz')
        # check that F is a byte array (bytes)
        self.assertTrue(isinstance(F, bytes))
        # check that r is a list of n return codes
        self.assertTrue(isinstance(r, list) and len(r) == 10)

    def testGenSecretVoterDataL0(self):
        # generate some points for 6 candidates [3 per election], 1 selection per election, 2 simult. elections,
        points, yvalues = GenPoints(testparams.n, testparams.k, testparams.t, secparams_l0)
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
