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


def dist(vertex1, vertex2):
    distance = (sum(np.absolute(vertex1 - vertex2) ** 2)) ** .5
    return distance


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

# cv2.imshow('img6', img6)

# Hough transform for line detection
minLineLength = 5
maxLineGap = 20
lines = cv2.HoughLinesP(img6, 1, np.pi / 180, 100, minLineLength, maxLineGap)

# print(lines)
"""
print(type(lines))
print(lines[0, 0, :])
print(lines.shape)
"""

# Reduce the number of closely spaced lines by comparing difference in their endpoints
newline = np.array([])
newline = np.hstack((newline, lines[0, 0, :]))
newline = newline[np.newaxis, :]
# print(newline)
for i in range(1, lines.shape[0]):
    flag = 0
    for j in range(newline.shape[0]):
        check = np.absolute(lines[i, 0, :] - newline[j, :])
        if (check < 10).all():
            newline[j, :] = (newline[j, :] + lines[i, 0, :]) / 2
            flag = 1
            break
    if flag == 0:
        newline = np.vstack((newline, lines[i, 0, :]))

# print('newline:')
# print(newline)

newline = np.round(newline)
newline = newline.astype(int)

# print('lines=', lines.shape)
# print(lines)

# Remove duplicate corners
vertices = np.vstack((newline[:, 0:2], newline[:, 2:4]))
k = 0
corners = np.array([])
corners = np.hstack((corners, vertices[0, :]))
corners = np.expand_dims(corners, axis=0)
print(corners.shape)
for i in range(1, vertices.shape[0]):
    flag = 0
    for j in range(corners.shape[0]):
        vertex1 = vertices[i, :]
        vertex2 = corners[j, :]
        """
        print('i=', i, 'j=', j)
        print('vertex1', vertex1)
        print('vertex2', vertex2)
        print('dis', dist(vertex1, vertex2), '\n')
        """
        if dist(vertex1, vertex2) < 20:
            corners[j, :] = (vertex1 + vertex2) / 2
            flag = 1
            break

    if flag == 0:
        corners = np.vstack((corners, vertex1))

# corners[0, 0:3] = []
vertices = np.round(vertices)
vertices = vertices.astype(int)
corners = np.round(corners)
corners = corners.astype(int)

print('vertices=', vertices.shape)
print(vertices)

print('corners=', corners.shape)
print(corners)

# Show detected lines with coordinate reduction algorithm
for [x1, y1, x2, y2] in newline:
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

# Show detected lines without coordinate reduction algorithm
img_copy = img
for [[x1, y1, x2, y2]] in lines:
    cv2.line(img_copy, (x1, y1), (x2, y2), (0, 0, 255), 2)


cv2.imshow('img4', img4)
cv2.imshow('img', img)
cv2.imshow('img_copy', img_copy)
cv2.waitKey(0)

