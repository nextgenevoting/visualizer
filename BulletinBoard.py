class BulletinBoard(object):

    t = None         # number of elections
    v_bold = []      # voters descriptions
    E_bold = []      # eligibility matrix E = (e_ij) N x t
    c_bold = []      # candidates
    n_bold = []      # number of candidates
    k_bold = []      # number of selections

    # Data generated during the election preparation (Protocol 6.1)
    D_hat_bold = []  # Electorate data
    pk = None        # public key

    def __init__(self):
        pass

    def setupElectionEvent(self, v_bold, n_bold, k_bold, t, c_bold, E_bold):
        """
        Election Event setup, done by the Election Administration before the election

        Args:
            v_bold (list):           Voter Descriptions
            n_bold (list):           Number of candidates
            k_bold (list):           Number of selections
            t (int):                 Number of elections
            c_bold (list):           Candidate descriptions
            E_bold (list):           Elegibility matrix
        """

        self.v_bold = v_bold
        self.c_bold = c_bold
        self.n_bold = n_bold
        self.k_bold = k_bold
        self.t = t
        self.E_bold = E_bold

    def getCandidateSelectionParams(self):
        """
        Protocol 6.4: Returns the parameters required by the voting client

        Returns:
            tuple:  (c_bold,n_bold,k_bold,E_bold)
        """

        return self.c_bold, self.n_bold, self.k_bold, self.E_bold

    @property
    def n_sum(self):
        """
        Returns the total number of candidates among all elections

        Returns:
           int:  The total number of candidates
        """

        return sum(self.n_bold)

    @property
    def N_E(self):
        """
        Returns the total number of eligible voters

        Returns:
           int:     the total number of eligible voters
        """

        return len(self.v_bold)
