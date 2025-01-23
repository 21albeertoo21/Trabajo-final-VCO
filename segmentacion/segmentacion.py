import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os 

FOLDERPATH = '../Test/Resized'
UMBRAL = 184

class Cards:

    def __init__(self, imgColor, imgGray, centroid, boundingBox, realSuit, realFigure):
        self.imgColor = imgColor
        self.imgGray = imgGray
        self.centroid = centroid
        self.boundingBox = boundingBox
        self.realSuit = realSuit
        self.realFigure = realFigure
        

def label2rgb(label_img):
    label_hue = np.uint8(179*(label_img)/np.max(label_img))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    # Convertir a BGR
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    # Poner el fondo a negro. El fondo son los píxeles con etiqueta 0
    labeled_img[label_ids==0] = 0

    return labeled_img

# Supongamos que 'img' es la imagen cargada
img = cv2.imread('../Test/Test/IMG_20210321_122121.jpg')
gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

# Aplicar el umbral
threshold = 184  # Ajusta este valor según tus necesidades
thresh1 = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY_INV)[1]



contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    if w >=980 and h >= 780 and w <= 1300:
        contournCard = thresh1[y:y+h, x:x+w]
        analysis1 = cv2.connectedComponentsWithStatsWithAlgorithm(contournCard, 4, cv2.CV_32S, cv2.CCL_DEFAULT)  
        ( totalLabels1, label_ids1, stats1, centroid1) = analysis1
        
"""
output = np.zeros(gray_img.shape, dtype="uint8")
areaMinima = 300000

for i in range(1, totalLabels1): # Para todos los objetos encontrados

    # Área de los componentes
    area = values[i, cv2.CC_STAT_AREA]
    key=1
    if (stats1[i][4] > areaMinima): # Filtrado carta
        componentMask = (label_ids == i).astype("uint8") * 255
        output = cv2.bitwise_or(output, componentMask)
        cv2.imshow("suu", output)
        cv2.waitKey()
    if key == ord('q') or key == 27: # 'q' o ESC para acabar
        break

#cv2.imwrite('segmentacion.jpg', label2rgb(stats1[i][4]))
cv2.destroyAllWindows()
"""








 