import gmpy2
from gmpy2 import mpz
from ElectionEvent import ElectionEvent
from Voter import Voter
from Candidate import Candidate
from Election import Election
from SecurityContext import SECURITYCONTEXT_L3
from Utils import AssertNummeric, isNummericType, ToByteArray
from RecHash import RecHash
from Crypto.GenElectorateData import GenElectorateData, PartitionGenElectorateData
import multiprocessing as mp
import time


def main():    
    # Set up a test election event
    voters = []
    for i in range (30000):
        voters.append(Voter("Voter"+str(i)))
    
    electionEvent = ElectionEvent([Election([Candidate("Donald Trump"), Candidate("Hillary Clinton"), Candidate("Vladimir Putin")]), Election([Candidate("Yes"), Candidate("No"), Candidate("Empty")])], voters)

    print("Number of simultaneous elections: %d, total candidates: %d" % (electionEvent.t, electionEvent.n))
    print("Number of voters: %d" % electionEvent.N)
    for el in electionEvent.elections:
        print("Election %s, candidates:" % el)
        for c in el.candidates:
            print("\t%s" % c.name)

    print("Generate electorate data...")
    start_time = time.time()

    # Set up parallel GenElectorateData call
    output = mp.Queue()
    numOfProc = 4
    processes = [mp.Process(target=PartitionGenElectorateData, args=(x, numOfProc, output, electionEvent.n, 10, electionEvent.E,electionEvent,)) for x in range(numOfProc)]
    # Run processes
    for p in processes:
        p.start()
    # Get results
    results = [output.get() for p in processes]    

    # Wait for the processs to complete
    for p in processes:
        p.join()

    reassembledResult = []
   # for pi in range(processes):
        # todo: reassemble the results
       # reassembledResult += results[pi]
   
    print("Elapsed time: %f s" % (time.time() - start_time))

    print("Generate electorate data...")

    # test without multiprocessing
    d,d_2, P, K = GenElectorateData(electionEvent.n, 10, electionEvent.E, electionEvent, SECURITYCONTEXT_L3)
    print("Elapsed time: %f s" % (time.time() - start_time))

if __name__ == '__main__':
    main()