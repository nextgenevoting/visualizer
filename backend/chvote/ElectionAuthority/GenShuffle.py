import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                       import AssertList, AssertMpz
from chvote.Types                             import *
from chvote.Common.SecurityParams import secparams_l3, secparams_l0
from chvote.ElectionAuthority.GenPermutation  import GenPermutation
from chvote.ElectionAuthority.GenReEncryption import GenReEncryption

def GenShuffle(e_bold, pk, secparams):
    """
    Algorithm 7.41: Generates a random permutation psi and uses it to shuffle a given
    list e = (e_1, ..., e_n) of ElGamal encryptions e_i = (a_i, b_i) in G_q^2.
    With psi_N = {(j_1, ..., j_N) : j_i in {1,...,N}, j_i_1 != j_i_2, forAll i_1 != i2}
    we denote the set of all N! possible permutations of the values {1, ..., N}

    Args:
       e_bold (list):                      ElGamal Encryptions
       pk (mpz):                           Encryption key pk
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
        tuple                              (e_prime, r_prime, psi)
    """

    AssertList(e_bold)
    AssertMpz(pk)

    psi_bold = GenPermutation(len(e_bold), secparams)
    e_prime_bold = []
    r_prime_bold = []

    N = len(e_bold)
    for i in range(N):
        (e_prime_i, r_prime_i) = GenReEncryption(e_bold[i], pk, secparams)
        e_prime_bold.append(e_prime_i)
        r_prime_bold.append(r_prime_i)

    e_prime_shuffled = [None] * len(e_prime_bold)
    for i in range(N):
        e_prime_shuffled[i] = e_prime_bold[psi_bold[i]]
    return (e_prime_shuffled, r_prime_bold, psi_bold)

class GenShuffleTest(unittest.TestCase):
    def testGenShuffle(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
