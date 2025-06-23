# 🚀 Missile Detection Over RTSP (Beta 0.2) Phase 1

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
  Stream and analyze live video feeds directly from RTSP cameras.

- 📼 **Offline video analysis mode**  
  Test and debug detection algorithms using local video files.

- 💡 **Brightness anomaly detection**  
  Identify sudden flashes or explosions by monitoring frame brightness and adaptive thresholds.

- 🎧 **Audio spike detection**  
  Detect explosion-like events using audio volume and spectral energy analysis with `ffmpeg` and `numpy`.

- 🧠 **AI-enhanced image verification**  
  Use OpenAI Vision (GPT-4o) to verify and classify suspect frames for higher accuracy.

- 📁 **Automatic logging**  
  Log all detection events and save flagged frames with precise timestamps for later review.

- ⚠️ **Threaded audio and video processing**  
  Ensure smooth, real-time monitoring by running audio and video analysis in parallel threads.

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

1. **Video Source**: Reads either from an RTSP stream or a local video file for flexible deployment and testing.
2. **Image Analysis**: Continuously monitors video frames for sudden brightness spikes, which may indicate missile launches, flares, or explosions.
3. **Audio Analysis**: Listens for loud noises and explosion-like audio spikes using real-time audio decoding and spectral analysis via `ffmpeg` and `numpy`.
4. **AI Verification**: Sends suspected frames to GPT-4o with the visual prompt:  
   _"Is there a missile or rocket in this night sky image?"_  
   This step reduces false positives by leveraging advanced AI vision capabilities.
5. **Alerting & Logging**: Flags and saves confirmed images, activates the alert function, and logs all detection events with detailed evidence for later review.

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
Version: beta 0.2
```
MissileDetectionRTSP/
├── main.py                # Main detection script | currently extremely beta, heavy dependence on ai models.
├── CamSnppits.py          # Saves random camera snippets from the RTSP source, used for advanced independent testing and fine-tuning.
├── /Tests/                # For manually storing test results and metadata.
├── /Flaged/               # Saved flagged image frames by the system.
├── /AlertSystem/          # The ESP32 Framework for outputting real-time alerts.
├── detection_log.jsonl    # logs with timestamps.
├── graph_spike.py         # simulates audio spikes and place them into a graph for more readable data
├── graph_thershold.py     # simulates audio thereshold in accordance to the video and place them into a graph for more readable data
└── token.env
```


---

## 📦 Previous versions

[<a href="https://github.com/RaziFalah/MissileDetectionOverRTSP/releases/tag/beta0.0phase1"> - **BETA 0.0 PHASE 1** </a>](https://github.com/RaziFalah/MissileDetectionOverRTSP/tree/beta0.0phase1)

