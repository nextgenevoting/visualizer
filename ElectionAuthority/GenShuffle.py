import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                       import AssertList, AssertMpz
from Types                             import *
from Crypto.SecurityParams             import secparams_default, secparams_l3, secparams_l0
from ElectionAuthority.GenPermutation  import GenPermutation
from ElectionAuthority.GenReEncryption import GenReEncryption

def GenShuffle(e, pk, secparams = secparams_default):
    """
    Algorithm 7.41: Generates a random permutation psi and uses it to shuffle a given
    list e = (e_1, ..., e_n) of ElGamal encryptions e_i = (a_i, b_i) in G_q^2.
    With psi_N = {(j_1, ..., j_N) : j_i in {1,...,N}, j_i_1 != j_i_2, forAll i_1 != i2}
    we denote the set of all N! possible permutations of the values {1, ..., N}

    Args:
       e (list):        ElGamal Encryptions
       pk (mpz):        Encryption key pk

    Returns:
        tuple           (e_prime, r_prime, psi)
    """

    AssertList(e)
    AssertMpz(pk)

    psi = GenPermutation(len(e))
    e_prime = []
    r_prime = []

    for i in range(len(e)):
        (e_prime_i, r_prime_i) = GenReEncryption(e[i], pk)
        e_prime.append((e_prime_i))
        r_prime.append((r_prime_i))

    return (e_prime, r_prime, psi)

class GenShuffleTest(unittest.TestCase):
    def testGenShuffle(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
