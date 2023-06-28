# this program is to get color for specific HSV Value

import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow('HSV')
cv2.createTrackbar('H', 'HSV', 0, 179, nothing)
cv2.createTrackbar('S', 'HSV', 255, 255, nothing)
cv2.createTrackbar('V', 'HSV', 255, 255, nothing)

img_hsv = np.zeros((258,500,3), np.uint8)

while True:
    h = cv2.getTrackbarPos('H', 'HSV')
    s = cv2.getTrackbarPos('S', 'HSV')
    v = cv2.getTrackbarPos('V', 'HSV')

    img_hsv[:] = (h,s,v)
    img_bgr = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)
    cv2.imshow('HSV', img_bgr)
    key = cv2.waitKey(1)

    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows