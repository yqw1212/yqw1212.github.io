from z3 import *

flag_enc = [BitVec("f%d" % i, 32) for i in range(4)]
s = Solver()

s.add(flag_enc[3]*0xCC8E + flag_enc[2]*0x71FB + flag_enc[1]*0xFB88 + flag_enc[0]*0x6DC0 == 0xBE18A1735995)
s.add(flag_enc[3]*0x9284 + flag_enc[2]*0xADD3 + flag_enc[1]*0x6AE5 + flag_enc[0]*0xF1BF == 0xA556E5540340)
s.add(flag_enc[3]*0xE712 + flag_enc[2]*0x652D + flag_enc[1]*0x8028 + flag_enc[0]*0xDD85 == 0xA6F374484DA3)
s.add(flag_enc[3]*0xF23A + flag_enc[2]*0x7C8E + flag_enc[1]*0xCA43 + flag_enc[0]*0x822C == 0xB99C485A7277)

if s.check() == sat:
    m = s.model()
    flag = [m[flag_enc[i]].as_long().to_bytes(4,'little').decode() for i in range(4)]
    print(''.join(flag))