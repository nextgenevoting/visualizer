import gmpy2
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils           import AssertMpz, AssertClass, AssertList
from chvote.Common.SecurityParams import SecurityParams


def GetPartialDecryptions(e_bold, sk_j, secparams):
    """
    Algorithm 7.49: Algorithm 7.49: Computes the partial decryptions of a given input list e of ElGamal
    encryption using a share sk_j of the private decryption key.

    Args:
       e_bold (list of ElGamalEncryption): ElGamal encryptions
       sk_j (mpz):                         Decryption key share
       secparams (SecurityParams):         Collection of public security parameters

    Returns:
        list of mpz                        Partial decryptions
    """

    AssertList(e_bold)
    AssertMpz(sk_j)
    AssertClass(secparams, SecurityParams)

    b_prime_bold = []
    N = len(e_bold)
    for i in range(N):
        b_prime_bold.append(gmpy2.powmod(e_bold[i][1], sk_j, secparams.p))

    return b_prime_bold


class GetPartialDecryptionsTest(unittest.TestCase):
    def testGetPartialDecryptions(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
