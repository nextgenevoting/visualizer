import os
import sys
import unittest
from gmpy2 import mpz

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Types                           import Point
from chvote.Utils.Utils                     import AssertInt
from chvote.Utils.Random                    import randomMpz
from chvote.Common.SecurityParams import secparams_l3, secparams_l0
from chvote.ElectionAuthority.GenPolynomial import GenPolynomial
from chvote.ElectionAuthority.GetYValue     import GetYValue
from chvote.UnitTestParams                  import unittestparams

def GenPoints(n, k, secparams):
    """
    Algorithm 7.7: Generates a list of n random points picket from t random polynomials
    A_j(X) of degree k_j - 1 (by picking n_j different random points from each polynomial).
    Additional, the values y_j = A_j(0) are computed for all random polynomials and returned together with the random points.

    Args:
        n (int):                            Number of candidates n >= 2
        k (int):                            Number of selections 0 < k < n
        secparams (SecurityParams):         Collection of public security parameters

    Returns:
        tuple:        (p,y'), points p ∈ (Z_p^2)^n, and the y value of x=0
    """

    AssertInt(n)
    AssertInt(k)

    p_bold = []

    a_bold = GenPolynomial(k - 1, secparams)               # the number of 1's in the eligibility matrix indicate how many selections the voter can make and therefore decides the degree of the polynomial
    X = []

    for i in range(n):
        x = mpz(0)
        # get a unique x from Z_p'
        while True:
            x = randomMpz(secparams.p_prime, secparams)
            if x not in X or secparams.deterministicRandomGen:      # if randomMpz is deterministic, we would be stuck in an endless loop
                X.append(x)
                break

        y = GetYValue(x,a_bold,secparams)                    # get the corresponding y value of x on the polynomial a_j
        p_i = Point(x,y)                                # Point tuple
        p_bold.append(p_i)                              # part of the private voter data

        y_prime = GetYValue(mpz(0),a_bold, secparams)        # Point (0,Y(0))

    return (p_bold, y_prime)

class GenPointsTest(unittest.TestCase):
    def testGenPoints(self):
        # generate dummy points
        points, y = GenPoints(2, 2, secparams_l3)

        # check if the number of points returned matches the total number of candidates
        self.assertTrue(len(points) == 2)


        for point in points:
            # check if each point consists of 2 mpz values
            self.assertTrue(len(point) == 2)
            # check if each point is a tuple
            self.assertTrue(isinstance(point, tuple))
            # check if x and y of each point are mpz values
            self.assertTrue(point[0].__class__.__name__ == 'mpz')
            self.assertTrue(point[1].__class__.__name__ == 'mpz')

    def testGenPointsL0(self):
        # Important! If deterministic random generation is enabled, and n > 1
        # genPoints will loop forever because it cannot find 2 x values from Z_p'!
        secparams = secparams_l0
        # make sure determnistic random gen is enabled!
        assert(secparams.deterministicRandomGen == True)
        points, y = GenPoints(2, 1, secparams)
        i = 1

if __name__ == '__main__':
    unittest.main()
