import unittest
import os, sys
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Types                          import *
from chvote.Utils.Random                   import randomMpz
from chvote.Common.SecurityParams import SecurityParams


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

    r_bold = []
    c_bold = []

    N = len(u_bold)

    c_bold.append(c_0)

    for i in range(N):
        c_i_minus_1 = c_bold[i]
        r_i = randomMpz(secparams.q, secparams)
        c_i = ((gmpy2.powmod(secparams.g, r_i, secparams.p) * gmpy2.powmod(c_i_minus_1,u_bold[i], secparams.p)) % secparams.p)

        r_bold.append(r_i)
        c_bold.append(c_i)

    del c_bold[0]

    return (c_bold, r_bold)

class GenCommitmentChainTest(unittest.TestCase):
    def testGenCommitmentChain(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
