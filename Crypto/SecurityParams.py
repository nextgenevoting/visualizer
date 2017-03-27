import hashlib
import gmpy2
from gmpy2 import mpz
from math import ceil, log2

from Utils.Utils import BitAbs

class SecurityParams(object):
    """
    This class holds all public security parameters used by many algorithms
    For every security level, a separate object should exist holding the corresponding values.

    For the purpose of easier unit testing, the parameters for securityLevel0 can be injected as an optional parameter
    """

    # Public crypto parameters
    p = q = k = g = h = p_hat = q_hat = k_hat = g_hat = p_hat = L = L_M = delta = tau = deterministicRandomGen = 0

    s = 3                                                           # Number of authorities
    Nmax = 255                                                      # Max. Number of candidates
    epsilon = 0.9999                                                # deterrence factor --> The chance of an undetected attack is 1-deterrenceFactor

    # Return code
    A_R = [ chr(i) for i in range(ord('A'), ord('Z') + 1) ]         # Return code alphabet
    L_R = 3                                                         # Length of Returncodes in bytes
    l_R = ceil((8 * L_R + BitAbs(Nmax)) / log2(len(A_R)))           # Length of return codes in characters

    # Finalization code
    A_F = [ chr(i) for i in range(ord('A'), ord('Z') + 1) ]         # Final. code alphabet
    L_F = 3                                                         # Length of finalizationcode in bytes
    l_F = ceil(8 * L_R / log2(len(A_F)))                            # Length of finalization codes in characters

    # Voting code
    q_hat_X = q_hat                                                 # Upper bound of secret voting credential x
    A_X = [ chr(i) for i in range(ord('A'), ord('Z') + 1) ]         # Voting code alphabet

    # Confirmation code
    q_hat_Y = q_hat                                                 # Upper bound of secret confirmation credential y
    A_Y = [ chr(i) for i in range(ord('A'), ord('Z') + 1) ]         # Confirmation code alphabet

    def hash(self, input):
        hashFunc = hashlib.new('sha256')                            # must be initialized every time before using hashFunc.update()
        hashFunc.update(input)
        hashByteLength = int(self.L // 8)
        return hashFunc.digest()[0:hashByteLength]                  # truncate the hash output to the hash length of the security level

    def __init__(self, delta, tau, p, q, k, g, h, p_hat, q_hat, k_hat, g_hat, p_prime, L, detRandomGen):
        #super(SecurityParams, self).__setattr__("hashObj", hashlib.new('sha256'))

        self.delta = delta                                          # Security strength delta in bits
        self.tau = tau                                              # Security strength tau in bits
        self.p = mpz(p)                                             # Prime group order p
        self.q = mpz(q)                                             # Safeprime group order q
        self.k = mpz(k)                                             # k
        self.g = mpz(g)                                             # Generator g
        self.h = mpz(h)                                             # Generator h
        self.p_hat = mpz(p_hat)                                     # p^
        self.q_hat = mpz(q_hat)                                     # q^
        self.k_hat = mpz(k_hat)                                     # k^
        self.g_hat = mpz(g_hat)                                     # g^
        self.p_prime = mpz(p_prime)                                 # p'
        self.L = L                                                  # Hash Length in bits
        self.deterministicRandomGen = detRandomGen                  # True is deterministic random generation should be used (for testing purposes only!)

        # calculated values:
        self.q_hat_X = q_hat
        self.q_hat_Y = q_hat
        self.L_M = 2 * ceil(BitAbs(p_prime) // 8)                   # Length of OT messages (bytes)
        self.l_X = ceil(BitAbs(self.q_hat_X) / log2(len(self.A_X))) # Length of voting codes (characters)
        self.l_Y = ceil(BitAbs(self.q_hat_Y) / log2(len(self.A_Y))) # Length of confirmation codes in characters

# global objects

secparams_l0 = SecurityParams(
    4,
    4,
    563,
    281,
    2,
    4,
    9,
    787,
    131,
    6,
    64,
    131,
    8,
    True
)

secparams_l1 = SecurityParams(
    80,
    80,
    0x80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001981BF,
    0x40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000CC0DF,
    2,
    4,
    9,
    0x80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007FFFFFFFFFFFAEC41EFA48B2E00000000000012B01,
    0x800000000000000000000000000000000000012B,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDAA00000000000000000000000000000000000574E3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF340F3680000000000000000000000000000001DC6476B0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFBA72D52BE8A00000000000000100,
    0x3E4EC67D0801039E0DAA11CA82D1798C899914750ADAE377DB63181A5657EEFCC8F110113B0E644DAA50A9193EAA6863001CA3BF1B91D6131746AB1056C17AD54367FC740B85CE7629CCC529D916A9A00C391308133AF108920407D35C0B1BCF406E1B9374DA697C55650F89743A4AED7D857F6FEB68EA3E5F2404B4ABF33FC4,
    0x800000000000000000000000000000000000012B,
    160,
    False
)

secparams_l2 = SecurityParams(
    112,
    112,
    0x800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000AD3AF,
    0x400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000569D7,
    2,
    4,
    9,
    0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002B3000000000000000000000000000010AE7A58BB039DF1DD000003FC4F,
    0x800000000000000000000000000000000000000000000000000000BD,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE8600000000000000000000000000000000000000000000000000022E23FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFCC7DED8000000000000000000000000000000000000000000000004C0E0F50FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8FB33D626600000000000000000000000000000000000000000000A5D1575CB563FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0B28E5011C2A58000000000000000000000000000000000000000169859DDC5C697A10000000566,
    0x8FC32AED89182BD1CAC46EA9CDBECF57DB18D8748E039355CCBC90DEDA214943780680CCD7D379440E833E03681AD5C93C3CCB3909333D2DC500688237C4D0623703823F026FCD67103BA49EE2D3B3DDFAC5B797636FFC4369177FFA357B722935B2EF3B2E3F1DFEA736903F76927794D071A723F79666EE23FF0EDE87AFB3F60792CFFC7078CB96D8A23066C8C412813F5943CF9E98B8FE3E21A0A8F241A830BF39C16BB8F2F21D53EB91F30262A86A043C5DF1167CB748B6EACC5946D612EB8DFEB454E0B1289A7CF66F2940C83CD46118B37B949905AEAF315F537B5B54BF75138603D54BCC4C2D6E72C0E7DD50B5925417E5C277E411B9394FB2FDAC0DF,
    0x800000000000000000000000000000000000000000000000000000BD,
    224,
    False
)

secparams_l3 = SecurityParams(
    128,
    128,
    0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006119DF,
    0x400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000308CEF,
    2,
    4,
    9,
    0x800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001F6FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC6C982AE8AA368D05E56D53,
    0x800000000000000000000000000000000000000000000000000000000000005F,
    0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF420000000000000000000000000000000000000000000000000000000000008D03FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF975708000000000000000000000000000000000000000000000000000000004DAD680FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC6594CC42000000000000000000000000000000000000000000000000000002AC9B906703FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE03E48AD38B0800000000000000000000000000000000000000000000000001791C60F6FED00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEE81CF008AEE194200000000000000000000000000000000000000000000000CFBA85D98E3494103FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF65D390A88874FA1BF0BEE,
    0x28F1F91B358840EEF71964530F6899BB54DD42062AB9D9CECBC625862F16949A5100F0E8297AD084B7E5528CF486E6CE3C2D426F587D8FB57E6BFACEBF9BE2FC56ECD08AEF52DD04755CE826FFD04FAA680198F7D60BD27D98B6DAC03751D568FB655CAEE672F0D595A32BD2E0E4DD22B9505153A85436F3237658DE414C5C288B21520B760275A7BE1B246A8F6391368104FC8DB45E4305CF6FAA1AB380516E131C90626BA9E5692CE390D5AA2200966D79D7815894AD82DF1B11ECE364CF7819BBA4CF02CE3ED48A643082CA8E49418A293CD535BA0A4CE02B9D32760560197A6831C2045D89A62212818BD95612A13274344323EF8F725DCFF619F1F0B7B6CE168D530E94F96BBB5E0450A352DE5C168CE0E4053D5C2DA11C2C50B3EAA869B82ABBB8D2D272DCB1D2BBDCB77D672BC5DC62A6D9D63CFBC44271D65F1984B5284B42822A03CF5B7E04A409D82EF019A36D25C5E358DE2F1AB83098BC180A4D957DD30A5D5247D047B14728532172340D9D6444B165FB80BBD77231CD0408BB,
    0x800000000000000000000000000000000000000000000000000000000000005F,
    256,
    False
)

secparams_default = secparams_l3
