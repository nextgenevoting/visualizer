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
from Crypto.GenElectorateData import GenElectorateData, PartitionGenElectorateData
import multiprocessing as mp

def main():    
    # Set up a test election event
    voters = []
    for i in range (50000):
        voters.append(Voter("V"+str(i)))
    
    electionEvent = ElectionEvent([Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")]), Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])], voters)
    electionEvent.buildMatrix()

    print("Number of simultaneous elections: %d with a total number of candidates: %d" % (electionEvent.t, electionEvent.n))    
    print("Number of voters: %d" % electionEvent.N)
    for el in electionEvent.elections:
        print("Election %s, candidates:" % el)
        for c in el.candidates:
            print("\t%s" % c.name)

    print("Generate electorate data...")
    # Set up parallel GenElectorateData call
    output = mp.Queue()
    numOfProc = 1
    processes = [mp.Process(target=PartitionGenElectorateData, args=(x, numOfProc, output, electionEvent.n, 10, electionEvent.E,electionEvent,)) for x in range(numOfProc)]
    # Run processes
    for p in processes:
        p.start()
    # Get results
    results = [output.get() for p in processes]
    # todo: reassemble the results

    # Wait for the processs to complete
    for p in processes:
        p.join()
   

    # test without multiprocessing
    #d,d_2, P, K = GenElectorateData(electionEvent.n, 10, electionEvent.E, electionEvent, SECURITYCONTEXT_L3)

    print("done")


if __name__ == '__main__':
    main()