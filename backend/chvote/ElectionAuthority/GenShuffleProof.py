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
from chvote.ElectionAuthority.GenPermutationCommitment import GenPermutationCommitment
from chvote.ElectionAuthority.GenCommitmentChain import GenCommitmentChain
from chvote.Utils.Random                       import randomMpz

def GenShuffleProof(e_bold, e_prime_bold, r_prime_bold, psi, pk, secparams):
    """
    Algorithm 7.44: Generates a NIZKP of shuffle relative to ElGamal encryptions e and e1,
    which is equivalent to proving knowledge of a permutation psi and randomizations r_prime such
    that e_prime = Shuffle_pk(e,r_prime,psi). The algorithm implements Wikström’s proof of a shuffle
    [19, 18], except for the fact that the offline and online phases are merged. For the proof
    verification, see Alg. 7.48. For further background information we refer to Section 5.5.

    Args:
       e_bold (list):                           ElGamal Encryptions
       e_prime_bold (list):                     Shuffled ElGamal Encryptions e'
       r_prime_bold (list):                     Re-encryption randomizations r'
       psi (list):                              Permutation
       pk (mpz):                                Encryption key pk
       secparams (SecurityParams):              Collection of public security parameters

    Returns:
        ShuffleProof
    """
    AssertList(e_bold)
    AssertList(e_prime_bold)
    AssertList(r_prime_bold)
    AssertList(psi)
    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    N = len(e_bold)
    h_bold = GetGenerators(N, secparams)
    (c_bold, r_bold) = GenPermutationCommitment(psi, h_bold, secparams)
    u_bold = GetNIZKPChallenges(N, (e_bold, e_prime_bold, c_bold), secparams.tau, secparams)

    u_prime_bold = [None] * N
    for i in range(N):
        u_prime_bold[i] = u_bold[psi[i]]

    (c_hat_bold, r_hat_bold) = GenCommitmentChain(secparams.h, u_prime_bold, secparams)

    w_1 = randomMpz(secparams.q, secparams)
    w_2 = randomMpz(secparams.q, secparams)
    w_3 = randomMpz(secparams.q, secparams)
    w_4 = randomMpz(secparams.q, secparams)

    w_hat_bold = [None] * N
    w_prime_bold = [None] * N
    for i in range(N):
        w_hat_bold[i] = randomMpz(secparams.q, secparams)
        w_prime_bold[i] = randomMpz(secparams.q, secparams)


    # Computing the T values:

    t_1 = gmpy2.powmod(secparams.g, w_1, secparams.p)
    t_2 = gmpy2.powmod(secparams.g, w_2, secparams.p)

    h_product = mpz(1)
    for i in range(N):
        h_product = (h_product * gmpy2.powmod(h_bold[i],w_prime_bold[i], secparams.p) ) % secparams.p

    t_3 = (gmpy2.powmod(secparams.g, w_3, secparams.p) * h_product) % secparams.p

    a_prime_i_product = mpz(1)
    for i in range(N):
        a_prime_i_product = (a_prime_i_product * gmpy2.powmod(e_prime_bold[i].a, w_prime_bold[i], secparams.p)) % secparams.p
    t_4_1 = (gmpy2.powmod(pk, -w_4, secparams.p) * a_prime_i_product) % secparams.p

    b_prime_i_product = mpz(1)
    for i in range(N):
        b_prime_i_product = (b_prime_i_product * gmpy2.powmod(e_prime_bold[i].b, w_prime_bold[i], secparams.p)) % secparams.p
    t_4_2 = (gmpy2.powmod(secparams.g, -w_4, secparams.p) * b_prime_i_product) % secparams.p

    c_hat_bold_tmp = []
    c_hat_bold_tmp.append(secparams.h)
    c_hat_bold_tmp.extend(c_hat_bold)

    t_hat_bold = [None] * N
    for i in range(N):
        t_hat_bold[i] = (gmpy2.powmod(secparams.g, w_hat_bold[i], secparams.p) * gmpy2.powmod(c_hat_bold_tmp[i], w_prime_bold[i], secparams.p) ) % secparams.p

    del c_hat_bold_tmp[0]   # remove the element c_0 that we manually inserted ???????????

    t = (t_1, t_2, t_3, (t_4_1, t_4_2), t_hat_bold)

    # Computing the challenge:
    y = (e_bold, e_prime_bold, c_bold, c_hat_bold, pk)
    c = GetNIZKPChallenge(y, t, secparams.tau, secparams)

    # Computing the S values:
    r_line = mpz(0)
    for i in range(N):
        r_line = (r_line + r_bold[i]) % secparams.q

    s_1 = mpz(0)
    for i in range(N):
        s_1 = (w_1 + c * r_line) % secparams.q

    v_bold = [None] * N
    v_bold[N-1] = mpz(1)
    for i in reversed(range(N-1)):
        v_bold[i] = (u_prime_bold[i+1] * v_bold[i+1]) % secparams.q

    r_hat = mpz(0)
    for i in range(N):
        r_hat = (r_hat + (r_hat_bold[i] * v_bold[i])) % secparams.q
    s_2 = (w_2 + c * r_hat ) % secparams.q

    r_tilde = mpz(0)
    for i in range(N):
        r_tilde = (r_tilde + (r_bold[i] * u_bold[i])) % secparams.q
    s_3 = (w_3 + c* r_tilde ) % secparams.q

    r_prime = mpz(0)
    for i in range(N):
        r_prime = (r_prime + (r_prime_bold[i] * u_bold[i])) % secparams.q
    s_4 = (w_4 + c* r_prime ) % secparams.q

    s_hat_bold = [None] * N
    s_prime_bold = [None] * N
    for i in range(N):
        s_hat_bold[i] = (w_hat_bold[i] + (c * r_hat_bold[i])) % secparams.q
        s_prime_bold[i] = (w_prime_bold[i] + (c * u_prime_bold[i])) % secparams.q

    s = (s_1, s_2, s_3, s_4, s_hat_bold, s_prime_bold)

    pi = ShuffleProof(t,s,c_bold,c_hat_bold)

    return pi

class GenShuffleProofTest(unittest.TestCase):
    def testGenShuffleProof(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
