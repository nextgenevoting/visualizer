import unittest
import os, sys
from gmpy2 import mpz
import gmpy2

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chvote.Utils.Utils                        import AssertList, AssertInt, AssertMpz, AssertClass
from chvote.Types                              import *
from chvote.Common.SecurityParams import secparams_l3, secparams_l0, SecurityParams
from chvote.ElectionAuthority.CheckShuffleProof import CheckShuffleProof

def CheckShuffleProofs(pi_bold, e_0_bold, E_bold, pk, i, secparams):
    """
    Algorithm 7.47: Checks if a chain of shuffle proofs generated by s different authorities is
    correct.

    Args:
       pi_bold (list of ShuffleProof):          Shuffle proof
       e_0_bold (list):                         ElGamal Encryptions
       E_bold (list):                           Shuffled ElGamal Encryptions
       pk (mpz):                                Encryption key pk
       i (int):                                 Authority index
       secparams (SecurityParams):              Collection of public security parameters

    Returns:
        bool
    """
    AssertList(pi_bold)
    AssertList(e_0_bold)
    AssertList(E_bold)
    AssertMpz(pk)
    AssertInt(i)
    AssertClass(secparams, SecurityParams)

    N = len(e_0_bold)
    e_bold_tmp = []
    e_bold_tmp.append(e_0_bold)
    e_bold_tmp.extend(E_bold)

    for j in range(secparams.s):
        if i != j:
            if not CheckShuffleProof(pi_bold[j], e_bold_tmp[j], e_bold_tmp[j+1],pk, secparams):
                return False
    return True


class CheckShuffleProofsTest(unittest.TestCase):
    def testCheckShuffleProofs(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
