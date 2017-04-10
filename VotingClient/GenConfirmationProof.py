import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                import AssertClass, AssertMpz
from Utils.Random               import randomMpz, randomQuadResMpz
from Crypto.SecurityParams      import SecurityParams, secparams_default, secparams_l0
from Crypto.GetNIZKPChallenge   import GetNIZKPChallenge

def GenConfirmationProof(y, y_hat, secparams=secparams_default):
    """
    Algorithm 7.33: Generates a NIZKP of knowledge of the secret confirmation
    credential y that matches with a given public confirmation credential y_hat.
    Note that this proof is equivalent to a Schnorr identification proof. For the
    verification of π, see Alg. 7.36.

    Args:
        y:          Secret confirmation credential
        y_hat:      Public confirmation credential

    Returns:
        π:          The NIZKP challenge
    """

    AssertMpz(y)
    AssertClass(secparams, SecurityParams)

    w = randomMpz(secparams.q_hat, secparams)
    t = gmpy2.powmod(secparams.g_hat, w, secparams.p_hat)
    c = GetNIZKPChallenge(y_hat, t, secparams.q_hat)
    s = w + c * y % secparams.q_hat
    pi = (t, s)

    return pi

class GenConfirmationProofTest(unittest.TestCase):
    def testGenConfirmationProof(self):
        # TODO For the verification of π, see Alg. 7.36.

        print(GenConfirmationProof(mpz(1), (1, 2, 3)))

        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
