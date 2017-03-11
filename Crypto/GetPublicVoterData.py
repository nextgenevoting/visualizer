import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils        import Truncate, AssertMpz
from Utils.ToInteger    import ToInteger
from SecurityParams     import secparams_default, secparams_l0, secparams_l3
from RecHash            import RecHash

def GetPublicVoterData(x, y, secparams = secparams_default):
    """
    Algorithm 7.11: Generates the public data for a single voter, which is sent to the bulletin board.

    Args:
       x (mpz):     Voting credential
       y (mpz):     Confirmation credential

    Returns:
       tuple:       Public data of a voter
    """
    AssertMpz(x)
    AssertMpz(y)

    h = ToInteger(RecHash(y, secparams)) % secparams.q_hat
    x_hat = gmpy2.powmod(secparams.g_hat, x, secparams.p_hat)
    y_hat = gmpy2.powmod(secparams.g_hat, y+h, secparams.p_hat)

    return (x_hat, y_hat) # as d_hat

# Unit Tests
class GetPublicVoterDataTest(unittest.TestCase):

    def testOne(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
