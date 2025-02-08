# 💬 Nova AI – AI Interview Preparation & Chatbot  

**Nova AI** is an advanced **AI-powered chatbot** designed for **interview preparation, conversation assistance, and knowledge retrieval** using **Google Gemini API**. It supports **PDF processing, voice recognition, speech synthesis, and AI-driven replies**.  

---

## 🚀 Features  

### 🎯 **Core Functionalities**  
✅ **AI Chatbot** – Uses **Google Gemini API** to generate intelligent responses.  
✅ **Voice-to-Text** – Converts speech into text using **SpeechRecognition**.  
✅ **Text-to-Speech (TTS)** – Uses **gTTS (Google Text-to-Speech)** for audio output.  
✅ **Smart AI Replies** – AI suggests smart responses.  
✅ **PDF Reader** – Extracts text from PDFs using `PyMuPDF (fitz)`.  
✅ **Weather Updates** – Fetches live weather using an API.  

### 🎭 **AI Personas (Modes)**  
🔹 **Normal Mode 🤖** – Default AI mode.  
🔹 **Teacher 👨‍🏫** – Explains concepts like a teacher.  
🔹 **Friend 😊** – Casual and friendly responses.  
🔹 **Expert 🎓** – Provides in-depth knowledge.  
🔹 **Comedian 🤣** – Generates humorous replies.  
🔹 **Code Debugger 🧑‍💻** – Analyzes and debugs code.  

---

## 🛠️ Tech Stack  

🔹 **Frontend** – Streamlit  
🔹 **Backend** – Google Gemini API, Python  
🔹 **Speech Recognition** – `speech_recognition`  
🔹 **Text-to-Speech (TTS)** – `gTTS`, `pygame`  
🔹 **PDF Processing** – `PyMuPDF (fitz)`  
🔹 **Translation & Language Detection** – `deep_translator`, `langdetect`  
🔹 **Scheduler for Background Tasks** – `APScheduler`  
🔹 **Environment Variables** – `dotenv`  

---

## 🏗️ Installation  

### 📌 **Step 1: Clone the Repository**  
```bash
git clone https://github.com/yourusername/nova-ai-chatbot.git
cd nova-ai-chatbot
```

### 📌 **Step 2: Create a Virtual Environment (Optional, Recommended)**  
```bash
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

### 📌 **Step 3: Install Dependencies**  
```bash
pip install -r requirements.txt
```

### 📌 **Step 4: Add API Keys**  
Create a `.env` file in the root directory and add:  
```
GENAI_API_KEY=your_google_gemini_api_key
WEATHER_API_KEY=your_weatherstack_api_key
```

### 📌 **Step 5: Run the Application**  
```bash
streamlit run app.py
```

---

## 🌐 Deployment on Render  

1. Add `pygame` and other dependencies to `requirements.txt`:  
   ```
   streamlit
   google-generativeai
   fitz
   speechrecognition
   gtts
   pygame
   requests
   aiohttp
   deep-translator
   langdetect
   apscheduler
   python-dotenv
   ```
2. **Deploy on Render** – Follow [Render’s Streamlit deployment guide](https://render.com/docs/deploy-a-streamlit-app).  
3. Set **environment variables** (`GENAI_API_KEY` & `WEATHER_API_KEY`).  

---

## 🤖 Usage  

- **Text Chat:** Type your message, and the AI responds.  
- **Voice Input:** Click **"🎤 Speak to AI"** to talk to the chatbot.  
- **Text-to-Speech:** Click **"🔊 Read Aloud"** to hear AI’s response.  
- **PDF Upload:** Upload a PDF, and AI will process its content.  
- **AI Persona:** Choose different AI personalities for tailored responses.  

---

## 📜 License  

This project is licensed under the **MIT License**.  

---

## 🛠️ Future Enhancements  

✅ **AI-driven Resume Review**  
✅ **More AI Personalities & Interview Coaching**  
✅ **Advanced Multi-Turn Memory**  
✅ **Enhanced UI/UX & Dark Mode Support**  

---

## ⭐ Contribute  

Pull requests are welcome! 🚀 Feel free to submit issues and contribute to this project.  

👨‍💻 **Developer:** Varikuntla Sai Manoj
📧 **Contact:** varikuntlasaimanoj@gmail.com 
