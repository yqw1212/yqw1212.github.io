flagdata = [0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 
  0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 
  0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

flag = []
for i in range(0, len(flagdata), 4):
    flag.append(flagdata[i])

# print(len(flag)) # 40
print(flag)

flag = flag[:36]
print(flag)

resultdata = [0x08, 0x44, 0x00, 0x00, 0xD8, 0x68, 0x00, 0x00, 0xD8, 0x7A, 
  0x00, 0x00, 0x08, 0x43, 0x00, 0x00, 0xD8, 0x7B, 0x00, 0x00, 
  0x08, 0x46, 0x00, 0x00, 0x08, 0x7B, 0x00, 0x00, 0xD8, 0x70, 
  0x00, 0x00, 0x08, 0x33, 0x00, 0x00, 0x08, 0x73, 0x00, 0x00, 
  0xD8, 0x76, 0x00, 0x00, 0xD8, 0x5C, 0x00, 0x00, 0xD8, 0x76, 
  0x00, 0x00, 0x08, 0x66, 0x00, 0x00, 0x08, 0x69, 0x00, 0x00, 
  0x08, 0x6E, 0x00, 0x00, 0xD8, 0x4B, 0x00, 0x00, 0xD8, 0x76, 
  0x00, 0x00, 0xD8, 0x3F, 0x00, 0x00, 0x08, 0x6F, 0x00, 0x00, 
  0xD8, 0x5E, 0x00, 0x00, 0xD8, 0x76, 0x00, 0x00, 0x08, 0x74, 
  0x00, 0x00, 0xD8, 0x46, 0x00, 0x00, 0x08, 0x5F, 0x00, 0x00, 
  0x08, 0x63, 0x00, 0x00, 0x08, 0x34, 0x00, 0x00, 0x08, 0x74, 
  0x00, 0x00, 0xD8, 0x76, 0x00, 0x00, 0xD8, 0x44, 0x00, 0x00, 
  0xD8, 0x4C, 0x00, 0x00, 0x08, 0x7D, 0x00, 0x00]

result = []
for i in range(0, len(resultdata), 4):
    result.append(resultdata[i+1]*256 + resultdata[i+0])

    # print(hex(resultdata[i+1]*256 + resultdata[i+0]))

f = ""
for i in range(32):

    if flag[i]:
        # a = a ^ 0x28
        # a = a << 8
        # a = a - 0x28
        f += chr(((result[i]+0x28)>>8)^0x28)
    else:
        f += chr(result[i]>>8)

print(f)
# DASCTF{Y3s_u_find_how_to_c4t_me}