import gmpy2
import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                        import AssertList, AssertMpz, AssertClass
from chvote.Types                              import *
from chvote.Common.SecurityParams import SecurityParams
from chvote.Utils.Random                       import randomMpz
from chvote.Common.GetNIZKPChallenge           import GetNIZKPChallenge

def GenDecryptionProof(sk_j, pk_j, e_bold, b_prime_bold, secparams):
    """
    Algorithm 7.50: Generates a decryption proof relative to ElGamal encryptions e and
    partial decryptions b'. This is essentially a NIZKP of knowledge of the private key share
    sk_j satisfying b'_i = b_i^sk_j for all input encryptions e_i = (a_i, b_i) and pk_j = g^sk_j.
    Proof verification, see Alg. 7.52.

    Args:
        sj_j (mpz):                             Decryption key share
        pk_j (mpz):                             Encryption key share
        e_bold (list of ElGamalEncryption):     ElGamal encryptions e_bold
        b_prime_bold (list):                    Partial decryptions
        secparams (SecurityParams):             Collection of public security parameters

    Returns:
        DecryptionProof
    """
    AssertMpz(sk_j)
    AssertMpz(pk_j)
    AssertList(e_bold)
    AssertList(b_prime_bold)
    AssertClass(secparams, SecurityParams)

    w = randomMpz(secparams.q, secparams)
    t_0 = gmpy2.powmod(secparams.g, w, secparams.p)

    t_1_to_N = []
    N = len(e_bold)
    for i in range(N):
        t_1_to_N.append(gmpy2.powmod(e_bold[i].b, w, secparams.p))

    t = (t_0, t_1_to_N)

    b_bold = [e.b for e in e_bold]

    y = (pk_j, b_bold, b_prime_bold)
    c = GetNIZKPChallenge(y, t, secparams.tau, secparams)

    s = (w + c * sk_j) % secparams.q
    pi = DecryptionProof(t,s)

    return pi



class GenDecryptionProofTest(unittest.TestCase):
    def testGenDecryptionProof(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
