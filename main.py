from Authority                              import Authority
from BulletinBoard                          import BulletinBoard
from Crypto.SecurityParams                  import secparams_default, secparams_l0, secparams_l3
from VoteClient                             import VoteClient
from PrintAuthority                         import PrintingAuthority

from Utils.ToString import  ToString
from Utils.StringToInteger import StringToInteger
from gmpy2 import mpz
from ProtocolRunner import ProtocolRunner

def main():

    level0test = ProtocolRunner("tests\\deterministic_level0.json")
    level0test.run(False)



if __name__ == '__main__':
    main()
