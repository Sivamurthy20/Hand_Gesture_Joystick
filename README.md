# 🖐️ Hand Gesture Joystick Controller

Control your favorite games like Temple Run using just your hand gestures!

## 🎮 Features
- Tracks hand with webcam using **MediaPipe**
- Draws a circular "joystick" on screen:
  - Inner circle = neutral zone
  - Outer direction = WASD keys
- Sends `W`, `A`, `S`, `D` key presses via **PyAutoGUI**
- Cooldown to prevent key spam

## 📷 How It Works
- Captures webcam using `cv2.VideoCapture`
- Tracks index finger tip (Landmark 8)
- Calculates distance & angle from center
- Converts to:
  - 🔼 Up = W
  - 🔽 Down = S
  - ◀️ Left = A
  - ▶️ Right = D

## 🛠 Requirements
```bash
pip install -r requirements.txt
