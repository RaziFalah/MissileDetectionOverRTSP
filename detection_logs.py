# You can copy-paste this into a new file, e.g., plot_detection_log.py

import matplotlib.pyplot as plt
import json
from datetime import datetime

# Paste your log lines here as a multiline string
log_data = """
{"timestamp": "2025-06-23T19:04:56.562756", "event_type": "video_suspect", "details": {"brightness": 118.9455685763889, "adaptive_threshold": 116.40715017121349, "motion_score": 0.02956510416666667}}
{"timestamp": "2025-06-23T19:05:04.549204", "event_type": "video_suspect", "details": {"brightness": 130.17023871527778, "adaptive_threshold": 127.68549103144878, "motion_score": 0.0195234375}}
{"timestamp": "2025-06-23T19:05:08.348145", "event_type": "video_suspect", "details": {"brightness": 130.2086111111111, "adaptive_threshold": 129.13556236666327, "motion_score": 0.019515625}}
{"timestamp": "2025-06-23T19:06:56.740737", "event_type": "video_suspect", "details": {"brightness": 136.33753472222222, "adaptive_threshold": 134.48401318221582, "motion_score": 0.4695763888888889}}
{"timestamp": "2025-06-23T19:06:58.334579", "event_type": "video_suspect", "details": {"brightness": 139.37384548611112, "adaptive_threshold": 138.93131962536253, "motion_score": 0.2976302083333333}}
{"timestamp": "2025-06-23T19:06:59.827327", "event_type": "video_suspect", "details": {"brightness": 194.37078993055556, "adaptive_threshold": 189.25343421155102, "motion_score": 0.3043958333333333}}
{"timestamp": "2025-06-23T19:07:05.114029", "event_type": "video_suspect", "details": {"brightness": 217.9737673611111, "adaptive_threshold": 202.01590631145953, "motion_score": 0.3806788194444445}}
{"timestamp": "2025-06-23T19:10:05.981067", "event_type": "video_suspect", "details": {"brightness": 136.33753472222222, "adaptive_threshold": 134.48401318221582, "motion_score": 0.4695763888888889, "timestamp": "2025-06-23 19:10:05"}}
{"timestamp": "2025-06-23T19:10:06.099483", "event_type": "video_suspect", "details": {"brightness": 139.37384548611112, "adaptive_threshold": 138.93131962536253, "motion_score": 0.2976302083333333, "timestamp": "2025-06-23 19:10:06"}}
{"timestamp": "2025-06-23T19:10:06.685256", "event_type": "video_suspect", "details": {"brightness": 194.37078993055556, "adaptive_threshold": 189.25343421155102, "motion_score": 0.3043958333333333, "timestamp": "2025-06-23 19:10:06"}}
{"timestamp": "2025-06-23T19:10:06.697088", "event_type": "video_suspect", "details": {"brightness": 217.9737673611111, "adaptive_threshold": 202.01590631145953, "motion_score": 0.3806788194444445, "timestamp": "2025-06-23 19:10:06"}}
"""

# Parse log lines
timestamps = []
brightness = []
adaptive_threshold = []
motion_score = []

for line in log_data.strip().split('\n'):
    entry = json.loads(line)
    if entry["event_type"] == "video_suspect":
        ts = entry["timestamp"]
        # Use the details timestamp if available (for more precise event time)
        if "timestamp" in entry["details"]:
            ts = entry["details"]["timestamp"]
        timestamps.append(datetime.fromisoformat(ts.replace(" ", "T")))
        brightness.append(entry["details"]["brightness"])
        adaptive_threshold.append(entry["details"]["adaptive_threshold"])
        motion_score.append(entry["details"]["motion_score"])

plt.figure(figsize=(12, 6))
plt.plot(timestamps, brightness, label="Brightness", marker='o')
plt.plot(timestamps, adaptive_threshold, label="Adaptive Threshold", marker='x')
plt.plot(timestamps, motion_score, label="Motion Score", marker='s')
plt.xlabel("Time")
plt.ylabel("Value")
plt.title("Brightness, Adaptive Threshold, and Motion Score Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()