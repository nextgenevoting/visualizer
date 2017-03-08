import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import gmpy2
from gmpy2 import mpz
import unittest
from Utils import ToInteger, AssertInt, AssertList
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L3
from Crypto.GenPolynomial import GenPolynomial
from Crypto.GetYValue import GetYValue
from Crypto.IsMember import IsMember
from Crypto.Random import randomMpz
from ElectionEvent import dummyElectionEvent

def GenPoints(n,k, electionEvent, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.7: Generates a list of n random points picket from t random polynomials
    A_j(X) of degree k_j - 1 (by picking n_j different random points from each polynomial).
    Additional, the values y_j = A_j(0) are computed for all random polynomials and returned together with the random points.

    remarks: 
    - t stands for the number of simultaneous elections
    - j \in {1, ..., t} is an identifier for the elections in an election event
    - n_j >= 2 denotes the number of candidates in the j-th election of an election event
    - k_j , 0 < k_j < n_j indicates the number of candidates a voter can select in each selection j and must be 0 < k_j < n_j
    - The total numberof selections over all elections  is therefore k = Sigma(j=1..t) k_j

    @type   n:  list
    @param  n:  List containing the number of candidates per election: n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j

    @type   k:  list
    @type   k:  List containing the number of selections k = (k_1, ..., k_t), 0 <= k_j <= n_j # k_j = 0 means ineligible

    @rtype:     Tuple
    @return:    (p,y)       p \in (Z_p^2)^n, y \in Z_q^t
    """    
    AssertList(n)
    AssertList(k)

    points = []
    yValues = []
    for j in range(0, len(electionEvent.elections)):
        a_j = GenPolynomial(k[j]-1, ctx)     # the number of 1's in the eligibility matrix indicate how many selections the voter can make and therefore decides the degree of the polynomial
        X = []
        for l in range(0, n[j]):           # loop over all candidates of election j
            x = 0
            # get a unique x from Z_p'
            while True:
                x = randomMpz(ctx.p_3)
                if x not in X:
                    X.append(x)
                    break;
            y = GetYValue(x,a_j,ctx)      # get the corresponding y value of x on the polynomial a_j
            p = (x,y)                     # Point tuple
            points.append(p)              # part of the private voter data
        yValues.append(GetYValue(0,a_j, ctx))     # Point (0,Y(0))

    return (points, yValues)

# Unit Tests
class GenPointsTest(unittest.TestCase):

    def testOne(self):
        # generate dummy points
        a = GenPoints(10, 5, dummyElectionEvent, SECURITYCONTEXT_L3)
        
        # check if the number of points returned matches the total number of candidates
        self.assertTrue(len(a[0]) == dummyElectionEvent.n)
        
        # check if the number of y values for x=0 matches the number of simult. elections (= the number of polynoms)
        self.assertTrue(len(a[1]) == dummyElectionEvent.t)
        
        for point in a[0]:
            # check if each point consists of 2 mpz values
            self.assertTrue(len(point) == 2)
            # check if each point is a tuple
            self.assertTrue(isinstance(point, tuple))
            # check if x and y of each point are mpz values
            self.assertTrue(point[0].__class__.__name__ == 'mpz')
            self.assertTrue(point[1].__class__.__name__ == 'mpz')

if __name__ == '__main__':
    unittest.main()
