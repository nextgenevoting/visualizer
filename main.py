import gmpy2
import time
from gmpy2 import mpz

from Utils.ToByteArray                      import ToByteArray
from Utils.RecHash                          import RecHash
from Crypto.SecurityParams                  import secparams_default
from ElectionAuthority.GenElectorateData    import GenElectorateData
from Candidate                              import Candidate
from Election                               import Election
from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from VoteClient                             import VoteClient

def main():
    bulletinBoard = BulletinBoard()

    # Set up a test election event
    voters = [str("Voter%d" %i) for i in range(10)]

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
    bulletinBoard.setupElectionEvent(voters, elections, [[True for el in elections] for v in voters])

    print("Number of simultaneous elections: %d" %bulletinBoard.t)
    print("Number of voters: %d" % bulletinBoard.N)
    print("Number of candidates: %d" % bulletinBoard.n_total)

    # set up s authorites
    authorities = []
    for j in range(0, secparams_default.s):
        authorities.append(Authority("S%d" % j))


    # Run Protocol 6.1: Election Preparation
    D_hat = []
    print("Generate electorate data")
    for authority in authorities:
        D_hat.append(authority.PerformGenElectorateData(bulletinBoard.n, [1,1], bulletinBoard.E, secparams_default))
    for authority in authorities:
        authority.PerformGetPublicCredentials(D_hat, bulletinBoard.N,secparams_default)

    # TODO: Run Protocol 6.2

    # TODO: Run Protocol 6.3
    pk_shares = []
    # Generate ElGamal key shares
    for authority in authorities:
        pk_shares.append(authority.PerformKeyGeneration(secparams_default))
    # combine the resulting public key
    for authority in authorities:
        authority.PerformGetPublicKey(pk_shares, secparams_default)

    # TODO: Run Protocol 6.4: Candidate Selection
    vc = VoteClient(1, bulletinBoard)
    vc.candidateSelection()


if __name__ == '__main__':
    main()
