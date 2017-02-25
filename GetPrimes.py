import securityParameters
from securityParameters import SECURITY_LEVEL_DEFAULT, SECURITY_LEVEL_0
from gmpy2 import mpz
from IsMember import IsMember



def GetPrimes(n, SECURITYPARAMS = SECURITY_LEVEL_DEFAULT):
    """
    Algorithm 7.1: Computes the first n prime numbers from Gq. The computation possibly
    fails if n is large and p is small, but this case is very unlikely in practice. In a more
    efficient implementation of this algorithm, the resulting list of primes is precomputed for
    the largest expected value n.

    @type   n:  number
    @param  n:  The number of primes to be calculated
    @type   p:  number
    @param  p:  The order of the group G_p (defaults to the specified security level parameters)

    @rtype:     list
    @return:    a list with length n containing the first n prime numbers in G_p
    """
    x = mpz(1)
    primes = []
    for i in range(n):
        while True:
            if x <= 2:
                x += 1
            else:
                x += 2

            if x >= SECURITYPARAMS.p:
                return []                           # n is incompatible with p
            if gmpy2.is_prime(x) and IsMember(x):   # see Alg. 7.2
                break
        primes.append(x)
    
    return primes                                   # p \elementof G_p \cap P)^n
   