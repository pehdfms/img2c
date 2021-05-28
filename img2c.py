import numpy as np
import cv2 as cv

img = cv.imread('input.bmp')

def convert_rgb565(pixel):
    r, g, b = pixel[2], pixel[1], pixel[0]

    rgb = ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)
    return hex(rgb)

def create_matrix(img):
    x, y, _ = img.shape

    colors = set()
    matrix_str = "static unsigned int sprite[] = {\n"

    byte_count = 0
    for i in range(x):
        matrix_str += "    "
        for j in range(y):
            current_color = convert_rgb565(img[i,j])

            colors.add(current_color)
            matrix_str += current_color + ", "

            byte_count += 1
        matrix_str += "\n"
    matrix_str += "}"

    print(f"Quantidade de Bytes utilizados: {byte_count}")
    if (byte_count > 2048):
        print("CUIDADO! IMAGEM PASSA DE 2KB!")
    print("Tome isto como uma guia, pois a quantidade exata de bytes usado pode variar dependendo das otimizacoes do compilador")

    count = 0
    colors_str = ""
    for color in list(colors):
        colors_str += f"#define C{count} {color}\n"
        matrix_str = matrix_str.replace(color, f"C{count}")
        count += 1

    return colors_str + "\n" + matrix_str

with open("output.txt", "w") as f:
    results = create_matrix(img)
    f.write(results)
