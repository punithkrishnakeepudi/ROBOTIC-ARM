# 🤖 6-DOF Robotic Arm: Physical-Digital Mirror

A state-of-the-art **6-Degree of Freedom (DOF) Robotic Arm** system that merges physical hardware with a high-fidelity **Webots Digital Twin**. This project enables real-time synchronization between a physical arm (controlled via NodeMCU) and its simulated counterpart using low-latency UDP broadcasting.

![Project Preview](./Screenshot%20from%202026-02-22%2009-38-14.png)

---

## 🌟 Key Features

- **🔗 Real-Time Mirroring**: Synchronized movement between physical hardware and the Webots simulation.
- **📶 Low-Latency UDP**: Custom UDP protocol ensures near-instant command delivery (4210 port).
- **✋ Hand Gesture Control**: Control the arm intuitively using computer vision (MediaPipe & OpenCV).
- **🌐 Web-Based UI**: Built-in dashboard hosted on the NodeMCU Access Point for manual control.
- **🌊 Smooth Motion**: Smart interpolation logic on the ESP8266 for fluid servo transformations.
- **🏗️ 6-DOF Support**: Full control over Base, Shoulder, Elbow, Wrist (Pitch/Roll), and Gripper.

---

## 🛠️ Tech Stack

- **Firmware:** ESP8266 (NodeMCU) / C++
- **Simulation:** [Webots](https://cyberbotics.com/) Digital Twin
- **AI/Vision:** Python, OpenCV, MediaPipe
- **Networking:** UDP (User Datagram Protocol)
- **Frontend:** Vanilla HTML/JS (Embedded in Firmware)

---

## 📂 Project Structure

| File | Description |
| :--- | :--- |
| `node-mcu.txt` | C++ firmware for the ESP8266 (Servo control, Web Server & UDP receiver). |
| `arm-webots-controller.py` | Python controller for the Webots simulation. |
| `robotic-arm-webots.wbt` | The 3D world/simulation environment in Webots. |
| `open-cv.py` | Vision-based control using hand tracking. |

---

## 🚀 Getting Started

### 1. Hardware Setup (Physical)

- **Microcontroller**: ESP8266 (NodeMCU).
- **Servos**: 6x Standard servos connected to pins `D0` to `D5`.
- **Power**: External 5V/3A power supply recommended for servos.
- **Firmware**: Upload the code in `node-mcu.txt` to your ESP8266 via Arduino IDE.

### 2. Simulation (Digital)

1. Open `robotic-arm-webots.wbt` in the **Webots** simulator.
2. Ensure the robot's controller is set to `arm-webots-controller.py`.
3. The simulation will listen for UDP packets on port `4210`.

### 3. Hand Gesture Control (Optional)

Run the OpenCV script to control the arm using your hand:

```bash
pip install opencv-python mediapipe numpy
python open-cv.py
```

---

## 📶 Network Configuration

- **SSID**: `RobotArm_AP`
- **Password**: `12345678`
- **Default IP**: `192.168.4.1`
- **UDP Port**: `4210`

---

## 📜 Control Protocol

Commands are sent as short strings to minimize bandwidth:

- Format: `S[ID]:[ANGLE]`
- Example: `S0:90` (Base to 90°), `S5:180` (Gripper OPEN).

---

## 🤝 Contributing

Feel free to fork this project and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

