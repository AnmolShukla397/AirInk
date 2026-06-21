print("1. Starting")
import time
import cv2
print("2. OpenCV loaded")

import mediapipe as mp
print("3. MediaPipe loaded")

import numpy as np
print("4. NumPy loaded")
print("Starting AirInk...")

# ---------------- MEDIAPIPE INIT ----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)

print("MediaPipe Loaded")

# ---------------- CAMERA ----------------
# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

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

    # Better thumb detection
    if handedness == "Right":
        thumb_open = lm[4].x < lm[2].x
    else:
        thumb_open = lm[4].x > lm[2].x

    fingers.append(int(thumb_open))

    # Other fingers
    finger_tips = [8, 12, 16, 20]

    for tip in finger_tips:
        fingers.append(
            1 if lm[tip].y < lm[tip - 2].y else 0
        )

    return fingers


def distance(p1, p2):
    return np.hypot(p2[0] - p1[0], p2[1] - p1[1])


def smooth_point(current, previous, alpha=0.55):
    if previous is None:
        return current

    x = int(previous[0] * alpha + current[0] * (1 - alpha))
    y = int(previous[1] * alpha + current[1] * (1 - alpha))

    return (x, y)

fps_prev = time.time()
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
     # RGB conversion
    small = cv2.resize(frame, (640, 480))

    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    rgb.flags.writeable = False
    results = hands.process(rgb)
    rgb.flags.writeable = True

    # ---------------- HAND DETECTION ----------------
    if results.multi_hand_landmarks:

        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):

            handedness = results.multi_handedness[i].classification[0].label

            lm = hand_landmarks.landmark

            index_tip = (
                int(lm[8].x * w),
                int(lm[8].y * h)
            )

            thumb_tip = (
                int(lm[4].x * w),
                int(lm[4].y * h)
            )

            fingers = fingers_up(hand_landmarks, handedness)
            finger_count = max(0, min(5, sum(fingers)))

            # Drawing
            if fingers == [0, 1, 0, 0, 0]:

                smoothed = smooth_point(index_tip, smooth_point_prev)

                if prev_point is None:
                    prev_point = smoothed

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

            # Color change
            pinch_distance = distance(index_tip, thumb_tip)

            current_time = time.time()

            if pinch_distance < 30:

                if (
                    not gesture_lock
                    and current_time - last_color_change > COLOR_DELAY
                ):

                    gesture_lock = True

                    if draw_color == (0, 0, 255):
                        draw_color = (255, 0, 0)

                    elif draw_color == (255, 0, 0):
                        draw_color = (0, 255, 0)

                    else:
                        draw_color = (0, 0, 255)

                    last_color_change = current_time

            else:
                gesture_lock = False

            # Clear
            if finger_count == 0:
                canvas = np.zeros_like(frame)

            # Skeleton
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

            # UI
            cv2.rectangle(
                frame,
                (0, 0),
                (w, 85),
                (20, 20, 20),
                -1
            )

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

            cv2.circle(
                frame,
                (w - 50, 42),
                18,
                draw_color,
                -1
            )

    # Merge canvas
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

    # FPS
    now = time.time()

    fps = int(1 / max(now - fps_prev, 0.001))

    fps_prev = now

    cv2.putText(
        final_frame,
        f"FPS: {fps}",
        (520, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 0),
        2,
        cv2.LINE_AA
    )
        # ---------------- SHOW ----------------
    cv2.imshow("AirInk", final_frame)

    key = cv2.waitKey(1) & 0xFF

    # ESC key to exit
    if key == 27:
        break


# ---------------- CLEANUP ----------------
cap.release()
cv2.destroyAllWindows()

print("AirInk Closed")