import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                import AssertMpz
from Utils.Random               import randomMpz
from Crypto.SecurityParams      import secparams_default
from Crypto.GetNIZKPChallenge   import GetNIZKPChallenge

def GenBallotProof(x, m, r, x_hat, a, b, pk, secparams=secparams_default):
    """
    Algorithm 7.21: Generates a NIZKP, which proves that the ballot has been formed properly.
    This proof includes a proof of knowledge of the secret voting credential x that matches with
    the public voting credential x_hat. Note that this is equivalent to a Schnorr Identification proof.

    Args:
        x (mpz):    Voting credential in Z_q_hat
        m (mpz):    Product of selected primes m in G_q
        r (mpz):    Randomization r in Z_q
        a (mpz):    ElGamal Encryption
        b (mpz):    ElGamal Encryption
        pk (mpz):   Encryption key pk in G_q

    Returns:
        tuple:     ((t_1, t_2, t_3), (s_1, s_2, s_3))
    """

    AssertMpz(x)
    AssertMpz(m)
    AssertMpz(r)
    AssertMpz(x_hat)
    AssertMpz(a)
    AssertMpz(b)
    AssertMpz(pk)

    w_1 = randomMpz(secparams.q_hat, secparams)
    w_2 = randomMpz(secparams.q, secparams)
    w_3 = randomMpz(secparams.q, secparams)
    t_1 = gmpy2.powmod(secparams.g_hat, w_1, secparams.p_hat)
    t_2 = w_2 * gmpy2.powmod(pk, w_3, secparams.p)
    t_3 = gmpy2.powmod(secparams.g, w_3, secparams.p)

    y = (x_hat, a, b)
    t = (t_1, t_2, t_3)
    c = GetNIZKPChallenge(y, t, min(secparams.q, secparams.q_hat))

    s_1 = w_1 + c * x % secparams.q_hat
    s_2 = w_2 * gmpy2.powmod(m, c, secparams.p)
    s_3 = w_3 + c * r % secparams.q

    s = (s_1, s_2, s_3)

    return (t,s)

class GenBallotProofTest(unittest.TestCase):
    def testGenBallotProof(self):
        self.assertTrue(False) # TODO

if __name__ == '__main__':
    unittest.main()