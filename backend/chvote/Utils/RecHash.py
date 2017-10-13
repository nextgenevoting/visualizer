import unittest
import gmpy2
from gmpy2 import mpz

from chvote.Utils.ToByteArray     import ToByteArray
from chvote.Types                 import Point

def RecHash(v, secparams):
    """
    Algorithm 4.9: Computes the hash value h(v_1,...v_k) of multiple inputs v_1..v_k in a recursive manner.

    Args:
       v (list):                            Input values v_i \in  V_i, V_i unspecified, k >= 0
       secparams (SecurityParams):          Collection of public security parameters

    Returns:
       bytes:           An immutable array of bytes representing the recursive hash of the input values with a length corresponding to the used hash function
    """

    # Check if v is a list with a single element. If this is the case,
    # use the single element as the actual value and check again.

    while (isinstance(v, list) or isinstance(v, tuple)) and len(v) == 1:
        v = v[0]

    if isinstance(v, list) or isinstance(v, tuple):
        res = bytearray()

        for vi in v:
            # Performance optimization: iteration instead of recursion.
            # res += RecHash(vi, secparams) # concatenate hashes
            if isinstance(vi, bytearray) or vi.__class__.__name__ == 'bytes':
                res += secparams.hash(vi)
            elif isinstance(vi, int) or vi.__class__.__name__ == 'mpz':
                res += secparams.hash(ToByteArray(vi))
            elif isinstance(vi, str):
                res += secparams.hash(vi.encode('utf-8'))
            elif isinstance(vi, list) or isinstance(vi, tuple):
                res += RecHash(vi, secparams)
            else:
                raise ValueError('Unable to handle input of type %s' % type(vi))

        # hash the concatenation of the hashes
        return secparams.hash(res)
    elif isinstance(v, bytearray) or v.__class__.__name__ == 'bytes':
        return secparams.hash(v)
    elif isinstance(v, int) or v.__class__.__name__ == 'mpz':
        return secparams.hash(ToByteArray(v))
    elif isinstance(v, str):
        return secparams.hash(v.encode('utf-8'))
    else:
        raise ValueError('Unable to handle input of type %s' % type(v))

class RecHashTest(unittest.TestCase):
    def testOne(self):
        self.assertEqual(RecHash(123), RecHash(123))        # test for deterministic output
        self.assertEqual(RecHash(123), RecHash([123]))      # test if we avoid h(h(B1)) for a single input
        self.assertEqual(RecHash(123), RecHash([[123]]))
        self.assertEqual(RecHash(123), RecHash([[[123]]]))
        self.assertEqual(RecHash([[1,2,3,4]]), b'\xb9\xb64j\xe9\x03\xa4.\xbb\x05\xaa\xa8\x87\xb6\xcb33\xf8a\xde1\xf6wk\xb5\x040F<7/\x1d')
        self.assertTrue(len(RecHash(mpz(1234))) > 0)
        self.assertTrue(len(RecHash([mpz(1234), mpz(2304)])) > 0)
        self.assertEqual(RecHash(Point(1, 2)), RecHash([1, 2]))

if __name__ == '__main__':
    unittest.main()
