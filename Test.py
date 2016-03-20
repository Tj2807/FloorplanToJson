import numpy as np
import cv2

img1 = cv2.imread('FloorPlan2.png', 1)
ret, img2 = cv2.threshold(img1, 200, 255, cv2.THRESH_BINARY_INV)

cv2.imshow('img1', img1)
cv2.imshow('img2', img2)


kernel = np.ones((2,2), 'uint8')
img3 = cv2.erode(img2, kernel, 1)
# img3 = cv2.dilate(img2, kernel, 5)
cv2.imshow('img3', img3)
cv2.waitKey(0)