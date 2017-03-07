import gmpy2
from gmpy2 import mpz
import hashlib

class SecurityContext(object):
    """
    This class holds all public security parameters used by many algorithms
    For every security level, a separate object should exist holding the corresponding values.

    For the purpose of easier unit testing, the parameters for securityLevel0 can then be injected as an ptional parameter into the algorithms

    To compensate for the lack of a CONST keyword in python, the __setattr__ interceptor forbids changing any property of this class
    """
    hashObj = 0
    p = q = k = g = h = p_2 = q_2 = k_2 = g_2 = p_3 = L = 0

    def hash(self, input):
        hashObj = hashlib.new('sha256')
        hashObj.update(input)
        hashByteLength = int(self.L // 8)        
        return (hashObj.digest())[0:hashByteLength]             # truncate the hash output to the hash length of the security level

    def __init__(self, p, q, k, g, h, p_2, q_2, k_2, g_2, p_3, L):        
        print("Security Context constructor")
        #super(SecurityContext, self).__setattr__("hashObj", hashlib.new('sha256')) 

        super(SecurityContext, self).__setattr__("p", mpz(p))        # Prime group order p
        super(SecurityContext, self).__setattr__("q", mpz(q))        # Safeprime group order q
        super(SecurityContext, self).__setattr__("k", mpz(k))        # k
        super(SecurityContext, self).__setattr__("g", mpz(g))        # Generator g
        super(SecurityContext, self).__setattr__("h", mpz(h))        # Generator h
        super(SecurityContext, self).__setattr__("p_2", mpz(p_2))    # p^
        super(SecurityContext, self).__setattr__("q_2", mpz(q_2))    # q^
        super(SecurityContext, self).__setattr__("k_2", mpz(k_2))    # k^
        super(SecurityContext, self).__setattr__("g_2", mpz(g_2))    # g^
        super(SecurityContext, self).__setattr__("p_3", mpz(p_3))    # p'
        super(SecurityContext, self).__setattr__("L", L)        # Hash Length in bits

    def __setattr__(self, name, val):
        raise ValueError("Trying to change a constant value", self)


SECURITYCONTEXT_L0 = SecurityContext(563, 281, 2, 4, 9, 787, 131, 6, 64, 131, 8)
SECURITYCONTEXT_L1 = SecurityContext(0x80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001981BF,
                                     0x40000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000CC0DF, 
                                     2, 
                                     4, 
                                     9, 
                                     0x80000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000007FFFFFFFFFFFAEC41EFA48B2E00000000000012B01,
                                     0x800000000000000000000000000000000000012B,
                                     0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFDAA00000000000000000000000000000000000574E3FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF340F3680000000000000000000000000000001DC6476B0FFFFFFFFFFFFFFFFFFFFFFFFFFFFFBA72D52BE8A00000000000000100,
                                     0x3E4EC67D0801039E0DAA11CA82D1798C899914750ADAE377DB63181A5657EEFCC8F110113B0E644DAA50A9193EAA6863001CA3BF1B91D6131746AB1056C17AD54367FC740B85CE7629CCC529D916A9A00C391308133AF108920407D35C0B1BCF406E1B9374DA697C55650F89743A4AED7D857F6FEB68EA3E5F2404B4ABF33FC4,
                                     0x800000000000000000000000000000000000012B,
                                     160
                     )
SECURITYCONTEXT_L2 = SecurityContext(0x800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000AD3AF,
                                     0x400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000569D7, 
                                     2, 
                                     4, 
                                     9, 
                                     0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000002B3000000000000000000000000000010AE7A58BB039DF1DD000003FC4F,
                                     0x800000000000000000000000000000000000000000000000000000BD,
                                     0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE8600000000000000000000000000000000000000000000000000022E23FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFCC7DED8000000000000000000000000000000000000000000000004C0E0F50FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8FB33D626600000000000000000000000000000000000000000000A5D1575CB563FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF0B28E5011C2A58000000000000000000000000000000000000000169859DDC5C697A10000000566,
                                     0x8FC32AED89182BD1CAC46EA9CDBECF57DB18D8748E039355CCBC90DEDA214943780680CCD7D379440E833E03681AD5C93C3CCB3909333D2DC500688237C4D0623703823F026FCD67103BA49EE2D3B3DDFAC5B797636FFC4369177FFA357B722935B2EF3B2E3F1DFEA736903F76927794D071A723F79666EE23FF0EDE87AFB3F60792CFFC7078CB96D8A23066C8C412813F5943CF9E98B8FE3E21A0A8F241A830BF39C16BB8F2F21D53EB91F30262A86A043C5DF1167CB748B6EACC5946D612EB8DFEB454E0B1289A7CF66F2940C83CD46118B37B949905AEAF315F537B5B54BF75138603D54BCC4C2D6E72C0E7DD50B5925417E5C277E411B9394FB2FDAC0DF,
                                     0x800000000000000000000000000000000000000000000000000000BD,
                                     224
                     )
SECURITYCONTEXT_L3 = SecurityContext(0x8000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006119DF,
                                     0x400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000308CEF, 
                                     2, 
                                     4, 
                                     9, 
                                     0x800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001F6FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC6C982AE8AA368D05E56D53,
                                     0x800000000000000000000000000000000000000000000000000000000000005F,
                                     0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF420000000000000000000000000000000000000000000000000000000000008D03FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF975708000000000000000000000000000000000000000000000000000000004DAD680FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC6594CC42000000000000000000000000000000000000000000000000000002AC9B906703FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFE03E48AD38B0800000000000000000000000000000000000000000000000001791C60F6FED00FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEE81CF008AEE194200000000000000000000000000000000000000000000000CFBA85D98E3494103FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF65D390A88874FA1BF0BEE,
                                     0x28F1F91B358840EEF71964530F6899BB54DD42062AB9D9CECBC625862F16949A5100F0E8297AD084B7E5528CF486E6CE3C2D426F587D8FB57E6BFACEBF9BE2FC56ECD08AEF52DD04755CE826FFD04FAA680198F7D60BD27D98B6DAC03751D568FB655CAEE672F0D595A32BD2E0E4DD22B9505153A85436F3237658DE414C5C288B21520B760275A7BE1B246A8F6391368104FC8DB45E4305CF6FAA1AB380516E131C90626BA9E5692CE390D5AA2200966D79D7815894AD82DF1B11ECE364CF7819BBA4CF02CE3ED48A643082CA8E49418A293CD535BA0A4CE02B9D32760560197A6831C2045D89A62212818BD95612A13274344323EF8F725DCFF619F1F0B7B6CE168D530E94F96BBB5E0450A352DE5C168CE0E4053D5C2DA11C2C50B3EAA869B82ABBB8D2D272DCB1D2BBDCB77D672BC5DC62A6D9D63CFBC44271D65F1984B5284B42822A03CF5B7E04A409D82EF019A36D25C5E358DE2F1AB83098BC180A4D957DD30A5D5247D047B14728532172340D9D6444B165FB80BBD77231CD0408BB,
                                     0x800000000000000000000000000000000000000000000000000000000000005F,
                                     256
                     )
SECURITYCONTEXT_DEFAULT = SECURITYCONTEXT_L3                                    # Set this to  SECURITYCONTEXT_L3 for production!
