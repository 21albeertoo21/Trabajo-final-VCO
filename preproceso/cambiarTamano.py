import cv2
import os

RESOLUTION = 0.5
FOLDER_PATH_TRAINING = '../Training/Training'
OUTPUT_FOLDER_TRAINING = '../Training/Resized'
FOLDER_PATH_TEST = '../Test/Test'
OUTPUT_FOLDER_TEST = '../Test/Resized'

def loadImagesTraining(folder):
    images = []
    filenames = []
    for file in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, file))
        if img is not None:
            images.append(img)
            filenames.append(file)
    return images, filenames

def loadImagesTest(folder):
    images = []
    filenames = []
    for file in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, file))
        if img is not None:
            images.append(img)
            filenames.append(file)
    return images, filenames

def resizeImages():
    # Cargar todas las imágenes Training en una lista
    imagesTraining, filenamesTraining = loadImagesTraining(FOLDER_PATH_TRAINING)
    imagesTest, filenamesTest = loadImagesTest(FOLDER_PATH_TEST)

    if not os.path.exists(OUTPUT_FOLDER_TRAINING):
        os.makedirs(OUTPUT_FOLDER_TRAINING)
    elif not os.path.exists(OUTPUT_FOLDER_TEST):
        os.makedirs(OUTPUT_FOLDER_TEST)

    # Redimensionar las imágenes y guardarlas en la carpeta de salida Training
    for img, filename in zip(imagesTraining, filenamesTraining):
        try:
            imgResized = cv2.resize(img, None, fx=RESOLUTION, fy=RESOLUTION, interpolation=cv2.INTER_AREA)
            output_path = os.path.join(OUTPUT_FOLDER_TRAINING, 'resized_' + filename)
            cv2.imwrite(output_path, imgResized)
        except Exception as e:
            print(f"Error processing image {filename}: {e}")

    for img, filename in zip(imagesTest, filenamesTest):
        try:
            imgResized = cv2.resize(img, None, fx=RESOLUTION, fy=RESOLUTION, interpolation=cv2.INTER_AREA)
            output_path = os.path.join(OUTPUT_FOLDER_TEST, 'resized_' + filename)
            cv2.imwrite(output_path, imgResized)
        except Exception as e:
            print(f"Error processing image {filename}: {e}")

resizeImages()
