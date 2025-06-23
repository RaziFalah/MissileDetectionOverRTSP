# Change Log for MissileDetectionOverRTSP version beta 0.2 phase 1

## 1. Visualization & Analysis Scripts

### detection_logs.py
- **Added a script to parse and visualize detection logs.**
  - Parses `video_suspect` events from log data.
  - Extracts and plots `brightness`, `adaptive_threshold`, and `motion_score` over time.
  - Helps visually inspect detection logic and event consistency.

<image src="https://github.com/RaziFalah/MissileDetectionOverRTSP/blob/main/images/graph_thershold.png?raw=true"></image>

## 2. Main Detection Logic

### main.py
- **Logging Improvements**
  - All detection and AI analysis events are logged to `detection_log.jsonl` with timestamps and details.
  - Added `log_event()` function for consistent event logging.
 



- **Updated AI Analysis Integration**
  - Added `analyze_image_with_openai()` to send suspect frames to OpenAI's API for further analysis.
  - Results (true/false positive) are logged and flagged frames are saved.

- **Updated Audio Explosion Detection**
  - Updated `listen_rtsp_audio()` function to analyze audio stream for explosion-like spikes using rolling mean, std, and FFT spectral energy.
  - Triggers alert and logs `audio_explosion` events when spikes are detected.

<image src="https://github.com/RaziFalah/MissileDetectionOverRTSP/blob/main/images/GraphTestVideoOf7Exp.png?raw=true"></image>
This graph is the results of a video containing 6 explosions, the program detected 7 explosions when the program was set on thershold mode (above 0.0020) and 5 when it was set on spike detection.

- **Video Motion & Brightness Detection**
  - Uses adaptive thresholding (rolling mean + 2*std) for brightness spike detection.
  - Uses frame differencing for motion detection.
  - Triggers AI analysis only when both brightness and motion spikes persist for multiple frames.

- **Multithreading**
  - AI analysis runs in a background worker thread to avoid blocking the main video/audio loop.
  - Audio analysis runs in a separate thread.

- **Alerting**
  - Alerts are printed and logged when missile/rocket is detected by either audio or video logic.

## 3. General Improvements

- **Consistent Use of Timestamps**
  - All events use ISO format timestamps for easier tracking and analysis.

- **Parameterization**
  - Paths, thresholds, and other parameters are easy to adjust at the top of the script.

---

**Summary:**  
The project now includes robust logging, visualization tools, AI-based frame analysis, and both video and audio-based detection with clear separation of concerns and multithreaded processing.
