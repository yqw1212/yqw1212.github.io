import code
from ctypes import *
import struct

def read_file(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()

file = read_file("./assets/OoooooOooo")
dex_file = list(read_file("./classes2.dex"))

print("Shell version: ", c_uint16(struct.unpack_from("<H", file, 0)[0]).value)

DexCount = c_uint16(struct.unpack_from("<H", file, 2)[0]).value
print("Count dex: ", DexCount)

dex_code_index = 4

dex_insns_file = []
for i in range(DexCount):
    offset = c_uint32(struct.unpack_from("<I", file, dex_code_index+4*i)[0]).value
    methodCount = c_uint16(struct.unpack_from("<H", file, offset)[0]).value

    offset += 2
    method_code_item = []
    for j in range(methodCount):
        code_item = []
        code_item.append(c_uint32(struct.unpack_from("<I", file, offset)[0]).value)
        
        offset += 4
        code_item.append(c_uint32(struct.unpack_from("<I", file, offset)[0]).value)

        offset += 4
        code_item.append(c_uint32(struct.unpack_from("<I", file, offset)[0]).value) # 字节码长度

        offset += 4
        code_item.append(offset) # 在资源文件中的偏移

        offset += code_item[2]
        method_code_item.append(code_item)
        print(code_item)

    dex_insns_file.append(method_code_item)

for i in dex_insns_file[1]:
    dex_file[i[1] : i[1]+i[2]] = file[i[3] : i[3]+i[2]]

with open("./classes2_dec.dex", "wb") as f:
    f.write(bytes(dex_file))
