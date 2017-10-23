from app.database import loadComplex, saveComplex

class Party(object):

    def __init__(self, collection, electionID, additionalConditions = None):
        self.collection = collection # db table
        self.state = None
        self.electionID = electionID
        self.additionalConditions = additionalConditions    # dict

        self.loadState()

    def loadState(self):
        loadCondition = {'election':self.electionID}
        if self.additionalConditions != None:
            loadCondition.update(self.additionalConditions)

        loadState = self.collection.find_one(loadCondition)
        if loadState != None:
            self.state = loadComplex(loadState["state"])
        else:
            raise RuntimeError("Failed to load state in {}".format(self.__class__.__name__))

    def persist(self):
        saveCondition = {"election": self.electionID}
        replaceCondition = {"election": self.electionID, "state": saveComplex (self.state)}
        if self.additionalConditions != None:
            saveCondition.update(self.additionalConditions)
            replaceCondition.update(self.additionalConditions)
        try:
            self.collection.replace_one(saveCondition, replaceCondition)
        except Exception as e:
            raise RuntimeError("Failed to persist state: {}".format(repr(e)))

    def getState(self):
        return self.state
