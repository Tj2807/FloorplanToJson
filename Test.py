import numpy as np
import cv2


# from scipy.spatial import distance


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


img = cv2.imread('K:\FloorplanToJson\images\FloorPlan6.png')
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 70, 255, cv2.THRESH_BINARY_INV)

element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# Erosion to remove noise
img3 = cv2.erode(img2, element, iterations=1)

# Closing to fill small holes inside foreground
kernel = np.ones((5, 5), np.uint8)
img4 = cv2.morphologyEx(img3, cv2.MORPH_CLOSE, kernel)

# Thin the image
kernel = np.ones((2, 2), np.uint8)
img5 = cv2.erode(img4, kernel, iterations=2)

# Obtain image skeleton
img6 = skeleton(img5)
cv2.imshow('img6', img6)

img7 = cv2.dilate(img6, element, iterations=2)
cv2.imshow('img7', img7)

# Hough transform for line detection
minLineLength = 10
maxLineGap = 20
lines = cv2.HoughLinesP(img6, 1, np.pi / 180, 100, minLineLength, maxLineGap)

# print(lines)
"""
print(type(lines))
print(lines[0, 0, :])
print(lines.shape)
"""

# arr = np.hstack((arr, np.array([1, 2, 3])))

newline = np.array([])
newline = np.hstack((newline, lines[0, 0, :]))
newline = newline[np.newaxis, :]
print(newline)
for i in range(1, lines.shape[0]):
    # print('i=', i)
    flag = 0
    for j in range(newline.shape[0]):
        # print('j=', j)
        # print('lines=', lines[i, 0, :])
        # print('newline=', newline[j, :])
        check = np.absolute(lines[i, 0, :] - newline[j, :])
        # print('check=', check)
        # print((check < 10).all())
        if (check < 10).all():
            # print('Inside check')
            newline[j, :] = (newline[j, :] + lines[i, 0, :]) / 2
            flag = 1
            break

    if flag == 0:
        newline = np.vstack((newline, lines[i, 0, :]))

print('newline:')
# print(newline)

newline = np.round(newline)
newline = newline.astype(int)

print('lines=', lines.shape)
print(lines)
print('newline=', newline.shape)
print(newline)

for [x1, y1, x2, y2] in newline:
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

img_copy = img
for [[x1, y1, x2, y2]] in lines:
    cv2.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)

cv2.imshow('img4', img4)
cv2.imshow('img', img)
cv2.imshow('img_copy', img_copy)

cv2.waitKey(0)

