## 📁 /Flaged

This folder is **automatically populated** by the missile detection system during runtime.

---

## 📸 Purpose


Each time the system detects a brightness or audio anomaly and submits the frame for AI analysis via OpenAI GPT-4o, a copy of the frame is saved here **only if** the AI response is **positive** (i.e., it confirms the presence of a missile or rocket).

---

## 🧠 When a Frame is Saved

A frame will be saved in this folder if all the following conditions are met:

1. A **sustained brightness spike** is detected in the video stream.
2. The frame is sent to the OpenAI API for **visual classification**.
3. The AI returns `"yes"` — confirming a potential missile or rocket presence.

---

## 🗂 File Naming Convention


Files are saved with a timestamp format for traceability:

---
