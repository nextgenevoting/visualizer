import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils              import AssertMpz, AssertClass, AssertList
from chvote.Utils.Random             import randomMpz, randomQuadResMpz
from chvote.Common.SecurityParams    import SecurityParams, secparams_l0
from chvote.Common.GetNIZKPChallenge import GetNIZKPChallenge
from chvote.UnitTestParams           import unittestparams
from chvote.Types                    import *

def GenBallotProof(x, m, r, x_hat, a_bold, pk, secparams):
    """
    Algorithm 7.21: Generates a NIZKP, which proves that the ballot has been formed properly.
    This proof includes a proof of knowledge of the secret voting credential x that matches with
    the public voting credential x_hat. Note that this is equivalent to a Schnorr Identification proof.

    Args:
        x (mpz):                            Voting credential ∈ Z_q_hat
        m (mpz):                            Product of selected primes m ∈ G_q
        r (mpz):                            Randomization r ∈ Z_q
        a_bold (list):                      OT queries
        pk (mpz):                           Encryption key pk ∈ G_q
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        tuple:                              ((t_1, t_2, t_3), (s_1, s_2, s_3))
    """

    AssertMpz(x)
    AssertMpz(m)
    AssertMpz(r)
    AssertMpz(x_hat)
    AssertList(a_bold)
    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    w_1 = randomMpz(secparams.q_hat, secparams)
    w_2 = randomQuadResMpz(secparams)
    w_3 = randomMpz(secparams.q, secparams)
    t_1 = gmpy2.powmod(secparams.g_hat, w_1, secparams.p_hat)
    t_2 = (w_2 * gmpy2.powmod(pk, w_3, secparams.p)) % secparams.p
    t_3 = gmpy2.powmod(secparams.g, w_3, secparams.p)

    y = (x_hat, a_bold)
    t = (t_1, t_2, t_3)
    c = GetNIZKPChallenge(y, t, secparams.tau, secparams)

    s_1 = (w_1 + c * x) % secparams.q_hat
    s_2 = (w_2 * gmpy2.powmod(m, c, secparams.p)) % secparams.p
    s_3 = (w_3 + c * r) % secparams.q

    s = (s_1, s_2, s_3)

    return BallotProof(t,s)

class GenBallotProofTest(unittest.TestCase):
    def testGenBallotProof(self):
        ballotProof = GenBallotProof(mpz(281401388481450), mpz(22), mpz(4), unittestparams.x_hat, unittestparams.a, unittestparams.b, unittestparams.pk, secparams_l0)
        self.assertTrue(False) # TODO

if __name__ == '__main__':
    unittest.main()
