import securityParameters
from securityParameters import SECURITY_LEVEL_DEFAULT
import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi

import unittest


def IsMember(x, SECURITYPARAMS = SECURITY_LEVEL_DEFAULT):
    """
    Algorithm 7.2: Checks if x P N is an element of Gq. 
    The core of the algorithm is the computation of the Jacobi symbol 
    for which we refer to existing algorithms

    @type   x:  mpz
    @param  x:  The number to test x \in N
    @type   p:  number
    @param  p:  The order of the group G_p (defaults to the specified security level parameters)

    @rtype:     list
    @return:    a list with length n containing the first n prime numbers in G_p
    """
    if (1 <= x and x < SECURITYPARAMS.p):
        j = jacobi(x, SECURITYPARAMS.p)

        if(j == 1):
            return True
    return False
