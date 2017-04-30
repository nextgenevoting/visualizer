import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                    import AssertList, AssertClass
from Types                          import *
from Utils.Random                   import randomMpz
from Crypto.SecurityParams          import SecurityParams, secparams_l3

def GenPermutationCommitment(psi, h_bold, secparams):
    """
    Algorithm 7.45: Generates a commitment c = com(psi, r_bold) to a permutation psi by committing
    to the columns of the corresponding permutation matrix. This algorithm is used in Alg. 7.44.

    Args:
       psi (list of int):                   Permutation
       h_bold (list of mpz):                Independent generators h = (h_1, ..., h_N), h_i in G_q\{1}
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                              (c,r)
    """

    AssertList(psi)
    AssertList(h_bold)
    AssertClass(secparams, SecurityParams)

    r_bold = [None] * len(psi)
    c_bold = [None] * len(psi)

    N = len(psi)
    for i in range(N):
        r_bold[psi[i]] = randomMpz(secparams.p, secparams)
        c_bold[psi[i]] = (gmpy2.powmod(secparams.g, r_bold[psi[i]], secparams.p) * h_bold[i]) % secparams.p

    return (c_bold, r_bold)

class GenPermutationCommitmentTest(unittest.TestCase):
    def testGenPermutationCommitment(self):
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
