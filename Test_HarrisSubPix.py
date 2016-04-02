import cv2
import numpy as np

cv2.destroyAllWindows()
img = cv2.imread('K:\FloorplanToJson\images\FloorPlan1.jpg')
img1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, img2 = cv2.threshold(img1, 70, 255, cv2.THRESH_BINARY_INV)

element = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

# Erosion to remove noise
img3 = cv2.erode(img2, element, iterations=1)

# Closing to fill small holes inside foreground
kernel = np.ones((5, 5), np.uint8)
img4 = cv2.morphologyEx(img3, cv2.MORPH_CLOSE, kernel)

# find Harris corners
dst = cv2.cornerHarris(img4, 5, 5, 0.04)
dst = cv2.dilate(dst, None)
ret, dst = cv2.threshold(dst, 0.5 * dst.max(), 255, 0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(img4, np.float32(centroids), (5, 5), (-1, -1), criteria)


# Now draw them
res = np.hstack((centroids, corners))
res = np.int0(res)

print(res)
img[res[:, 1], res[:, 0]] = [0, 0, 255]
img[res[:, 3], res[:, 2]] = [0, 255, 0]
cv2.imshow()
cv2.imshow('subpixel5.png', img)
cv2.waitKey(0)
