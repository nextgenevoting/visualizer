import unittest
import os, sys
import multiprocessing as mp

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                            import AssertInt, AssertList
from Crypto.SecurityParams                  import secparams_l0, secparams_l1, secparams_l2, secparams_l3, secparams_default
from ElectionAuthority.GenPoints            import GenPoints
from ElectionAuthority.GenSecretVoterData   import GenSecretVoterData
from ElectionAuthority.GetPublicVoterData   import GetPublicVoterData

def GenElectorateData(n, k, E, secparams = secparams_default):
    """
    Algorithm 7.6: Generates the data for the whole electorate

    Args:
        n (list):               A list containing the number of candidates: (n_1, ... , n_t)
        k (list):               A list containing the number of possible selections per election: (k_1, ... , k_t)
        E ([[]]):               Eligibility matrix [N][t], 1 means eligible

    Returns:
        tuple:       (d, d^, P, K)
    """
    AssertList(n)
    AssertList(k)

    N = len(E)
    t = len(k)

    d = []
    d_hat = []
    K = []      #  precomputed selection matrix Nxt
    P = []

    for i in range (N):  # loop over N (all voters)
        K_i = []
        for j in range(0, t):
            k_ij = E[i][j] * k[j]             # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j
            K_i.append(k_ij)

        # generate n random points
        p, y = GenPoints(n, K_i, t, secparams)
        # generate x, y values, finalization code and return codes
        x,y,F,R = GenSecretVoterData(p, secparams)

        # prepare return values
        d.append((x,y,F,R))                     # private voter data
        d_hat.append(GetPublicVoterData(x,y, p, secparams)) # public voter data
        K.append(K_i)                           # precomputed selection matrix Nxt
        P.append(p)                             # points on the polynomials

    return (d, d_hat, P, K)

# Unit Tests
class GenElectorateDataTest(unittest.TestCase):

    def testGenElectorateData(self):
        # Test with 3 voters, 2 elections, 2*3 candidates
        d, d_hat, P, K = GenElectorateData([3,3], [1,1], [[True, True],[True, True],[True, True]], secparams_l3)

        # Test if len(d) matches the number of voters (3)
        self.assertTrue(len(d) == 3)

        # Check the secret voter data
        # The elements of d must be tuples with 4 values
        for d_i in d:
            self.assertTrue(len(d_i) == 4 and d_i[0].__class__.__name__ == 'mpz' and d_i[1].__class__.__name__ == 'mpz' and isinstance(d_i[2], bytes) and isinstance(d_i[3], list))
            self.assertTrue(len(d_i[3]) == 6)    # total number of candidates


    def testGenElectorateDataL0(self):
        # Test with 3 voters, 2 elections, 2*3 candidates
        #d, d_hat, P, K = GenElectorateData([3,3], [1,1], [[True, True],[True, True],[True, True]], secparams_l0)
        self.assertTrue(False)  # TODO


if __name__ == '__main__':
    unittest.main()
