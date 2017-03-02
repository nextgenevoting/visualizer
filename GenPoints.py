import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from IsMember import IsMember
from Random import randomMpz
import unittest
from Utils import ToInteger
from ElectionEvent import electionEvent
from GenPolynomial import GenPolynomial
from GetYValue import GetYValue

def GenPoints(n,k, ctx = SECURITYCONTEXT_DEFAULT, election = electionEvent):
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

    @type   n:  int
    @param  n:  Number of candidates n = (n_1, ..., n_t), n_j >= 2, n = Sigma(j=1...t) n_j

    @type   k:  int
    @type   k:  Number of selections k = (k_1, ..., k_t), 0 <= k_j <= n_j # k_j = 0 means ineligible

    @rtype:     Tuple
    @return:    (p,y)       p \in (Z_p^2)^n, y \in Z_q^t
    """    
    i = 1
    retPoints = []
    retY = []
    for j in electionEvent.elections:
        a_j = GenPolynomial(k-1, ctx)        # the number of 1's in the eligibility matrix indicate how many selections the voter can make and therefore decide the degree of the polynomial
        X = []
        for l in range(0, j.n_j()):                 # loop over all candidates of election j
            # get a unique x from Z_p'
            x = 0
            while True:
                x = randomMpz(ctx.p_3)
                if x not in X:
                    X.append(x)
                    break;
            y = GetYValue(x,a_j,ctx)      # get the corresponding y value of x on the polynomial a_j
            p = (x,y)
            retPoints.append(p)           # part of the private voter data
            i += 1            
        retY.append(GetYValue(0,a_j, ctx))     # Point (0,Y(0))

    return (retPoints, retY)

# Unit Tests
class GenPointsTest(unittest.TestCase):

    def testOne(self):       
        #self.assertTrue(False)
        for v_i in range(0,len(electionEvent.voters)):
            eligibilityCount = 0
            for e_i in range(0, electionEvent.t()):
                eligibilityCount += electionEvent.E[v_i, e_i]

            GenPoints(10, eligibilityCount, ctx)

if __name__ == '__main__':
    unittest.main()