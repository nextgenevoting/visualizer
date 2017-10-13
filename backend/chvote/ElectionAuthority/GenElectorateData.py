import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils import AssertClass, AssertList
from chvote.Common.SecurityParams import SecurityParams, secparams_l3
from chvote.ElectionAuthority.GenPoints import GenPoints
from chvote.ElectionAuthority.GenSecretVoterData import GenSecretVoterData
from chvote.ElectionAuthority.GetPublicVoterData import GetPublicVoterData
from chvote.UnitTestParams import unittestparams


def GenElectorateData(n_bold, k_bold, E_bold, secparams):
    """
    Algorithm 7.6: Generates the data for the whole electorate

    Args:
        n_bold (list of int):                A list containing the number of candidates: (n_1, ... , n_t)
        k_bold (list of int):                A list containing the number of possible selections per election: (k_1, ... , k_t)
        E_bold (list of list):               Eligibility matrix [N][t], 1 means eligible
        secparams (SecurityParams):          Collection of public security parameters

    Returns:
        tuple:                               (d, d^, P)
    """

    AssertList(n_bold)
    AssertList(k_bold)
    AssertList(E_bold)
    AssertClass(secparams, SecurityParams)

    n = sum(n_bold)
    N_E = len(E_bold)
    t = len(k_bold)

    d_bold = []
    d_hat_bold = []
    P_bold = []

    for i in range (N_E):                                      # loop over N (all voters)
        k_prime_i = 0
        for j in range(t):
            k_prime_i = k_prime_i + (E_bold[i][j] * k_bold[j])               # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

        # generate n random points
        p_bold_i, y_prime_i = GenPoints(n, k_prime_i, secparams)
        P_bold.append(p_bold_i)  # points on the polynomials

        # generate x, y values, finalization code and return codes
        d_i = GenSecretVoterData(p_bold_i, secparams)
        d_bold.append(d_i)                     # private voter data

        d_hat_i = GetPublicVoterData(d_i.x_i,d_i.y_i, y_prime_i, secparams)
        d_hat_bold.append(d_hat_i) # public voter data

    return (d_bold, d_hat_bold, P_bold)

class GenElectorateDataTest(unittest.TestCase):
    def testGenElectorateData(self):
        # Test with 2 voters, 2 elections, 2*3 candidates
        d, d_hat, P = GenElectorateData(unittestparams.n, unittestparams.k, unittestparams.E, secparams_l3)

        # Test if len(d) matches the number of voters (3)
        self.assertTrue(len(d) == 2)

        # Check the secret voter data
        # The elements of d must be tuples with 4 values
        for d_i in d:
            self.assertTrue(len(d_i) == 4 and d_i[0].__class__.__name__ == 'mpz' and d_i[1].__class__.__name__ == 'mpz' and isinstance(d_i[2], bytes) and isinstance(d_i[3], list))
            self.assertTrue(len(d_i[3]) == 6)    # total number of candidates

if __name__ == '__main__':
    unittest.main()
