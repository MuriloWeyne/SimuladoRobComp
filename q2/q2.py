import cv2
from matplotlib import lines
import numpy as np
from fotogrametria import encontrar_maior_contorno

font = cv2.FONT_HERSHEY_SIMPLEX
org = (50, 50)  
fontScale = 1
color = (255, 255, 0)
thickness = 2

def escreve_texto(img ,coordenadas, texto):
    cv2.putText(img, texto, coordenadas, font, fontScale, color, thickness, cv2.LINE_AA)


def encontra_figuras(img_bgr):
    """
    Cria e retorna uma nova imagem BGR com os
    pontos de fuga desenhados.

    Entrada:
    - img_bgr: imagem original no formato BGR

    Saída:
    - resultado: imagem BGR com os nomes das figuras escritos 
    """
    

    resultado = img_bgr.copy()

    return resultado

if __name__ == "__main__":
    bgr = cv2.imread('bitmap.png')
    resultado = encontra_figuras(bgr)
    minimo_preto = (0, 0, 0)
    maximo_preto = (0, 0, 0)
    mask_escuro = cv2.inRange(resultado, minimo_preto, maximo_preto)
    contornos, arvore = cv2.findContours(mask_escuro, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x0, y0, w, h = cv2.boundingRect(contornos[0])
    x1, y1, w1, h1 = cv2.boundingRect(contornos[1])
    x2, y2, w2, h2 = cv2.boundingRect(contornos[2])
    canny = cv2.Canny(mask_escuro, 100, 200)
    img1 = canny[y0-10:y0+h+10, x0-10:x0+w+10]
    img2 = canny[y1-5:y1+h1+5, x1-5:x1+w1+5]
    img3 = canny[y2:y2+h2, x2:x2+w2]
    linesP_img1 = cv2.HoughLinesP(img1, 1, np.pi/180, 50, None, minLineLength=20, maxLineGap=5)
    linesP_img2 = cv2.HoughLinesP(img2, 1, np.pi/180, 50, None, minLineLength=20, maxLineGap=5)
    linesP_img3 = cv2.HoughLinesP(img3, 1, np.pi/180, 50, None, minLineLength=20, maxLineGap=5)
    if len(linesP_img1) == 4:
        escreve_texto(resultado, (x0, y0-5), "Quadrado")
    if len(linesP_img3) >= 10:
        escreve_texto(resultado, (x2, y2), "Estrela")
    if linesP_img2 == None:
        escreve_texto(resultado, (x1, y1), "Circulo")
    cv2.imwrite("figura_q2_resultado.png", resultado)
    cv2.imshow('Original', bgr)
    cv2.imshow('Resultado', resultado)
    cv2.waitKey()
    cv2.destroyAllWindows()

