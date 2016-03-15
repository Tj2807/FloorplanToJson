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


img1 = cv2.imread('FloorPlan1.jpg', 0)
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

## Extract vertices

# Find row and column locations that are non-zero
(rows, cols) = np.nonzero(img6)

# Initialize empty list of co-ordinates
skel_coords = []

# For each non-zero pixel...
for (r, c) in zip(rows, cols):

    # Extract an 8-connected neighbourhood
    (col_neigh, row_neigh) = np.meshgrid(np.array([c - 1, c, c + 1]), np.array([r - 1, r, r + 1]))

    # Cast to int to index into image
    col_neigh = col_neigh.astype('int')
    row_neigh = row_neigh.astype('int')

    # Convert into a single 1D array and check for non-zero locations
    pix_neighbourhood = img6[row_neigh, col_neigh].ravel() != 0

    # If the number of non-zero locations equals 2, add this to
    # our list of co-ordinates
    if np.sum(pix_neighbourhood) <= 2:
        skel_coords.append((r, c))
r, c = img6.shape
vertices = np.zeros((r, c, 3), 'uint8')
map = np.zeros((r, c), 'uint8')

for (r, c) in zip(rows, cols):
    vertices.itemset((r, c, 0), 255)
    vertices.itemset((r, c, 1), 255)
    vertices.itemset((r, c, 2), 255)

for (r, c) in skel_coords:
    vertices.itemset((r, c, 0), 0)
    vertices.itemset((r, c, 1), 0)
    vertices.itemset((r, c, 2), 255)
    map.itemset((r, c), 255)

    # print(k)
# print('\n\n')
# (rows, cols) = np.nonzero(vertices)
# print(rows, cols)
# print(vertices[:,:,2])
# map = vertices[:, :, 2]
map = cv2.dilate(map, kernel, 15)
vertices[:, :, 2] = map;

cv2.imshow('Figure', vertices)
cv2.imshow('Vertices', map)
# cv2.imshow('Dim2', vertices[:, :, 2])
# cv2.imshow('map', map)

cv2.waitKey(0)
