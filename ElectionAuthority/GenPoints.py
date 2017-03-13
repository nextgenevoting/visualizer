import unittest
import os, sys
import gmpy2
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                        import AssertInt, AssertList
from Utils.ToInteger                    import ToInteger
from Utils.Random                       import randomMpz
from SecurityParams                     import secparams_default, secparams_l3, secparams_l0
from Crypto.IsMember                    import IsMember
from ElectionAuthority.GenPolynomial    import GenPolynomial
from ElectionAuthority.GetYValue        import GetYValue
from ElectionEvent                      import dummyElectionEvent

def GenPoints(n,k, t, secparams = secparams_default):
    """
    Algorithm 7.7: Generates a list of n random points picket from t random polynomials
    A_j(X) of degree k_j - 1 (by picking n_j different random points from each polynomial).
    Additional, the values y_j = A_j(0) are computed for all random polynomials and returned together with the random points.

    Args:
        n (list):  A list containing the number of candidates per election: n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j
        k (list):  A list containing the number of selections k = (k_1, ..., k_t), 0 <= k_j <= n_j # k_j = 0 means ineligible

    Returns:
        tuple:        (p,y), points p in (Z_p^2)^n, and the y values of x=0 in Z_q^t
    """
    AssertList(n)
    AssertList(k)

    p = []
    y = []
    for j in range(0, t):
        a_j = GenPolynomial(k[j]-1, secparams)          # the number of 1's in the eligibility matrix indicate how many selections the voter can make and therefore decides the degree of the polynomial
        X = []
        for l in range(0, n[j]):                        # loop over all candidates of election j
            x = 0
            # get a unique x from Z_p'
            while True:
                x = randomMpz(secparams.p_prime, secparams)
                if x not in X:
                    X.append(x)
                    break;
            y_j = GetYValue(x,a_j,secparams)            # get the corresponding y value of x on the polynomial a_j
            p_i = (x,y_j)                               # Point tuple
            p.append(p_i)                               # part of the private voter data
        y.append(GetYValue(0,a_j, secparams))       # Point (0,Y(0))

    return (p, y)

# Unit Tests
class GenPointsTest(unittest.TestCase):

    def testOne(self):
        # generate dummy points
        points, y = GenPoints(dummyElectionEvent.n, [1,2], dummyElectionEvent.t, secparams_l3)

        # check if the number of points returned matches the total number of candidates
        self.assertTrue(len(points) == dummyElectionEvent.n_total)

        # check if the number of y values for x=0 matches the number of simult. elections (= the number of polynoms)
        self.assertTrue(len(y) == dummyElectionEvent.t)

        for point in points:
            # check if each point consists of 2 mpz values
            self.assertTrue(len(point) == 2)
            # check if each point is a tuple
            self.assertTrue(isinstance(point, tuple))
            # check if x and y of each point are mpz values
            self.assertTrue(point[0].__class__.__name__ == 'mpz')
            self.assertTrue(point[1].__class__.__name__ == 'mpz')

    def testDeterministicGenPoints(self):
        # Important! If deterministic random generation is enabled, and n > 1
        # genPoints will loop forever because it cannot find 2 x values from Z_p'!
        secparams = secparams_l0
        # make sure determnistic random gen is enabled!
        assert(secparams.deterministicRandomGen == True)
        points, y = GenPoints([1], [1], 1, secparams)
        i = 1


if __name__ == '__main__':
    unittest.main()