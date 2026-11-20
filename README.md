# GestureOS

<p align="center">
  <strong>Touchless computer control using real-time hand tracking and computer vision.</strong>
</p>

<p align="center">
  Move your cursor, click, scroll, navigate presentation slides, adjust volume, and launch selected Windows apps using simple hand gestures.
</p>

<p align="center">
  <em>Exhibition Edition · Python · OpenCV · MediaPipe · PyAutoGUI</em>
</p>

---

## 1. What is GestureOS?

GestureOS is a webcam-based, touch-free computer interaction project. It detects one hand in a live camera feed, interprets the position of the fingers and palm, and translates recognised gestures into computer actions.

Instead of relying only on a physical mouse or keyboard, a user can:

- Move the mouse pointer by moving an index finger.
- Click by bringing the thumb and index finger together.
- Scroll through pages using vertical hand movement.
- Navigate presentation slides using horizontal hand movement.
- Take screenshots, change system volume, and open selected Windows utilities.

GestureOS is a Python computer-vision prototype built for learning, demonstrations, and exhibitions. It is not an operating system replacement, and it does not currently understand every sign language or arbitrary hand pose.

## 2. Why did we build it?

We use computers for learning, work, communication, and presentations. Most of the time, interacting with a computer means touching a mouse, keyboard, or trackpad.

We wanted to explore a different question:

**What if your hand could become the controller?**

That idea led us to GestureOS. We combined real-time hand tracking with gesture recognition and desktop automation to create a practical demonstration of touchless human-computer interaction.

The project helped us explore:

- **Computer vision:** detecting a hand and tracking its landmark positions through a webcam.
- **Gesture recognition:** interpreting finger positions and combinations as commands.
- **Human-computer interaction (HCI):** designing a simple way for people to control a computer without a physical mouse.
- **Automation:** connecting recognised gestures to mouse, keyboard, volume, screenshot, and application actions.
- **Software engineering:** separating camera processing, recognition, motion tracking, and command execution into individual Python modules.

## 3. Features

| Feature | What it does |
| --- | --- |
| Live hand tracking | Detects and draws hand landmarks in the camera window |
| Cursor movement | Moves the pointer using the index finger |
| Left click | Pinch the thumb and index finger |
| Right click | Hold the two-finger gesture briefly |
| Double click | Raise three fingers |
| Scrolling | Move the two-finger gesture vertically |
| Slide navigation | Move the two-finger gesture horizontally |
| Pause / resume | Show an open palm to pause or resume gesture actions |
| Screenshot | Use the index-finger + pinky gesture |
| Calculator | Show a thumbs-up |
| Notepad | Raise only the pinky |
| Volume control | Use the index + ring gesture for volume up, or thumbs-down for volume down |

## 4. Gesture controls

Use one hand and keep it visible to the webcam. The table describes the gestures recognised by the current implementation.

| Hand gesture | GestureOS action |
| --- | --- |
| Index finger only | Move cursor |
| Thumb + index finger pinch | Left click |
| Index + middle fingers | Right-click after a short hold, or motion control |
| Index + middle + ring fingers | Double click |
| Open palm (all four tracked fingers raised) | Pause / resume |
| Index finger + pinky | Take screenshot |
| Index finger + ring finger | Volume up |
| Thumbs up (other four fingers down) | Open Calculator |
| Thumbs down (other four fingers down) | Volume down |
| Pinky only | Open Notepad |

### Two-finger motion controls

The two-finger gesture has two behaviours:

- **Hold still:** after a short delay, GestureOS performs a right click.
- **Move vertically:** scroll up or down.
- **Move horizontally:** send a previous-slide or next-slide key press.

For slide navigation, open a presentation in an application that responds to the left and right arrow keys. Keep the two-finger gesture active while making a clear horizontal movement.

### Keyboard controls

- Press **Q** to exit.
- Press **Esc** to exit.

