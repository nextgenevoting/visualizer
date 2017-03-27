import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                    import AssertMpz, AssertClass
from Crypto.SecurityParams          import SecurityParams, secparams_default, secparams_l0
from Crypto.GetNIZKPChallenge       import GetNIZKPChallenge
from UnitTestParams                 import unittestparams
from VotingClient.GenBallotProof    import GenBallotProof
from Types                          import BallotProof, PublicValue

def CheckBallotProof(pi, x_hat, a, b, pk, secparams=secparams_default):
    """
    Algorithm 7.24: Checks the correctness of a ballot proof Pi generated by Alg. 7.21. The
    public values of this proof are the public voting credential x_hat and the ElGamal encryption (a,b)

    Args:
        pi (BallotProof):   Ballot proof pi = (t,s)
        x_hat (mpz):        Voting credential x_hat
        a (mpz):            ElGamal Encryption
        b (mpz):            ElGamal Encryption
        pk (mpz):           ElGamal key pk

    Returns:
        bool:           (t_1 == t'_1 and t_2 == t'_2 and t_3 == t'_3)
    """
    AssertClass(pi, BallotProof)
    AssertMpz(x_hat)
    AssertMpz(a)
    AssertMpz(b)
    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    y = PublicValue(x_hat, a, b)
    t = pi[0]
    (t_1, t_2, t_3) = t
    s = pi[1]
    (s_1, s_2, s_3) = s

    c = GetNIZKPChallenge(y, t, min(secparams.q, secparams.q_hat), secparams)

    t_prime_1 = (gmpy2.powmod(x_hat, -c, secparams.p_hat) * gmpy2.powmod(secparams.g_hat, s_1, secparams.p_hat)) % secparams.p_hat
    t_prime_2 = (gmpy2.powmod(a, -c, secparams.p) *  s_2 * gmpy2.powmod(pk, s_3, secparams.p)) % secparams.p
    t_prime_3 = (gmpy2.powmod(b, -c, secparams.p) * gmpy2.powmod(secparams.g, s_3, secparams.p)) % secparams.p

    return t_1 == t_prime_1 and t_2 == t_prime_2 and t_3 == t_prime_3

class CheckBallotProofTest(unittest.TestCase):
    def testCheckBallotProofL0(self):
        ballotProof = ((mpz(161), mpz(195), mpz(16)), (mpz(79), mpz(137), mpz(157)))
        x_hat = mpz(607)
        a = mpz(546)
        b = mpz(256)
        pk = mpz(4096)

        self.assertTrue(CheckBallotProof(GenBallotProof(mpz(281401388481450), mpz(22), mpz(4), mpz(252), a, b, pk, secparams_l0), mpz(252), a, b, pk, secparams_l0))
if __name__ == '__main__':
    unittest.main()
