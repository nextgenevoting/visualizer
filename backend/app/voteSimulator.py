from chvote.Common.SecurityParams import secparams_l1
from app.models.electionAuthorityState import ElectionAuthorityState
from app.parties.ElectionAuthority import ElectionAuthority


class VoteSimulator(object):
    authorities = []
    secparams = secparams_l1
    bulletinBoardState = None

    def __init__(self, bbState, electionAuthorityStates):
        print("VoteSimulator init")
        self.bulletinBoardState = bbState
        # create new (empty) electionAuthorityStates if none have been passed
        if electionAuthorityStates == []:
            for j in range(self.secparams.s):
                electionAuthorityStates.append(ElectionAuthorityState(j))
        self.authorities = [ElectionAuthority(electionAuthorityStates[j]) for j in range(self.secparams.s)]


    def genElectorateData(self):
        for authority in self.authorities:
            authority.GenElectionData(self.bulletinBoardState, self.secparams)

