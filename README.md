# AirInk 🚀
### AI-Powered Air Drawing & Gesture-Controlled Digital Canvas

AirInk is a real-time computer vision application that transforms hand movements into digital drawings using a webcam. Powered by MediaPipe and OpenCV, it enables users to draw in the air using their index finger, switch colors with gestures, clear the canvas, and interact naturally without touching any physical device.

---

# ✨ Features

## 🎨 Air Drawing
Draw on a virtual canvas using only your index finger.

## 🖐️ Real-Time Hand Tracking
Tracks hand landmarks in real time using MediaPipe Hands.

## 🌈 Gesture-Based Color Switching
Change drawing colors using a pinch gesture (thumb + index finger).

## 🧹 Gesture-Based Canvas Clearing
Clear the canvas instantly using a fist gesture.

## 🔢 Finger Counter
Displays the number of fingers detected in real time.

## ✏️ Smooth Stroke Rendering
Uses stroke smoothing algorithms to create fluid and natural-looking lines.

## 🎯 Hand Skeleton Visualization
Displays a professional hand skeleton overlay with:
- White hand connections
- Red landmark joints

## ⚡ Low Latency Performance
Optimized for real-time responsiveness and smooth interaction.

---

# 🛠️ Tech Stack

### Programming Language
- Python 3.11+

### Libraries Used
- OpenCV
- MediaPipe
- NumPy

### Computer Vision
- MediaPipe Hands
- Real-time Hand Landmark Detection
- Gesture Recognition

---

# 📂 Project Structure

```text
AirInk/
│
├── main.py
├── README.md
├── requirements.txt
│
├── assets/
│   ├── screenshots/
│   └── demo.gif
│
└── venv/
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AirInk.git
cd AirInk
```

## 2. Create Virtual Environment

### macOS / Linux

```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## 3. Install Dependencies

```bash
pip install --upgrade pip
pip install numpy
pip install opencv-python
pip install mediapipe==0.10.14
```

---

# ▶️ Running the Project

Start AirInk:

```bash
python main.py
```

Press **ESC** to exit the application.

---

# 🎮 Controls

| Gesture | Action |
|----------|----------|
| ☝️ Index Finger | Draw |
| 🤏 Thumb + Index Pinch | Change Color |
| ✊ Fist | Clear Canvas |
| ESC Key | Exit Application |

---

# 🧠 How It Works

## Hand Tracking
MediaPipe detects 21 hand landmarks from the webcam feed.

## Gesture Recognition
Specific landmark relationships are analyzed to identify gestures such as:

- Index finger drawing
- Pinch detection
- Fist detection
- Finger counting

## Drawing Engine
The index finger tip position is continuously tracked and rendered onto a virtual canvas using OpenCV.

## Stroke Smoothing
Drawing coordinates are filtered and smoothed to produce cleaner and more natural strokes.

---

# 📸 Screenshots

## Main Interface

![AirInk Interface](assets/screenshots/interface.png)

## Drawing Example

![AirInk Drawing](assets/screenshots/drawing.png)

---

# 💡 Future Enhancements

### Planned Features

- Multi-hand support
- Gesture-based Undo / Redo
- Save drawing as image
- Brush thickness control
- AI shape recognition
- Virtual color palette
- Text recognition from air writing
- Collaborative drawing mode
- AR-based drawing environment

---

# 📈 Performance

| Metric | Value |
|----------|----------|
| FPS | 25–60 |
| Detection Latency | Real-Time |
| Tracking Model | MediaPipe Hands |
| Supported Hands | 1 |
| Drawing Method | Air Gesture |

---

# 🎓 Learning Outcomes

This project demonstrates practical implementation of:

- Computer Vision
- Human-Computer Interaction
- Real-Time Gesture Recognition
- OpenCV Applications
- MediaPipe Hand Tracking
- Interactive UI Development

---

# 🤝 Contributing

Contributions, feature requests, and suggestions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a pull request

---

# 📜 License

This project is released under the MIT License.

---

# 👨‍💻 Author

**Anmol Shukla**

AirInk was developed as a computer vision and gesture interaction project to explore intuitive, touchless digital drawing experiences.

---

## ⭐ If you found this project useful, consider giving it a star on GitHub!