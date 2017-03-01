import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from IsMember import IsMember
from Random import randomMpz
import unittest
from Utils import ToInteger


def GenPoints(d, ctx = SECURITYCONTEXT_DEFAULT):
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
#    for j in range(1
            

def printPolynomial(a):
    """ 
    Helper function to print a polynomial with coefficients a 

    @type   a:  list
    @param  a:  List of coefficients for polynomial P

    @rtype:     void
    @return:
    """
    print("P(x)=", end='')
    for i in range(len(a)):
        print("%dx^%d" % (a[i], i), end='')
        if i != len(a)-1: print(" + ", end='')
    print('')

# Unit Tests
class GenPolynomialTest(unittest.TestCase):

    def testOne(self):
        # check if a polynomial of degree x has x+1 coefficients
        self.assertTrue(len(GenPolynomial(5)) == 6)

        # test for security level 3
        a = GenPolynomial(5, SECURITYCONTEXT_L3)

        printPolynomial(a)
        self.assertTrue(len(a) == 6)

if __name__ == '__main__':
    unittest.main()