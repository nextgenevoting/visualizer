import gmpy2
from gmpy2 import mpz
import unittest
from SecurityContext import SECURITYCONTEXT_DEFAULT, SECURITYCONTEXT_L0, SECURITYCONTEXT_L3
from Utils import ToInteger, AssertNummeric
from Crypto.IsMember import IsMember
from Crypto.Random import randomMpz
from Utils import AssertInt

def GenPolynomial(d, ctx = SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.8: Generates the coefficients a_0,...,a_d of a random polynomial A(X) = Sigma(i=0...d) a_i X^i mod p' of degree d >= 0. 
    The algorithm also accepts d = -1 as input, which we interpret as the polynomial A(X) = 0. 
    In this case, the algorithm returns the coefficient list a = (0).

    @type   d:  int
    @param  d:  Degree d >= -1

    @rtype:     list
    @return:    a list of coefficients a_0 ... a_d of polynomial A(X)
    """
    AssertInt(d)

    a = []
    a_d = 0
    if (d == -1):
        return [0]
    else:
        for i in range (0, d):
            a.append(randomMpz(ctx.p_3))
        # generate the last coefficient != 0
        while a_d == 0: a_d = randomMpz(ctx.p_3)
        a.append(a_d)
    return a
        

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