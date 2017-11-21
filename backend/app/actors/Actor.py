from app.database import deserializeState, serializeState
from app.utils.JsonParser import mpzconverter
from app.states.state import State
import app.utils.jsonpatch as jsonpatch
import json
import copy

class Actor(object):

    def __init__(self, collection, electionID, additionalConditions=None, state=None):
        self.collection = collection # db table
        self.state = None
        self.originalState = State()
        self.electionID = electionID
        self.additionalConditions = additionalConditions    # dict

        if state != None:
            self.state = state
        else:
            self.loadState()

    def loadState(self):
        loadCondition = {'election':self.electionID}
        if self.additionalConditions != None:
            loadCondition.update(self.additionalConditions)

        loadState = self.collection.find_one(loadCondition)
        if loadState != None:
            self.state = deserializeState(loadState["state"])
            self.originalState = copy.deepcopy(self.state)
        else:
            raise RuntimeError("Failed to load state in {}".format(self.__class__.__name__))

    def getJSONPatch(self):
        return jsonpatch.make_patch(json.loads(self.originalState.toJSON()), json.loads(self.state.toJSON())).patch

    def persist(self):
        whereCondition = {"election": self.electionID}
        replaceCondition = {"election": self.electionID, "state": serializeState (self.state)}
        if self.additionalConditions != None:
            whereCondition.update(self.additionalConditions)
            replaceCondition.update(self.additionalConditions)
        try:
            self.collection.replace_one(whereCondition, replaceCondition)
        except Exception as e:
            raise RuntimeError("Failed to persist state: {}".format(repr(e)))

    def getState(self):
        return self.state
