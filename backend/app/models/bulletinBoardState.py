from app.models.state import State
from chvote.Utils.JsonParser import mpzconverter
import json

class BulletinBoardState(State):

    def __init__(self, id, v_bold, w_bold, c_bold, n_bold, k_bold):
        self.voters = v_bold
        self.countingCircles = w_bold
        self.candidates = c_bold
        self.numberOfCandidates = n_bold
        self.numberOfSelections = k_bold
        self.t = len(self.numberOfCandidates)
        self.elegibilityMatrix = [[True for el in range(self.t)] for i in range(len(self.voters))]

        self.publicCredentials = []
