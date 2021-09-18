from z3 import *

condition = []

# v1,v2,v3,v4,v5,v6,v7,v8=Ints('v1 v2 v3 v4 v5 v6 v7 v8')
# s=Solver()
# s.add(v1*v2==0x249E15C5)
# s.add(v2-v1==0xA644)
# s.add(v3*v4==0x34C7EAE2)
# s.add(v3-v4==0x216B)
# s.add(v5*v6==0x637973BA)
# s.add(v5-v6==0x819D)
# s.add(v7*v8==0xE5FD104)
# s.add(v7-v8==0x9393)
# print(s.check())
# print(s.model())


# for i in range(0, 0xffff):
#     for j in range(0, 0xffff):

#         if i*j==0x249E15C5 and i-j==0xA644:
#             print("v1:", j)
#             print("v2:", i)

#         if i*j==0x34C7EAE2 and i-j==0x216B:
#             print("v3:", i)
#             print("v4:", j)

#         if i*j==0x637973BA and i-j==0x819D:
#             print("v5:", i)
#             print("v6:", j)

#         if i*j==0xE5FD104 and i-j==0x9393:
#             print("v7:", i)
#             print("v8:", j)

flag = [11387, 53951, 34341, 25786, 60683, 27502, 43343, 5564]
result = ""
for i in flag:
    result += str(hex(i))[2:]
print(result.upper())