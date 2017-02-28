import unittest
import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi
from SecurityContext import SECURITYCONTEXT_DEFAULT

def IsMember(x, ctx=SECURITYCONTEXT_DEFAULT):
    """
    Algorithm 7.2: Checks if x P N is an element of Gq.
    The core of the algorithm is the computation of the Jacobi symbol
    for which we refer to existing algorithms

    @type   x:  mpz
    @param  x:  The number to test x \in N

    @rtype:     list
    @return:    a list with length n containing the first n prime numbers in G_p
    """

    if 1 <= x and x < ctx.p:
        j = jacobi(x, ctx.p)

        if j == 1:
            return True

    return False

# Unit Tests
class GetPrimesTest(unittest.TestCase):
    def testOne(self):
        self.assertTrue(IsMember(mpz(1)))

if __name__ == '__main__':
    unittest.main()
