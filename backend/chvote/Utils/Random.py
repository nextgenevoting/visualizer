import gmpy2
import os
import sys
import unittest
from gmpy2 import mpz
from random import randint

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Common.SecurityParams import secparams_l0, secparams_l3

seed = int.from_bytes(os.urandom(secparams_l3.p.bit_length()), byteorder='big')
rstate = gmpy2.random_state(seed)

def randomMpz(n, secparams):
    """
    An algorithm for picking elements uniformly at random from Z_n

    Args:
       n (int | mpz):                       The order of Z
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       mpz:     Random number < n (returns 2 if deterministic mode is set)
    """

    if not secparams.deterministicRandomGen:
        r = gmpy2.mpz_random(rstate, n)     # mpz_random(random_state, n) returns a uniformly distributed random integer between 0 and n-1
        if r == 0:
            r == 1
        return r
    else:
        return mpz(2)

def randomInt(n, secparams):
    """
    An algorithm for picking elements uniformly at random from Z_n

    Args:
       n (int):                             The order of Z
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       int:     Random number < n (returns 2 if deterministic mode is set)
    """

    if not secparams.deterministicRandomGen:
        randint(1, n)
    else:
        return 2

def randomQuadResMpz(secparams):
    """
    An algorithm for picking elements uniformly at random from G_q \subset Z_p^*

    Args:

    Returns:
       mpz:                                 Random element of G_q
       secparams (SecurityParams):          Collection of public security parameters
    """

    if not secparams.deterministicRandomGen:
        x = randomMpz(secparams.q, secparams)
        return gmpy2.powmod(secparams.g, x, secparams.p)
    else:
        return mpz(2)

def randomBoundedMpz(lb, ub, secparams):
    """
    An algorithm for picking elements uniformly at random from Z_ub \ Z_lb

    Args:
       lb (int | mpz):                      lower bound
       ub (int | mpz):                      upper bound
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       mpz:     Random number: lb < r < ub (returns lb if deterministic mode is set)
    """

    assert(ub > lb)

    if not secparams.deterministicRandomGen:
        return gmpy2.mpz_random(rstate, ub - lb) + lb
    else:
        return mpz(lb)

def randomBoundedInt(lb, ub, secparams):
    """
    An algorithm for picking elements uniformly at random from Z_ub \ Z_lb

    Args:
       lb (int):                            lower bound
       ub (int):                            upper bound
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       int:         Random number: lb < r < ub (returns lb if deterministic mode is set)
    """

    assert(ub >= lb)

    if not secparams.deterministicRandomGen:
        return randint(lb, ub)
    else:
        return lb

def randomRelativePrimeMpz(n, secparams):
    """
    An algorithm for picking elements uniformly at random from Z_n^*

    Args:
       n (int | mpz):                       Group order
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       mpz:     Random number < n (returns 1 if deterministic mode is set)
    """

    # check for deterministic mode and return before doing the while True loop,
    # otherwise (depending on the deterministic randomMpz result, we might end up
    # being stuck in an endless loop

    if secparams.deterministicRandomGen:
        return mpz(1)

    while True:
        r = randomMpz(n, secparams)
        if gmpy2.gcd(r, n) == 1:
            break

    return r

def randomEltMpz(g, q, secparams):
    """
    An algorithm for picking elements uniformly at random from G

    Args:
       g (int | mpz):                       generator
       q (int | mpz):                       group order |G|
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       mpz:     Random group element (returns g^1 if deterministic mode is set)
    """

    r = randomMpz(q, secparams)

    if not secparams.deterministicRandomGen:
        return mpz(g ** r)
    else:
        return mpz(g ** 1)

class randomMpzTest(unittest.TestCase):
    def testBounds(self):
        # check that the bit_length of the randomly generated number is close to the upper bound
        self.assertTrue(randomMpz(secparams_l3.p).bit_length() >= secparams_l3.p.bit_length() - 10)

        for i in range(100):
            r = randomBoundedMpz(2 ** 1024,  2 ** 1028).bit_length()
            self.assertTrue(r >= 1024 and r <= 1028)

    def testReturnTypes(self):
        for i in range(200):
            self.assertEqual(randomMpz(2 ** i, secparams_l0).__class__.__name__, 'mpz')
            self.assertEqual(randomBoundedMpz(2 ** i, 2 ** (i + 1), secparams_l0).__class__.__name__, 'mpz')
            self.assertEqual(randomRelativePrimeMpz(2 ** i, secparams_l0).__class__.__name__, 'mpz')
            self.assertEqual(randomEltMpz(2, 11, secparams_l0).__class__.__name__, 'mpz')

    def testDeterminism(self):
        for i in range(200):
            # randomMpz should always return 2 with deterministic random gen
            self.assertEqual(randomMpz(2**i, secparams_l0), 2)
            # randomBoundedMpz should always return lb with deterministic random gen
            self.assertEqual(randomBoundedMpz(2**i, 2**(i+1), secparams_l0), 2**i)
            # randomRelativePrimeMpz should always return 1 with deterministic random gen
            self.assertEqual(randomRelativePrimeMpz(2**i, secparams_l0), 1)
            # randomEltMpz should always return g^1 with deterministic random gen
            self.assertEqual(randomEltMpz(2,11, secparams_l0), 2**1)

if __name__ == '__main__':
    unittest.main()
