import json
from abc import ABC

from app.utils.JsonParser import mpzconverter


class State(ABC):
    def toJSON(self):
        d = self.__dict__
        return json.dumps(d, default=mpzconverter)
