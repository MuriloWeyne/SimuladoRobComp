#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 
from biblioteca_cow import calcula_iou
from fotogrametria import encontrar_maior_contorno
import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "laserdefense.mp4"



if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 50)  
    fontScale = 1
    colorW = (255, 255, 255)
    thickness = 2
    menor_laranja = (20/2, 50, 50)
    maior_laranja = (40/2, 255, 255)

    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")
    contador = 0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            #cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            break

        # Our operations on the frame come here
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask_nave = cv2.inRange(hsv, menor_laranja, maior_laranja)
        contorno = encontrar_maior_contorno(mask_nave)
        area_contorno_nave = cv2.contourArea(contorno)

        if area_contorno_nave <= 9050:
            frame[mask_nave == 255] = (255, 255, 255)
            contador += 1
        if contador >= 10:
            frame[mask_nave == 255] = (128, 128, 128)
            
        cv2.putText(frame, str(contador), org, font, fontScale, colorW, thickness, cv2.LINE_AA)

        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', frame)
        cv2.imshow("Mask", mask_nave)


        # Pressione 'q' para interromper o video
        if cv2.waitKey(1000//30) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

