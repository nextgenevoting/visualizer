import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertMpz, AssertClass
from chvote.Types                 import *
from chvote.Utils.Random          import randomMpz
from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3

def GenReEncryption(e, pk, secparams):
    """
    Algorithm 7.43: Generates a re-encryption e' = (a * pk^r', b*g^r') of the given ElGamal encryption
    e = (a,b) in G_q^2. The re-encryption e' is returned together with the randomization r' in Z_q

    Args:
       e (tuple):                          ElGamal encryption e = (a,b)
       pk (mpz):                           Encryption key pk
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
        tuple         Re-Encryption (e', r')
    """

    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    (a, b) = e
    r_prime = randomMpz(secparams.q, secparams)
    a_prime = (a * gmpy2.powmod(pk, r_prime, secparams.p)) % secparams.p
    b_prime = (b * gmpy2.powmod(secparams.g, r_prime, secparams.p)) % secparams.p
    e_prime = ElGamalEncryption(a_prime, b_prime)

    return (e_prime, r_prime)

class GenReEncryptionTest(unittest.TestCase):
    def testGenReEncryption(self):
        # Testing is done with integration tests
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
