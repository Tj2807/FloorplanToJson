import cv2
import numpy as np
import imtool


def dist(vertex1, vertex2):
    distance = (sum(np.absolute(vertex1 - vertex2) ** 2)) ** .5
    return distance


def draw_line(x1, y1, x2, y2, skip):
    vertex1 = np.array([x1, y1])
    vertex2 = np.array([x2, y2])
    distance = dist(vertex1, vertex2)
    skip = np.round(skip * distance)
    # print('skip=', skip)
    xp = np.array([])
    yp = np.array([])
    for t in np.linspace(0, 1, num=skip):
        xp = np.hstack((xp, [x1 + t * (x2 - x1)]))
        yp = np.hstack((yp, [y1 + t * (y2 - y1)]))
    return xp, yp


# ----------------------------------------------------------------------------------------------------------------------
filename = '.\images\FloorPlan6.png'
cv2.destroyAllWindows()
img = cv2.imread(filename)
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 70, 255, cv2.THRESH_BINARY_INV)

element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

#  ---------------------------------------------------------------------------------------------------------------------
#  Erosion to remove noise
img3 = cv2.erode(img2, element, iterations=1)

# ----------------------------------------------------------------------------------------------------------------------
# Closing to fill small holes inside foreground
kernel = np.ones((5, 5), np.uint8)
img4 = cv2.morphologyEx(img3, cv2.MORPH_CLOSE, kernel)

# ----------------------------------------------------------------------------------------------------------------------
# Remove the small disturbance caused by noise and text in between
img4_copy = img4

_, contours, hierarchy = cv2.findContours(img4, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for i in contours:
    area = cv2.contourArea(i)
    if 0.0 <= area < 100.0:
        cv2.drawContours(img4_copy, [i], 0, (0, 0, 0), -1)
    else:
        cv2.drawContours(img4_copy, [i], 0, (255, 0, 0), -1)

# ----------------------------------------------------------------------------------------------------------------------
# Find Harris corners
dst = cv2.cornerHarris(np.float32(img4), 5, 5, 0.1)
r, c = np.nonzero(dst > .5 * dst.max())

# print('r=', r.shape, r)
# print('c=', c.shape, c)
# print('\n\n')

# ----------------------------------------------------------------------------------------------------------------------
# Removing nearby corners
corners = np.array([])
corners = np.hstack((corners, np.array([r[0], c[0]])))
corners = np.expand_dims(corners, axis=0)
# print(corners.shape)
for i in range(1, r.shape[0]):
    flag = 0
    for j in range(corners.shape[0]):
        vertex1 = np.array([r[i], c[i]])
        vertex2 = corners[j]
        if dist(vertex1, vertex2) < 30:
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

# ----------------------------------------------------------------------------------------------------------------------
# Find whether a wall exists between two corners
skip = .1
img4 = cv2.dilate(img4, element, iterations=10)
cv2.imshow('it=10', img4)

img4 = cv2.dilate(img4, element, iterations=15)
cv2.imshow('it=15', img4)

img5 = np.array(np.zeros(img.shape))
for k in range(img.shape[2]):
    img5[:, :, k] = img4

# ----------------------------------------------------------------------------------------------------------------------
# Show corners found by Harris algorithm
mask = np.zeros(img4.shape, dtype=bool)
mask[corners[:, 0], corners[:, 1]] = True
mask = cv2.dilate(mask.astype(np.float32), None, iterations=2)
mask = mask > 0
img5[mask] = [0, 0, 255]

walls = np.empty((0, 4), np.uint8)

for i in range(corners.shape[0]):
    for j in range(i + 1, corners.shape[0]):
        if i == j:
            continue
        xp, yp = draw_line(corners[i, 0], corners[i, 1], corners[j, 0], corners[j, 1], skip)

        xp = np.round(xp)
        xp = xp.astype(int)

        yp = np.round(yp)
        yp = yp.astype(int)

        lineIndices = img4[xp, yp]
        percentage = np.sum(lineIndices) / (255 * lineIndices.shape[0])

        if percentage >= .95:
            mask = np.zeros(img4.shape, dtype=bool)
            mask[xp, yp] = True

            mask = cv2.dilate(mask.astype(np.float32), None, iterations=1)
            mask = mask > 0
            img5[mask] = [255, 0, 0]
            walls = np.vstack((walls, [corners[i, 0], corners[i, 1], corners[j, 0], corners[j, 1]]))

# Output
print('walls=', walls)
imtool.coors('img5')  # Creates a named window and attaches coordinates mouse callback with it
cv2.imshow('img5', img5)
cv2.imshow('dst', img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()
