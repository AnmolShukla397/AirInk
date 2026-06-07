import cv2
import pytesseract


def recognize_text(canvas):

    gray = cv2.cvtColor(canvas,cv2.COLOR_BGR2GRAY)

    blur = cv2.GaussianBlur(gray,(5,5),0)

    thresh = cv2.adaptiveThreshold(
        blur,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15,
        8
    )

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
    clean = cv2.morphologyEx(thresh,cv2.MORPH_CLOSE,kernel)

    text = pytesseract.image_to_string(
        clean,
        config="--psm 6 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )

    return text.strip()