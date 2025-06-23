## 🧪 Test Report Template

> Use this structure to document each test case in `/Tests/`.

---

### 🎥 Tested Media
**Video / Audio Source**:  
`[Path or description of the test media]`

---

### 🎯 Test Objective
**Goal**:  
`[Describe what this test is trying to validate or simulate]`

**Missile Event Type**:  
`[e.g., Ground hit, Air explosion, No explosion (dud), Other]`

---

### 🔍 Expected Outcome
- **Brightness Detection**: `[Expected behavior or threshold spike]`  
- **Audio Detection**: `[Expected reaction to sound spike]`  
- **OpenAI Image Analysis**: `[Expected GPT-4o response (yes/no)]`

---

### 🧪 Actual Outcome
**Program Behavior Summary**:  
`[Describe what happened during execution]`

**Terminal Logs**:
```text
[Paste the relevant terminal or console output here]
```

---

### 📸 Flagged Results

- **Flagged Image(s)**:  
  List the image file names saved in `/Flaged` (e.g., `flagged_20250623_011122.jpg`).

- **Positive Detections**:  
  How many times the program correctly detected a missile or explosion.

- **False Positive Detections**:  
  How many times the program falsely flagged a detection when none occurred.

---

### 📊 Accuracy Estimate

**Formula**:
```text
(10 + (POSITIVE DETECTIONS / FALSE POSITIVE DETECTIONS) * 100%) * 100
```
---

---

## 🗂 Current test opearations

<a href="https://github.com/RaziFalah/MissileDetectionOverRTSP/blob/main/Tests/OperationDemoAlpha.md"> - **Operation demo alpha** audio test, ground explosion. </a>


---

Got any additional data? Could be even more helpful.
