# AirInk 🚀
### AI-Powered Air Drawing Using Hand Gestures

AirInk is a real-time computer vision application that allows users to draw in the air using hand gestures captured through a webcam. Powered by MediaPipe and OpenCV, AirInk transforms hand movements into smooth digital strokes, creating a touchless drawing experience.

---

## ✨ Features

### 🎨 Air Drawing
Draw naturally in the air using your index finger.

### 🌈 Gesture-Based Color Switching
Change brush colors using a pinch gesture.

### 🧹 Canvas Clearing
Clear the canvas instantly using a fist gesture.

### 🔢 Real-Time Finger Counter
Displays the number of fingers currently detected.

### ✏️ Smooth Stroke Rendering
Uses stroke stabilization and smoothing for cleaner lines.

### 🖐️ Hand Skeleton Tracking
Visualizes hand landmarks and finger joints in real time.

### ⚡ Real-Time Performance
Optimized for low latency and smooth interaction.

---

## 🛠️ Technologies Used

- Python 3.11
- OpenCV
- MediaPipe
- NumPy

---

## 📂 Project Structure

```text
AirInk/
│
├── venv/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── main.py
├── config.py
│
├── gesture_utils.py
├── shape_utils.py
├── text_utils.py
├── ui_utils.py
├── smoothing.py
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/AirInk.git
cd AirInk
```

### 2. Create a Virtual Environment

#### macOS / Linux

```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run AirInk

```bash
python main.py
```

Press **ESC** to exit the application.

---

## 🎮 Controls

| Gesture | Action |
|----------|----------|
| ☝️ Index Finger | Draw |
| 🤏 Thumb + Index Pinch | Change Color |
| ✊ Fist | Clear Canvas |
| ESC | Exit Application |

---

## 🧠 How It Works

### Hand Tracking
MediaPipe detects and tracks 21 hand landmarks from the webcam feed.

### Gesture Recognition
Custom gesture logic is used to identify:

- Drawing gesture
- Pinch gesture
- Fist gesture
- Finger count

### Stroke Rendering
The index finger tip coordinates are continuously tracked and rendered onto a virtual canvas.

### Smoothing Engine
Stroke stabilization reduces jitter and produces cleaner, more natural-looking lines.

---

## 📈 Performance

| Metric | Value |
|----------|----------|
| FPS | 25–60 |
| Tracking | Real-Time |
| Model | MediaPipe Hands |
| Drawing Mode | Air Gesture |
| Supported Hands | 1 |

---

## 📚 Learning Outcomes

This project demonstrates:

- Computer Vision
- Hand Tracking
- Gesture Recognition
- Human Computer Interaction
- Real-Time Video Processing
- OpenCV Applications
- MediaPipe Integration

---

## 🔮 Future Enhancements

- Multi-hand support
- Undo / Redo gestures
- Brush size control
- Save drawings as images
- Gesture customization
- AI-powered shape recognition improvements
- Air handwriting recognition
- AR drawing environment

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Anmol Shukla**

AirInk was built as a computer vision project exploring intuitive, touchless digital drawing experiences through hand gesture interaction.

---

### ⭐ If you found this project useful, consider giving it a star on GitHub!