# Explosion Detection Test Report

## 📁 Tested Media
**File:** `/home/razi/Desktop/Project-CEE/MissileDetectionAdvanced/TestFeed/Easy2.mp4`  
**Goal:** Evaluate the program’s efficiency in detecting explosions using audio and visual data.

## 🧪 Test Scenario
- **Explosion Type:** Ground explosion (missile not visible in the sky)
- **Expected Detection:**
  - **Brightness Module:** `FLAGGED SUSPECTED BRIGHTNESS`
  - **Audio Module:** `FLAGGED EXPLOSION NOISE`
  - **OpenAI Analysis:** `FLAGGED EXPLOSION`

## ✅ Program Behavior & Logs


### 🔍 Detection Timeline

| Timestamp | ΔBrightness | OpenAI Response | AI Detection |
|----------|-------------|-----------------|--------------|
| 02:14:37 | 15.08       | “can’t confirm” | False        |
| 02:14:38 | 29.06       | “can’t determine” | False      |
| 02:14:39 | 32.63       | “can’t determine” | False      |
| 02:14:40 | 34.06       | “no”             | False        |
| 02:14:42 | 36.76       | “no”             | False        |
| 02:14:43 | 33.69       | “no”             | False        |
| 02:14:44 | 22.92       | “yes”            | **True**     |
| 02:14:45 | 13.84       | “no”             | False        |
| 02:14:47 | 13.29       | “no”             | False        |
| 02:14:48 | 14.32       | “no”             | False        |
| 02:14:49 | 18.08       | “no”             | False        |
| 02:14:50 | 19.57       | “no”             | False        |
| 02:14:51 | 16.23       | “no”             | False        |
| 02:14:52 | 21.06       | “no”             | False        |
| 02:14:57 | 21.87       | “can’t answer”   | False        |
| 02:14:58 | 20.84       | “no”             | False        |
| 02:14:59 | 17.09       | “can’t determine”| False        |
| 02:15:00 | 14.92       | “no”             | False        |
| 02:15:00 | 10.84       | “no”             | False        |
| 02:15:02 | 11.79       | “no”             | False        |
| 02:15:03 | 14.00       | “no”             | False        |
| 02:15:04 | 15.05       | “no”             | False        |
| 02:15:05 | 14.57       | “no”             | False        |
| 02:15:06 | 10.38       | “yes”            | **True**     |
| 02:15:08 | 27.06       | “no”             | False        |
| 02:15:09 | 41.74       | “yes”            | **True**     |
| 02:15:10 | 49.51       | “can’t tell”     | False        |

**Stream ended or failed to grab frame**

---

## 🖼️ Flagged Images
|         Image         |
|        -------        |
| <a href="Flaged/FalsePositve1.jpg" target="_blank">FalsePositve1.jpg </a>|
| <a href="Flaged/FalsePositve2.jpg" target="_blank">FalsePositve2.jpg </a>|
|<a href="Flaged/FalsePositve3.jpg" target="_blank"> FalsePositve3.jpg </a>|



<image src="/Flaged/FalsePositve2.jpg"></image>
<image src="/Flaged/FalsePositve3.jpg"></image>

Tip: Images did not load? Use links instead.

---

## 📊 Detection Summary

- **Total detections triggered:** `24`
- **Expected detections estimated:** `NOT CALCULATED`
- **Correct positive detections:** `0`
- **False positive detections:** `3`
- **Success rate:** `10%` ➤ **TEST FAILED**

---

## 📌 Notes

Although the program technically responded with the correct alerts, they were **not** based on actual explosion recognition. Instead, it flagged brightness spikes that were then **incorrectly** labeled as explosions by the AI. The following images were flagged as positive but were **false positives**:  
**Images:** `1`, `2`, `3`
