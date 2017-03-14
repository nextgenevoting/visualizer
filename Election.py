class Election(object):
    """
    The Election class represents a single election of an election event
    """
    candidates = []
    k = None

    def __init__(self, candidates, k):
        self.candidates = candidates
        self.k = k

    @property
    def n(self):   # numberOfCandidates
        """
        n_j >= 2 denotes the number of candidates in the j-th election of an election event

        Returns:
           int:     The number of candidates (n_j) of the election (j)
        """
        return len(self.candidates)
