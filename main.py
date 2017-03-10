import gmpy2
from gmpy2 import mpz
from ElectionEvent import ElectionEvent
from Voter import Voter
from Candidate import Candidate
from Election import Election
from SecurityParams import secparams_l3
from Utils import AssertNummeric, isNummericType, ToByteArray
from RecHash import RecHash
from Crypto.GenElectorateData import GenElectorateData, GenElectorateData
import time
from Authority import Authority


def main():    
    # Set up a test election event
    voters = []
    for i in range (100):
        voters.append(Voter("Voter"+str(i)))
    
    electionEvent = ElectionEvent([Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")]), Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])], voters)

    print("Number of simultaneous elections: %d" %electionEvent.t)
    print("Number of voters: %d" % electionEvent.N)
    for el in electionEvent.elections:
        print("Election %s, candidates:" % el)
        for c in el.candidates:
            print("\t%s" % c.name)

    
    # set up s authority instances
    authorities = []
    for j in range(0,secparams_l3.s):
        authorities.append(Authority("S" + str(j)))

   
    # Simulate generation of electorate data
    D_hat = []
    print("Generate electorate data")
    for authority in authorities:
        d_hat_j = authority.PerformGenElectorateData(electionEvent.n, [1,1], electionEvent.E, electionEvent.N, electionEvent.t, secparams_l3)
        D_hat.append(d_hat_j)    
    print("done")

    for authority in authorities:
        authority.PerformGetPublicCredentials(D_hat, electionEvent.N)

if __name__ == '__main__':
    main()