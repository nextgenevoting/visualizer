import gmpy2
from gmpy2 import mpz
from ElectionEvent import ElectionEvent
from Voter import Voter
from Candidate import Candidate
from Election import Election
from SecurityContext import SECURITYCONTEXT_L3
from Utils import AssertNummeric, isNummericType, ToByteArray
from RecHash import RecHash
from Crypto.GenElectorateData import GenElectorateData, GenElectorateData
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

    print("Generate electorate data with %d processes" %mp.cpu_count())
    start_time = time.time()

    # Set up parallel GenElectorateData call
    output = mp.Queue()
    processes = [mp.Process(target=GenElectorateData, args=(True, x, output, electionEvent.n, 10, electionEvent.E,electionEvent,)) for x in range(mp.cpu_count())]
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

    # test without multiprocessing
    print("Generate electorate data (single process)")
    start_time = time.time()    
    d,d_2, P, K = GenElectorateData(False, None, None, electionEvent.n, 10, electionEvent.E, electionEvent, SECURITYCONTEXT_L3)
    print("Elapsed time: %f s" % (time.time() - start_time))

if __name__ == '__main__':
    main()