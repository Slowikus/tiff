# import cv2
import numpy as np
import tiff as tf
import matplotlib.pyplot as plt

####DFT

# img = cv2.imread('slowikus.tif',0)
# f = np.fft.fft2(img)
# fshift = np.fft.fftshift(f)
# magnitude_spectrum = 20*np.log(np.abs(fshift))
#
# plt.subplot(121),plt.imshow(img, cmap = 'gray')
# plt.title('Input Image'), plt.xticks([]), plt.yticks([])
# plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
# plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
# plt.show()



#operacje na obrazie

#kopiowanie działa


image = 'slowikus.tif'
image_anonimized = 'anonim.tif'
tiff_file = tf.Tiff(image)

# img = plt.imread(image)
# plt.imshow(img)
# plt.show()
