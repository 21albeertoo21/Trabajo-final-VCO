import cv2
import os

RESOLUTION = 0.5
FOLDERPATH = '../Training/Training'
OUTPUT_FOLDER = '../Training/Resized'

def loadImages(folder):
    images = []
    filenames = []
    for file in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, file))
        if img is not None:
            images.append(img)
            filenames.append(file)
    return images, filenames

def resizeImages():
    # Cargar todas las imágenes en una lista
    images, filenames = loadImages(FOLDERPATH)

    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    for img, filename in zip(images, filenames):
        try:
            imgResized = cv2.resize(img, None, fx=RESOLUTION, fy=RESOLUTION, interpolation=cv2.INTER_AREA)
            output_path = os.path.join(OUTPUT_FOLDER, 'resized_' + filename)
            cv2.imwrite(output_path, imgResized)
        except Exception as e:
            print(f"Error processing image {filename}: {e}")

resizeImages()