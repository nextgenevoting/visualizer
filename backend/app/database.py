import os
import pymongo
import json
from bson.json_util import dumps
import gmpy2
from gmpy2 import mpz
from pymongo.son_manipulator import SONManipulator
import pickle
from app.states.bulletinBoardState import BulletinBoardState
import unittest

# use the following function to convert an arbitrary complex data structure into a binary string
def serializeState(obj):
    return pickle.dumps(obj)

# use the following function to recover the original data structure
def deserializeState(bson):
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
    def electionAuthorityStates(self):
        return self._db.electionAuthorityStates

    @property
    def printingAuthorityStates(self):
        return self._db.printingAuthorityStates

    @property
    def voterStates(self):
        return self._db.voterStates

    @property
    def electionAdministratorStates(self):
        return self._db.electionAdministratorStates

    @property
    def testSchema(self):
        return self._db.testSchema

db = database()

class Testobj():
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = mpz(c)

class databaseTest(unittest.TestCase):
    def testSerialization(self):
        testObj = Testobj(1,2,5)
        id = db.testSchema.insert({'test': 'test','state' : serializeState(testObj)})
        recoveredRecord = db.testSchema.find_one({"_id": id})
        recoveredState = deserializeState(recoveredRecord["state"])

        self.assertTrue(recoveredState.a==1)
        self.assertTrue(recoveredState.b == 2)
        self.assertTrue(recoveredState.c == mpz(5))

if __name__ == '__main__':
    unittest.main()
