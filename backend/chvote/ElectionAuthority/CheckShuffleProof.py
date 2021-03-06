import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                        import AssertList, AssertMpz, AssertClass
from chvote.Types                              import *
from chvote.Common.SecurityParams import SecurityParams
from chvote.Common.GetGenerators               import GetGenerators
from chvote.Common.GetNIZKPChallenges          import GetNIZKPChallenges
from chvote.Common.GetNIZKPChallenge          import GetNIZKPChallenge


def CheckShuffleProof(pi, e_bold, e_prime_bold, pk, secparams):
    """
    Algorithm 7.48: Checks the correctness of a NIZKP of a shuffle pi generated by Alg. 7.44.
    The public values are the ElGamal encryptions e and e' and the public encryption key pk.

    Args:
       pi (ShuffleProof):                       Shuffle proof
       e_bold (list):                           ElGamal Encryptions
       e_prime_bold (list):                     Shuffled ElGamal Encryptions e'
       pk (mpz):                                Encryption key pk
       secparams (SecurityParams):              Collection of public security parameters

    Returns:
        ShuffleProof
    """
    AssertClass(pi, ShuffleProof)
    AssertList(e_bold)
    AssertList(e_prime_bold)
    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    N = len(e_bold)
    c_bold = pi.c_bold
    c_hat_bold = pi.c_hat_bold

    s_1 = pi.s[0]
    s_2 = pi.s[1]
    s_3 = pi.s[2]
    s_4 = pi.s[3]
    s_hat = pi.s[4] # tuple
    s_prime = pi.s[5] # list

    t_1 = pi.t[0]
    t_2 = pi.t[1]
    t_3 = pi.t[2]
    t_4_1 = pi.t[3][0]
    t_4_2 = pi.t[3][1]
    t_hat = pi.t[4]

    assert len(e_prime_bold) == N, "The size of e_prime_bold must be identical to N ( = len(e_bold))"
    assert len(c_bold) == N, "The size of c_bold must be identical to N ( = len(e_bold))"
    assert len(c_hat_bold) == N, "The size of c_bold must be identical to N ( = len(e_bold))"
    assert len(pi.t[3]) == 2, "The size of t_4 must be identical to 2"
    assert len(t_hat) == N, "The size of t_hat must be identical to N ( = len(e_bold))"
    assert len(s_hat) == N, "The size of s_hat must be identical to N ( = len(e_bold))"

    h_bold = GetGenerators(N, secparams)
    u_bold = GetNIZKPChallenges(N, (e_bold, e_prime_bold, c_bold), secparams.tau, secparams)
    y = (e_bold, e_prime_bold, c_bold, c_hat_bold, pk)
    c = GetNIZKPChallenge(y, pi.t, secparams.tau, secparams)

    c_product = mpz(1)
    for i in range(N):
        c_product = (c_product * pi.c_bold[i]) % secparams.p

    h_product = mpz(1)
    for i in range(N):
        h_product = (h_product * h_bold[i]) % secparams.p

    c_line = (c_product * gmpy2.invert(h_product, secparams.p)) % secparams.p

    u = mpz(1)
    for i in range(N):
        u = (u * u_bold[i]) % secparams.q

    c_hat = (c_hat_bold[N-1] * gmpy2.invert(gmpy2.powmod(secparams.h,u, secparams.p), secparams.p)) % secparams.p

    c_product2 = mpz(1)
    for i in range(N):
        c_product2 = (c_product2 * gmpy2.powmod(c_bold[i], u_bold[i], secparams.p)) % secparams.p
    c_tilde = c_product2 % secparams.p

    a_prime = mpz(1)
    for i in range(N):
        a_prime = (a_prime * gmpy2.powmod(e_bold[i].a, u_bold[i], secparams.p)) % secparams.p

    b_prime = mpz(1)
    for i in range(N):
        b_prime = (b_prime * gmpy2.powmod(e_bold[i].b, u_bold[i], secparams.p)) % secparams.p

    t_prime_1 = (gmpy2.powmod(c_line, -c, secparams.p) * gmpy2.powmod(secparams.g, s_1, secparams.p)) % secparams.p
    t_prime_2 = (gmpy2.powmod(c_hat, -c, secparams.p) * gmpy2.powmod(secparams.g, s_2,secparams.p)) % secparams.p
    h_product2 = mpz(1)
    for i in range(N):
        h_product2 = (h_product2 * gmpy2.powmod(h_bold[i], s_prime[i], secparams.p)) % secparams.p
    t_prime_3 = (gmpy2.powmod(c_tilde, -c, secparams.p) * gmpy2.powmod(secparams.g, s_3,secparams.p) * h_product2) % secparams.p

    a_prime_product = mpz(1)
    for i in range(N):
        a_prime_product = (a_prime_product * gmpy2.powmod(e_prime_bold[i].a, s_prime[i], secparams.p)) % secparams.p
    t_prime_4_1 = (gmpy2.powmod(a_prime, -c, secparams.p) * gmpy2.powmod(pk, -s_4, secparams.p) * a_prime_product) % secparams.p

    b_prime_product = mpz(1)
    for i in range(N):
        b_prime_product = (b_prime_product * gmpy2.powmod(e_prime_bold[i].b, s_prime[i], secparams.p)) % secparams.p
    t_prime_4_2 = (gmpy2.powmod(b_prime, -c, secparams.p) * gmpy2.powmod(secparams.g, -s_4, secparams.p) * b_prime_product) % secparams.p


    c_hat_bold_tmp = []
    c_hat_bold_tmp.append(secparams.h)
    c_hat_bold_tmp.extend(c_hat_bold)

    t_hat_prime_bold = [None] * N
    for i in range(N):
        t_hat_prime_bold[i] = (gmpy2.powmod(c_hat_bold_tmp[i+1], -c, secparams.p) * gmpy2.powmod(secparams.g, s_hat[i], secparams.p) * gmpy2.powmod(c_hat_bold_tmp[i], s_prime[i], secparams.p)) % secparams.p

    return (t_1 == t_prime_1) and (t_2 == t_prime_2) and (t_3 == t_prime_3) and (t_4_1 == t_prime_4_1) and (t_4_2 == t_prime_4_2) and (t_hat == t_hat_prime_bold)

class CheckShuffleProofTest(unittest.TestCase):
    def testCheckShuffleProof(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
