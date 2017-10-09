class ElectionParams(object):
    id = ""
    voters = []
    countingCircles = []
    candidates = []
    numberOfCandidates = []
    numberOfSelections = []
    elegibilityMatrix = []

    def __init__(self, id, v, w, c, n, k, E):
        self.voters = v
        self.countingCircles = w
        self.candidates = c
        self.numberOfCandidates = n
        self.numberOfSelections = k
        self.elegibilityMatrix = E