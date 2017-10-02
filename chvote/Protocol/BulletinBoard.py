class BulletinBoard(object):

    def __init__(self):
        self.t = None  # number of elections
        self.v_bold = []  # voters descriptions
        self.E_bold = []  # eligibility matrix E = (e_ij) N x t
        self.c_bold = []  # candidates
        self.n_bold = []  # number of candidates
        self.k_bold = []  # number of selections
        self.w_bold = []  # Counting circles
        self.EN_bold = [] # encryptions (E_bold in specification!)
        self.pi_bold = [] # Shuffle proofs
        self.B_prime_bold = [] # partial decryptions
        self.pi_prime_bold = [] # Decryption proofs
        self.delta_bold = []
        self.s = 0

        # Data generated during the election preparation (Protocol 6.1)
        self.D_hat_bold = []  # Electorate data
        self.pk_bold = []  # public key shares

    def setupElectionEvent(self, v_bold, n_bold, k_bold, w_bold, t, c_bold, E_bold, s):
        """
        Election Event setup, done by the Election Administration before the election

        Args:
            v_bold (list):           Voter Descriptions
            n_bold (list):           Number of candidates
            k_bold (list):           Number of selections
            w_bold (list):           Counting circles
            t (int):                 Number of elections
            c_bold (list):           Candidate descriptions
            E_bold (list):           Elegibility matrix
        """

        self.v_bold = v_bold
        self.c_bold = c_bold
        self.n_bold = n_bold
        self.k_bold = k_bold
        self.w_bold = w_bold
        self.t = t
        self.E_bold = E_bold
        self.s = s
        self.delta_bold = [[None] * self.s for i in range(len(self.E_bold))]

    def getCandidateSelectionParams(self):
        """
        Protocol 6.4: Returns the parameters required by the voting client

        Returns:
            tuple:  (c_bold, n_bold, k_bold, E_bold)
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
