import gmpy2
from gmpy2 import mpz
import hashlib

class SecurityContext(object):
    """
    This class holds all public security parameters used by many algorithms
    For every security level, a separate object should exist holding the corresponding values.

    For the purpose of easier unit testing, the parameters for securityLevel0 can then be injected as an ptional parameter into the algorithms

    To compensate for the lack of a CONST keyword in python, the __setattr__ interceptor forbids changing any property of this class
    """

    p = q = k = g = h = 0

    def hash(self, input):
        # does the hash function depend on the security level or do we always use sha256?
        h = hashlib.new('sha256')
        h.update(input)
        return h.digest()

    def __init__(self, p, q, k, g, h):
        super(SecurityContext, self).__setattr__("p", p)
        super(SecurityContext, self).__setattr__("q", q)
        super(SecurityContext, self).__setattr__("k", k)
        super(SecurityContext, self).__setattr__("g", g)
        super(SecurityContext, self).__setattr__("h", h)
        #self.p = p
        #self.q = q
        #self.k = k
        #self.g = g
        #self.h = h

    def __setattr__(self, name, val):
        raise ValueError("Trying to change a constant value", self)


SECURITYCONTEXT_L0 = SecurityContext(563, 281, 2, 4, 9)                         # always use test parameters from the specification
SECURITYCONTEXT_L1 = SecurityContext(423432, 234234, 23432, 343, 43243)
#....
SECURITYCONTEXT_DEFAULT = SECURITYCONTEXT_L0                                    # Set this to  SECURITYCONTEXT_L3 for production!
