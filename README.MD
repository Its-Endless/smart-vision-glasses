# **Smart Vision Glasses – An AI-Powered Assistive System for the Visually Impaired**

Smart Vision Glasses is an AI-driven assistive technology designed to empower visually impaired individuals with real-time understanding of their surroundings.
This system combines **computer vision**, **speech interaction**, and **multimodal AI features** to create an accessible, reliable, and low-cost solution.

The project currently runs as a **software prototype on a laptop**, with future plans to integrate it into lightweight wearable smart glasses.

---

## 🌟 **Features**

### ✅ **1. Object Detection (YOLOv5su)**

* Detects people, vehicles, and obstacles in real time.
* Announces object name, direction, and approximate distance.
* Helps the user stay aware of their surroundings.

### ✅ **2. Face Recognition (On-Device Training)**

* Detects and recognizes known individuals.
* Allows users to **scan new faces** via voice and trains instantly on local device.
* Works fully offline using LBPH.

### ✅ **3. Text Reader (OCR – EasyOCR)**

* Reads printed text from signboards, documents, labels, menus, etc.
* Works offline and speaks text aloud in real time.
* Uses threaded processing for smooth performance.

### ✅ **4. Emotion Detection**

* Identifies basic facial emotions (happy, sad, neutral).
* Provides social context cues for visually impaired users.

### ✅ **5. GPS Mode (Prototype)**

* Basic location and direction support.
* Future integration with mobile app for full navigation.

### 🎤 **Hands-Free Voice Control**

* Hotword detection: **“Hey Vision”**
* Commands like:

  * “Turn on object detection”
  * “Open text reader”
  * “Scan new face”
  * “Stop face detection”
* Voice recognition with keyboard fallback for noisy environments.

---

## 🧱 **System Architecture**

```
main.py 
   ↳ mode_manager.py
       ↳ modes/
           • object_detection.py
           • face_detection.py
           • text_reader.py
           • emotion_detection.py
           • gps_mode.py
       ↳ utils/
           • speech_engine.py
           • camera_stream.py
           • audio_alerts.py
           • ocr_utils.py
```

Each mode is **independent**, easy to extend, and communicates via the central controller.
The modular design enables multiple developers to work in parallel.

---

## 🚀 **Installation**

### 1. Clone the repository

```
git clone https://github.com/<your-username>/smart-vision-glasses
cd smart-vision-glasses
```

### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ **Run the Project**

```
python main.py
```

Then speak:

> **“Hey Vision, turn on object detection”**
> or
> **“Hey Vision, open text reader”**

Press **Q** anytime to exit a mode.

---

## 📂 **Project Structure**

```
smart_glasses/
│── main.py
│── mode_manager.py
│── config/
│── modes/
│── utils/
│── assets/
│── models/
│── logs/
│── tests/
│── requirements.txt
│── README.md
```

---

## 🧪 **Current Status (MVP)**

All primary features implemented and tested:

| Feature              | Status        |
| -------------------- | ------------- |
| Object Detection     | ✅ Working     |
| Text Reader (OCR)    | ✅ Working     |
| Face Recognition     | ✅ Working     |
| Emotion Detection    | ✅ Working     |
| GPS Mode             | ⚠️ Prototype  |
| SOS Mode             | ⏳ Coming soon |
| Live Calling         | ⏳ Coming soon |
| Hardware Integration | ⏳ Planned     |

The prototype works reliably on a laptop and is already suitable for trials.

---

## 🎯 **Impact**

This project aims to:

* Improve independence for visually impaired individuals
* Make assistive technology more **affordable**, **accessible**, and **offline-capable**
* Provide instant awareness of the environment
* Enable intelligent human-like interaction with surroundings
* Move towards a fully wearable pair of AI-powered smart glasses

This is more than a project — it is a step toward **inclusive, human-centered technology**.

---

## 🛣️ **Future Roadmap**

* 📱 Android mobile application
* 🔔 Emergency SOS mode
* 📞 Live caregiver calling
* 🥽 Wearable hardware (smart glasses)
* 🌙 Night vision with IR camera
* 🗺️ Full offline navigation
* 🗣️ On-device speech recognition (Vosk/DeepSpeech)

---

## 🤝 **Contributing**

We welcome collaboration!
Please open an issue or pull request to contribute features, fixes, or ideas.

---

## 📜 **License**

This project is released under the **MIT License** — free to use, modify, and distribute.

---
