from chvote.PrintingAuthority.GetVotingCards   import GetVotingCards

class PrintingAuthority(object):
    """
    The PrintingAuthority class represents the printing authority
    """

    bulletinBoard = None

    def __init__(self, bulletinBoardRef):
        self.bulletinBoard = bulletinBoardRef

    def getVotingCards(self, D_bold, secparams):
        """
        (Protocol 6.2) getVotingCards: Prints the voting sheets for all voters

        Args:
            V (list):   Voter description
            c (list):   List of candidate descriptions
            n (int):    Number of candidates
            k (int):    Number of selections
            E (list):   Eligibility Matrix
            D_bold (tuple):  Code Sheet Data

        Returns:
            list:       code sheet
        """

        (s, rawSheetData) = GetVotingCards(self.bulletinBoard.v_bold, self.bulletinBoard.w_bold, self.bulletinBoard.c_bold, self.bulletinBoard.n_bold, self.bulletinBoard.k_bold, self.bulletinBoard.E_bold, D_bold, secparams)

        return (s, rawSheetData)
