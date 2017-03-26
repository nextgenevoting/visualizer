from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Candidate                              import Candidate
from Crypto.SecurityParams                  import secparams_default, secparams_l0, secparams_l3
from Election                               import Election
from VoteClient                             import VoteClient
from PrintAuthority                         import PrintingAuthority

from Utils.ToString import  ToString
from Utils.StringToInteger import StringToInteger
from gmpy2 import mpz

def main():
    A = ['0', '1']  # Alphabet
    k = 8
    x = mpz(5)
    s = ToString(x, k, A)
    i = StringToInteger(s,A)



    bulletinBoard = BulletinBoard()
    secparams = secparams_l0

    # Set up a test election event
    # 2 voters
    voters = [str("Voter%d" %i) for i in range(2)]

    # 2 simult. elections with 3 candidates each, 6 in total
    elections = [
        Election(
            [ Candidate("Donald Trump")
            , Candidate("Hillary Clinton")
            , Candidate("Vladimir Putin")
            ],1)
        , Election(
            [ Candidate("Yes")
            , Candidate("No")
            , Candidate("Empty")
            ],1)
        ]

    # set up s authorites
    authorities = [Authority("S%d" % j) for j in range (secparams.s)]

    # publish the data on the bulletin board
    bulletinBoard.setupElectionEvent(voters, elections, [[True for el in elections] for v in voters])
    print("Number of simultaneous elections: %d, of voters: %d, candidates: %d" %(bulletinBoard.t, bulletinBoard.N, bulletinBoard.n_total))


    # TODO: Run Protocol 6.1: Election Preparation
    D_hat = []
    print("Generate electorate data")
    for authority in authorities:
        D_hat.append(authority.PerformGenElectorateData(bulletinBoard.n, [1,1], bulletinBoard.E, secparams))
    for authority in authorities:
        authority.PerformGetPublicCredentials(D_hat, secparams)

    # TODO: Run Protocol 6.2: Printing of Code Sheets
    printAuth = PrintingAuthority(bulletinBoard)
    D = [authority.d_j for authority in authorities]
    sheets = printAuth.PerformGetSheets(D, secparams)
    print("Printing voting sheets:\n")
    for sheet in sheets: print(sheet)

    # TODO: Run Protocol 6.3: Key Generation
    pk_shares = []
    # Generate ElGamal key shares
    for authority in authorities:
        pk_shares.append(authority.PerformKeyGeneration(secparams))
    # combine the resulting public key
    for authority in authorities:
        pk = authority.PerformGetPublicKey(pk_shares, secparams)
    bulletinBoard.pk = pk

    # TODO: Run Protocol 6.4 & 6.5: Candidate Selection & Vote Casting
    votingClients = []
    for i in range(0, len(voters)):
        votingClient = VoteClient(i, bulletinBoard)
        votingClients.append(votingClient)
        # Get selection (6.4)
        s = votingClient.candidateSelection(secparams)

        # Create ballot (6.5)
        (ballot,r) = votingClient.castVote(s, secparams)
        proof = ballot.pi
        # Check ballot (6.5)
        for authority in authorities:
            valid = authority.PerformCheckBallot(i,ballot, secparams)
            print("Ballot Proof validity checked by authority %s: %r" % (authority.name, valid))


if __name__ == '__main__':
    main()
