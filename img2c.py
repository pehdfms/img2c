import numpy as np
import cv2 as cv

def convert_rgb565(pixel):
    b, g, r = pixel[0:3]
    rgb = ((r & 0b11111000) << 8) | ((g & 0b11111100) << 3) | (b >> 3)

    return hex(rgb)

def create_matrix(img):
    altura, largura, _ = img.shape

    colors = set()
    matrix_str = "static unsigned int sprite[] = {\n"

    for i in range(altura):
        matrix_str += "    "
        for j in range(largura):
            current_color = convert_rgb565(img[i,j])

            colors.add(current_color)
            matrix_str += current_color + ", "
        matrix_str += "\n"
    matrix_str += "}"

    byte_count = altura*largura
    print(f"Quantidade de Bytes utilizados: {byte_count}")
    if (byte_count > 2048):
        print("CUIDADO! IMAGEM PASSA DE 2KB!")
    print("Tome isto como uma guia, pois a quantidade exata de bytes usado pode variar dependendo das otimizacoes do compilador")

    colors_str = ""
    for idx, color in enumerate(list(colors)):
        color_n = "C" + str(idx)
        colors_str += f"#define {color_n} {color}\n"
        matrix_str = matrix_str.replace(color, color_n)

    colors_str += "\n"
    dimensions_str = f"#define W {largura}\n#define H {altura}\n"

    return colors_str + dimensions_str + matrix_str

def write_file(file_name, info):
    with open(file_name, "w") as f:
        f.write(info)

def main():
    img = cv.imread('input.bmp')
    info = create_matrix(img)

    write_file('output.txt', info)

if __name__ == '__main__':
    main()
