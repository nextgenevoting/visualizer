import gmpy2
from gmpy2 import mpz

class SecurityParams(object):
    """
    This class holds all public security parameters used by many algorithms
    For every security level, a separate object should exist holding the corresponding values.

    For the purpose of easier unit testing, the parameters for securityLevel0 can then be injected as an ptional parameter into the algorithms

    TODO: Should be made const (intercepting setter) as the values do not change
    """

    p = q = k = g = h = 0

    def __init__(self, p, q, k, g, h):
        self.p = p
        self.q = q
        self.k = k
        self.g = g
        self.h = h


SECURITY_LEVEL_0 = SecurityParams(563, 281, 2, 4, 9)
SECURITY_LEVEL_1 = SecurityParams(423432, 234234, 23432, 343, 43243)
#....
SECURITY_LEVEL_DEFAULT = SECURITY_LEVEL_0