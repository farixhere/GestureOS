
import math

# GestureOS - Gesture Recognition Engine

def distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def fingers_up(hand):
    landmarks = hand.landmark

    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    return [
        landmarks[tip].y < landmarks[pip].y
        for tip, pip in zip(tips, pips)
    ]


def detect_gesture(hand):
    lm = hand.landmark

    index, middle, ring, pinky = fingers_up(hand)

    pinch = distance(lm[4], lm[8])

    # Pinch: thumb and index touch
    if pinch < 0.045:
        return "LEFT CLICK"

    # Index finger only
    if index and not middle and not ring and not pinky:
        return "CURSOR"

    # Two fingers
    if index and middle and not ring and not pinky:
        return "RIGHT CLICK"

    # Three fingers
    if index and middle and ring and not pinky:
        return "DOUBLE CLICK"

    # All fingers raised
    if index and middle and ring and pinky:
        return "OPEN PALM"

    # Closed fist
    if not any([index, middle, ring, pinky]):
        return "FIST"

    return "UNKNOWN"
