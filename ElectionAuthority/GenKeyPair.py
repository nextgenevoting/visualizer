import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils            import AssertMpz
from Utils.ToInteger        import ToInteger
from Utils.RecHash          import RecHash
from Utils.Random           import randomMpz
from Crypto.SecurityParams  import secparams_default, secparams_l0, secparams_l3

def GenKeyPair(secparams=secparams_default):
    """
    Algorithm 7.15: Generates a random ElGamal encryption key pair (sk, pk) in Z_q x G_q.
    This algorithm is used in Prot. 6.3 by the authorities to generate private shares of a common public encryption key.

    Args:

    Returns:
        tuple:    Key Pair (sk, pk) in Z_q x G_q.
    """
    sk = randomMpz(secparams.q, secparams)
    pk = gmpy2.powmod(secparams.g, sk, secparams.p)
    return (sk,pk)

class GenKeyPairTest(unittest.TestCase):
    def test(self):
        (sk, pk) = GenKeyPair(secparams_l3)
        self.assertTrue(sk.bit_length() in range(secparams_l3.q.bit_length()-5, secparams_l3.q.bit_length()+1))
        self.assertTrue(pk.bit_length() in range(secparams_l3.p.bit_length()-5, secparams_l3.p.bit_length()+1))

    def testDeterministic(self):
        (sk,pk) = GenKeyPair(secparams_l0)
        self.assertEqual(sk, mpz(2))        # deterministic randomMpz returns 2
        self.assertEqual(pk, mpz(16))       # 4^2 mod 563 = 16

if __name__ == '__main__':
    unittest.main()
