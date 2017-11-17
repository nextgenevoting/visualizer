import unittest
from gmpy2 import mpz
import uuid

def mpzconverter(o):
    if o.__class__.__name__ == 'mpz':
        return str(o)

    if isinstance(o, bytearray):
        return str(o)

    if isinstance(o, bytes):
        return str(o)

    if isinstance(o, uuid.UUID):
        return str(o)

    if hasattr(o, '__dict__'):
        return o.__dict__

class mpzconverterTest(unittest.TestCase):
    def testMpzConversion(self):
        import json

        testObj = mpz(5)
        testJson = json.dumps(testObj, default=mpzconverter)
        self.assertTrue(testJson == '"5"')

if __name__ == '__main__':
    unittest.main()
