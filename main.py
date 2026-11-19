
import cv2
import mediapipe as mp
import time

# ==========================================
# GESTURE OS - TOUCHLESS COMPUTER CONTROL
# Exhibition Edition
# ==========================================

from src.gesture_recognition import detect_gesture
from src.custom_gestures import detect_custom_gesture
from src.custom_commands import execute_custom_command

from src.mouse_control import move_cursor, perform_click
from src.motion_controls import MotionController

from src.system_commands import (
    scroll_up,
    scroll_down,
    next_slide,
    previous_slide
)

# ==========================================
# CAMERA SETTINGS
# ==========================================

CAM_W, CAM_H = 1280, 720

STABLE_FRAMES = 8

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAM_W)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAM_H)

if not cap.isOpened():
    hands.close()
    raise RuntimeError("Webcam unavailable.")

# ==========================================
# SYSTEM STATE
# ==========================================

motion = MotionController()

paused = False

candidate = None
stable_count = 0
previous_gesture = None

# Two-finger motion detection
two_finger_since = None
two_finger_action_done = False

RIGHT_CLICK_DELAY = 0.65

# ==========================================
# CLICK ENGINE
# ==========================================

def execute_click(gesture):

    if gesture == "LEFT CLICK":
        perform_click("left")

    elif gesture == "RIGHT CLICK":
        perform_click("right")

    elif gesture == "DOUBLE CLICK":
        perform_click("double")


# ==========================================
# STARTUP
# ==========================================

print("\n================================")
print("       GESTURE OS ONLINE")
print("================================")

print("INDEX FINGER       : CURSOR")
print("PINCH              : LEFT CLICK")
print("TWO FINGERS        : RIGHT CLICK / MOTION")
print("THREE FINGERS      : DOUBLE CLICK")
print("OPEN PALM          : PAUSE / RESUME")

print("\nCUSTOM EXHIBITION COMMANDS")
print("FIST               : SCREENSHOT")
print("THUMBS UP          : CALCULATOR")
print("PINKY ONLY         : NOTEPAD")
print("INDEX + RING       : VOLUME UP")
print("THUMBS DOWN        : VOLUME DOWN")

print("\nQ OR ESC           : EXIT")
print("================================\n")


# ==========================================
# MAIN ENGINE
# ==========================================

try:

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = hands.process(rgb)

        gesture = "NO HAND DETECTED"
        action_text = "READY"

        # ==================================
        # HAND DETECTION
        # ==================================

        if results.multi_hand_landmarks:

            hand = results.multi_hand_landmarks[0]

            mp_draw.draw_landmarks(
                frame,
                hand,
                mp_hands.HAND_CONNECTIONS
            )

            # Base gesture recognition
            base_gesture = detect_gesture(hand)

            # Custom gesture recognition
            custom_gesture = detect_custom_gesture(hand)

            # Custom gestures take priority
            gesture = (
                custom_gesture
                if custom_gesture
                else base_gesture
            )

            # ==================================
            # GESTURE STABILITY
            # ==================================

            if candidate == gesture:

                stable_count += 1

            else:

                candidate = gesture
                stable_count = 1

            # ==================================
            # EXECUTE STABLE GESTURES
            # ==================================

            if stable_count >= STABLE_FRAMES:

                # OPEN PALM: PAUSE / RESUME
                if gesture == "OPEN PALM":

                    if gesture != previous_gesture:

                        paused = not paused

                        motion.reset()

                        two_finger_since = None
                        two_finger_action_done = False

                        print(
                            "SYSTEM:",
                            "PAUSED" if paused else "RESUMED"
                        )

                        action_text = (
                            "SYSTEM PAUSED"
                            if paused
                            else "SYSTEM RESUMED"
                        )

                elif not paused:

                    # ==================================
                    # CUSTOM EXHIBITION COMMANDS
                    # ==================================

                    if gesture in (
                        "SCREENSHOT",
                        "CALCULATOR",
                        "NOTEPAD",
                        "VOLUME_UP",
                        "VOLUME_DOWN"
                    ):

                        if gesture != previous_gesture:

                            action_text = execute_custom_command(
                                gesture
                            )

                        motion.reset()

                        two_finger_since = None
                        two_finger_action_done = False

                    # ==================================
                    # CURSOR CONTROL
                    # ==================================

                    elif gesture == "CURSOR":

                        move_cursor(hand)

                        motion.reset()

                        two_finger_since = None
                        two_finger_action_done = False

                    # ==================================
                    # LEFT CLICK
                    # ==================================

                    elif gesture == "LEFT CLICK":

                        if gesture != previous_gesture:

                            execute_click(gesture)
                            action_text = "LEFT CLICK"

                        motion.reset()
                        two_finger_since = None

                    # ==================================
                    # DOUBLE CLICK
                    # ==================================

                    elif gesture == "DOUBLE CLICK":

                        if gesture != previous_gesture:

                            execute_click(gesture)
                            action_text = "DOUBLE CLICK"

                        motion.reset()
                        two_finger_since = None

                    # ==================================
                    # TWO-FINGER MOTION ENGINE
                    # ==================================

                    elif gesture == "RIGHT CLICK":

                        if two_finger_since is None:

                            two_finger_since = time.time()
                            motion.reset()

                        motion_action = motion.update(hand)

                        if motion_action:

                            if motion_action == "SCROLL UP":
                                scroll_up()

                            elif motion_action == "SCROLL DOWN":
                                scroll_down()

                            elif motion_action == "SWIPE RIGHT":
                                next_slide()

                            elif motion_action == "SWIPE LEFT":
                                previous_slide()

                            action_text = motion_action

                            two_finger_action_done = True

                        elif (
                            not two_finger_action_done
                            and time.time() - two_finger_since
                            >= RIGHT_CLICK_DELAY
                        ):

                            execute_click("RIGHT CLICK")

                            two_finger_action_done = True

                            action_text = "RIGHT CLICK"

                previous_gesture = gesture

        # ==================================
        # NO HAND DETECTED
        # ==================================

        else:

            candidate = None
            stable_count = 0
            previous_gesture = None

            two_finger_since = None
            two_finger_action_done = False

            motion.reset()

        # ==================================
        # DISPLAY INTERFACE
        # ==================================

        height, width, _ = frame.shape

        # Header
        cv2.rectangle(
            frame,
            (0, 0),
            (width, 85),
            (20, 20, 20),
            -1
        )

        cv2.putText(
            frame,
            "GESTURE OS",
            (25, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 180),
            2
        )

        # System status
        status = "PAUSED" if paused else "ACTIVE"

        cv2.putText(
            frame,
            "SYSTEM: " + status,
            (width - 260, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (0, 0, 255) if paused else (0, 255, 180),
            2
        )

        # Footer
        cv2.rectangle(
            frame,
            (10, height - 75),
            (width - 10, height - 10),
            (20, 20, 20),
            -1
        )

        cv2.putText(
            frame,
            "GESTURE: " + gesture,
            (25, height - 43),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 180),
            2
        )

        cv2.putText(
            frame,
            "ACTION: " + action_text,
            (width - 330, height - 43),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            1
        )

        cv2.putText(
            frame,
            "Q / ESC: EXIT",
            (width - 200, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1
        )

        # Show camera
        cv2.imshow(
            "GESTURE OS | Exhibition Edition",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key in (ord("q"), 27):
            break


# ==========================================
# SAFE SHUTDOWN
# ==========================================

finally:

    cap.release()

    hands.close()

    cv2.destroyAllWindows()

    print("\nGESTURE OS SHUTDOWN COMPLETE")
