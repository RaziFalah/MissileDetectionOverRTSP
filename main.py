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

USE_VIDEO_FILE = False
rtsp_url = "rtsp://user:password@ip:port/path"
video_path = "" #in case of testing using local video, please set USE_VIDEO_FILE = True and add a path to the video here.

print(os.path.exists(video_path))

def send_alert():
    print("\033[91mMissile/rocket detected! Sending alert...\033[0m")
    #Currently not paired with the esp32 (/AlertSystem)
    #You may choose your own way of activating the alert (Email, Home assistants, speakers...)

def analyze_image_with_openai(
    image,
    prompt="Is there a missile or rocket in this night sky image? Reply only 'yes' or 'no'.",
    save_flagged_path="/home/razi/Desktop/Project-CEE/MissileDetectionAdvanced/Flaged"
):
    temp_filename = "temp_frame.jpg"
    cv2.imwrite(temp_filename, image)

    api_key = ""
    # For production, use: api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("FATAL ERROR: API KEY?")
        exit()

    with open(temp_filename, "rb") as img_file:
        img_bytes = img_file.read()
        img_b64 = base64.b64encode(img_bytes).decode()

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
        os.remove(temp_filename)
        return flagged
    else:
        print(f"OpenAI API error: {response.status_code} {response.text}")
        os.remove(temp_filename)
        return False

def listen_rtsp_audio(input_source, threshold=0.1, chunk_duration=1, samplerate=16000):
    """
    Listen to RTSP or video file audio and trigger alert if loud sound detected.
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

    print("Listening for explosions in audio...")
    try:
        while True:
            audio_chunk = process.stdout.read(chunk_size)
            if len(audio_chunk) < chunk_size:
                break
            audio_np = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32) / 32768.0
            volume = np.linalg.norm(audio_np) / len(audio_np)
            # print(f"Audio volume: {volume:.4f}")
            if volume > threshold:
                print("Explosion sound detected from audio!")
                send_alert()
    except KeyboardInterrupt:
        print("Audio listening interrupted.")
    finally:
        process.terminate()

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
    rolling_window = deque(maxlen=15)
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

            # Analyze the entire frame
            mean_brightness = np.mean(enhanced)
            rolling_window.append(mean_brightness)

            if len(rolling_window) == rolling_window.maxlen:
                avg_brightness = np.mean(rolling_window)
                brightness_diff = mean_brightness - avg_brightness

                # Lower threshold, require persistence
                if brightness_diff > 10:
                    spike_frames += 1
                else:
                    spike_frames = 0

                if spike_frames >= 2:
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(f"[{timestamp}] [Suspecting explosion] Persistent brightness spike detected! ΔBrightness: {brightness_diff:.2f} request to AI analysis...")
                    # Use the original frame for AI analysis
                    if analyze_image_with_openai(frame):
                        print("[True] AI analysis: Missile/rocket detected!")
                        send_alert()
                    else:
                        print("[False] AI analysis: No missile/rocket detected.")
                    spike_frames = 0

            prev_frame = enhanced

            cv2.imshow("Enhanced Night Feed", enhanced)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("Interrupted by user")

cap.release()
cv2.destroyAllWindows()
