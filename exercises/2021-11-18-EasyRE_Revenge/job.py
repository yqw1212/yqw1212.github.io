from z3 import *
from Crypto.Util.number import *

condition = []

v0 = BitVec('v0', 32)
v1 = BitVec('v1', 32)
v2 = BitVec('v2', 32)
v3 = BitVec('v3', 32)
v4 = BitVec('v4', 32)
v5 = BitVec('v5', 32)
v6 = BitVec('v6', 32)
v7 = BitVec('v7', 32)
s=Solver()

data = [v0, v1, v2, v3, v4, v5, v6, v7]

# 7 * i + 2
# 2,1,0,7,6,5,4,3

v4 = [0x271E150C, 0x3B322920, 0x5F564D44, 0x736A6158, 0x978E857C, 0xABA29990, 0xCFC6BDB4, 0xE3DAD1C8]

for i in range(8):
    data[i] ^= v4[(7*i+2)%8]

result = [0xEEE8B042, 0x57D0EE6C, 0xF3F54B32, 0xD3F0B7D6, 0x0A61C389, 0x38C7BA40, 0x0C3D9E2C, 0xD64A9284]

for j in range(8):
    data[j] ^= data[j] << 7
    data[j] ^= v4[(7 * j + 3) % 8]
    data[j] ^= data[(5 * j + 3) % 8]
    data[j] ^= data[j] << 0xD
    data[j] ^= v4[(7 * j + 5) % 8]
    data[j] ^= data[j] << 0x11

for i in range(8):
    s.add(data[i]==result[i])

print(s.check())
print(s.model())

flag = [1630954594, 828781622, 862085687, 909140836, 825516597, 1633759329, 879047012,943285560]
flag_str = ""
for f in flag:
    # flag_str += str(hex(f))[2:]
    flag_str += long_to_bytes(f).decode()[::-1]

print(flag_str)