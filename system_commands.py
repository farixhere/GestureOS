
import pyautogui
import time

# GestureOS - System Command Engine

pyautogui.PAUSE = 0.02

COMMAND_COOLDOWN = 0.6
last_command_time = 0


def can_execute():
    global last_command_time

    now = time.time()

    if now - last_command_time < COMMAND_COOLDOWN:
        return False

    last_command_time = now
    return True


def scroll_up():
    if can_execute():
        pyautogui.scroll(3)
        print("ACTION: SCROLL UP")


def scroll_down():
    if can_execute():
        pyautogui.scroll(-3)
        print("ACTION: SCROLL DOWN")


def next_slide():
    if can_execute():
        pyautogui.press("right")
        print("ACTION: NEXT SLIDE")


def previous_slide():
    if can_execute():
        pyautogui.press("left")
        print("ACTION: PREVIOUS SLIDE")


def volume_up():
    if can_execute():
        pyautogui.press("volumeup")
        print("ACTION: VOLUME UP")


def volume_down():
    if can_execute():
        pyautogui.press("volumedown")
        print("ACTION: VOLUME DOWN")


def switch_application():
    if can_execute():
        pyautogui.hotkey("alt", "tab")
        print("ACTION: SWITCH APPLICATION")
