# 🧠 Fluenter  
**AI-Powered Real-Time Grammar & Writing Suggestion Tool**  
*Like Grammarly — built with Electron, Gemini, and Python.*

---

## 🚀 Overview

**Fluenter** is a desktop app that provides **AI-driven grammar and writing suggestions system-wide**, across any Windows application — including WhatsApp Desktop, browsers, Notepad, and others.

It continuously monitors text input fields, analyzes the text using **Google’s Gemini model**, and displays smart correction or rephrasing suggestions in a **floating overlay window** (built with Electron).

---

## ✨ Features

| Feature | Description |
|----------|-------------|
| 🧩 **System-Wide Text Capture** | Uses Windows **UIAutomation API** to read text from any focused input control. |
| 🤖 **AI Grammar Engine** | Powered by **Gemini 1.5 Flash/Pro** model via Vertex AI API for grammar correction and style improvement. |
| 💬 **Floating Suggestion Overlay** | Transparent, always-on-top **Electron** overlay window that displays grammar suggestions near your cursor. |
| ⚙️ **Cross-App Integration** | Works in browsers, chat apps, office tools, IDEs, etc. |
| 🔤 **Real-Time Correction** | Detects changes in active text and provides live feedback within milliseconds. |
| 🧱 **Modular Architecture** | Separate **Python backend**, **Electron UI**, and **automation layer** for easy upgrades. |
| 🔒 **Privacy-Friendly** | Runs locally except when querying Gemini API; text is never stored. |

---

## 🧩 Architecture

```
+-------------------------------+
|   Windows Application (e.g.,  |
|   WhatsApp / Notepad / Word)  |
+-------------------------------+
              │
              ▼
   [Windows Text Capture Layer]
     (Python + UIAutomation)
              │
              ▼
       [FastAPI Backend]
   (Grammar correction engine)
              │
              ▼
       [Gemini AI Model API]
         (via Vertex AI)
              │
              ▼
   [Electron Overlay UI Window]
 (Shows suggestions near cursor)
```

---

## 🛠️ Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend (Grammar API)** | Python, FastAPI |
| **AI Model** | Google Gemini 1.5 (via Vertex AI SDK) |
| **Frontend (Overlay)** | Electron.js |
| **Text Capture** | UIAutomation / pywinauto |
| **Injection** | PyAutoGUI / Windows Input APIs |
| **Communication** | REST + IPC (Electron ↔ Python) |

---

## ⚙️ Setup Instructions

### 1️⃣ Clone Repo
```bash
git clone https://github.com/yourusername/fluenter.git
cd fluenter
```

### 2️⃣ Backend Setup (Python)
```bash
cd backend
pip install fastapi uvicorn google-cloud-aiplatform transformers torch uiautomation requests pyautogui
```

Set your Google Cloud credentials:
```bash
set GOOGLE_APPLICATION_CREDENTIALS="path\to\your\service-account.json"
```

Run the backend:
```bash
uvicorn app:app --reload
```

---

### 3️⃣ Electron UI Setup
```bash
cd client
npm install
npm start
```

This launches the overlay window, which will display grammar suggestions.

---

### 4️⃣ Text Capture Agent
Run watcher script:
```bash
python client/watcher.py
```
This continuously checks your focused text box, sends the content to the backend, and notifies the Electron overlay when suggestions are ready.

---

## ⚡ Key Files

| File | Description |
|------|--------------|
| `backend/app.py` | FastAPI grammar correction API |
| `backend/gemini_client.py` | Gemini integration (via Vertex AI) |
| `client/watcher.py` | Windows UIAutomation-based text watcher |
| `client/main.js` | Electron main process |
| `client/overlay.html` | Floating suggestion UI |
| `requirements.txt` | Python dependencies |
| `package.json` | Electron dependencies |

---

## 🧠 Gemini Prompt Example

Prompt used to generate grammar correction:
```
Correct the grammar of the following text:
"I has a apple and she go to school everydays."
```

Gemini Response:
```
"I have an apple and she goes to school every day."
```

---

## 🪄 Future Enhancements

| Feature | Description |
|----------|-------------|
| 🪶 **Stylistic Suggestions** | Rephrase sentences for clarity, tone, or formality. |
| 🧠 **Local LLM Integration** | Option to run open-source models (Llama, Mistral) locally. |
| 🌍 **Multilingual Support** | Extend to other languages via LanguageTool or Gemini multilingual mode. |
| 🎨 **Better Overlay UX** | Modern material design overlay with animations and icons. |
| ⚡ **Event Hooks** | Switch from polling to event-driven capture via Text Services Framework (TSF). |
| 🧰 **System Tray Integration** | Add tray menu for toggling, configuration, and updates. |

---

## 🔒 Privacy Notice

Your text is only processed temporarily for generating suggestions.
No data is logged or shared beyond the Gemini API call.
For full privacy, you can disable cloud correction and use a local model.

---

## 🧑‍💻 Author

**Project Lead:** [ErrorFound404](https://github.com/ErrorFound404)  
**Languages:** Python, JavaScript (Electron), Flutter, Django, LangChain  
**Purpose:** Build an AI-powered writing assistant for Windows developers and users.

---

## 🪄 License

This project is under the **MIT License**.  
You’re free to modify, distribute, and use it for personal or commercial projects.

---

## 💬 Contributing

1. Fork the repository  
2. Create a new feature branch  
3. Submit a pull request  

Suggestions and improvements are always welcome!

---

### 💡 Example Screenshot (Future)

```
┌─────────────────────────────┐
│ WhatsApp Desktop            │
│ [You]: I has a apple 🍏     │
│ └──────────────┐            │
│                ▼            │
│ 💡 Did you mean: “I have an apple”? │
└─────────────────────────────┘
```

---

## 🌟 Summary

**Fluenter** is your personal AI proofreader for every app on Windows —  
powered by **Gemini**, designed with **Electron**, and built for **real-time productivity**.

> Write smarter. Everywhere.
