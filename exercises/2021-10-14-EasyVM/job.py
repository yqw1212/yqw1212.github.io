flag = ""
result = [74, 25, 221, 15, 27, 137, 25, 84, 79, 78,
          85, 86, 142, 73, 14, 75, 6, 84, 26, 66,
          83, 31, 82, 219, 25, 217, 25, 85, 25, 0,
          75, 30]
dword = [0x7B, 0x2F, 0xE8, 0x37, 0x2F, 0xE8, 0x7B, 0x37, 0x7B, 0x7B,
         0x37, 0x37, 0xE8, 0x2F, 0x37, 0x7B, 0x37, 0x37, 0x2F, 0x7B,
         0x37, 0x7B, 0x37, 0xE8, 0x7B, 0xE8, 0x7B, 0x37, 0x2F, 0x37,
         0x7B, 0x2F]
for i in range(len(result)):
    flag += chr(result[i]^dword[i])

(a << 24 + b << 16 + c << 8 + d) >> 5 ^ (a << 24 + b << 16 + c << 8 + d)

print(flag)