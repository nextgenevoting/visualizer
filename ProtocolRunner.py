from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Crypto.SecurityParams                  import secparams_l0, secparams_l1, secparams_l2, secparams_l3
from VoteClient                             import VoteClient
from PrintAuthority                         import PrintingAuthority
from VotingClient.CheckReturnCodes          import CheckReturnCodes
from ElectionAuthority.GetDecryptions       import GetDecryptions
from ElectionAdministrator.GetVotes         import GetVotes
from ElectionAuthority.CheckDecryptionProofs import CheckDecryptionProofs
import json

class ProtocolRunner(object):
    jsonData = None
    bulletinBoard = None
    secparams = None
    authorities = []
    printingAuth = None
    voters = []

    def __init__(self, file):
        self.bulletinBoard = BulletinBoard()

        # read the profile json file
        with open(file) as data_file:
            self.jsonData = json.load(data_file)

        if self.jsonData["securityLevel"] == 0:     self.secparams = secparams_l0
        elif self.jsonData["securityLevel"] == 1:   self.secparams = secparams_l1
        elif self.jsonData["securityLevel"] == 2:   self.secparams = secparams_l2
        elif self.jsonData["securityLevel"] == 3:   self.secparams = secparams_l3
        else:                                       self.secparams = secparams_l3

        self.secparams.deterministicRandomGen = self.jsonData["deterministicRandomGeneration"]

        # set up s authorites
        self.authorities = [Authority(j, self.bulletinBoard) for j in range(self.secparams.s)]

        # extract voter names from json data
        self.voters = [voter["name"] for voter in self.jsonData["voters"]]

        self.printingAuth = PrintingAuthority(self.bulletinBoard)

    def run(self, autoInput = False, verbose = False):

        # ********** PRE ELECTION PHASE **********
        # publish the data on the bulletin board
        self.bulletinBoard.setupElectionEvent(self.voters, self.jsonData["n"], self.jsonData["k"], self.jsonData["t"], self.jsonData["c"], self.jsonData["E"])
        if verbose: print("Number of simultaneous elections: %d, of voters: %d, candidates: %d" %(self.bulletinBoard.t, self.bulletinBoard.N_E, self.bulletinBoard.n_sum))

        # Protocol step 6.1: Election Preparation
        for authority in self.authorities:
            authority.GenElectionData(self.secparams)


        for authority in self.authorities:
            authority.GetPublicCredentials(self.secparams)
            if verbose: authority.printPoints()

        # Protocol step 6.2: Printing of Code Sheets
        D = [authority.d_j_bold for authority in self.authorities]
        # rawSheetData is required for automatic user input and checking of the voting, confirmation and return codes
        (sheets, rawSheetData) = self.printingAuth.getVotingCards(D, self.secparams)
        for sheet in sheets: print(sheet)

        # Protocol step 6.3: Key Generation
        for authority in self.authorities:
            authority.GenKeyPair(self.secparams)
        for authority in self.authorities:
            authority.getPublicKey(self.secparams)         # combine the resulting public key

        # ********** ELECTION PHASE **********
        # Protocol steps 6.4 & 6.5: Candidate Selection & Vote Casting
        votingClients = [VoteClient(i, self.jsonData["voters"][i], rawSheetData[i], self.bulletinBoard) for i in range(len(self.voters))]
        for votingClient in votingClients:

            # Get selection (6.4)
            s = votingClient.candidateSelection(autoInput, self.secparams)
            # Generate ballot & send oblivious transfer query (6.5)
            (ballot,r) = votingClient.castVote(s, autoInput, self.secparams)

            # Generate oblivious transfer response & check ballot (6.5)
            responses = [(authority.name, authority.runCheckBallot(votingClient.i,ballot, self.secparams)) for authority in self.authorities]
            for res in responses: print("Ballot validity checked by authority %s: %r" % (res[0], res[1]))

            beta = [authority.genResponse(votingClient.i,ballot.a_bold, ballot, self.secparams)[0] for authority in self.authorities]
            P_s = votingClient.getPointsFromResponse(beta, self.secparams)
            if verbose: print(P_s)
            returnCodes = votingClient.getReturnCodes(self.secparams)
            if verbose: print(returnCodes)
            print("CheckReturnCodes: %r" %CheckReturnCodes(votingClient.votingSheet.rc, returnCodes, s))

            # Confirmation (6.6)
            (i, gamma) = votingClient.confirm(autoInput, self.secparams)
            confirmationResults = [(authority.name, authority.checkConfirmation(i,gamma, self.secparams)) for authority in self.authorities]
            for res in confirmationResults: print("Confirmation-Code checked by authority %s: %r" % (res[0], res[1]))

        # ********** POST ELECTION PHASE **********
        # Mixing (6.7)
        for authority in self.authorities:
            authority.shuffle(self.secparams)

        # Decryption (6.8)
        shuffleResults = [(authority.name, authority.decrypt(self.secparams)) for authority in self.authorities]
        for res in shuffleResults: print("Shuffle Proof checked by authority %s: %r" % (res[0], res[1]))

        if not all(res[1] == True for res in shuffleResults):
            print("Shuffle proof / Decryption failed. Aborting")
            return

        if not CheckDecryptionProofs(self.bulletinBoard.pi_prime_bold, self.bulletinBoard.pk_bold, self.bulletinBoard.EN_bold[-1], self.bulletinBoard.B_prime_bold, self.secparams):
            print("Decryption proofs checks failed! Aborting.")
            return
        else: print("Decryption proofs are valid.")

        # Tallying (6.9) by the election administrator
        m_bold = GetDecryptions(self.bulletinBoard.EN_bold[-1], self.bulletinBoard.B_prime_bold, self.secparams)
        V_bold = GetVotes(m_bold, self.bulletinBoard.n_sum, self.secparams)
        print("Election result: ")
        print(V_bold)