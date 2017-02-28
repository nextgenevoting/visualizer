import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0
from IsMember import IsMember
import unittest
from Utils import ToInteger



def GenPolynomial(d, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.8: Generates the coefficients a_0;...;a_d of a random polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' of degree d >= 0. 
    The algorithm also accepts d = -1 as input, which we interpret as the polynomial A(X) = 0. 
    In this case, the algorithm returns the coefficient list a = (0).

    @type   d:  number
    @param  d:  Degree d >= -1

    @rtype:     list
    @return:    a list of coefficients a_0 ... a_d of polynomial A(X)
    """    
    a = []
    if (d == -1):
        a = [0]
    else:
        for i in range (0, d):
            a.append()

# Unit Tests
class GenPolynomialTest(unittest.TestCase):

    def testOne(self):
        pass

def main():
    unittest.main()

if __name__ == '__main__':
    main()
