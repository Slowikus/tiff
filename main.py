import cv2
import numpy as np


import tiff as tf
import matplotlib.pyplot as plt



# operacje na obrazie
# file_name= input("Enter file name: ")
file_name = 'obraz1.tif'
val = input("Enter mode: ")
tiff_file = tf.Tiff(file_name, val)

img1 = plt.imread(file_name)
img2 = plt.imread('zakodowanyECB.tif')
img3 = plt.imread('odkodowanyECB.tif')
img4 = plt.imread('zakodowanyCBC.tif')
img5 = plt.imread('odkodowanyCBC.tif')
img6 = plt.imread('zakodowanyCTR.tif')
img7 = plt.imread('odkodowanyCTR.tif')

plt.subplot(331),plt.imshow(img1)
plt.title('Oryginal')
plt.subplot(332),plt.imshow(img2)
plt.title('ECB')
plt.subplot(333),plt.imshow(img3)
plt.title('ECB')
plt.subplot(334),plt.imshow(img1)
plt.title('Oryginal')
plt.subplot(335),plt.imshow(img4)
plt.title('CBC')
plt.subplot(336),plt.imshow(img5)
plt.title('CBC')
plt.subplot(337),plt.imshow(img1)
plt.title('Oryginal')
plt.subplot(338),plt.imshow(img6)
plt.title('CTR')
plt.subplot(339),plt.imshow(img7)
plt.title('CTR')
plt.show()






