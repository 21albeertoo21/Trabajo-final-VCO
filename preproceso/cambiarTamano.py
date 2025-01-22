import cv2
import os

def cargarImagenes(carpetaImagenes):
    images = []
    for fichero in os.listdir(carpetaImagenes):
        img = cv2.imread(os.path.join(carpetaImagenes, fichero))
        if img is not None:
            images.append(img)
    return images

# Ruta a la carpeta que contiene las imágenes
rutaImagenes = '../Training'

# Cargar todas las imágenes en una lista
images = cargarImagenes(rutaImagenes)

# Ahora puedes trabajar con la lista de imágenes
if images:
    print('Se han cargado', len(images), 'imágenes')
else:  
    print('No se han encontrado imágenes en la carpeta')