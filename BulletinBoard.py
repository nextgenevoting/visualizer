class BulletinBoard(object):

    voter = []
    t = None
    E = []  # eligibility matrix E = (e_ij) N x t
    c = []
    n = []
    k = []

    pk = None

    def __init__(self):
        pass

    def setupElectionEvent(self, v, n, k, t, c, E):
        """
        Election Event setup, done by the Election Administration before the election

        Args:
            v (list):           Voter Descriptions
            elections (list):   List of elections (replaces c,n,k)
            E ([[]]):           Elegibility matrix
        """
        self.v = v
        self.c = c
        self.n = n
        self.k = k
        self.t = t
        self.E = E

    def getCandidateSelectionParams(self):
        """
        Protocol 6.4: Returns the required parameters by the voting client

        Returns:
            tuple:  (c,n,k,E)
        """
        return (self.c, self.n, self.k, self.E)

    @property
    def n_sum(self):
        """
        Returns the total number of candidates among all elections

        Returns:
           int:  The total number of candidates
        """
        return sum(self.n)

    @property
    def N(self):
        """
        Returns the total number of eligible voters

        Returns:
           int:     the total number of eligible voters
        """
        return len(self.v)