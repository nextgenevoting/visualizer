from chvote.Utils.JsonParser import mpzconverter
import json
import jsonpickle
import gmpy2
from gmpy2 import mpz

class Custom(object):
    def __init__(self):
        self.__a = 5
        self.b = 3
        self.c = mpz(5)

if __name__ == '__main__':
    testobj = Custom()
    # d = testobj.__dict__
    # print(json.dumps(d))
    print(jsonpickle.encode(testobj))
