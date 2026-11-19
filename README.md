# GestureOS

**Touchless computer control using real-time hand tracking and Python.**

GestureOS uses your webcam to detect hand gestures and lets you control the mouse, clicks, scrolling, slides, and a few Windows applications without touching your computer.

> Exhibition Edition

## Features

- Real-time hand tracking with MediaPipe and OpenCV.
- Cursor movement using your index finger.
- Gesture-based left click, right click, and double click.
- Hand-motion scrolling and slide navigation.
- Custom gestures for screenshots, volume, Calculator, and Notepad.
- Gesture stability checks and cooldowns to reduce accidental actions.

## Gesture controls

| Hand gesture | Action |
| --- | --- |
| Index finger only | Move the cursor |
| Pinch thumb and index finger | Left click |
| Two fingers raised | Right click (hold) or motion control |
| Three fingers raised | Double click |
| Open palm | Pause / resume GestureOS |
| Index finger + pinky | Take a screenshot |
| Index finger + ring finger | Volume up |
| Thumbs up | Open Calculator |
| Thumbs down | Volume down |
| Pinky only | Open Notepad |
| Q or Esc | Exit |

**Two-finger motion controls:** move your hand vertically to scroll, or horizontally to navigate slides. Keep the two-finger gesture active while making the movement.

Screenshots are saved in your Windows Pictures folder, inside `Pictures/GestureOS`.

## Requirements

- Windows 10 or Windows 11
- Python 3.12 recommended
- A working webcam
- Git (optional, only needed to clone the repository)

## Installation

Open PowerShell in the folder where you want the project, then run:

```powershell
git clone https://github.com/farixhere/GestureOS.git
cd GestureOS
```

Create and activate a virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run GestureOS

With the virtual environment activated, run:

```powershell
python main.py
```

Allow webcam access if Windows asks for permission. The GestureOS camera window should appear.

## Safety and usage notes

- Keep your hand clearly visible to the webcam and use good lighting.
- GestureOS uses PyAutoGUI to control your mouse and keyboard.
- PyAutoGUI's fail-safe is enabled: move the mouse to the top-left corner of the screen to trigger its emergency stop.
- Press **Q** or **Esc** while the camera window is focused to close GestureOS.
- Close other applications or save your work before testing system-control gestures.

## Project structure

```text
GestureOS/
├── src/
│   ├── __init__.py
│   ├── custom_commands.py
│   ├── custom_gestures.py
│   ├── gesture_recognition.py
│   ├── motion_controls.py
│   ├── mouse_control.py
│   └── system_commands.py
├── main.py
├── settings.py          # Empty placeholder; not currently used
├── requirements.txt
├── README.md
└── .gitignore
```

## Dependencies

The required Python packages are listed in [requirements.txt](requirements.txt).

## Project status

GestureOS is an exhibition project. Gesture recognition and control can vary with webcam quality, lighting, hand position, and system configuration.
**Why We Built GestureOS**

We use computers every day, but most interactions still depend on physical devices like a mouse and keyboard.

We asked ourselves: What if we could control a computer just by moving our hands?

That question inspired us to build GestureOS.

GestureOS is a touchless computer control system powered by computer vision and hand gesture recognition. It uses a webcam to recognize hand movements and translate them into computer commands.

With it, users can move the cursor, click, scroll, navigate presentation slides, adjust volume and open applications without directly touching their computer.

We built this project to explore new possibilities in human-computer interaction, including accessibility, touch-free interfaces and smarter ways of using technology.

**GestureOS — Your hands are the controller.**

---

Made with Python, OpenCV, MediaPipe, and PyAutoGUI.