The camera preview window must be focused for these keyboard shortcuts to work.

## 5. How GestureOS works

GestureOS processes the webcam feed continuously. The main program coordinates the modules below:

1. **Camera capture:** OpenCV reads frames from the webcam and mirrors the image for a natural interaction experience.
2. **Hand tracking:** MediaPipe Hands detects a hand and provides landmark coordinates for the fingers and palm.
3. **Gesture recognition:** the recognition modules examine landmark positions and distances to identify a gesture.
4. **Stability check:** a gesture must remain consistent for several frames before it is accepted. This helps reduce accidental commands caused by momentary detection changes.
5. **Action execution:** PyAutoGUI performs the corresponding mouse, keyboard, screenshot, or volume action. Python subprocess launches the supported Windows utilities.
6. **Visual feedback:** the OpenCV window displays the tracked hand, detected gesture, action status, and whether the system is active or paused.

### How the recognition logic is built

The project uses MediaPipe's hand landmark model rather than training a custom machine-learning model. The landmarks provide normalised positions for key points on the hand.

The current recognition logic uses:

- The relative vertical positions of fingertip and finger-joint landmarks to estimate which fingers are raised.
- The distance between the thumb tip and index fingertip to detect a pinch.
- The thumb's position and extension to distinguish thumbs-up and thumbs-down gestures.
- The average position of selected palm landmarks to track hand movement for scrolling and slide navigation.
- Frame stability and cooldown timers to reduce repeated or accidental actions.

This is a rule-based gesture recogniser built on top of a pre-trained hand-tracking model. It is not a custom-trained gesture-classification neural network.

## 6. Project structure

```text
GestureOS/
├── src/
│   ├── __init__.py
│   ├── custom_commands.py       # Screenshots, volume, Calculator, Notepad
│   ├── custom_gestures.py      # Exhibition-specific gesture detection
│   ├── gesture_recognition.py  # Main finger and pinch recognition
│   ├── motion_controls.py      # Hand movement, scrolling, slide swipes
│   ├── mouse_control.py       # Cursor movement and mouse clicks
│   └── system_commands.py     # Scroll and presentation key commands
├── main.py                    # Camera loop and application coordinator
├── settings.py                 # Reserved placeholder; currently unused
├── requirements.txt            # Python dependencies
├── README.md
└── .gitignore
```

### What each important file does

- **main.py:** starts the webcam, runs MediaPipe, coordinates gesture detection, checks gesture stability, executes actions, and displays the camera interface.
- **src/gesture_recognition.py:** recognises the basic gestures such as cursor, pinch, two fingers, three fingers, and open palm.
- **src/custom_gestures.py:** detects the extra gestures used for exhibition commands.
- **src/mouse_control.py:** maps index-finger movement to screen coordinates and performs mouse clicks. It also applies cursor smoothing and click cooldown.
- **src/motion_controls.py:** tracks palm movement over time and decides whether the user intended to scroll or swipe.
- **src/custom_commands.py:** handles screenshots, volume changes, and launching Calculator or Notepad.
- **src/system_commands.py:** sends scroll and left/right arrow key commands.

## 7. Technology stack

| Technology | Role in the project |
| --- | --- |
| Python 3.12 | Main programming language |
| OpenCV | Webcam capture, image processing, and camera interface |
| MediaPipe | Real-time hand detection and landmark tracking |
| NumPy | Numerical dependency used by the computer-vision stack |
| PyAutoGUI | Mouse, keyboard, screenshot, and volume automation |

All Python dependencies are listed in [requirements.txt](requirements.txt).

## 8. Installation on Windows

The current exhibition edition is designed for **Windows 10 and Windows 11**. A working webcam is required.

### Step 1 — Install Python

Install **Python 3.12** from the official Python website:

https://www.python.org/downloads/

During installation, enable **Add Python to PATH** if the installer offers that option.

Check that Python is available. Open PowerShell and run:

