# from z3 import *

# condition = []

# s=Solver()


# c = [BitVec("v{}".format(i), 8) for i in range(36)]
# s.add()



# while s.check() == sat:
#     flag = "".join([chr(s.model().eval(j).as_long()) for j in c])
#     print(flag)
#     break
#     # print(s.model())

v4 = 0x67616C66
index = 0
while(1):
    v4 += 0x67616C66
    v4 = v4 & 0xFFFFFFFF
    index += 1
    print(hex(v4))
    if v4 == 0xD89114C8:
        break
print(index)