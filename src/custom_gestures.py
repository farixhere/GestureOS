
# GestureOS - Custom Exhibition Gesture Detector
# Updated: Unique Volume and Spider-Man Screenshot gestures

import math


def detect_custom_gesture(hand):

    lm = hand.landmark

    # Finger states: index, middle, ring, pinky
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]

    fingers = [
        lm[tip].y < lm[pip].y
        for tip, pip in zip(tips, pips)
    ]

    index, middle, ring, pinky = fingers

    # Thumb detection
    thumb_length = math.hypot(
        lm[4].x - lm[2].x,
        lm[4].y - lm[2].y
    )

    thumb_extended = thumb_length > 0.10

    thumb_up = (
        thumb_extended
        and lm[4].y < lm[3].y - 0.045
    )

    thumb_down = (
        thumb_extended
        and lm[4].y > lm[3].y + 0.045
    )

    # =================================
    # SPIDER-MAN: SCREENSHOT
    # Index + pinky raised
    # =================================

    if index and not middle and not ring and pinky:
        return "SCREENSHOT"

    # =================================
    # VOLUME UP
    # Index + ring raised
    # =================================

    if index and not middle and ring and not pinky:
        return "VOLUME_UP"

    # =================================
    # CALCULATOR: THUMBS UP
    # =================================

    if not any(fingers) and thumb_up:
        return "CALCULATOR"

    # =================================
    # VOLUME DOWN: THUMBS DOWN
    # =================================

    if not any(fingers) and thumb_down:
        return "VOLUME_DOWN"

    # =================================
    # NOTEPAD: PINKY ONLY
    # =================================

    if not index and not middle and not ring and pinky:
        return "NOTEPAD"

    return None
