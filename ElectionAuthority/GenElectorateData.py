import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                          import AssertClass, AssertList
from Crypto.SecurityParams                import SecurityParams, secparams_l0, secparams_l3
from ElectionAuthority.GenPoints          import GenPoints
from ElectionAuthority.GenSecretVoterData import GenSecretVoterData
from ElectionAuthority.GetPublicVoterData import GetPublicVoterData
from UnitTestParams                       import unittestparams
from Types                                import *


def GenElectorateData(n_bold, k_bold, E_bold, secparams):
    """
    Algorithm 7.6: Generates the data for the whole electorate

    Args:
        n_bold (list of int):                A list containing the number of candidates: (n_1, ... , n_t)
        k_bold (list of int):                A list containing the number of possible selections per election: (k_1, ... , k_t)
        E_bold (list of list):               Eligibility matrix [N][t], 1 means eligible
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                               (d, d^, P, K)
    """

    AssertList(n_bold)
    AssertList(k_bold)
    AssertList(E_bold)
    AssertClass(secparams, SecurityParams)

    N_E = len(E_bold)
    t = len(k_bold)

    d_bold = []
    d_hat_bold = []
    K_bold = []                                      #  precomputed selection matrix Nxt
    P_bold = []

    for i in range (N_E):                         # loop over N (all voters)
        K_i_bold = []
        for j in range(t):
            k_ij = E_bold[i][j] * k_bold[j]               # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j
            K_i_bold.append(k_ij)

        # generate n random points
        p_bold, y_bold = GenPoints(n_bold, K_i_bold, secparams)

        # generate x, y values, finalization code and return codes
        d_hat_i = GenSecretVoterData(p_bold, secparams)

        # prepare return values
        d_bold.append(d_hat_i)                     # private voter data
        d_hat_bold.append(GetPublicVoterData(d_hat_i.x_i,d_hat_i.y_i, y_bold, secparams)) # public voter data
        K_bold.append(K_i_bold)                           # precomputed selection matrix Nxt
        P_bold.append(p_bold)                             # points on the polynomials

    return (d_bold, d_hat_bold, P_bold, K_bold)

class GenElectorateDataTest(unittest.TestCase):
    def testGenElectorateData(self):
        # Test with 2 voters, 2 elections, 2*3 candidates
        d, d_hat, P, K = GenElectorateData(unittestparams.n, unittestparams.k, unittestparams.E, secparams_l3)

        # Test if len(d) matches the number of voters (3)
        self.assertTrue(len(d) == 2)

        # Check the secret voter data
        # The elements of d must be tuples with 4 values
        for d_i in d:
            self.assertTrue(len(d_i) == 4 and d_i[0].__class__.__name__ == 'mpz' and d_i[1].__class__.__name__ == 'mpz' and isinstance(d_i[2], bytes) and isinstance(d_i[3], list))
            self.assertTrue(len(d_i[3]) == 6)    # total number of candidates

if __name__ == '__main__':
    unittest.main()