```powershell
py -3.12 --version
```

You should see a Python 3.12 version number.

### Step 2 — Download the project

You can either download the repository as a ZIP from GitHub and extract it, or use Git.

**Option A — Git (recommended)**

Install Git if it is not already installed:

https://git-scm.com/downloads

Then open PowerShell in the folder where you want to keep the project and run:

```powershell
git clone https://github.com/farixhere/GestureOS.git
cd GestureOS
```

**Option B — Download ZIP**

1. Open https://github.com/farixhere/GestureOS
2. Select **Code → Download ZIP**.
3. Extract the ZIP file.
4. Open the extracted `GestureOS` folder in File Explorer.
5. Open PowerShell in that folder.

### Step 3 — Create a virtual environment

A virtual environment keeps this project's Python packages separate from other Python projects.

```powershell
py -3.12 -m venv .venv
```

### Step 4 — Activate the environment

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation because of the execution policy, you can activate it for the current PowerShell process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

This process-scoped setting does not permanently change the machine's execution policy.

### Step 5 — Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Wait for the packages to finish installing. MediaPipe and OpenCV may take a little time.

### Step 6 — Start GestureOS

Make sure the virtual environment is active and that your terminal is in the project folder. Run:

```powershell
python main.py
```

Allow camera access if Windows displays a permission prompt. The **GESTURE OS | Exhibition Edition** camera window should open.

### Step 7 — Test the gestures

Start with the index-finger cursor gesture. Then test a pinch, open palm, and the custom commands one at a time. Use the camera window's on-screen gesture and action labels to understand what GestureOS detects.

To close the program, focus the camera window and press **Q** or **Esc**.

## 9. Running GestureOS again later

You do not need to reinstall the dependencies every time.

1. Open PowerShell in the `GestureOS` folder.
2. Activate the virtual environment.
3. Run the application.

```powershell
.\.venv\Scripts\Activate.ps1
python main.py
```

If the environment is already active, you can simply run `python main.py`.

## 10. Preparing GestureOS for a college exhibition

A reliable demonstration is easier when the computer and camera are prepared before visitors arrive.

### Before the presentation

- Use a Windows laptop or desktop with Python 3.12 and the dependencies installed.
- Test the webcam and make sure Windows allows desktop applications to access it.
- Place the camera near eye level and keep the user's hand inside the camera frame.
- Use a well-lit area. Avoid strong backlighting and clutter behind the hand.
- Keep the mouse pointer away from important buttons before testing gestures.
- Open a presentation in PowerPoint or another application that responds to left/right arrow keys.
- Save any open work. GestureOS can send real mouse and keyboard input.
- Test every gesture once before the audience arrives.

### Suggested live demonstration

1. Run `python main.py` and introduce the live hand-tracking window.
2. Raise only the index finger and move the cursor around the screen.
3. Pinch the thumb and index finger to demonstrate a left click.
4. Raise two fingers and move your hand vertically to scroll a page.
5. Use a horizontal two-finger movement to navigate presentation slides.
6. Show the custom gestures: screenshot, Calculator, Notepad, and volume control.
7. Show the open-palm gesture to pause and resume the system.

**Exhibition tip:** demonstrate one gesture at a time and pause briefly between gestures. This makes the recognition and resulting action easier for the audience to follow.

## 11. How can GestureOS be useful?

GestureOS is currently an educational prototype, but it demonstrates ideas that can be useful in several areas.

### Accessibility research

Touch-free interaction can be worth exploring for people who find conventional mouse or keyboard interaction difficult. GestureOS is not yet an accessibility-certified product, and it should not be presented as a replacement for assistive technology.

### Touch-free environments

A gesture-controlled interface could be useful in situations where people want to avoid touching shared input devices, such as demonstrations, kiosks, or certain laboratory environments. The current project is a prototype and has not been validated for hygiene-critical settings.

### Presentations and teaching

