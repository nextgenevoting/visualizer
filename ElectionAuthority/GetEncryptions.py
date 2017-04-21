import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Crypto.SecurityParams             import SecurityParams, secparams_l0, secparams_l3
from Utils.Utils                       import AssertList, AssertClass
from Types                             import *
from ElectionAuthority.HasConfirmation import HasConfirmation

def GetEncryptions(B, C, secparams):
    """
    Algorithm 7.40: Computes a sorted list of ElGamal encryptions from the list of submitted
    ballots, for which a valid confirmation is available. Sorting this list is necessary
    to guarantee a unique order. For this, we define a total order over G_q^2 by e_i <= e_j
    <-> (a_i < a_j) or (a_i = a_a and b_i <= b_j), for e_i = (a_i, b_i) and e_j = (a_j, b_j)

    Args:
        B (list):           Ballot List
        C (list):           Confirmation list C

    Returns:
        list
    """

    AssertList(B)
    AssertList(C)
    AssertClass(secparams, SecurityParams)

    i = 0
    e = []

    for j in range(len(B)):
        (i_j, alpha_j, r_j) = B[j]
        a_j = 1

        if HasConfirmation(i_j, C):
            for l in range(len(alpha_j.a)):
                a_j = (a_j * alpha_j.a[l]) % secparams.p

            e.append((a_j, alpha_j.b))
            i += 1

    e.sort(key=lambda tup: (tup[0], tup[1]), reverse=False)

    return e

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
