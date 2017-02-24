import gmpy2
from gmpy2 import mpz

# python doesn't have a const keyword. We are using a class with an intercepting setter to create a const class
class ConstSecurityParams(object):
    p = q = k = g = h = 0

    def __init__(self, p, q, k, g, h):
        self.p = p
        self.q = q
        self.k = k
        self.g = g
        self.h = h


SECURITY_LEVEL_0 = ConstSecurityParams(563, 281, 2, 4, 9)
SECURITY_LEVEL_1 = ConstSecurityParams(423432, 234234, 23432, 343, 43243)
#....

SECURITY_LEVEL_DEFAULT = SECURITY_LEVEL_0