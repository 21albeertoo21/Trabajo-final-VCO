import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import numpy as np
import os 

FOLDER_PATH_TEST = '../Test/Resized'
FOLDER_PATH_TRAINING = '../Training/Resized'
THRESHOLD = 184
MIN_AREA_CARD = 200000
AREA_BACKGROUND = 2129920 # (2080 x 1024)
BOUNDING_BOX_INDEX = 4

class Cards:

    def __init__(self, imgColor, imgGray, centroid, boundingBox, realSuit, realFigure):
        self.imgColor = imgColor
        self.imgGray = imgGray
        self.centroid = centroid
        self.boundingBox = boundingBox
        self.realSuit = ""
        self.realFigure = ""
        #self.Motif = [] # lista para almacenar los motivos asociados a cada carta
    
    def addMotif(self, motif):
        # Agregar un motivo a la lista de motivos
        self.Motif.append(motif)
        
def loadImagesTraining(folder):
    images = []
    filenames = []
    for file in os.listdir(folder):
        try:
            img = cv2.imread(os.path.join(folder, file))
            if img is not None:
                images.append(img)
                filenames.append(file)
        except Exception as e:
            print(f"Error processing file: {e}")
    return images, filenames

def loadImagesTest(folder):
    images = []
    filenames = []
    for file in os.listdir(folder):
        try:
            img = cv2.imread(os.path.join(folder, file))
            if img is not None:
                images.append(img)
                filenames.append(file)
        except Exception as e:
            print(f"Error processing file: {e}")
    return images, filenames

def inputCardDetails(cardColor):
    cv2.imwrite("card.jpg", cardColor)

    # Solicitar el tipo de carta
    valid_suits = {'D', 'C', 'P', 'T'}
    typeCard = input("De qué tipo es la carta (D, C, P, T): ").upper()
    while typeCard not in valid_suits:
        print("Entrada no válida. Por favor, ingrese D, C, P o T.")
        typeCard = input("De qué tipo es la carta (D, C, P, T): ").upper()
    
    # Solicitar el número de carta
    valid_numbers = {'A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'}
    numberCard = input("Qué número es la carta (A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K): ").upper()
    while numberCard not in valid_numbers:
        print("Entrada no válida. Por favor, ingrese A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q o K.")
        numberCard = input("Qué número es la carta (A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K): ").upper()
    
    #!cv2.destroyWindow("card")
    return typeCard, numberCard

def segmentCards():
    # Cargar todas las imágenes Training y Test en las lista correspondientes
    #!imagesTraining, filenamesTraining = loadImagesTraining(FOLDER_PATH_TRAINING)
    imagesTest, filenamesTest = loadImagesTest(FOLDER_PATH_TEST)

    listCards = [] # Lista para almacenar toda la información de cada carta

    for img, filename in zip(imagesTest, filenamesTest):
        try:
            # Pasamos la imagen a gris
            gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Aplicar el umbral
            thresh = cv2.threshold(gray_img, THRESHOLD, 255, cv2.THRESH_BINARY_INV)[1]
            # Sacar todos los contornos de la imagen
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            cont = 1
            # Iterar por todos los contornos para quedarnos con los que son contorno de carta
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)
                areaBoundingBox = w * h
                if areaBoundingBox >= MIN_AREA_CARD and areaBoundingBox < AREA_BACKGROUND:
                    cardColorContour = img[y:y+h, x:x+w]
                    cardGreyContour = thresh[y:y+h, x:x+w]
                    cardColor = cv2.rectangle(cardColorContour, (x,y), (x+w,y+h), (0,255,0), 2)
                    cardGrey = cv2.rectangle(cardGreyContour, (x,y), (x+w,y+h), (0,255,0), 2)

                    # análisis de características
                    analysisCard = cv2.connectedComponentsWithStatsWithAlgorithm(cardGrey, 4, cv2.CV_32S, cv2.CCL_DEFAULT)  
                    (totalLabels, label_ids, statsCard, centroidCard) = analysisCard
                    cardSuit, cardNumber = inputCardDetails(cardColor)
                    listCards.append(Cards(cardColor, cardGrey, centroidCard[cont], statsCard[cont][BOUNDING_BOX_INDEX], cardSuit, cardNumber))
                    cont = cont + 1
            break
        except Exception as e:
            print(f"Error processing image {filename}: {e}")

segmentCards()

#cv2.imwrite(f"segmentacion{i}.jpg", cv2.drawContours(img, cnt, -1, (0, 255, 0), 10))

"""
lista = []
contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
i = 0
for cnt in contours:
    x,y,w,h = cv2.boundingRect(cnt)
    areaBoundingBox = w * h
    if areaBoundingBox >= MIN_AREA_CARD and areaBoundingBox < AREA_BACKGROUND:
        contournCardColor = img[y:y+h, x:x+w]
        cv2.imwrite(f"segmentacion{i}.jpg", cv2.rectangle(contournCardColor,(x,y),(x+w,y+h),(0,255,0),2))
        i = i + 1
        
        contournCardGray = thresh1[y:y+h, x:x+w]
        contournCardColor = img[y:y+h, x:x+w]
        analysis1 = cv2.connectedComponentsWithStatsWithAlgorithm(contournCardGray, 4, cv2.CV_32S, cv2.CCL_DEFAULT)  
        ( totalLabels1, label_ids1, stats1, centroid1) = analysis1
        lista.append(Cards(contournCardColor, contournCardGray, centroid1[i], stats1[i][4], "picas", 9))
        i = i + 1
        
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

# Supongamos que 'img' es la imagen cargada
img = cv2.imread('../Test/Test/IMG_20210321_122224.jpg')
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar el umbral
threshold = 184  # Ajusta este valor según tus necesidades
thresh1 = cv2.threshold(gray_img, threshold, 255, cv2.THRESH_BINARY_INV)[1]

def label2rgb(label_img):
    label_hue = np.uint8(179*(label_img)/np.max(label_img))
    blank_ch = 255*np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    # Convertir a BGR
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    # Poner el fondo a negro. El fondo son los píxeles con etiqueta 0
    labeled_img[label_ids==0] = 0

    return labeled_img





"""

 