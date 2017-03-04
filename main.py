import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi
from ElectionEvent import electionEvent, Candidate, Election
import ElectionEvent
from Crypto.GenPoints import GenPoints
from SecurityContext import SECURITYCONTEXT_L3
from Crypto.GenSecretVoterData import GenSecretVoterData

def main():
    print("Number of simultaneous elections: %d with a total number of candidates: %d" % (electionEvent.t, electionEvent.n))
    for el in electionEvent.elections:
        print("Election %s, candidates:" % el)
        for c in el.candidates:
            print("\t%s" % c.name)


    # Generate points for all voters
    for v_i in range(0,len(electionEvent.voters)):
        eligibilityCount = 0
        for e_i in range(0, electionEvent.t):
            eligibilityCount += electionEvent.E[v_i][e_i]

        p, y = GenPoints(10, eligibilityCount, SECURITYCONTEXT_L3)
        
        # get secret voter data
        x,y_2,F, R = GenSecretVoterData(p, SECURITYCONTEXT_L3)
        print("Finalization code for Voter %d: % s" % (v_i,F))

if __name__ == '__main__':
    main()
