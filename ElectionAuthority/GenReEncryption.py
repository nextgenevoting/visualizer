import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils           import AssertMpz
from Types                 import *
from Utils.Random          import randomMpz
from Crypto.SecurityParams import SecurityParams, secparams_default, secparams_l0, secparams_l3

def GenReEncryption(e, pk, secparams = secparams_default):
    """
    Algorithm 7.43: Generates a re-encryption e' = (a * pk^r', b*g^r') of the given ElGamal encryption
    e = (a,b) in G_q^2. The re-encryption e' is returned together with the randomization r' in Z_q

    Args:
       e (tuple):     ElGamal encryption e = (a,b)
       pk (mpz):      Encryption key pk

    Returns:
        tuple         Re-Encryption (e', r')
    """

    AssertMpz(pk)

    (a, b) = e
    r_prime = randomMpz(secparams.q)
    a_prime = (a * gmpy2.powmod(pk, r_prime, secparams.p)) % secparams.p
    b_prime = (b * gmpy2.powmod(secparams.g, r_prime, secparams.p)) % secparams.p
    e_prime = (a_prime, b_prime)

    return e_prime

class GenReEncryptionTest(unittest.TestCase):
    def testGenReEncryption(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
