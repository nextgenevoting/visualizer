import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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

    Args:
       n (int | mpz):       The order of Z
    
    Returns:
       mpz:     Random number < n
    """    
    return gmpy2.mpz_random(rstate, n)


def randomBoundedMpz(lb, ub):
    """
    An algorithm for picking elements uniformly at random from Z_ub \ Z_lb

    Args:
       lb (int | mpz):       lower bound
       ub (int | mpz):       upper bound
    
    Returns:
       mpz:     Random numberr: lb < r < ub
    """    


    return gmpy2.mpz_random(rstate, ub - lb) + lb

def randomRelativePrimeMpz(n):
    """
    An algorithm for picking elements uniformly at random from Z_n^*

    Args:
       n (int | mpz):       Group order
    Returns:
       mpz:     Random number < n
    """   


    r = 0

    while True:
        r = randomMpz(n)
        if gmpy2.gcd(r, n) == 1:
            break

    return r

def randomEltMpz(g,q):
    """
    An algorithm for picking elements uniformly at random from G

    Args:
       g (int | mpz):       generator
       q (int | mpz):       group order |G|
    
    Returns:
       mpz:     Random group element
    """  

 
    r = randomMpz(q)

    return g ** r


# Unit Tests
class randomMpzTest(unittest.TestCase):
    def testBounds(self):
        # check that the bit_length of the randomly generated number is close to the upper bound
        self.assertTrue(randomMpz(secparams_default.p).bit_length() >= secparams_default.p.bit_length() - 10)

        for i in range(0,100):
            r = randomBoundedMpz(2**1024,  2**1028).bit_length()
            self.assertTrue(r >= 1024 and r <= 1028)


if __name__ == '__main__':
    unittest.main()
    