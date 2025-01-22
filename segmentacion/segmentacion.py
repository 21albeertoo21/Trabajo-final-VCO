import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os 

FOLDERPATH = '../Training/Resized'
UMBRAL = 184

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

analysis = cv2.connectedComponentsWithStats(thresh1, 4, cv2.CV_32S)
(totalLabels, label_ids, values, centroid) = analysis

output = np.zeros(gray_img.shape, dtype="uint8")

areaMinima = 300000

for i in range(1, totalLabels): # Para todos los objetos encontrados

    # Área de los componentes
    area = values[i, cv2.CC_STAT_AREA]
    key=1
    if (area < areaMinima): # Filtrado por área mínima
        componentMask = (label_ids == i).astype("uint8") * 255
        output = cv2.bitwise_or(output, componentMask)

    if key == ord('q') or key == 27: # 'q' o ESC para acabar
        break

cv2.imwrite('segmentacion.jpg', label2rgb(label_ids))
cv2.destroyAllWindows()






 