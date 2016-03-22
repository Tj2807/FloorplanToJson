import cv2
import source

drawing = False
ix, iy = -1, -1


def mouse_event(event, x, y, flags, param):
    global ix, iy, drawing, mode
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        print('BGR->', source.img[iy, ix][0], source.img[iy, ix][1], source.img[iy, ix][2])
        print('Coordinates->', ix, iy, '\n')
        drawing = False


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True,
# help = "Path to the image")
# args = vars(ap.parse_args())
# img = cv2.imread('K:\FloorplanToJson\images\FloorPlan1.jpg')
cv2.destroyAllWindows()
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_event)

cv2.imshow('image', source.img)
cv2.waitKey(0)

cv2.destroyAllWindows()
