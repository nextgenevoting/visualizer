import gmpy2
from gmpy2 import mpz
from gmpy2 import jacobi
from ElectionContext import electionContext, Candidate, Election
import ElectionContext

def main():
    print("Number of simultaneous elections: %d with a total number of candidates: %d" % (electionContext.t(), electionContext.n()))
    for el in electionContext.elections:
        print("Election %s, candidates:" % el)
        for c in el.candidates:
            print("\t%s" % c.getName())

if __name__ == '__main__':
    main()
