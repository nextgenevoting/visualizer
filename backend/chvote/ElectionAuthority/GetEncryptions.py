import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import SecurityParams, secparams_l0, secparams_l3
from chvote.Utils.Utils                       import AssertList, AssertClass
from chvote.Types                             import *
from chvote.ElectionAuthority.HasConfirmation import HasConfirmation
from chvote.Common.GetPrimes                  import GetPrimes

def GetEncryptions(B, C, n_bold, w_bold, secparams):
    """
    Algorithm 7.40: Computes a sorted list of ElGamal encryptions from the list of submitted
    ballots, for which a valid confirmation is available. Sorting this list is necessary
    to guarantee a unique order. For this, we define a total order over G_q^2 by e_i <= e_j
    <-> (a_i < a_j) or (a_i = a_a and b_i <= b_j), for e_i = (a_i, b_i) and e_j = (a_j, b_j)

    Args:
        B (list of Ballot):                Ballot List
        C (list of tuple):                 Confirmation list C
        n_bold (list):                     Number of candidates n
        w_bold (list):                     Counting circles w
        secparams (SecurityParams):         Collection of public security parameters


    Returns:
        list of ElGamalEncryption:         ElGamal Encryptions
    """

    AssertList(B)
    AssertList(C)
    AssertList(n_bold)
    AssertList(w_bold)
    AssertClass(secparams, SecurityParams)

    n = sum(n_bold)
    w = max(w_bold)
    p_bold = GetPrimes(n+w, secparams)
    i = 0

    e_bold = []
    for j in range(len(B)):
        #(v, alpha, z) = B[j]
        v = B[j].voterId
        alpha = B[j].ballot
        z = B[j].randomizations

        a_1 = mpz(1)
        a_2 = mpz(1)
        if HasConfirmation(v, C, secparams):
            a_j_1_product = mpz(1)
            for j in range(len(alpha.a_bold)):
                a_j_1_product = (a_j_1_product * alpha.a_bold[j][0]) % secparams.p
                a_2 = (a_2 * alpha.a_bold[j][1]) % secparams.p
            a_1 = (p_bold[(n-1)+w_bold[v]] * a_j_1_product) % secparams.p
            e_bold.append(ElGamalEncryption(a_1, a_2))

            i += 1

    e_bold.sort(key=lambda enc: (enc.a, enc.b), reverse=False)

    return e_bold

class GetEncryptionsTest(unittest.TestCase):
    def testGetEncryptions(self):
        ballot = Ballot(x_hat=mpz(607), a=[mpz(401), mpz(423)], b=mpz(256), pi=BallotProof(t=(mpz(161), mpz(195), mpz(16)), s=(mpz(48), mpz(292), mpz(101))))
        ballot2 = Ballot(x_hat=mpz(607), a=[mpz(401), mpz(423)], b=mpz(256), pi=BallotProof(t=(mpz(161), mpz(195), mpz(16)), s=(mpz(48), mpz(292), mpz(101))))
        B = [(607,ballot, 123), (111 ,ballot2, 123),]
        e = GetEncryptions(B, [(607,14234234), (111,4234234)], secparams_l0)
        self.assertEqual(len(B), len(e))

    def testGetEncryptionsWhenEmpty(self):
        ballot = Ballot(x_hat=mpz(607), a=[mpz(401), mpz(423)], b=mpz(256),pi=BallotProof(t=(mpz(161), mpz(195), mpz(16)),s=(mpz(48), mpz(292), mpz(101))))
        B = [(607,ballot, 123)]
        e = GetEncryptions(B, [], secparams_l0)
        self.assertEqual(len(e), 0)

if __name__ == '__main__':
    unittest.main()
