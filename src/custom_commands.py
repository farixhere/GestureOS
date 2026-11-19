
# GestureOS - Custom Exhibition Commands

import pyautogui
import subprocess
from pathlib import Path
from datetime import datetime
import time

last_command_time = 0
COMMAND_COOLDOWN = 0.8


def execute_custom_command(command):
    global last_command_time

    now = time.time()

    if now - last_command_time < COMMAND_COOLDOWN:
        return "COMMAND COOLDOWN"

    try:

        # SCREENSHOT
        if command == "SCREENSHOT":

            folder = Path.home() / "Pictures" / "GestureOS"
            folder.mkdir(parents=True, exist_ok=True)

            filename = datetime.now().strftime(
                "GestureOS_%Y%m%d_%H%M%S.png"
            )

            filepath = folder / filename

            pyautogui.screenshot().save(str(filepath))

            print("SCREENSHOT SAVED:", filepath)
            message = "SCREENSHOT CAPTURED"

        # CALCULATOR
        elif command == "CALCULATOR":

            subprocess.Popen(["calc.exe"])
            print("CALCULATOR LAUNCHED")
            message = "CALCULATOR OPENED"

        # NOTEPAD
        elif command == "NOTEPAD":

            subprocess.Popen(["notepad.exe"])
            print("NOTEPAD LAUNCHED")
            message = "NOTEPAD OPENED"

        # VOLUME UP
        elif command == "VOLUME_UP":

            pyautogui.press("volumeup")
            print("VOLUME UP")
            message = "VOLUME INCREASED"

        # VOLUME DOWN
        elif command == "VOLUME_DOWN":

            pyautogui.press("volumedown")
            print("VOLUME DOWN")
            message = "VOLUME DECREASED"

        else:
            return "UNKNOWN COMMAND"

        last_command_time = now
        return message

    except Exception as error:
        print("COMMAND ERROR:", error)
        return "COMMAND FAILED"
