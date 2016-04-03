import cv2
import numpy as np


def dist(vertex1, vertex2):
    distance = (sum(np.absolute(vertex1 - vertex2) ** 2)) ** .5
    return distance


filename = '.\images\FloorPlan6.png'
cv2.destroyAllWindows()
img = cv2.imread(filename)
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 70, 255, cv2.THRESH_BINARY_INV)

element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# Erosion to remove noise
img3 = cv2.erode(img2, element, iterations=1)

# Closing to fill small holes inside foreground
kernel = np.ones((5, 5), np.uint8)
img4 = cv2.morphologyEx(img3, cv2.MORPH_CLOSE, kernel)

cv2.imshow('img4', img4)
img4_copy = img4
_, contours, hierarchy = cv2.findContours(img4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in contours:
    area = cv2.contourArea(i)
    if 0.0 <= area < 100.0:
        cv2.drawContours(img4_copy, [i], 0, (0, 0, 0), -1)
    else:
        cv2.drawContours(img4_copy, [i], 0, (255, 0, 0), -1)

cv2.imshow('img4_modified', img4_copy)
# img4 is black and white image

# Find Harris corners
dst = cv2.cornerHarris(np.float32(img4), 5, 5, 0.1)
r, c = np.nonzero(dst > .5 * dst.max())

"""
print('r=', r.shape, r)
print('c=', c.shape, c)
print('\n\n');
"""

# Removing nearby corners
corners = np.array([])
corners = np.hstack((corners, np.array([r[0], c[0]])))
corners = np.expand_dims(corners, axis=0)
# print(corners.shape)
for i in range(1, r.shape[0]):
    flag = 0
    for j in range(corners.shape[0]):
        vertex1 = np.array([r[i], c[i]])
        vertex2 = np.array([r[j], c[j]])
        if dist(vertex1, vertex2) < 20:
            corners[j, :] = (vertex1 + vertex2) / 2
            flag = 1
            break

    if flag == 0:
        corners = np.vstack((corners, np.array([r[i], c[i]])))

corners = np.round(corners)
corners = corners.astype(int)
# print('corners=', corners.shape, corners)

# result is dilated for marking the corners, not important
dst = cv2.dilate(dst, None)

img5 = np.array(np.zeros(img.shape))
for k in range(img.shape[2]):
    img5[:, :, k] = img4
# Threshold for an optimal value, it may vary depending on the image.
img5[dst > 0.5 * dst.max()] = [0, 0, 255]

cv2.imshow('img5', img5)
# cv2.imshow('dst', img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
