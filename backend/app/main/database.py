import pymongo
import json
from bson.json_util import dumps
import gmpy2
from gmpy2 import mpz
from pymongo.son_manipulator import SONManipulator
import pickle

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
        client = pymongo.MongoClient('localhost', 27017)
        self._db = client.chvote

    @property
    def elections(self):
        return self._db.elections

    @property
    def electorateData(self):
        return self._db.electorateData

    @property
    def counter(self):
        return self._db.counter


    @property
    def test(self):
        return self._db.test

    def insertSample(self):
        a = (mpz(1), mpz(2))
        valueToStore = saveComplex(a)

        self.electorateData.insert({'tupletest': valueToStore})

        loadedValue = self.electorateData.find().sort([('timestamp', -1)]).limit(1)
        restored = loadComplex(loadedValue[0]["tupletest"])
        print(restored)


db = database()
#db._db.add_son_manipulator(TransformMPZ())

if __name__ == '__main__':
    db.insertComplex()