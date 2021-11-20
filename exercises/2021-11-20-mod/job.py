from z3 import *

table = "ABCDFEGH1JKLRSTMNP0VWQUXY2a8cdefijklmnopghwxyqrstuvzOIZ34567b9+/"

result = "2aYcdfL2fS1BTMMF1RSeMTTASS1OJ8RHTJdBYJ2STJfNMSMAYcKUJddp"

flag_str = ""
for i in range(0, len(result), 4):
    flag = [BitVec("v{}".format(i), 8) for i in range(3)]

    s=Solver()
    # s.add(table.index(result[i+0]) == (((4 * (flag[2] & 3)) | flag[1] & 0x30 | flag[0] & 0xC0) >> 2))
    # s.add(table.index(result[i+1]) == (((4 * (flag[0] & 3)) | flag[2] & 0x30 | flag[1] & 0xC0) >> 2))
    # s.add(table.index(result[i+2]) == (((4 * (flag[1] & 3)) | flag[0] & 0x30 | flag[2] & 0xC0) >> 2))
    # s.add(table.index(result[i+3]) == ((flag[2] & 0xC | (4 * flag[1]) & 0x30 | (0x10 * flag[0]) & 0xC0) >> 2))
    s.add((table.index(result[i+0]) << 2) == (((4 * (flag[2] & 3)) | flag[1] & 0x30 | flag[0] & 0xC0) ))
    s.add((table.index(result[i+1]) << 2) == (((4 * (flag[0] & 3)) | flag[2] & 0x30 | flag[1] & 0xC0) ))
    s.add((table.index(result[i+2]) << 2) == (((4 * (flag[1] & 3)) | flag[0] & 0x30 | flag[2] & 0xC0) ))
    s.add((table.index(result[i+3]) << 2) == ((flag[2] & 0xC | (4 * flag[1]) & 0x30 | (0x10 * flag[0]) & 0xC0) ))

    assert s.check() == sat
    model = s.model()
    print(model)
    flag_str += "".join([chr(model.eval(j).as_long()) for j in flag])

print(flag_str)