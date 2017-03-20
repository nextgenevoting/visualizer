from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Candidate                              import Candidate
from Crypto.SecurityParams                  import secparams_default, secparams_l0
from Election                               import Election
from VoteClient                             import VoteClient


def main():
    bulletinBoard = BulletinBoard()

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
    authorities = []
    for j in range(0, secparams_default.s):
        authorities.append(Authority("S%d" % j))

    # publish the data on the bulletin board
    bulletinBoard.setupElectionEvent(voters, elections, [[True for el in elections] for v in voters])
    print("Number of simultaneous elections: %d, of voters: %d, candidates: %d" %(bulletinBoard.t, bulletinBoard.N, bulletinBoard.n_total))


    # TODO: Run Protocol 6.1: Election Preparation
    D_hat = []
    print("Generate electorate data")
    for authority in authorities:
        D_hat.append(authority.PerformGenElectorateData(bulletinBoard.n, [1,1], bulletinBoard.E, secparams_l0))
    for authority in authorities:
        authority.PerformGetPublicCredentials(D_hat, secparams_l0)

    # TODO: Run Protocol 6.2: Printing of Code Sheets

    # TODO: Run Protocol 6.3: Key Generation
    pk_shares = []
    # Generate ElGamal key shares
    for authority in authorities:
        pk_shares.append(authority.PerformKeyGeneration(secparams_l0))
    # combine the resulting public key
    for authority in authorities:
        pk = authority.PerformGetPublicKey(pk_shares, secparams_l0)
    bulletinBoard.pk = pk

    # TODO: Run Protocol 6.4 & 6.5: Candidate Selection & Vote Casting
    votingClients = []
    for i in range(0, len(voters)):
        votingClient = VoteClient(i, bulletinBoard)
        votingClients.append(votingClient)
        # Get selection (6.4)
        s = votingClient.candidateSelection(secparams_l0)

        # Create ballot (6.5)
        (ballot,r) = votingClient.castVote(s, secparams_l0)
        proof = ballot.pi
        # Check ballot (6.5)
        for authority in authorities:
            valid = authority.PerformCheckBallot(i,ballot, secparams_l0)
            print("Ballot Proof validity checked by authority %s: %r" % (authority.name, valid))


if __name__ == '__main__':
    main()
