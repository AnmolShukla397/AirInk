import cv2
import numpy as np
import mediapipe as mp
import time

print("Starting AirInk...")

# ---------------- MEDIAPIPE INIT ----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.85,
    min_tracking_confidence=0.85
)

print("MediaPipe Loaded")

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

if not cap.isOpened():
    print("❌ Camera failed to open")
    exit()

print("Camera Initialized")

# ---------------- CANVAS ----------------
canvas = None

# Drawing settings
draw_color = (0, 0, 255)
brush_thickness = 8

# Smoothing
prev_point = None
smooth_point_prev = None

# Gesture timing
last_color_change = 0
COLOR_DELAY = 1.0
gesture_lock = False

# ---------------- FUNCTIONS ----------------

def fingers_up(hand_landmarks, handedness):
    lm = hand_landmarks.landmark
    fingers = []

    # Thumb detection (front + back fixed)
    if handedness == "Right":
        fingers.append(1 if lm[4].x < lm[3].x else 0)
    else:
        fingers.append(1 if lm[4].x > lm[3].x else 0)

    # Other fingers
    finger_tips = [8, 12, 16, 20]

    for tip in finger_tips:
        fingers.append(1 if lm[tip].y < lm[tip - 2].y else 0)

    return fingers


def distance(p1, p2):
    return np.hypot(p2[0] - p1[0], p2[1] - p1[1])


def smooth_point(current, previous, alpha=0.75):
    """
    Apple Pencil style smoothing
    """
    if previous is None:
        return current

    x = int(previous[0] * alpha + current[0] * (1 - alpha))
    y = int(previous[1] * alpha + current[1] * (1 - alpha))

    return (x, y)


# ---------------- MAIN LOOP ----------------
while True:

    success, frame = cap.read()

    if not success:
        print("❌ Failed to read frame")
        break

    frame = cv2.flip(frame, 1)

    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros_like(frame)

    # Background dim
    dark_overlay = np.zeros_like(frame)
    frame = cv2.addWeighted(frame, 0.75, dark_overlay, 0.25, 0)

    # RGB conversion
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand tracking
    results = hands.process(rgb)

    # ---------------- HAND DETECTION ----------------
    if results.multi_hand_landmarks:

        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):

            handedness = results.multi_handedness[i].classification[0].label

            lm = hand_landmarks.landmark

            # Finger coordinates
            index_tip = (
                int(lm[8].x * w),
                int(lm[8].y * h)
            )

            thumb_tip = (
                int(lm[4].x * w),
                int(lm[4].y * h)
            )

            # Finger states
            fingers = fingers_up(hand_landmarks, handedness)
            finger_count = sum(fingers)

            # ---------------- DRAWING ----------------
            # ONLY index finger up
            if fingers == [0, 1, 0, 0, 0]:

                # Smooth point
                smoothed = smooth_point(index_tip, smooth_point_prev)

                if prev_point is None:
                    prev_point = smoothed

                # Super smooth line
                cv2.line(
                    canvas,
                    prev_point,
                    smoothed,
                    draw_color,
                    brush_thickness,
                    cv2.LINE_AA
                )

                prev_point = smoothed
                smooth_point_prev = smoothed

            else:
                prev_point = None
                smooth_point_prev = None

            # ---------------- COLOR CHANGE ----------------
            pinch_distance = distance(index_tip, thumb_tip)

            current_time = time.time()

            # Pinch gesture
            if pinch_distance < 30:

                if (
                    not gesture_lock
                    and current_time - last_color_change > COLOR_DELAY
                ):

                    gesture_lock = True

                    # Cycle colors
                    if draw_color == (0, 0, 255):
                        draw_color = (255, 0, 0)

                    elif draw_color == (255, 0, 0):
                        draw_color = (0, 255, 0)

                    else:
                        draw_color = (0, 0, 255)

                    last_color_change = current_time

            else:
                gesture_lock = False

            # ---------------- CLEAR ----------------
            # Fist gesture
            if finger_count == 0:
                canvas = np.zeros_like(frame)

            # ---------------- HAND SKELETON ----------------
            # Red joints
            for point in lm:

                cx = int(point.x * w)
                cy = int(point.y * h)

                cv2.circle(
                    frame,
                    (cx, cy),
                    6,
                    (0, 0, 255),
                    -1
                )

            # White skeleton
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_draw.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2
                ),
                mp_draw.DrawingSpec(
                    color=(255, 255, 255),
                    thickness=2
                )
            )

            # ---------------- UI ----------------
            # Top panel
            cv2.rectangle(
                frame,
                (0, 0),
                (w, 85),
                (20, 20, 20),
                -1
            )

            # Title
            cv2.putText(
                frame,
                "AirInk",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2,
                cv2.LINE_AA
            )

            # Finger count
            cv2.putText(
                frame,
                f"Fingers: {finger_count}",
                (20, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

            # Controls
            cv2.putText(
                frame,
                "Index = Draw",
                (250, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (220, 220, 220),
                2,
                cv2.LINE_AA
            )

            cv2.putText(
                frame,
                "Pinch = Color",
                (250, 70),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (220, 220, 220),
                2,
                cv2.LINE_AA
            )

            # Current color indicator
            cv2.circle(
                frame,
                (w - 50, 42),
                18,
                draw_color,
                -1
            )

    # ---------------- MERGE CANVAS ----------------
    gray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)

    _, mask = cv2.threshold(
        gray,
        20,
        255,
        cv2.THRESH_BINARY
    )

    mask_inv = cv2.bitwise_not(mask)

    frame_bg = cv2.bitwise_and(
        frame,
        frame,
        mask=mask_inv
    )

    canvas_fg = cv2.bitwise_and(
        canvas,
        canvas,
        mask=mask
    )

    final_frame = cv2.add(frame_bg, canvas_fg)

    # ---------------- SHOW ----------------
    cv2.imshow("AirInk", final_frame)

    key = cv2.waitKey(1)

    # ESC to exit
    if key == 27:
        break

# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()
print("AirInk Closed")