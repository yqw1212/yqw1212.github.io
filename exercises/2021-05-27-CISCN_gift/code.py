enc = 0
v22 = [0x54, 0x5E, 0x52, 0x04, 0x55, 0x05, 0x53, 0x5F, 0x50, 0x07, 0x54, 0x56, 0x51, 0x02, 0x03, 0x00, 0x57]
timeLists = [
    1, 3, 6, 9, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x12, 0x14,
    0x19, 0x1E, 0x28, 0x42, 0x66, 0x0A0, 0x936, 0x3D21, 0x149A7, 0x243AC,
    0x0CB5BE, 0x47DC61, 0x16C0F46, 0x262C432, 0x4ACE299, 0x10FBC92A,
    0x329ECDFD, 0x370D7470
]

def main_goooo(array):
    box = [0] * 5
    for tmp in array:
        box[tmp] ^= 1
    return box[1] == 0 and box[3] == 0

def main_wtf(depth, j, array):
    global enc
    array[depth] = j
    if depth == len(array) - 1:
        if (main_goooo(array)):
            enc = enc - 17 * (((enc + (((enc + 1) * 0xF0F0F0F0F0F0F0F1) >> 64) + 1) >> 4) - ((enc + 1) >> 63)) + 1
            # enc = (enc+1) % 17
    else:
        for jj in [1, 2, 3, 4]:
            main_wtf(depth + 1, jj, array)

def main_main():
    global enc
    for aTime in timeLists:
        enc = 0
        for j in [1, 2, 3, 4]:
            main_wtf(0, j, [0] * aTime)
        print(chr(v22[enc] ^ 0x66))

main_main()