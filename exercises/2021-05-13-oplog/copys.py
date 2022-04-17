from z3 import *
from functools import reduce
def chinese_remainder(n, a):
    sum = 0
    prod = reduce(lambda a, b: a*b, n)
    for n_i, a_i in zip(n, a):
        p = prod // n_i
        sum += a_i * mul_inv(p, n_i) * p
    return sum % prod



def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1: return 1
    while a > 1:
        q = a // b
        a, b = b, a%b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0: x1 += b0
    return x1

#flag = BitVec('flag', 256)

s = Solver()
s.add(1 == 1)
SAT = s.check()
# s = Solver()
'''
r1 = flag % 0x88c218df8c5c25674af5808d963bfee9
r2 = flag % 0xfa8cca1bced017e0ab064d4844c3020b
r3 = flag % 0xe0ac283049469716cebd61a5b97b8bef
'''
r1 = BitVec('r1', 256)
r2 = BitVec('r2', 256)
r3 = BitVec('r3', 256)

x1 = 0xd062 * r1 + 0x37b9 * r2 + 0xcc13 * r3
x2 = 0xa4fb * r1 + 0xa0a5 * r2 + 0x2fca * r3
x3 = 0x8f9b * r1 + 0x9805 * r2 + 0xa6a0 * r3
s.add(x1 == 14678491206170330851881690558556870568208252)

key1 = BitVec('key1', 256)
#key2 = BitVec('key2', 256)
#key3 = BitVec('key3', 256)

'''
temp2 = x1 & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
temp4 = temp2 ^ (x1 & 0x555555555555555555555555555555555555) ^ key1
temp6 = temp4 ^ temp2 ^ key2;
x1 = temp6 ^ temp6 ^ temp4 ^ key3;

temp8 = x2 & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;
temp9 = temp8 ^ (x2 & 0x555555555555555555555555555555555555) ^ key1;
temp10 = temp9 ^ temp8 ^ key2;
x2 = temp10 ^ temp10 ^ temp9 ^ key3;

temp11 = x3 & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa;
temp12 = temp11 ^ (x3 & 0x555555555555555555555555555555555555) ^ key1;
temp13 = temp12 ^ temp11 ^ key2;
x3 = temp13 ^ temp13 ^ temp12 ^ key3;
'''

x1 = (x1 & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) ^ (x1 & 0x555555555555555555555555555555555555) ^ key1# ^ key3
x2 = (x2 & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) ^ (x2 & 0x555555555555555555555555555555555555) ^ key1# ^ key3
x3 = (x3 & 0x2aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa) ^ (x3 & 0x555555555555555555555555555555555555) ^ key1# ^ key3

s.add(x1 == 2357997788534811140333166336809177915724020)
s.add(x2 == 94024083436562980853861433269689272115769)
s.add(x3 == 7686765725723381031146546660250331403246417)

print(s.check())
print(s.model())

while s.check() == SAT:
    print(s.model())

    r11 = s.model()[r1].as_long()
    r22 = s.model()[r2].as_long()
    r33 = s.model()[r3].as_long()

    m = [0x88c218df8c5c25674af5808d963bfee9, 0xfa8cca1bced017e0ab064d4844c3020b, 0xe0ac283049469716cebd61a5b97b8bef]
    x = [r11, r22, r33]
    ff = chinese_remainder(m, x)
    LCM = 18079899862495296260944292753688576132233298796008754698177042981570096503703413266619648780022095131173540040113613
    ff %= LCM
    print(ff)
    hexy = hex(ff)[2:]
    if len(hexy) % 2 == 1:
        hexy = '0' + hexy
    if bytes.fromhex(hexy)[:4] == b'flag':
        print(bytes.fromhex(hexy))
        break
    assert(ff % m[0] == x[0] % m[0])
    assert(ff % m[1] == x[1] % m[1])
    assert(ff % m[2] == x[2] % m[2])

    s.add(And(r1 != s.model()[r1].as_long(), r2 != s.model()[r2].as_long(),r3 != s.model()[r3].as_long()))