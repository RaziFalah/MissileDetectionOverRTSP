import cv2
import numpy as np
import datetime
import os
import time
import requests
import base64
from collections import deque
import threading
import subprocess
import json
from queue import Queue

USE_VIDEO_FILE = True
rtsp_url = ""
video_path = ""  # Set if using a local video file

LOG_PATH = "detection_log.jsonl"
FLAGGED_PATH = "/home/razi/Desktop/repos/MissileDetectionOverRTSP/Flaged"

def log_event(event_type, details):
    event = {
        "timestamp": datetime.datetime.now().isoformat(),
        "event_type": event_type,
        "details": details
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(event) + "\n")

def send_alert():
    print("\033[91mMissile/rocket detected! Sending alert...\033[0m")
    log_event("alert_sent", {"message": "Missile/rocket detected!"})
    # Extend with your alerting mechanism

def analyze_image_with_openai(
    image,
    prompt="Do you see any evdence of a missile or rocket in this image? Please look for any sings of ground / sky impact or even a missile appears to be flying Please answer with 'yes' or 'no' and try to minimize false positives.",
    save_flagged_path=FLAGGED_PATH
):
    # In-memory encoding
    _, img_encoded = cv2.imencode('.jpg', image)
    img_bytes = img_encoded.tobytes()
    img_b64 = base64.b64encode(img_bytes).decode()

    api_key = ""
    # For production, use: api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("FATAL ERROR: API KEY?")
        exit()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}}
                ]
            }
        ],
        "max_tokens": 10
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )

    flagged = False
    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"].strip().lower()
        print(f"OpenAI API response: {answer}")
        if "yes" in answer:
            flagged = True
            if save_flagged_path:
                os.makedirs(save_flagged_path, exist_ok=True)
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                save_path = os.path.join(save_flagged_path, f"flagged_{ts}.jpg")
                cv2.imwrite(save_path, image)
        log_event("ai_analysis", {"answer": answer, "flagged": flagged})
        return flagged
    else:
        print(f"OpenAI API error: {response.status_code} {response.text}")
        log_event("ai_error", {"status_code": response.status_code, "text": response.text})
        return False
def listen_rtsp_audio(input_source, chunk_duration=1, samplerate=16000):
    """
    Listen to RTSP or video file audio and trigger alert if explosion-like sound detected.
    Uses spike detection (rolling mean + std) and spectral analysis (FFT).
    """
    ffmpeg_cmd = [
        'ffmpeg',
        '-i', input_source,
        '-vn',
        '-acodec', 'pcm_s16le',
        '-ar', str(samplerate),
        '-ac', '1',
        '-f', 's16le',
        '-'
    ]
    process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    bytes_per_sample = 2  # 16 bits = 2 bytes
    chunk_size = samplerate * bytes_per_sample * chunk_duration
    window_size = 5
    spike_factor = 0.5  # Number of std deviations above mean to consider a spike
    rolling_volumes = deque(maxlen=window_size)

    print("Listening for explosions in audio...")
    audio_time = 0.0
    try:
        while True:
            audio_chunk = process.stdout.read(chunk_size)
            print(f"[{audio_time:.1f}s] Received audio chunk of size: {len(audio_chunk)} bytes")
            if len(audio_chunk) < chunk_size:
                print("Audio stream ended or not enough data.")
                break
            audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0

            volume = np.linalg.norm(audio_np) / len(audio_np)
            print(f"[{audio_time:.1f}s] Audio volume: {volume:.4f}")

            fft = np.fft.fft(audio_np)
            fft_magnitude = np.abs(fft)[:len(fft)//2]
            spectral_energy = np.sum(fft_magnitude)

            # Spike detection using rolling mean and std
            rolling_volumes.append(volume)
            if len(rolling_volumes) == window_size:
                mean = np.mean(rolling_volumes)
                std = np.std(rolling_volumes)
                if std > 0 and volume > mean + spike_factor * std and spectral_energy > 100:
                    print(f"[{audio_time:.1f}s] Spike detected! Volume: {volume:.4f} (mean: {mean:.4f}, std: {std:.4f})")
                    log_event("audio_explosion", {
                        "audio_time": audio_time,
                        "volume": float(volume),
                        "mean": float(mean),
                        "std": float(std),
                        "spectral_energy": float(spectral_energy)
                    })
                    send_alert()

            if USE_VIDEO_FILE:
                time.sleep(chunk_duration)
            audio_time += chunk_duration
    except KeyboardInterrupt:
        print("Audio listening interrupted.")
    finally:
        process.terminate()

# --- AI Worker Thread ---
ai_queue = Queue()

def ai_worker():
    while True:
        item = ai_queue.get()
        if item is None:
            break
        frame, event_info = item
        if analyze_image_with_openai(frame):
            print("[True] AI analysis: Missile/rocket detected!")
            log_event("ai_true_positive", event_info)
            send_alert()
        else:
            print("[False] AI analysis: No missile/rocket detected.")
            log_event("ai_false_positive", event_info)
        ai_queue.task_done()

# Start AI worker thread
threading.Thread(target=ai_worker, daemon=True).start()

if USE_VIDEO_FILE:
    cap = cv2.VideoCapture(video_path)
    audio_source = video_path
else:
    cap = cv2.VideoCapture(rtsp_url)
    audio_source = rtsp_url

print("Starting video and audio processing...")

# Start audio listening in a background thread
audio_thread = threading.Thread(target=listen_rtsp_audio, args=(audio_source,), daemon=True)
audio_thread.start()

if not cap.isOpened():
    print("Cannot connect to camera")
else:
    prev_frame = None
    prev_brightness = None
    spike_frames = 0
    rolling_window = deque(maxlen=30)  # Larger window for adaptive threshold
    motion_window = deque(maxlen=5)
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame or stream ended")
                break

            resized_frame = cv2.resize(frame, (640, 360))
            gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(gray)

            # Adaptive threshold: use rolling mean and std
            mean_brightness = np.mean(enhanced)
            rolling_window.append(mean_brightness)
            adaptive_threshold = np.mean(rolling_window) + 2 * np.std(rolling_window)

            # Motion detection (frame differencing)
            motion_score = 0
            if prev_frame is not None:
                frame_diff = cv2.absdiff(enhanced, prev_frame)
                motion_score = np.sum(frame_diff > 25) / frame_diff.size  # Fraction of changed pixels
                motion_window.append(motion_score)
            else:
                motion_window.append(0)

            # Combine adaptive brightness spike and motion
            brightness_spike = mean_brightness > adaptive_threshold
            motion_detected = np.mean(motion_window) > 0.01  # Tune as needed

            if brightness_spike and motion_detected:
                spike_frames += 1
            else:
                spike_frames = 0

            if spike_frames >= 2:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{timestamp}] [Suspecting explosion] Persistent brightness spike + motion detected! Requesting AI analysis...")
                event_info = {
                    "brightness": float(mean_brightness),
                    "adaptive_threshold": float(adaptive_threshold),
                    "motion_score": float(np.mean(motion_window)),
                    "timestamp": timestamp
                }
                log_event("video_suspect", event_info)
                # Send frame and event info to AI worker thread
                ai_queue.put((frame.copy(), event_info))
                spike_frames = 0

            prev_frame = enhanced

            cv2.imshow("Enhanced Night Feed", enhanced)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Limit FPS only for video files
            if USE_VIDEO_FILE:
                time.sleep(1/15)  # Limit to ~15 FPS, adjust as needed

    except KeyboardInterrupt:
        print("Interrupted by user")

cap.release()
cv2.destroyAllWindows()
# Signal AI worker to exit
ai_queue.put(None)