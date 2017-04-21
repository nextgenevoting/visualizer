import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Utils.Utils                        import AssertList, AssertMpz, AssertClass
from Types                              import *
from Crypto.SecurityParams              import secparams_l3, secparams_l0, SecurityParams
from Crypto.GetGenerators               import GetGenerators
from Crypto.GetNIZKPChallenges          import GetNIZKPChallenges

def GenShuffleProof(e, e_prime, r_prime, psi, pk, secparams):
    """
    Algorithm 7.44: Generates a NIZKP of shuffle relative to ElGamal encryptions e and e1,
    which is equivalent to proving knowledge of a permutation psi and randomizations r_prime such
    that e_prime = Shuffle_pk(e,r_prime,psi). The algorithm implements Wikström’s proof of a shuffle
    [19, 18], except for the fact that the offline and online phases are merged. For the proof
    verification, see Alg. 7.48. For further background information we refer to Section 5.5.

    Args:
       e (list):                ElGamal Encryptions
       e_prime (list):          Shuffled ElGamal Encryptions e'
       r_prime (list):          Re-encryption randomizations r'
       psi (list):              Permutation
       pk (mpz):                Encryption key pk

    Returns:
        ShuffleProof
    """
    AssertList(e)
    AssertList(e_prime)
    AssertList(r_prime)
    AssertList(psi)
    AssertMpz(pk)
    AssertClass(secparams, SecurityParams)

    h = GetGenerators(len(e))
    (c,r) = GenPermutationCommitment(psi, h)
    u = GetNIZKPChallenges(len(e), (e,e_prime,c), secparams.q)

    return False

class GenShuffleProofTest(unittest.TestCase):
    def testGenShuffleProof(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
