import numpy as np
import cv2


def skeleton(img):
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))
    done = False

    while not done:
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True

        return skel


img = cv2.imread('FloorPlan2.png')
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 220, 255, cv2.THRESH_BINARY_INV)

#element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# Erosion to remove noise
#img3 = cv2.erode(img2, element, iterations=1)

# Closing to fill small holes inside foreground
#kernel = np.ones((5, 5), np.uint8)
#img4 = cv2.morphologyEx(img3, cv2.MORPH_CLOSE, kernel)

# Thin the image
#kernel = np.ones((2, 2), np.uint8)
#img5 = cv2.erode(img4, kernel, iterations=2)

# Obtain image skeleton
#img6 = skeleton(img5)

#cv2.imshow('img6', img6)

# Hough transform for line detection
minLineLength = 5
maxLineGap = 1
lines = cv2.HoughLinesP(img2, 1, np.pi / 180, 100, minLineLength, maxLineGap)
print(lines)
for [[x1, y1, x2, y2]] in lines:
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)


cv2.imshow('img2', img2)
cv2.imshow('img', img)
cv2.waitKey(0)
# cv2.imwrite('houghlines5.jpg',img)
