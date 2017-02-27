import gmpy2
from gmpy2 import mpz
from math import ceil, floor, log2

def bit_abs(i):
    """
    This algorithm implements the ||i|| operator used in the specification document, defined on page 11

    @type   i:  number
    @param  i:  The number to get the absolute value of

    @rtype:     int
    @return:    absolute bit length of i
    """
              
    # return math.floor(math.log2(abs(i)))+1
    # Alternative without floating-point operations:
    return i.bit_length() 


def ToByteArray(x):
    """
    Converts the given expression into an array of bytes

    @type   x   number, ...
    @param  x:  The number to be converted into an array of bytes

    @rtype:     []
    @return:    Array of bytes
    """

    # n_min = ceil(bit_abs(x)/8)
    # Alternative without floating-point operations:
    q,r = divmod(bit_abs(x),8)
    q += bool(r)

    return ToByteArrayN(x, n_min)

def ToByteArrayN(x, n):
    """
    Converts the given expression into an array of bytes

    @type   x   number, ...
    @param  x:  The number to be converted into an array of bytes

    @type   n   
    @param  n:  

    @rtype:     []
    @return:    Array of bytes
    """
    B = []
    for i in range(0,int(n)):        
        b = x % 256
        x = x // 256                  # // = integer division => floor
        B.insert(0,b)
    return B
