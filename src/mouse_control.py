
import pyautogui
import time

# =====================================
# GestureOS - Precision Mouse Engine
# =====================================

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0

SCREEN_W, SCREEN_H = pyautogui.size()

# Virtual camera control zone
ZONE_LEFT = 0.25
ZONE_RIGHT = 0.75
ZONE_TOP = 0.20
ZONE_BOTTOM = 0.80

# Cursor tuning
SMOOTHING = 0.45
CLICK_COOLDOWN = 0.5

smooth_x = SCREEN_W / 2
smooth_y = SCREEN_H / 2

last_click_time = 0


def move_cursor(hand):
    global smooth_x, smooth_y

    point = hand.landmark[8]

    # Map the smaller camera zone to the full screen
    x = (point.x - ZONE_LEFT) / (ZONE_RIGHT - ZONE_LEFT)
    y = (point.y - ZONE_TOP) / (ZONE_BOTTOM - ZONE_TOP)

    # Clamp movement to the screen boundaries
    x = max(0.0, min(1.0, x))
    y = max(0.0, min(1.0, y))

    target_x = (1.0 - x) * (SCREEN_W - 1)
    target_y = y * (SCREEN_H - 1)

    # Smooth cursor movement
    smooth_x += (target_x - smooth_x) * SMOOTHING
    smooth_y += (target_y - smooth_y) * SMOOTHING

    smooth_x = max(0, min(SCREEN_W - 1, smooth_x))
    smooth_y = max(0, min(SCREEN_H - 1, smooth_y))

    pyautogui.moveTo(int(smooth_x), int(smooth_y))


def perform_click(click_type="left"):
    global last_click_time

    now = time.time()

    if now - last_click_time < CLICK_COOLDOWN:
        return False

    if click_type == "left":
        pyautogui.click()
        print("ACTION: LEFT CLICK")

    elif click_type == "right":
        pyautogui.rightClick()
        print("ACTION: RIGHT CLICK")

    elif click_type == "double":
        pyautogui.doubleClick()
        print("ACTION: DOUBLE CLICK")

    else:
        return False

    last_click_time = now
    return True
