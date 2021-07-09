import cv2
import numpy as np

img = cv2.imread("Resources/test.png")

imgResize = cv2.resize(img, (1000, 500))

print(img.shape)
print(imgResize.shape)

imgCropped = img[0: 200, 200:500]

cv2.imshow("Image", img)
# cv2.imshow("Image Resize", imgResize)
cv2.imshow("Image Cropped", imgCropped)

cv2.waitKey(0)