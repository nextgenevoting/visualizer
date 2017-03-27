from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Crypto.SecurityParams                  import secparams_default, secparams_l0, secparams_l1, secparams_l2, secparams_l3
from VoteClient                             import VoteClient
from PrintAuthority                         import PrintingAuthority
import json


class ProtocolRunner(object):

    data = None
    bulletinBoard = None
    secparams = secparams_l0
    authorities = []

    def __init__(self, file):
        with open(file) as data_file:
            self.data = json.load(data_file)
        bulletinBoard = BulletinBoard()

    def run(self, autoInput = False):
        self.bulletinBoard = BulletinBoard()

        if self.data["securityLevel"] == 0:
            self.secparams = secparams_l0
        elif self.data["securityLevel"] == 1:
            self.secparams = secparams_l1
        elif self.data["securityLevel"] == 2:
            self.secparams = secparams_l2
        elif self.data["securityLevel"] == 3:
            self.secparams = secparams_l3
        else:
            self.secparams = secparams_default

        # set up s authorites
        self.authorities = [Authority("S%d" % j) for j in range (self.secparams.s)]

        voters = [voter["name"] for voter in self.data["voters"]]

        # publish the data on the bulletin board
        self.bulletinBoard.setupElectionEvent(voters, self.data["n"], self.data["k"], self.data["t"], self.data["c"], self.data["E"])
        print("Number of simultaneous elections: %d, of voters: %d, candidates: %d" %(self.bulletinBoard.t, self.bulletinBoard.N, self.bulletinBoard.n_sum))


        # TODO: Run Protocol 6.1: Election Preparation
        D_hat = []
        print("Generate electorate data")
        for authority in self.authorities:
            D_hat.append(authority.PerformGenElectorateData(self.bulletinBoard.n, [1,1], self.bulletinBoard.E, self.secparams))
        for authority in self.authorities:
            authority.PerformGetPublicCredentials(D_hat, self.secparams)

        # TODO: Run Protocol 6.2: Printing of Code Sheets
        printAuth = PrintingAuthority(self.bulletinBoard)
        D = [authority.d_j for authority in self.authorities]
        (sheets, rawSheetData) = printAuth.PerformGetSheets(D, self.secparams)
        print("Printing voting sheets:\n")
        for sheet in sheets: print(sheet)

        # TODO: Run Protocol 6.3: Key Generation
        pk_shares = []
        # Generate ElGamal key shares
        for authority in self.authorities:
            pk_shares.append(authority.PerformKeyGeneration(self.secparams))
        # combine the resulting public key
        for authority in self.authorities:
            pk = authority.PerformGetPublicKey(pk_shares, self.secparams)
            self.bulletinBoard.pk = pk

        # TODO: Run Protocol 6.4 & 6.5: Candidate Selection & Vote Casting
        votingClients = []
        for i in range(0, len(voters)):
            votingClient = VoteClient(i, self.data["voters"][i], rawSheetData[i], self.bulletinBoard)
            votingClients.append(votingClient)
            # Get selection (6.4)
            s = votingClient.candidateSelection(autoInput, self.secparams)

            # Create ballot (6.5)
            (ballot,r) = votingClient.castVote(s, autoInput, self.secparams)
            proof = ballot.pi
            # Check ballot (6.5)
            for authority in self.authorities:
                valid = authority.PerformCheckBallot(i,ballot, self.secparams)
                print("Ballot Proof validity checked by authority %s: %r" % (authority.name, valid))
