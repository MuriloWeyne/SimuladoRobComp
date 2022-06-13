#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np
import math

def encontrar_foco(D,H,h):
    """Não mude ou renomeie esta função
    Entradas:
       D - distancia real da câmera até o objeto (papel)
       H - a distancia real entre os circulos (no papel)
       h - a distancia na imagem entre os circulos
    Saída:
       f - a distância focal da câmera
    """
    return (D*h)/H

def segmenta_circulo_ciano(hsv): 
    """Não mude ou renomeie esta função
    Entrada:
        hsv - imagem em hsv
    Saída:
        mask - imagem em grayscale com tudo em preto e os pixels do circulos ciano em branco
    """
    mask = hsv[:,:,0]
    menor_ciano=(int(160/2), 50, 50)
    maior_ciano = (int(200/2), 255, 255)
    mask_ciano = cv2.inRange(hsv, menor_ciano, maior_ciano)
    return mask_ciano

def segmenta_circulo_magenta(hsv):
    """Não mude ou renomeie esta função
    Entrada:
        hsv - imagem em hsv
    Saída:
        mask - imagem em grayscale com tudo em preto e os pixels do circulos magenta em branco
    """
    mask = hsv[:,:,0]
    menor_magenta = (int(280/2), 50, 50)
    maior_magenta = (int(320/2), 255, 255)
    mask_magenta = cv2.inRange(hsv, menor_magenta, maior_magenta)
    return mask_magenta


def encontrar_maior_contorno(segmentado):
    """Não mude ou renomeie esta função
    Entrada:
        segmentado - imagem em preto e branco
    Saída:
        contorno - maior contorno obtido (APENAS este contorno)
    """
    contornos, hierarchy = cv2.findContours(segmentado, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    
    contorno = max(contornos, key=cv2.contourArea)
    return contorno

def encontrar_centro_contorno(contorno):
    """Não mude ou renomeie esta função
    Entrada:
        contorno: um contorno (não o array deles)
    Saída:
        (Xcentro, Ycentro) - uma tuple com o centro do contorno (no formato 'int')!!! 
    """ 
    M = cv2.moments(contorno)
    if M["m00"] == 0:
        return (0,0)
    Xcentro = int(M["m10"] / M["m00"])
    Ycentro = int(M["m01"] / M["m00"])
    return (Xcentro, Ycentro)

def calcular_h(centro_ciano, centro_magenta):
    """Não mude ou renomeie esta função
    Entradas:
        centro_ciano - ponto no formato (X,Y)
        centro_magenta - ponto no formato (X,Y)
    Saída:
        distancia - a distancia Euclidiana entre os pontos de entrada 
    """

    ciano_x = centro_ciano[0]
    ciano_y = centro_ciano[1]

    magenta_x = centro_magenta[0]
    magenta_y = centro_magenta[1]


    dentro_da_raiz = (ciano_x-magenta_x)**2+(ciano_y-magenta_y)**2
    distancia = math.sqrt(dentro_da_raiz)
    return distancia

def encontrar_distancia(f,H,h):
    """Não mude ou renomeie esta função
    Entrada:
        f - a distância focal da câmera
        H - A distância real entre os pontos no papel
        h - a distância entre os pontos na imagem
    Saída:
        D - a distância do papel até câmera
    """
    if h == 0:
        return 0;
    D = (f*H)/h
    return D

def calcular_distancia_entre_circulos(img):
    """Não mude ou renomeie esta função
    Deve utilizar as funções acima para calcular a distancia entre os circulos a partir da imagem BGR
    Entradas:
        img - uma imagem no formato BGR
    Saídas:
        h - a distância entre os os circulos na imagem
        centro ciano - o centro do círculo ciano no formato (X,Y)
        centro_magenta - o centro do círculo magenta no formato (X,Y)
        img_contornos - a imagem com os contornos desenhados
    """
    img_contornos = img.copy()
    img_contornos_hsv = cv2.cvtColor(img_contornos, cv2.COLOR_BGR2HSV)


    segmenta_ciano = segmenta_circulo_ciano(img_contornos_hsv)
    segmenta_magenta = segmenta_circulo_magenta(img_contornos_hsv)
    contorno_ciano = encontrar_maior_contorno(segmenta_ciano)
    contorno_magenta = encontrar_maior_contorno(segmenta_magenta)

    centro_ciano = encontrar_centro_contorno(contorno_ciano)        
    centro_magenta = encontrar_centro_contorno(contorno_magenta)
    
    h = calcular_h(centro_ciano, centro_magenta)
    if np.all(contorno_ciano) and np.all(contorno_magenta):
        cv2.drawContours(img_contornos, contorno_ciano, -1, [0, 0, 255], 3);
        cv2.drawContours(img_contornos, contorno_magenta, -1, [255, 0, 0], 3);
        return h, centro_ciano, centro_magenta, img_contornos
    else:
        return 0, centro_ciano, centro_magenta, img_contornos
def calcular_angulo_com_horizontal_da_imagem(centro_ciano, centro_magenta):
    """Não mude ou renomeie esta função
        Deve calcular o angulo, em graus, entre o vetor formado com os centros do circulos e a horizontal.
    Entradas:
        centro_ciano - centro do círculo ciano no formato (X,Y)
        centro_magenta - centro do círculo magenta no formato (X,Y)
    Saídas:
        angulo - o ângulo entre os pontos em graus
    """
    vetorX = (1,0)
    vetorCentro = (centro_ciano[0]-centro_magenta[0], centro_ciano[1]-centro_magenta[1])
    escalar = vetorX[0]*vetorCentro[0] + vetorX[1]*vetorCentro[1]
    vetorX_modulo = math.sqrt(vetorX[0]**2+vetorX[1]**2)
    vetorCentro_modulo = math.sqrt(vetorCentro[0]**2+vetorCentro[1]**2)
    produto_modulos = vetorX_modulo*vetorCentro_modulo
    angulo = math.degrees(np.arccos(escalar/produto_modulos))
    return angulo
