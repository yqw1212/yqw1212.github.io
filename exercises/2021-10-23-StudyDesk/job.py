a=[31, 41, 59, 26, 53, 58, 97, 93, 23, 84, 62, 64, 33, 83, 27, 95, 2, 88, 41, 97, 16, 93, 99, 37, 51, 5, 82, 9, 74, 94, 45, 92, 30, 78, 16, 40, 62, 86, 20, 89, 98, 62, 80, 34, 82, 53, 42, 11, 70, 67, 98, 21, 48, 8, 65, 13, 28, 23, 6, 64, 70, 93, 84, 46, 9, 55, 5, 82, 23, 17, 25, 35, 94, 8, 12, 84, 81, 11, 74, 50, 28, 41, 2, 70, 19, 38, 52, 11, 5, 55, 96, 44, 62, 29, 48, 95, 49, 30, 38, 19, 64, 42, 88, 10, 97, 56, 65, 93, 34, 46, 12, 84, 75, 64, 82, 33, 78, 67, 83, 16, 52, 71, 20, 19, 9, 14, 56, 48, 56, 69, 23, 46, 3, 48, 61, 4, 54, 32, 66, 48, 21, 33, 93, 60, 72, 60, 24, 91, 41, 27, 37, 24, 58, 70, 6, 60, 63, 15, 58, 81, 74, 88, 15, 20, 92, 9, 62, 82, 92, 54, 9, 17, 15, 36, 43, 67, 89, 25, 90, 36]
binstr=""
for i in a:
    binstr=binstr+"{:08b}".format(i)

print(binstr)
