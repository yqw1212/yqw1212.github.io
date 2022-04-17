from z3 import *
import gmpy2
from Crypto.Util.number import long_to_bytes, inverse
from functools import reduce

def merge(a1,n1,a2,n2):
    d = math.gcd(n1,n2)
    c = a2-a1
    if c%d!=0:
        return 0
    c = (c%n2+n2)%n2
    c = c//d
    n1 = n1//d
    n2 = n2//d
    c *= gmpy2.invert(n1,n2)
    c %= n2
    c *= n1*d
    c += a1
    global n3
    global a3
    n3 = n1*n2*d
    a3 = (c%n3+n3)%n3
    return 1
def exCRT(a,n):
    a1=a[0]
    n1=n[0]
    le= len(a)
    for i in range(1,le):
        a2 = a[i]
        n2=n[i]
        if not merge(a1,n1,a2,n2):
            return -1
        a1 = a3
        n1 = n3
    global mod
    mod=n1
    return (a1%n1+n1)%n1

def egcd(a, b):
    if 0 == b:
        return 1, 0, a
    x, y, q = egcd(b, a % b)
    x, y = y, (x - a // b * y)
    return x, y, q
def chinese_remainder(pairs):
    mod_list, remainder_list = [p[0] for p in pairs], [p[1] for p in pairs]
    mod_product = reduce(lambda x, y: x * y, mod_list)
    mi_list = [mod_product//x for x in mod_list]
    mi_inverse = [egcd(mi_list[i], mod_list[i])[0] for i in range(len(mi_list))]
    x = 0
    for i in range(len(remainder_list)):
        x += mi_list[i] * mi_inverse[i] * remainder_list[i]
        x %= mod_product
    return x

s = z3.Solver()

r1 = BitVec('r1',256)
r2 = BitVec('r2',256)
r3 = BitVec('r3',256)

x1 = (r1 * 0xd062) + (r2 * 0x37b9) + (r3 * 0xcc13)
x2 = (r1 * 0xa4fb) + (r2 * 0xa0a5) + (r3 * 0x2fca)
x3 = (r1 * 0x8f9b) + (r2 * 0x9805) + (r3 * 0xa6a0)

n = 2357997788534811140333166336809177915724020 ^ (x1 & 0x2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) ^ (x1 & 0x555555555555555555555555555555555555)

s.add(x1 == 2357997788534811140333166336809177915724020)
s.add((x2 & 0x2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) ^ (x2 & 0x555555555555555555555555555555555555) ^ n == 94024083436562980853861433269689272115769)
s.add((x3 & 0x2AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA) ^ (x3 & 0x555555555555555555555555555555555555) ^ n == 7686765725723381031146546660250331403246417)

while s.check() == sat:
    c = []
    c.append(s.model()[r1].as_long())
    c.append(s.model()[r2].as_long())
    c.append(s.model()[r3].as_long())
    print(c)

    n = [0x88c218df8c5c25674af5808d963bfee9,0xfa8cca1bced017e0ab064d4844c3020b,0xe0ac283049469716cebd61a5b97b8bef]

    # p_3 = exCRT(c,n)
    # p = gmpy2.iroot(p_3,3)[0]

    # p = chinese_remainder([(n[0], c[0]), (n[1], c[1]), (n[2], c[2])])
    # p = long_to_bytes(p)
    # print(p)

    M = n[0] * n[1] * n[2]
    flag_long=0
    for i in range(3):
        Mi = M // n[i]
        flag_long += Mi * inverse(n[i],Mi) * c[i]
    flag_long %= M
    p = long_to_bytes(flag_long)
    print(p)

    if p[:4] == (b'flag'):
        break
    
    s.add(And(r1 != s.model()[r1].as_long(), r2 != s.model()[r2].as_long(),r3 != s.model()[r3].as_long()))
