import json
from chvote.Utils.JsonParser import mpzconverter
from abc import ABC, abstractmethod


class State(ABC):
    def toJSON(self):
        d = self.__dict__
        return json.dumps(d, default=mpzconverter)
