
import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi
import os, sys
from random import randint
import hashlib

seed = int.from_bytes(os.urandom(0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006119DF.bit_length()), byteorder='big')
rstate = gmpy2.random_state(seed)

def randomMpz(n):
    r = gmpy2.mpz_random(rstate,
                         n)  # mpz_random(random_state, n) returns a uniformly distributed random integer between 0 and n-1
    if r == 0:
        r == 1
    return r

def randomInt(n):
    randint(1, n)


def randomQuadResMpz(Z_q, g, p):
    x = randomMpz(Z_q)
    return gmpy2.powmod(g, x, p)

def GetPrimes(n, Z_p):

    assert n >= 2, "n must be greater or equal 2"

    x = mpz(1)
    primes = []

    for i in range(n):                                # i = 0, ... , n-1
        while True:
            x += 1 if x <= 2 else mpz(2)

            if x >= Z_p:
                return []                                # n is incompatible with p
            if gmpy2.is_prime(x) and IsMember(x, Z_p):   # see Alg. 7.2
                break

        primes.append(x)

    return primes                                        # p \elementof G_p \cap P)^n

def GetSelectedPrimes(s_bold, Z_p):
    s_k = max(s_bold)+1
    p_bold = GetPrimes(s_k, Z_p)
    q_bold = [ p_bold[s_i] for s_i in s_bold ]
    return q_bold


def IsMember(x, Z_p):
    if 1 <= x and x < Z_p:
        return jacobi(x, Z_p) == 1

    return False

def Truncate(B, l):

    return B[0:l]

def Skip(B, l):
    return B[l:len(B)]

def ToByteArray(x):

    # this seems faster than the original code:
    x = int(x)  # convert mpz to int because mpz has no .to_bytes method
    return x.to_bytes((x.bit_length() + 7) // 8, byteorder='big')

    # Alternative without floating-point operations:
    #q, r = divmod(BitAbs(x), 8)
    #q += bool(r)

    #return ToByteArrayN(x, q)

def ToByteArrayN(x, n):
    n = int(n)

    x = int(x)      # convert mpz to int because mpz has no .to_bytes method
    return x.to_bytes(n, byteorder='big')

    #B = bytearray(n)

    #for i in range(n):
    #    b = x % 256
    #    x = x // 256                  # // = integer division => floor
    #    B.insert(0, b)

    #return bytes(B)

def hash(input, L):
    hashFunc = hashlib.new('sha256')                            # must be initialized every time before using hashFunc.update()
    hashFunc.update(input)
    hashByteLength = int(L)
    return hashFunc.digest()[0:hashByteLength]                  # truncate the hash output to the hash length of the security level

def RecHash(v, L):

    while (isinstance(v, list) or isinstance(v, tuple)) and len(v) == 1:
        v = v[0]

    if isinstance(v, list) or isinstance(v, tuple):
        res = bytearray()

        for vi in v:
            # Performance optimization: iteration instead of recursion.
            # res += RecHash(vi, secparams) # concatenate hashes
            if isinstance(vi, bytearray) or vi.__class__.__name__ == 'bytes':
                res += hash(vi, L)
            elif isinstance(vi, int) or vi.__class__.__name__ == 'mpz':
                res += hash(ToByteArray(vi), L)
            elif isinstance(vi, str):
                res += hash(vi.encode('utf-8'), L)
            elif isinstance(vi, list) or isinstance(vi, tuple):
                res += RecHash(vi)
            else:
                raise ValueError('Unable to handle input of type %s' % type(vi))

        # hash the concatenation of the hashes
        return hash(res, L)
    elif isinstance(v, bytearray) or v.__class__.__name__ == 'bytes':
        return hash(v, L)
    elif isinstance(v, int) or v.__class__.__name__ == 'mpz':
        return hash(ToByteArray(v), L)
    elif isinstance(v, str):
        return hash(v.encode('utf-8'), L)
    else:
        raise ValueError('Unable to handle input of type %s' % type(v))


def XorByteArray(BS):
    assert len(BS) >= 2, "BS must contain at least 2 bytearrays"

    byteArraySize = len(BS[0])
    res = bytearray(BS[0])

    for i in range(1, len(BS)):
        assert len(BS[i]) == byteArraySize, "All bytearrays must be of the same length!"

        for j in range(len(BS[i])):
            res[j] ^= BS[i][j]

    return res