# 🚀 Missile Detection Over RTSP (Beta 0.0) Phase 1

A real-time missile/rocket detection system using RTSP streams or video files. This project combines image analysis, audio signal processing, and OpenAI's GPT-4o vision capabilities to detect potential missile launches or explosions.

---

## 🧪 Development Phase

<p>This project is currently in Beta 0.0 (Phase 1) and is not intended for practical use. The system serves purely as a simulation to test the feasibility of using brightness spike detection, audio spike detection, and AI-based visual verification for identifying potential missile events.

The goal of Phase 1 is to gather meaningful test data under various conditions (e.g., different lighting, angles, explosion types) as outlined in /Tests/structure.md. This phase focuses on validating whether these detection methods show any promise in real-world-like scenarios.

Once sufficient testing and evaluation are completed, the project will transition to Phase 2 (Beta 1.0), where more advanced or alternative detection techniques will be explored and implemented.
</p>
---


---

## 🔍 Key Features

- 🎥 **Real-time RTSP camera support**  
- 📼 **Offline video analysis mode** for testing purposes  
- 💡 **Brightness anomaly detection** for identifying flashes/explosions  
- 🎧 **Audio spike detection** using `ffmpeg` and `numpy`  
- 🧠 **AI-enhanced image verification** via OpenAI Vision (GPT-4o)  
- 📁 **Automatic logging** of flagged frames with timestamped image storage  
- ⚠️ **Threaded audio and video processing** for live monitoring  

---


## 🚧 Limitations & Notes

❗ Beta mode – Not production-ready.

- **False positives/negatives possible due to visual/audio anomalies.**

- **AI detection limited to the accuracy and prompt of OpenAI's model.**

- **Designed for night-time visuals; however, RTSP and Local videos are converted to infrared modes for better accuracy.**
Project showing real promise, however, it's important to note that this system (beta 0.0) is highly un-reliable in the meantime and exists to explore potential approaches and techniques for detection under challenging conditions.

---

## 🔐 Security Disclaimer
This project is for experimental and educational purposes only and is not intended for use in critical or sensitive defense systems.

While the system integrates AI and audio/visual analysis, it has no guarantees of accuracy, robustness, or reliability. It should not be relied upon for real-world safety or military applications without significant additional validation, encryption, and security hardening.

<h3>If integrating into any networked or monitored system:</h3>

- **Ensure API keys are kept secret (do not hardcode them in public repositories).**
- **Validate and sanitize any RTSP input sources.**
- **All image and audio analysis are processed locally, except for flagged frames sent to OpenAI for classification — which is subject to <a href="https://openai.com/policies/terms-of-use/" target="_blank">OpenAI’s API Terms of Use.</a>**
<br>
If you discover any potential issue regarding OPENAI violations or misuse in the code, please report it privately via email instead of creating a public GitHub issue.<br>
The developer take no responsibility for any damage, data loss, misuse, or unintended behavior caused by this software, whether directly or indirectly.<br>

**Do not use this system in any real-world defense, surveillance, or emergency response context. If you wish to try the system, please consider testing it with accordance to the test structure and upload the results. Thank you in advance.---**

## ⚙️ How It Works

1. **Video Source**: Reads either from RTSP stream or a local video file.
2. **Image Analysis**: Detects sudden brightness spikes (e.g., missile flares or explosions).
3. **Audio Analysis**: Listens for loud noises (e.g., explosions) using real-time audio decoding via `ffmpeg`.
4. **AI Verification**: Sends suspected frames to GPT-4o with a visual prompt:  
   _"Is there a missile or rocket in this night sky image?"_
5. **Alerting & Logging**: Flags confirmed images, activates alert function, and saves evidence.

---

## 🛠️ Installation

Clone the repo:

```bash
git clone https://github.com/yourusername/MissileDetectionRTSP.git
cd MissileDetectionRTSP
```
---

## 🧩 Dependencies

```
pip install opencv-python numpy requests

```
For linux
```
sudo apt install ffmpeg
```

---

## 🧪 Test Result Template

For each test run, create a file in the `/Tests/` folder using the following format:

### 🧾 Test Report Structure

- **Tested video/audio**: `[Path to test media files]`
- **Goal**: `[The objective of this test]`
- **Type**: `[Missile type — e.g., Ground hit / Air explosion / Dud (no explosion)]`
- **Expected outcome**:  
  - `Brightness function`: `[Expected brightness detection behavior]`  
  - `Audio function`: `[Expected sound detection behavior]`  
  - `OpenAI`: `[Expected AI response]`
- **Actual outcome**: `[What the program actually did during this run]`
- **Program logs**:  
  ```text
  [Terminal/console output here]

- **Flaged Image(s)**: `[IMAGES THAT WAS FLAGED AND STORED IN /Flaged (FILE NUMBER ONLY)]`
- **positives detections**: `[HOW MANY TIMES THE PROGRAM DETECTED CORRECTLY]`
- **False positive detections**: `[HOW MANY TIMES DID THE PROGRAM DETECTED INCOORECTLY]`
- **Success rate**: `[(10(in case of correct return based on incorrect assumptions) + (POSITIVE DETECTIONS/FALSE POSITIVE DETECTIONS) * 100%) * 100]`
- **Additional details**: `[ANY EXTRA INFO WORTH MENTIONING]`

---

## 📂 Project Structure
Version: beta 0.0
```
MissileDetectionRTSP/
├── main.py                # Main detection script | currently extremely beta, heavy dependence on ai models.
├── CamSnppits.py          # Saves random camera snippets from the RTSP source, used for advanced independent testing and fine-tuning.
├── /Tests/                # For manually storing test results and metadata.
├── /Flaged/               # Saved flagged image frames by the system.
└── /AlertSystem/          # The ESP32 Framework for outputting real-time alerts.
```


---
