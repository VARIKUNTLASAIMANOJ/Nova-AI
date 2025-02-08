import streamlit as st
import google.generativeai as genai
import os
import datetime
import time
import base64
import fitz
import speech_recognition as sr
import requests
import aiohttp
from deep_translator import GoogleTranslator
from langdetect import detect
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv
from gtts import gTTS
import tempfile
import pygame

load_dotenv()
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if GENAI_API_KEY:
    genai.configure(api_key=GENAI_API_KEY)
else:
    st.error("⚠️ Missing Gemini API Key! Check your .env file.")

st.set_page_config(page_title="Nova AI", layout="wide")
st.title("💬 Nova AI")

with st.sidebar:
    st.subheader("📜 Chat History")
    
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}

    selected_chat = st.selectbox("Select a previous chat:", ["New Chat"] + list(st.session_state.chat_history.keys()))

    if selected_chat != "New Chat":
        if st.button(f"🗑️ Delete '{selected_chat}'"):
            del st.session_state.chat_history[selected_chat]
            st.experimental_rerun()

    if st.button("🗑️ Clear All Chats"):
        st.session_state.chat_history = {}
        st.rerun()

    st.subheader("📂 Upload a PDF")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    
    if uploaded_file:
        st.success(f"✅ Uploaded: {uploaded_file.name}")

    st.subheader("🎭 Choose AI Persona")
    ai_persona = st.selectbox("Select AI Mode", [
        "Normal Mode 🤖",
        "Teacher 👨‍🏫",
        "Friend 😊",
        "Expert 🎓",
        "Comedian 🤣",
        "Code Debugger 🧑‍💻"
    ])


def extract_text_from_pdf(uploaded_file):
    pdf_text = ""
    try:
        with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
            for page in doc:
                pdf_text += page.get_text("text") + "\n"
    except Exception as e:
        st.error(f"❌ Error reading PDF: {e}")
    return pdf_text.strip()

pdf_text = ""
if uploaded_file:
    pdf_text = extract_text_from_pdf(uploaded_file)
    with st.expander("📖 View Extracted Text"):
        st.text_area("Extracted PDF Content:", pdf_text, height=300)

def get_suggestions(query):
    suggestions = ["What is AI?", "Explain Quantum Computing", "How does Machine Learning work?"]
    return [s for s in suggestions if query.lower() in s.lower()]

st.subheader("💡 Quick Prompts")
user_input = st.chat_input("Type your message...")
suggested_questions = get_suggestions(user_input) if user_input else []

if suggested_questions:
    st.write("🔍 Suggested Questions:")
    for question in suggested_questions:
        if st.button(question):
            user_input = question

try:
    model = genai.GenerativeModel("gemini-1.5-flash")

    if selected_chat == "New Chat":
        chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.messages = []
    else:
        chat_id = selected_chat
        st.session_state.messages = st.session_state.chat_history.get(chat_id, [])

    for msg in st.session_state.messages:
        avatar = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"]):
            st.markdown(f"{avatar} {msg['content']}")

    if st.button("🎤 Speak to AI"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("🎙️ Listening...")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                st.success(f"🗣️ You said: {user_input}")
            except sr.UnknownValueError:
                st.error("❌ Could not understand audio.")
            except sr.RequestError:
                st.error("⚠️ Speech Recognition service error.")

    if user_input:
        persona_prompts = {
            "Normal Mode 🤖": "",
            "Teacher 👨‍🏫": "Explain concepts like a teacher to a student: ",
            "Friend 😊": "Respond as a friendly and casual chatbot: ",
            "Expert 🎓": "Provide detailed expert-level information: ",
            "Comedian 🤣": "Make responses humorous and engaging: ",
            "Code Debugger 🧑‍💻": "Analyze and debug the following code: "
        }

        if pdf_text:
            user_input = f"Refer to the following document:\n\n{pdf_text}\n\n{persona_prompts[ai_persona]}{user_input}"
        else:
            user_input = persona_prompts[ai_persona] + user_input

        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"👤 {user_input}")

        with st.chat_message("assistant"):
            bot_area = st.empty()
            bot_area.markdown("🤖 AI is typing...")
            time.sleep(1.5)

        response = model.generate_content({"parts": [{"text": user_input}]})
        bot_reply = response.text if response else "⚠️ No response from AI."

        try:
            detected_lang = detect(bot_reply)
            if detected_lang != "en":
                bot_reply = GoogleTranslator(source="auto", target="en").translate(bot_reply)
        except Exception as e:
            st.warning(f"⚠️ Translation Skipped Due to Error: {e}")

        bot_area.empty()

        with st.chat_message("assistant"):
            st.markdown(f"🤖 {bot_reply}")

        if st.button("🔊 Read Aloud"):
            with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
                tts = gTTS(text=bot_reply, lang="en")
                tts.save(temp_audio.name)
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(temp_audio.name)
                pygame.mixer.music.play()

                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)  # Wait for playback to finish

                pygame.mixer.quit()

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.session_state.chat_history[chat_id] = st.session_state.messages

except Exception as e:
    st.error(f"⚠️ Error: {e}")

def get_weather(city):
    if not WEATHER_API_KEY:
        return "⚠️ Weather API Key is missing!"
    
    url = f"http://api.weatherstack.com/current?access_key={WEATHER_API_KEY}&query={city}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if "current" in data:
            return f"{city}: {data['current']['temperature']}°C, {data['current']['weather_descriptions'][0]}"
        else:
            return f"❌ Could not fetch weather for '{city}'. Please check the city name."

    except requests.exceptions.RequestException as e:
        return f"⚠️ API Error: {e}"

st.sidebar.subheader("🌦️ Get Weather")
city = st.sidebar.text_input("Enter city name", "New York")
if st.sidebar.button("Get Weather"):
    st.sidebar.write(f"Current Weather: {get_weather(city)}")
