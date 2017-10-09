class ElectionParams(object):
    id = ""
    voters = []
    countingCircles = []
    candidates = []
    numberOfCandidates = []
    numberOfSelections = []
    elegibilityMatrix = []
    t = 0

    def __init__(self, id, v, w, c, n, k):
        self.voters = v
        self.countingCircles = w
        self.candidates = c
        self.numberOfCandidates = n
        self.numberOfSelections = k
        self.t = len(self.numberOfCandidates)
        self.elegibilityMatrix = [[True for el in range(self.t)] for i in range(len(self.voters))]
