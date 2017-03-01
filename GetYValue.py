import gmpy2
from gmpy2 import mpz
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from IsMember import IsMember
from Random import randomMpz
from GenPolynomial import GenPolynomial, printPolynomial
import unittest
from Utils import ToInteger


def GetYValue(x, a, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.9: Computes the value y = A(x) \in Z_p' obtained from evaluating the polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' at position x. 
    The algorithm is an implementation of Horners method.

    @type   x:  int
    @param  x:  value x \in Z_p'
    
    @type   a:  list
    @param  a:  list of coefficients

    @rtype:     int
    @return:    a list of coefficients a_0 ... a_d of polynomial A(X)
    """    
    if x == 0:
        y = a[0]
    else:
        y = 0
        for i in reversed(range(len(a))):
            y = (a[i] + x * y) % ctx.p_3
    return y

# Unit Tests
class GetYValueTest(unittest.TestCase):

    def testOne(self):
        # Test 1: Compare with manually calculated value        
        a = [1,3,6,9,15]    # P(x) = 1 + 3x + 6x^2 + 9x^3 + 15x^4
        #solved with wolfram alpha: P(17) = y = (1+3*17 +6*17^2+9*17^3+15*17^4 )% 131 = 84       
        self.assertTrue(GetYValue(17, a, SECURITYCONTEXT_L0) == 84)

if __name__ == '__main__':
    unittest.main()