A presenter can use hand movements to navigate slides and control a demonstration without standing next to the keyboard. This is one of the most straightforward uses to show during an exhibition.

### Learning computer vision

Students can explore how a camera feed becomes structured landmark data, how simple rules classify gestures, and how software turns those classifications into actions.

### Human-computer interaction experiments

GestureOS can serve as a starting point for experimenting with natural interfaces, gesture design, tracking stability, and feedback between people and computers.

## 12. Troubleshooting

| Problem | Things to check |
| --- | --- |
| Webcam unavailable | Close other apps using the camera, check Windows camera permissions, and verify that the webcam is connected |
| Camera window does not open | Confirm that OpenCV installed correctly and that the selected camera is available |
| `ModuleNotFoundError` | Activate `.venv` and run `pip install -r requirements.txt` again |
| Python version or package installation errors | Confirm that Python 3.12 is installed and that the virtual environment was created with `py -3.12` |
| Gestures are detected incorrectly | Improve lighting, keep the full hand visible, face the palm toward the camera, and avoid very fast movements |
| Cursor feels inaccurate | Keep the hand inside the central camera area and ensure the display resolution is detected correctly |
| Gesture triggers more than once | Hold the pose steadily and allow the cooldown to finish before repeating it |
| Calculator or Notepad does not open | Confirm that you are running the Windows edition of the project |
| Slide navigation does not work | Focus the presentation application and confirm that left/right arrow keys change slides |
| PowerShell will not activate the environment | Use the process-scoped execution-policy command in the installation section |

## 13. Safety, privacy, and limitations

GestureOS interacts with your desktop. Please use it carefully.

- **Mouse and keyboard control:** recognised gestures can move the pointer, click, scroll, or send keyboard commands. Save your work before testing.
- **Emergency stop:** PyAutoGUI's fail-safe is enabled. Moving the physical mouse pointer to the top-left corner of the screen triggers PyAutoGUI's fail-safe exception.
- **Normal exit:** press Q or Esc while the camera window is focused.
- **Pause:** use the open-palm gesture to pause or resume gesture actions.
- **Camera:** the program requires webcam access for live hand tracking. The current code does not upload camera frames to a cloud service.
- **Lighting and camera quality:** detection accuracy depends on lighting, camera quality, hand visibility, and distance.
- **Gesture scope:** the project recognises a defined set of gestures; it does not translate sign language or understand arbitrary gestures.
- **Platform:** the current command implementations target Windows. Other operating systems are not supported by this exhibition edition.
- **Prototype status:** this project is intended for learning and demonstration, not safety-critical or unattended control.

## 14. Current project status and possible future improvements

The current repository contains a working exhibition-oriented prototype with webcam hand tracking, rule-based gesture recognition, cursor control, mouse actions, motion controls, and selected Windows commands.

Possible future improvements include:

- User-configurable gesture mappings and sensitivity settings.
- Better calibration for different screen sizes and camera positions.
- A more accessible visual interface and guided onboarding.
- Support for additional operating systems.
- More robust gesture classification and personal calibration.
- A configurable gesture set for presentations and other workflows.

These are ideas for future development, not features that should be assumed to exist in the current version.

## 15. Contributing

Suggestions, bug reports, and improvements are welcome.

1. Fork the repository.
2. Create a branch for your change.
3. Make and test your changes on a Windows machine with a webcam.
4. Open a pull request describing what changed and how it was tested.

Please keep desktop-control actions clear and predictable when adding new gestures.

## 16. Project information

- **Project:** GestureOS
- **Edition:** Exhibition Edition
- **Repository:** https://github.com/farixhere/GestureOS
- **Primary language:** Python
- **Core technologies:** OpenCV, MediaPipe, PyAutoGUI

---

<p align="center">
  <strong>GestureOS — Your hands are the controller.</strong>
  <br />
  Built to explore a more natural way to interact with computers.
</p>
