from chvote.Common.SecurityParams import secparams_l1
from chvote.Protocol.Authority import Authority

class VoteSimulator(object):
    simulationBoard=None
    authorities = []
    secparams = secparams_l1

    def __init__(self):
        print("VoteSimulator init")
        self.authorities = [Authority(j, self.simulationBoard) for j in range(self.secparams.s)]


    def loadState(self, simulationBoard):
        self.simulationBoard = simulationBoard
        if self.simulationBoard.electionParams == None:
            raise RuntimeError("Uninitialized simulationBoard!")

