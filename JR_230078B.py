from math import cos, pi, sqrt


def compress_y_block(rgb):
    block = [[0.299*r + 0.587*g + 0.114*b - 128
              for r, g, b in row] for row in rgb]
    q = [
        [16, 11, 10, 16, 24, 40, 51, 61],
        [12, 12, 14, 19, 26, 58, 60, 55],
        [14, 13, 16, 24, 40, 57, 69, 56],
        [14, 17, 22, 29, 51, 87, 80, 62],
        [18, 22, 37, 56, 68, 109, 103, 77],
        [24, 35, 55, 64, 81, 104, 113, 92],
        [49, 64, 78, 87, 103, 121, 120, 101],
        [72, 92, 95, 98, 112, 100, 103, 99]
    ]
    result = [[0]*8 for _ in range(8)]
    for u in range(8):
        for v in range(8):
            cu = 1/sqrt(2) if u == 0 else 1
            cv = 1/sqrt(2) if v == 0 else 1
            total = 0
            for x in range(8):
                for y in range(8):
                    total += (block[x][y]
                              * cos((2*x+1)*u*pi/16)
                              * cos((2*y+1)*v*pi/16))
            dct = cu*cv*total/4
            result[u][v] = round(dct/q[u][v])
    return result


rgb = [[(100, 150, 200)]*8 for _ in range(8)]
for row in compress_y_block(rgb):
    print(row)
