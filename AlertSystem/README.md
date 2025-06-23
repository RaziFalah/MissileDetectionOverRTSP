# 🔔 /AlertSystem – ESP32 Alert System

This folder contains the firmware and logic responsible for **activating real-world alerts** using an ESP32 microcontroller.

---

## 📡 Purpose

The ESP32-based system functions as a **physical alert module**. It activates audible and visual warnings in real time under the following conditions:

### 1. ⚠️ Missile Detected by Program
When the main missile detection software (in `main.py`) confirms a threat via:
- Brightness spike detection  
- Audio anomaly detection  
- Positive confirmation by OpenAI GPT-4o  

It sends a signal to the ESP32 to activate connected alert components.

### 2. 🛰️ Incoming Missile Alert from Official API
The ESP32 can also fetch or receive real-time threat alerts directly from **official government/public APIs** (e.g., national early-warning systems for missile attacks). This allows the ESP32 to trigger alerts even **independently of the local video/audio detection system**.

---

## 🚨 Output Devices Controlled

- **LED(s)**: Used to provide a visual warning signal.
- **Speaker / Buzzer**: Emits an audible a
