import os
import pymongo
import json
from bson.json_util import dumps
import gmpy2
from gmpy2 import mpz
from pymongo.son_manipulator import SONManipulator
import pickle
from app.models.bulletinBoardState import BulletinBoardState


def encode_mpz(son):
    return {'_type': 'mpz', 'value': str(son)}


def encode_bytearray(son):
    return {'_type': 'bytearray', 'value': str(son)}


def decode_mpz(son):
    if son["_type"] == 'mpz':
        return mpz(son["value"])


def decode_bytearray(son):
    if son["_type"] == 'bytearray':
        return bytearray(son["value"])


class TransformMPZ(SONManipulator):
    def transform_incoming(self, son, collection):
        if isinstance(son, dict):
            for (key, value) in son.items():
                son[key] = self.transform_incoming(value, collection)
        elif isinstance(son, tuple):
            l = []
            for el in son:
                l.append(self.transform_incoming(el, collection))
            return {'_type': 'tuple', 'value': l}
        elif isinstance(son, list):
            son = [self.transform_incoming(el, collection) for el in son]
        elif son.__class__.__name__ == 'mpz':
            son = encode_mpz(son)
        elif isinstance(son, bytearray):
            son = encode_mpz(son)
        else:
            son = son

        print(son)
        return son

    def transform_outgoing(self, son, collection):
        if isinstance(son, dict):
            for (key, value) in son.items():
                if key == 'tuple':
                    son = tuple(value)
                elif key == 'mpz':
                    son = mpz(value)
                elif isinstance(son, bytearray):
                    son = decode_bytearray(son)
                else:
                    son[key] = self.transform_outgoing(value, collection)


        else:
            son = son
        return son


# use the following function to convert an arbitrary complex data structure into a binary JSON string
def saveComplex(obj):
    return pickle.dumps(obj)

# use the following function to recover the original data structure
def loadComplex(bson):
    return pickle.loads(bson)

class database(object):
    _db = None

    def __init__(self):
        #client = pymongo.MongoClient('mongodb://chvote:chv0t3_2017_$$$@cluster0-shard-00-00-wrqp9.mongodb.net:27017,cluster0-shard-00-01-wrqp9.mongodb.net:27017,cluster0-shard-00-02-wrqp9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        client = pymongo.MongoClient(os.environ['MONGODB_HOST'] if 'MONGODB_HOST' in os.environ else 'localhost',
            os.environ['MONGODB_PORT'] if 'MONGODB_PORT' in os.environ else 27017)
        self._db = client.chvote

    # Mongo DB collections (tables):

    @property
    def elections(self):
        return self._db.elections

    @property
    def bulletinBoardStates(self):
        return self._db.bulletinBoardStates

    @property
    def counter(self):
        return self._db.counter

    @property
    def test(self):
        return self._db.test

    def transformTest(self):
        a = (mpz(1), (mpz(2), mpz(3)))
        self.test.insert({'tuplempztest': a})

        loadedValue = self.test.find().sort([('timestamp', -1)]).limit(1)
        restored = loadedValue[0]["tuplempztest"]
        print(restored)

db = database()
db._db.add_son_manipulator(TransformMPZ())

if __name__ == '__main__':
    from chvote.Types import Custom
    from chvote.foo import foo

    a = Custom()
    foo(a)
