import gmpy2
from gmpy2 import mpz

class SecurityContext(object):
    """
    This class holds all public security parameters used by many algorithms
    For every security level, a separate object should exist holding the corresponding values.

    For the purpose of easier unit testing, the parameters for securityLevel0 can then be injected as an ptional parameter into the algorithms

    To compensate for the lack of a CONST keyword in python, the __setattr__ interceptor forbids changing any property of this class
    """

    p = q = k = g = h = 0
    def hash(input):
        # tbd
        return hash(input)

    def __init__(self, p, q, k, g, h):
        super(SecurityContext, self).__setattr__("p", p)
        super(SecurityContext, self).__setattr__("q", q)
        super(SecurityContext, self).__setattr__("k", k)
        super(SecurityContext, self).__setattr__("g", g)
        super(SecurityContext, self).__setattr__("h", h)

    def __setattr__(self, name, val):
        raise ValueError("Trying to change a constant value", self)


SECURITYCONTEXT_L0 = SecurityContext(563, 281, 2, 4, 9)
SECURITYCONTEXT_L1 = SecurityContext(423432, 234234, 23432, 343, 43243)
#....
SECURITYCONTEXT_DEFAULT = SECURITYCONTEXT_L0