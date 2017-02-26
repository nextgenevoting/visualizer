import gmpy2
from gmpy2 import mpz
from math import ceil, floor, log2

def bit_abs(i):
    """
    The ||i|| operator in the specification
    Equals the absolute value in bits
    Defined on page 11

    @type   i:  int
    @param  i:  The int

    @rtype:     int
    @return:    absolute bit length of i
    """
    
    if(i.__class__.__name__ == 'mpz'):
        return gmpy2.floor(gmpy2.log2(abs(i)))+1        
    else:
        return floor(log2(abs(i)))+1

def ToByteArray(x):
    
    if(x.__class__.__name__ == 'mpz'):
        n_min = gmpy2.ceil(bit_abs(x)/8)
    else:
        n_min = ceil(bit_abs(x)/8)

    return ToByteArrayN(x, n_min)

def ToByteArrayN(x, n):
    B = []
    for i in range(0,int(n)):        
        b = x % 256
        if(x.__class__.__name__ == 'mpz'):
            x = mpz(gmpy2.floor(x/256))         # how to avoid mpz()? floor returns an mpfr :/
        else:
            x = floor(x/256)
        print(str(x))
        B.insert(0,b)
    return B
