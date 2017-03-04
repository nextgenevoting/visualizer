class Election(object):
    candidates = []

    def __init__(self, candidates = []):
        self.candidates = candidates

    def addCandidate(self, candidate):
        self.candidates.append(candidate)

    
    @property
    def n(self):   # numberOfCandidates
        """
        n_j >= 2 denotes the number of candidates in the j-th election of an election event
        """
        return len(self.candidates)
