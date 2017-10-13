import json
from chvote.Utils.JsonParser import mpzconverter

class State(object):

    def __init__(self):
        self._modified = False

    @property
    def modified(self):
        return self._x

    @modified.setter
    def modified(self, value):
        print("setter of x called")
        self._x = value


    def toJSON(self):
        d = self.__dict__
        return json.dumps(d, default=mpzconverter)
