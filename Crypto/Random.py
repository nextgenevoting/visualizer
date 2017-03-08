import unittest
import gmpy2
from gmpy2 import mpz
import os
from SecurityParams import secparams_default, secparams_l3
from Utils import AssertNummeric

seed = int.from_bytes(os.urandom(secparams_default.p.bit_length()), byteorder='big')
rstate = gmpy2.random_state(seed)

def randomMpz(n):
    """
    An algorithm for picking elements uniformly at random from Z_n

    @type   n:  int | mpz
    @param  n:  The order of Z

    @rtype:     mpz
    @return:    Random number < n
    """    
    return gmpy2.mpz_random(rstate, n)


def randomBoundedMpz(lb, ub):
    """
    An algorithm for picking elements uniformly at random from Z_ub \ Z_lb

    @type   lb:  int | mpz
    @param  lb:  Lower bound

    @type   ub:  int | mpz
    @param  ub:  Upper bound

    @rtype:     mpz
    @return:    Random Integer < n
    """    
    assertNummeric(lb)
    assertNummeric(ub)


    return gmpy2.mpz_random(rstate, ub - lb) + lb

def randomRelativePrimeMpz(n):
    """
    An algorithm for picking elements uniformly at random from Z_n^*

    @type   n:  int | mpz
    @param  n:  Group order

    @rtype:     mpz
    @return:    Random number < n
    """   
    assertNummeric(n)

    r = 0

    while True:
        r = randomMpz(n)
        if gmpy2.gcd(r, n) == 1:
            break

    return r

def randomEltMpz(g,q):
    """
    An algorithm for picking elements uniformly at random from G

    @type   g:  int | mpz
    @param  g:  generator

    @type   q:  int | mpz
    @param  q:  group order |G|

    @rtype:     mpz
    @return:    Random Integer < n
    """  
    assertNummeric(g)
    assertNummeric(q)
 
    r = randomMpz(q)

    return g ** r


# Unit Tests
class randomMpzTest(unittest.TestCase):
    def testOne(self):
        self.assertTrue(randomMpz(secparams_default.p) in range(0,secparams_default.p)) # TODO        

if __name__ == '__main__':
    unittest.main()
    