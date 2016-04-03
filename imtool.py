import cv2
# imtool.coors takes a windowName as an argument, creates that namedWindow and attaches
# a mouse callback with it to give back coordinates


def coors(windowname):
    drawing = False
    ix, iy = -1, -1

    def mouse_event(event, x, y, flags, param):
        global ix, iy, drawing, mode
        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y
        elif event == cv2.EVENT_LBUTTONUP:
            print('Coordinates->', ix, iy, '\n')
            drawing = False

    cv2.namedWindow(windowname)
    cv2.setMouseCallback(windowname, mouse_event)