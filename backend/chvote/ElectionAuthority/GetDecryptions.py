import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertClass, AssertList
from chvote.Types                 import *
from chvote.Common.SecurityParams import SecurityParams


def GetDecryptions(e_bold, B_prime_bold, secparams):
    """
    Algorithm 7.53: Computes the list of decryptions m = (m_1, ..., m_N) by assembling the
    partial decryptions b_prime_ij obtained from s different authorities.

    Args:
       e_bold (list of ElGamalEncryption): ElGamal encryptions
       B_prime_bold (list of list):        Partial decryptions
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
        list of mpz                        Partial decryptions
    """

    AssertList(e_bold)
    AssertList(B_prime_bold)
    AssertClass(secparams, SecurityParams)

    m_bold = []
    N = len(e_bold)
    for i in range(N):
        b_prime_i = mpz(1)
        for j in range(secparams.s):
            b_prime_i = (b_prime_i * B_prime_bold[j][i]) % secparams.p

        m_bold.append((e_bold[i][0]  * gmpy2.invert(b_prime_i,secparams.p) ) % secparams.p)

    return m_bold


class GetPartialDecryptionsTest(unittest.TestCase):
    def testGetPartialDecryptions(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
