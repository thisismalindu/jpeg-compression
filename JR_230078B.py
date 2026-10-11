
from math import cos, pi, sqrt, floor

def compress_y_block(rgb, quality=50):
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

    # Match the website's quality scaling
    quality = max(1, min(100, round(quality)))
    scale = 5000 // quality if quality < 50 else 200 - 2*quality

    flat_q = [
        max(1, min(255, (value * scale + 50) // 100))
        for row in q for value in row
    ]

    # Match the website's quantization table arrangement
    zigzag = [
        0, 1, 8, 16, 9, 2, 3, 10,
        17, 24, 32, 25, 18, 11, 4, 5,
        12, 19, 26, 33, 40, 48, 41, 34,
        27, 20, 13, 6, 7, 14, 21, 28,
        35, 42, 49, 56, 57, 50, 43, 36,
        29, 22, 15, 23, 30, 37, 44, 51,
        58, 59, 52, 45, 38, 31, 39, 46,
        53, 60, 61, 54, 47, 55, 62, 63
    ]

    q_site = [0] * 64
    for i, position in enumerate(zigzag):
        q_site[position] = flat_q[i]

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

            # Match JavaScript Math.round()
            result[u][v] = floor(dct/q_site[u*8+v] + 0.5)

    return result


values = [
    [195, 195, 195, 195, 195, 195, 194, 194],
    [195, 194, 194, 194, 193, 193, 193, 193],
    [195, 195, 195, 194, 193, 193, 192, 192],
    [197, 196, 196, 196, 195, 194, 193, 193],
    [198, 197, 196, 196, 195, 194, 193, 193],
    [196, 196, 196, 195, 194, 193, 192, 192],
    [196, 196, 195, 194, 193, 192, 192, 191],
    [196, 196, 195, 194, 193, 193, 192, 192]
]

rgb = [[(v, v, v) for v in row] for row in values]

for row in compress_y_block(rgb, quality=50):
    print(row)
