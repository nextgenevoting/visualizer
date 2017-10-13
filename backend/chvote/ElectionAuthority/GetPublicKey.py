import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertMpz, AssertClass, AssertList
from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3

def GetPublicKey(pk_bold, secparams):
    """
    Algorithm 7.16: Computes a public ElGamal encryption key pk ∈ G_q from given shares pk_j ∈ G_q

    Args:
       pk_bold (list of mpz):              List of public keys = (pk_1, ... , pk_s), pk_j ∈ G_q
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
        mpz:                               Public Key pk
    """

    AssertList(pk_bold)
    AssertClass(secparams, SecurityParams)

    resultPk = mpz(1)

    for j in range(secparams.s): # loop over s (authorities)
        resultPk = (resultPk * pk_bold[j]) % secparams.p

    AssertMpz(resultPk)

    return resultPk

class GetPublicKeyTest(unittest.TestCase):
    def testGetPublicKeyL0(self):
        pk = GetPublicKey([20,25,30], secparams_l0)
        self.assertEqual(pk, 362) # 20 * 25 * 30 % secparams_l0 = 15000 % 563 = 362

if __name__ == '__main__':
    unittest.main()
