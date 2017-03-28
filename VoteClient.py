from VotingClient.GetVotingPage             import GetVotingPage
from BulletinBoard                          import BulletinBoard
from VotingClient.GenBallot                 import GenBallot
from VotingClient.GetPointMatrix            import GetPointMatrix

class VoteClient(object):
    """
    The VoteClient class represents a voting client participating in the protocols (for example prot 6.5)
    """

    voter = None
    i = None
    bulletinBoard = None                # Reference to the bulletinBoard object
    k_i = None
    s = None
    votingSheet = None
    r = None

    def __init__(self, i, voter, votingSheet, bulletinBoard):
        self.i = i
        self.bulletinBoard = bulletinBoard
        self.voterData = voter
        self.votingSheet = votingSheet

    def candidateSelection(self, autoInput, secparams):
        """
        Protocol 6.4: Candidate selection

        Returns:
            list:       Selection
        """

        c,n,k,E = self.bulletinBoard.getCandidateSelectionParams()

        # Calculate eligibility vector
        self.k_i = []
        for j in range(len(k)):
            self.k_i.append(E[self.i][j] * k[j]) # if voter i is eligible to cast a vote in election j, multiply 1 * the number of selections in j

        # Get the voting page string
        P_i = GetVotingPage(self.i, c,n,self.k_i)

        print(P_i)
        if autoInput:
            s = self.voterData["selection"]
            print("Voter selected: %s" % s)
        else:
            s = input('Enter your selection : ')

        self.s = [int(s) for s in s.split(',')]
        return self.s

    def castVote(self, s, autoInput, secparams):
        pk = self.bulletinBoard.pk

        if autoInput:
            X = self.votingSheet.X
            print("Voter entered voting code: %s" % X)
        else:
            X = input('Enter your voting code: ')

        (alpha, r) = GenBallot(X, s, pk, secparams)
        self.r = r
        return (alpha, r)


    def getPointsFromResponse(self, beta, secparams):
        P_s = GetPointMatrix(beta, self.k_i, self.s, self.r, secparams)
        print(P_s)
        #rc_s = GetReturnCodes(self.s, P_s)



