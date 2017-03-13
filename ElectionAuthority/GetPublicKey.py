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

def GetPublicKey(pk, secparams=secparams_default):
    """
    Algorithm 7.16: Computes a public ElGamal encryption key pk in G_q from given shares pk_j in G_q

    Args:
        pk (list):   List of public keys = (pk_1, ... , pk_s), pk_j in G_q

    Returns:
        mpz:    Public Key pk
    """
    resultPk = mpz(1)
    for j in range(secparams_default.s):  # loop over s (authorities)
        resultPk *= pk[j]
    resultPk = resultPk % secparams.p

    AssertMpz(resultPk)
    return resultPk


class GetPublicKeyTest(unittest.TestCase):
    def test(self):
        pk = GetPublicKey([20,25,30], secparams_l0)
        self.assertEqual(pk, 362)  # 20 * 25 * 30 % secparams_l0 = 15000 % 563 = 362

if __name__ == '__main__':
    unittest.main()
