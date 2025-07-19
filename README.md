# EYE/O 👁🎮  
**Vision-Based Game Controller for Hands-Free Interaction**

**EYE/O** is a computer vision-powered input system designed to allow users—especially those with limited mobility—to control games or applications using **eye blinks** and **facial/head movements**. Built using Python, the system maps real-time facial gestures to keyboard inputs, enabling an intuitive, hands-free experience.

This project was developed as part of a 14-hour hackathon by a team of two—**Haziq Baba** and **Sheikh Daaim**—with a mission to explore the potential of AI-driven accessibility tools.

---

## 🚀 Features

- **Blink-to-Click**: Detects double/single blinks to simulate a keyboard "Enter" or action key.
- **Head Movement Detection**: Maps directional head gestures (left, right, up, down) to WASD or arrow key inputs.
- **No Wearables Required**: Runs on any standard webcam.
- **Cross-Platform**: Pure Python implementation—can be run on any system with Python and OpenCV.


---

## 🔧 Libraries Used

- MediaPipe
- OpenCV
- NumPy
- pynput

---

## 💡 Motivation

Traditional game controllers and keyboards are not accessible to everyone, especially people with upper limb disablities. **EYE/O** aims to redefine human-computer interaction by leveraging natural, vision-based input—making gaming and digital navigation more inclusive and empowering.

---

## 🛠 How It Works

1. **Face and Eye Landmark Detection** via MediaPipe.
2. **Eye Blink Detection** using eye aspect ratio.
3. **Head Direction Inference** by tracking nose positions.
4. **Action Mapping**: Gestures are mapped to specific keypress events in real time.

---

## 🖥 Demo

<!-- Insert a GIF or link to a demo video here -->
*(Demo video coming soon)*


---

## 👥 Authors

- [**Haziq Baba**](https://github.com/HaziqBaba7)
- [**Sheikh Daaim**](https://github.com/picine143)

---
