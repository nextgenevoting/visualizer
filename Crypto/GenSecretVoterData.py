import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gmpy2
from gmpy2 import mpz
import unittest
from SecurityParams import secparams_default, secparams_l0, secparams_l3
from Utils import Truncate, AssertList
from Crypto.Random import randomMpz
from RecHash import RecHash
from math import floor
from GenPoints import GenPoints

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
    x = randomMpz(q_hat_apos_x)
    y = randomMpz(q_hat_apos_y)

    F = Truncate(RecHash(p, secparams),secparams.L_F)        # Finalization code
    r = []                                                   # Return codes
    for i in range(0, len(p)):
        r.append(Truncate(RecHash(p[i], secparams), secparams.L_R))

    return (x,y,F,r)

# Unit Tests
class GenSecretVoterDataTest(unittest.TestCase):

    def testOne(self):

        # generate some points for 10 voters [5 per election]
        points, yvalues = GenPoints([5,5], [3,2], 2)
        x,y,F,r = GenSecretVoterData(points, secparams_l3)

        # check that x and y are of type MPZ
        self.assertTrue(x.__class__.__name__ == 'mpz' and y.__class__.__name__ == 'mpz')
        # check that F is a byte array (bytes)
        self.assertTrue(isinstance(F, bytes))
        # check that r is a list of n return codes
        self.assertTrue(isinstance(r, list) and len(r) == 10)

if __name__ == '__main__':
    unittest.main()