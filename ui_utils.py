import cv2

def draw_panel(img, x, y, w, h, color=(35,35,35)):
    overlay = img.copy()
    cv2.rectangle(overlay, (x,y), (x+w,y+h), color, -1)
    cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

def draw_text(img, text, x, y, size=0.72, color=(255,255,255)):
    cv2.putText(img, text, (x,y),
                cv2.FONT_HERSHEY_SIMPLEX,
                size, color, 2, cv2.LINE_AA)

def draw_color_indicator(img, color, x=300, y=55):
    cv2.circle(img,(x,y),16,color,-1)
    cv2.circle(img,(x,y),16,(255,255,255),2)