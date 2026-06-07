import cv2
import numpy as np

def detect_shape(cnt):

    area = cv2.contourArea(cnt)

    if area < 5000:
        return None

    peri = cv2.arcLength(cnt,True)

    approx = cv2.approxPolyDP(cnt,0.04*peri,True)

    vertices = len(approx)

    circularity = 4*np.pi*area/(peri*peri)

    if circularity > 0.75:
        return "Circle"

    if vertices == 3:
        return "Triangle"

    if vertices == 4:

        x,y,w,h = cv2.boundingRect(approx)
        ratio = w/float(h)

        if 0.85 < ratio < 1.15:
            return "Square"
        else:
            return "Rectangle"

    if 5 <= vertices <= 6:
        return "Polygon"

    return None