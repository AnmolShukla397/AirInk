def fingers_up(hand_landmarks):
    lm = hand_landmarks.landmark
    fingers = [0,0,0,0,0]

    # detect hand orientation
    if lm[17].x < lm[5].x:
        hand_type = "RIGHT"
    else:
        hand_type = "LEFT"

    # THUMB
    if hand_type == "RIGHT":
        if lm[4].x > lm[3].x and abs(lm[4].y - lm[3].y) > 0.02:
            fingers[0] = 1
    else:
        if lm[4].x < lm[3].x and abs(lm[4].y - lm[3].y) > 0.02:
            fingers[0] = 1

    # INDEX
    if lm[8].y < lm[6].y:
        fingers[1] = 1

    # MIDDLE
    if lm[12].y < lm[10].y:
        fingers[2] = 1

    # RING
    if lm[16].y < lm[14].y:
        fingers[3] = 1

    # PINKY
    if lm[20].y < lm[18].y:
        fingers[4] = 1

    return fingers