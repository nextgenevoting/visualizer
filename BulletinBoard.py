class BulletinBoard(object):

    elections = []
    voter = []
    t = None
    E = []  # eligibility matrix E = (e_ij) N x t
    c = []
    n = []
    k = []
    def __init__(self):
        pass

    def setupElectionEvent(self, v, elections, E):
        """
        Election Event setup, done by the Election Administration before the election

        Args:
            v (list):           Voter Descriptions
            elections (list):   List of elections (replaces c,n,k)
            E ([[]]):           Elegibility matrix
        """
        self.v = v
        self.elections = elections
        self.t = len(elections)

        for el in elections:
            self.n.append(len(el.candidates))
            self.k.append(el.k)
            for candidate in el.candidates:
                self.c.append(candidate.name)

        self.E = E

    def getCandidateSelectionParams(self):
        """
        Protocol 6.4: Returns the required parameters by the voting client

        Returns:
            tuple:  (c,n,k,E)
        """
        return (self.c, self.n, self.k, self.E)


    @property
    def n_total(self):
        """
        Returns the total number of candidates among all elections

        Returns:
           int:  The total number of candidates
        """
        count = 0;
        for n_i in self.n:
            count += n_i
        return count

    @property
    def N(self):
        """
        Returns the total number of eligible voters

        Returns:
           int:     the total number of eligible voters
        """
        return len(self.v)