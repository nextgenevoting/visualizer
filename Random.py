import unittest
import gmpy2
from gmpy2 import mpz
import time

# todo: better random seed (os.urandom?)

def randomMpz(n):
    """
    An algorithm for picking elements uniformly at random from Z_n

    @type   n:  int
    @param  n:  The order of Z

    @rtype:     integer
    @return:    Random Integer < n
    """    
    #seed = int(os.urandom(4).encode()
    return gmpy2.mpz_random(gmpy2.random_state(int(time.time())),n)


def randomBoundedMpz(lb, ub):
    """
    An algorithm for picking elements uniformly at random from Z_ub \ Z_lb

    @type   lb:  int
    @param  lb:  Lower bound

    @type   ub:  int
    @param  ub:  Upper bound

    @rtype:     integer
    @return:    Random Integer < n
    """    
    return gmpy2.mpz_random(gmpy2.random_state(int(time.time())),ub-lb) + lb



def randomRelativePrimeMpz(n):
    """
    An algorithm for picking elements uniformly at random from Z_n^*

    @type   n:  int
    @param  n:  Group order

    @rtype:     integer
    @return:    Random Integer < n
    """   
    r = 0
    while True:
        r = randomMpz(n)
        if gmpy2.gcd(r,n) == 1:
            break;

    return r;


def randomEltMpz(g,q):
    """
    An algorithm for picking elements uniformly at random from G

    @type   g:  int
    @param  g:  generator

    @type   q:  int
    @param  q:  group order |G|

    @rtype:     integer
    @return:    Random Integer < n
    """   
    r = randomMpz(q)

    return g**r;


# Unit Tests
class randomMpzTest(unittest.TestCase):
    def testOne(self):
        # tbd
        pass

        
def main():
    unittest.main()

if __name__ == '__main__':
    main()
