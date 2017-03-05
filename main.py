import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi
from ElectionEvent import ElectionEvent
from Voter import Voter
from Candidate import Candidate
from Election import Election
from Crypto.GenPoints import GenPoints
from SecurityContext import SECURITYCONTEXT_L3
from Crypto.GenSecretVoterData import GenSecretVoterData
from Utils import AssertNummeric, isNummericType, ToByteArray
from RecHash import RecHash
from Crypto.GetPublicVoterData import GetPublicVoterData
from Crypto.GenElectorateData import GenElectorateData

def main():
    
    # 5 voter election Event 1 with 2 sim. elections, 6 candidates
    election1 = Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")])
    election2 = Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])
    
    electionEvent5 = ElectionEvent([election1, election2], [Voter("V1"), Voter("V2"), Voter("V3"), Voter("V4"), Voter("V5")])
    electionEvent5.buildMatrix()

    # 10k voter election event with 2 sim. elections, 6 candidates
    voters = []
    for i in range (0, 10000):
        voters.append(Voter("V"+str(i)))
    
    electionEvent10k = ElectionEvent([election1, election2], voters)
    electionEvent10k.buildMatrix()

    # which one to test?
    electionEvent = electionEvent10k

    # Generate electorate data for electionEvent
    print("Number of simultaneous elections: %d with a total number of candidates: %d" % (electionEvent.t, electionEvent.n))    
    print("Number of voters: %d" % electionEvent.N)

    for el in electionEvent.elections:
        print("Election %s, candidates:" % el)
        for c in el.candidates:
            print("\t%s" % c.name)


    d,d_2, P, K = GenElectorateData(electionEvent.N, 10, electionEvent.E, electionEvent, SECURITYCONTEXT_L3)
    print("done")


if __name__ == '__main__':
    main()