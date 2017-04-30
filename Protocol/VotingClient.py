from ElectionAuthority.GetPublicKey import GetPublicKey
from VotingClient.GenBallot      import GenBallot
from VotingClient.GenConfirmation import GenConfirmation
from VotingClient.GetPointMatrix import GetPointMatrix
from VotingClient.GetReturnCodes import GetReturnCodes
from VotingClient.GetVotingPage  import GetVotingPage

class VotingClient(object):
    """
    The VotingClient class represents a voting client participating in the protocols (for example prot 6.5)
    """

    def __init__(self, i, voterData, votingSheet, bulletinBoard):
        self.i = i
        self.bulletinBoard = bulletinBoard
        self.voterData = voterData
        self.votingSheet = votingSheet

        self.k_i_bold = None  # Number of allowed selections per election of voter i
        self.s_bold = None  # Selection (candidate indices)
        self.pk = None
        self.alpha = None  # Ballot
        self.r = None  # Ballot randomizations
        self.P_s_bold = [None]
        self.rc_s_bold = [None]
        self.gamma = None


    def candidateSelection(self, autoInput, secparams):
        """
        Protocol 6.4: Candidate selection

        Returns:
            list:       Selection
        """

        c_bold, n_bold, k_bold, E_bold = self.bulletinBoard.getCandidateSelectionParams()

        # Calculate eligibility vector
        self.k_i_bold = []
        for j in range(len(k_bold)):
            self.k_i_bold.append(E_bold[self.i][j] * k_bold[j]) # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

        # Get the voting page string
        P_i = GetVotingPage(self.i, c_bold,n_bold,self.k_i_bold)

        print(P_i)
        if autoInput:
            s = self.voterData["selection"]
            print("Voter selected: %s" % s)
        else:
            s = input('Enter your selection : ')

        self.s = [int(s) for s in s.split(',')]

        return self.s

    def castVote(self, s, autoInput, secparams):

        self.pk = GetPublicKey(self.bulletinBoard.pk_bold,secparams)
        if autoInput:
            X = self.votingSheet.X
            print("Voter entered voting code: %s" % X)
        else:
            X = input('Enter your voting code: ')

        (self.alpha, self.r) = GenBallot(X, s, self.pk, secparams)

        return (self.alpha, self.r)

    def getPointsFromResponse(self, beta, secparams):
        self.P_s_bold = GetPointMatrix(beta, self.k_i_bold, self.s, self.r, secparams)

        if not all(points != None for points in self.P_s_bold):
            raise RuntimeError('Failed to get points from OT response! Invalid selection?')

        return self.P_s_bold

    def getReturnCodes(self, secparams):
        self.rc_s_bold = GetReturnCodes(self.s, self.P_s_bold, secparams)
        return self.rc_s_bold


    def confirm(self, autoInput, secparams):
        if autoInput:
            Y_i = self.votingSheet.Y
            print("Voter entered confirmation code: %s" % Y_i)
        else:
            Y_i = input('Enter your confirmation code: ')

        self.gamma = GenConfirmation(Y_i,self.P_s_bold, self.k_i_bold, secparams)
        return (self.i, self.gamma)

        return

