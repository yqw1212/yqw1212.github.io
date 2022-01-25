from z3 import *

table = "ABCDFEGH1JKLRSTMNP0VWQUXY2a8cdefijklmnopghwxyqrstuvzOIZ34567b9+/"

result = [0xBE, 0x36, 0xAC, 0x27, 0x99, 0x4F, 0xDE, 0x44, 0xEE, 0x5F, 
          0xDA, 0x0B, 0xB5, 0x17, 0xB8, 0x68, 0xC2, 0x4E, 0x9C, 0x4A, 
          0xE1, 0x43, 0xF0, 0x22, 0x8A, 0x3B, 0x88, 0x5B, 0xE5, 0x54, 
          0xFF, 0x68, 0xD5, 0x67, 0xD4, 0x06, 0xAD, 0x0B, 0xD8, 0x50, 
          0xF9, 0x58, 0xE0, 0x6F, 0xC5, 0x4A, 0xFD, 0x2F, 0x84, 0x36, 
          0x85, 0x52, 0xFB, 0x73, 0xD7, 0x0D, 0xE3]

# de = []
# tmp = 0
# for i in range(len(result)):
#     de.append(result[i]^238^tmp)
#     tmp = result[i]
# print(de)
# print(len(de))

de = [80, 102, 116, 101, 80, 56, 127, 116, 68, 95,
      107, 63, 80, 76, 65, 62, 68, 98, 60, 56,
      69, 76, 93, 60, 70, 95, 93, 61, 80, 95,
      69, 121, 83, 92, 93, 60, 69, 72, 61, 102,
      71, 79, 86, 97, 68, 97, 89, 60, 69, 92,
      93, 57, 71, 102, 74, 52]
print("".join(chr(i) for i in de))

for i in range(0, 56, 4):
    de[i] ^= 0xA
    de[i+1] ^= 0xB
    de[i+2] ^= 0xC
    de[i+3] ^= 0xD

print(de)
print("".join(chr(i) for i in de))
# ZmxhZ3syNTg2ZGM3Ni05OGQ1LTQ0ZTItYWQ1OC1kMDZlNjU1OWQ4MmF9
# flag{2586dc76-98d5-44e2-ad58-d06e6559d82a}


# flag_str = ""

# flag = [BitVec("v{}".format(i), 4) for i in range(0x2A)]

# j=0
# s=Solver()
# for i in range(0, 56, 4):

#     # s.add(result[i] == table[flag[j] >> 2] ^ 0xA)
#     # s.add(result[i+1] == table[(flag[j+1] >> 4) | (0x10 * (flag[j] & 3))] ^ 0xB)
#     # s.add(result[i+2] == table[(flag[j+2] >> 6) | (4 * (flag[j+1] & 0xF))] ^ 0xC)
#     # s.add(result[i+3] == table[flag[j+2] & 0x3F] ^ 0xD)

#     # s.add(result[i] ^ 0xA == table[flag[j] >> 2])
#     # s.add(result[i+1] ^ 0xB == table[(flag[j+1] >> 4) | (0x10 * (flag[j] & 3))])
#     # s.add(result[i+2] ^ 0xC == table[(flag[j+2] >> 6) | (4 * (flag[j+1] & 0xF))])
#     # s.add(result[i+3] ^ 0xD == table[flag[j+2] & 0x3F])
    
#     s.add(table.index(result[i] ^ 0xA) == flag[j] >> 2)
#     s.add(table.index(result[i+1] ^ 0xB) == (flag[j+1] >> 4) | (0x10 * (flag[j] & 3)))
#     s.add(table.index(result[i+2] ^ 0xC) == (flag[j+2] >> 6) | (4 * (flag[j+1] & 0xF)))
#     s.add(table.index(result[i+3] ^ 0xD) == flag[j+2] & 0x3F)

#     j += 3
    

# assert s.check() == sat
# model = s.model()
# print(model)
# flag_str += "".join([chr(model.eval(j).as_long()) for j in flag])

# print(flag_str)