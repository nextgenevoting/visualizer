from chvote.ElectionAuthority.GetPublicKey     import GetPublicKey
from chvote.VotingClient.GenBallot             import GenBallot
from chvote.VotingClient.GenConfirmation       import GenConfirmation
from chvote.VotingClient.GetPointMatrix        import GetPointMatrix
from chvote.VotingClient.GetReturnCodes        import GetReturnCodes
from chvote.VotingClient.GetVotingPage         import GetVotingPage
from chvote.VotingClient.GetFinalizationCode   import GetFinalizationCode
from chvote.VotingClient.CheckFinalizationCode import CheckFinalizationCode

class VotingClient(object):
    """
    The VotingClient class represents a voting client participating in the protocols (for example prot 6.5)
    """

    def __init__(self, v, voterData, rawSheetData, bulletinBoard):
        self.v = v
        self.bulletinBoard = bulletinBoard
        self.voterData = voterData
        self.rawSheetData = rawSheetData

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
            self.k_i_bold.append(E_bold[self.v][j] * k_bold[j]) # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

        # Get the voting page string
        P_i = GetVotingPage(self.v, c_bold,n_bold,self.k_i_bold)

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
            X = self.rawSheetData.votingCode
            print("Voter entered voting code: %s" % X)
        else:
            X = input('Enter your voting code: ')

        (self.alpha, self.r) = GenBallot(X, s, self.pk, secparams)

        return (self.alpha, self.r)

    def getPointsFromResponse(self, beta, secparams):
        self.P_s_bold = GetPointMatrix(beta, self.s, self.r, secparams)

        if not all(points != None for points in self.P_s_bold):
            raise RuntimeError('Failed to get points from OT response! Invalid selection?')

        return self.P_s_bold

    def getVerificationCodes(self, secparams):
        self.rc_s_bold = GetReturnCodes(self.s, self.P_s_bold, secparams)
        return self.rc_s_bold


    def confirm(self, autoInput, secparams):
        if autoInput:
            Y_v = self.rawSheetData.confirmationCode
            print("Voter entered confirmation code: %s" % Y_v)
        else:
            Y_v = input('Enter your confirmation code: ')

        self.gamma = GenConfirmation(Y_v,self.P_s_bold, secparams)
        return (self.v, self.gamma)

    def finalize(self, autoInput, secparams):
        delta_bold_i = self.bulletinBoard.delta_bold[self.v]
        FC = GetFinalizationCode(delta_bold_i, secparams)
        print("Displayed finalization code: %s" % FC)

        if autoInput:
            FC_i = self.rawSheetData.finalizationCode
            print("Voter entered finalization code: %s" % FC_i)
        else:
            FC_i = input('Enter your finalization code: ')

        if (CheckFinalizationCode(FC_i, FC, secparams)):
            return True
        else:
            return False
