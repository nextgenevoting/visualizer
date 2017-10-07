import pymongo
import json
from bson.json_util import dumps
import gmpy2
from gmpy2 import mpz

class database(object):
    _db = None

    def __init__(self):
        client = pymongo.MongoClient('mongodb://chvote:chv0t3_2017_$$$@cluster0-shard-00-00-wrqp9.mongodb.net:27017,cluster0-shard-00-01-wrqp9.mongodb.net:27017,cluster0-shard-00-02-wrqp9.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')
        self._db = client.chvote

    @property
    def elections(self):
        return self._db.elections

    def insert(self):
        self._db.mpztest.insert({'test': str(mpz(123))})

db = database()


if __name__ == '__main__':
    db.insert()