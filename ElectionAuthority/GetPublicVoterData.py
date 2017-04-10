import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz, AssertList, AssertClass
from Utils.ToInteger       import ToInteger
from Utils.RecHash         import RecHash
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0, secparams_l3

def GetPublicVoterData(x, y, yValues, secparams = secparams_default):
    """
    Algorithm 7.11: Generates the public data for a single voter, which is sent to the bulletin board.

    Args:
       x (mpz):             Voting credential
       y (mpz):             Confirmation credential
       yValues (list):      Values y ∈ Z_p_prime ^t

    Returns:
       tuple:               Public data of a voter
    """

    AssertMpz(x)
    AssertMpz(y)
    AssertList(yValues)
    AssertClass(secparams, SecurityParams)

    h = ToInteger(RecHash(yValues, secparams)) % secparams.q_hat
    x_hat = gmpy2.powmod(secparams.g_hat, x, secparams.p_hat)
    y_hat = gmpy2.powmod(secparams.g_hat, y+h, secparams.p_hat)

    return (x_hat, y_hat) # as d_hat

class GetPublicVoterDataTest(unittest.TestCase):
    def testGetPublicVoterDataL0(self):
        # compare the algorithms result with some manually calculated data
        # we assume that h = 108 for y = 2 and q_hat = 131
        x_hat, y_hat = GetPublicVoterData(mpz(5), mpz(2), [1,2], secparams_l0)
        self.assertEqual(x_hat, 735) # manually calculated: x_hat = 64^5 mod 787  => 735
        self.assertEqual(y_hat, 464) # manually calculated: y_hat = 64^{2 + 108} mod 787 => 464

if __name__ == '__main__':
    unittest.main()
