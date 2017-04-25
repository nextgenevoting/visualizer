import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                    import AssertList, AssertClass
from Types                          import *
from Utils.Random                   import randomMpz
from Crypto.SecurityParams          import SecurityParams, secparams_l3

def GenCommitmentChain(c_0, u_bold, secparams):
    """
    Algorithm 7.46: Generates a commitment chain c_0 -> c_1 --> ... --> c_N relative to a list of 
    public challenges u_bold and starting with a given commitment c_0. This algorithm is used in Alg. 7.44

    Args:
       c_0 (mpz):                           Initial commitment c_0 in G_q
       u_bold (list of mpz):                Public challenges u = (u_1, ..., u_N), u_i in Z_q
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                              (c,r)
    """

    r_bold = [None] * len(u_bold)
    c_bold = [None] * len(u_bold)

    for i in range(len(u_bold)):
        c_i_minus_1 = c_0 if i == 0 else c_bold[i-1]
        r_bold[i] = randomMpz(secparams.p, secparams)
        c_bold[i] = (gmpy2.powmod(secparams.g, r_bold[i], secparams.p) * gmpy2.powmod(c_i_minus_1,u_bold[i], secparams.p)) % secparams.p

    return (c_bold, r_bold)

class GenCommitmentChainTest(unittest.TestCase):
    def testGenCommitmentChain(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
