import cv2
import numpy as np
import tiff as tf
import matplotlib.pyplot as plt

# file_name= 'tifExample.tiff'
print("Podaj nazwę pliku: ")
file_name= str(input())

####DFT

img_c1 = cv2.imread(file_name, 0)
img_c2 = np.fft.fft2(img_c1)
img_c3 = np.fft.fftshift(img_c2)

plt.subplot(121), plt.imshow(img_c1, "gray"), plt.title("Originał"),plt.xticks([]), plt.yticks([])
plt.subplot(122), plt.imshow(np.log(1+np.abs(img_c3)), "gray"), plt.title("Widmo obrazu"),plt.xticks([]), plt.yticks([])
plt.show()

#operacje na obrazie


tiff_file = tf.Tiff(file_name)

# img = plt.imread(image)
# plt.imshow(img)
# plt.show()
