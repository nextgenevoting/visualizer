import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                        import AssertList, AssertInt, AssertMpz, AssertClass
from Types                              import *
from Crypto.SecurityParams              import secparams_l3, secparams_l0, SecurityParams
from Crypto.GetNIZKPChallenge           import GetNIZKPChallenge

def CheckDecryptionProof(pi_prime, pk_j, e_bold, b_prime_bold, secparams):
    """
    Algorithm 7.52: Checks the correctness of a decryption proof  generated by Alg. 7.50.
    The public values are the ElGamal encryptions e, the partial decryptions b1, and the
    share pkj of the public encryption key.

    Args:
        pi_prime (DecryptionProof):                 Decryption
        pk_j (mpz):                                 Encryption key share
        e_bold (list of ElGamalEncryption):         ElGamal encryptions
        b_prime_bold (list):                        Partial decryptions
        secparams (SecurityParams):                 Collection of public security parameters

    Returns:
        bool:                                       (t_0 = t_prime_0) and for i = 1..N: t_i = t_prime_i
    """
    #AssertMpz(pi_prime)
    AssertMpz(pk_j)
    AssertList(e_bold)
    AssertList(b_prime_bold)
    AssertClass(secparams, SecurityParams)

    t_0 = pi_prime.t[0]
    t_1_to_N = pi_prime.t[1]

    b_bold = [e.b for e in e_bold]
    y = (pk_j, b_bold, b_prime_bold)
    c = GetNIZKPChallenge(y, pi_prime.t,secparams.tau, secparams)
    t_prime_0 = (gmpy2.powmod(pk_j, -c, secparams.p) * gmpy2.powmod(secparams.g, pi_prime.s, secparams.p)) % secparams.p

    t_prime_bold = []
    N = len(e_bold)
    for i in range(N):
        t_prime_bold.append((gmpy2.powmod(b_prime_bold[i],-c, secparams.p) * gmpy2.powmod(b_bold[i], pi_prime.s, secparams.p)) % secparams.p)


    return (t_0 == t_prime_0 and t_prime_bold == t_1_to_N)



class CheckDecryptionProofsTest(unittest.TestCase):
    def testCheckDecryptionProofs(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
