import streamlit as st
import hashlib
import numpy as np
import time
import threading
import requests
import json
from random import choice
from transformers import pipeline
from scipy.stats import ks_2samp

try:
    import sounddevice as sd
    import speech_recognition as sr
    has_audio = True
except Exception:
    has_audio = False

try:
    import websocket
    has_ws = True
except ImportError:
    has_ws = False

st.set_page_config(page_title="IntelliCore AGI", layout="wide")
PASSWORD = "Stakeholder2025"

def check_password():
    def encrypt(p): return hashlib.sha256(p.encode()).hexdigest()
    input_pass = st.sidebar.text_input("🔐 Enter Password:", type="password")
    if encrypt(input_pass) != encrypt(PASSWORD):
        st.warning("🔒 Access denied")
        st.stop()

check_password()
st.sidebar.success("✅ Access Granted")

st.title("🤖 IntelliCore AGI — Jarvis Demo")
st.markdown("Live telemetry, voice input, and Cortex response simulation.")

if 'last_decision' not in st.session_state:
    st.session_state['last_decision'] = None

tabs = st.tabs(["🎤 Voice-to-Cortex", "📡 Live Telemetry", "🔄 Reflection", "😊 Emotion", "⚠️ Drift"])

# 🎤 Voice Control
with tabs[0]:
    st.markdown("### 🎙️ Talk to IntelliCore")
    if not has_audio:
        st.warning("🔇 Voice not supported in this environment.")
    else:
        if st.button("🎧 Start Listening"):
            recognizer = sr.Recognizer()
            mic = sr.Microphone()
            with mic as source:
                st.info("🎤 Listening for 5 seconds...")
                audio = recognizer.listen(source, timeout=5)
            try:
                result = recognizer.recognize_google(audio)
                st.success(f"🗣 You said: {result}")
                response = choice([
                    "Acknowledged. Initiating scan of Sector 3.",
                    "Holding position. Awaiting further input.",
                    "Deploying agent to coordinate entry protocol."
                ])
                st.info(f"🤖 Cortex: {response}")
            except Exception as e:
                st.error(f"Speech recognition error: {e}")

# 📡 WebSocket Telemetry
with tabs[1]:
    st.markdown("### 📡 Live Agent Telemetry (WebSocket or Mock)")
    telemetry_box = st.empty()

    def mock_stream():
        updates = [
            {"agent": "drone", "status": "Scanning", "zone": "Sector A"},
            {"agent": "humanoid", "status": "Assisting", "zone": "Zone B"},
            {"agent": "virtual", "status": "Reporting", "zone": "HQ"}
        ]
        for _ in range(10):
            telemetry_box.json(choice(updates))
            time.sleep(1)

    def start_websocket_stream():
        def on_message(ws, message):
            data = json.loads(message)
            telemetry_box.json(data)
        ws = websocket.WebSocketApp("wss://your-backend.example/ws/telemetry", on_message=on_message)
        threading.Thread(target=ws.run_forever).start()

    if has_ws:
        if st.button("📶 Start WebSocket Feed"):
            start_websocket_stream()
    if st.button("▶️ Use Simulated Telemetry"):
        threading.Thread(target=mock_stream).start()

# 🔄 Reflection Logs
with tabs[2]:
    st.markdown("### 🧠 Self-Reflection Logs")
    logs = [
        {"timestamp": "2025-04-15T12:01Z", "change": "Improved route planning", "why": "Reduce time latency"},
        {"timestamp": "2025-04-14T09:22Z", "change": "Switched power mode", "why": "Battery optimization"}
    ]
    for log in logs:
        st.markdown(f"**🕒 {log['timestamp']}** — *{log['change']}*  
> _Reason:_ {log['why']}")

# 😊 Emotion NLP
with tabs[3]:
    st.markdown("### 😊 Emotion Analysis")
    text = st.text_area("Input text for emotional context:")
    if st.button("🧠 Analyze Emotion"):
        emo = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        st.json(emo(text))

# ⚠️ Drift Detection
with tabs[4]:
    st.markdown("### ⚠️ Data Drift Check")
    if st.button("🔎 Detect Drift"):
        ref = np.random.normal(size=500)
        new = np.concatenate([ref, np.random.normal(loc=1.3, size=100)])
        stat, p = ks_2samp(ref, new)
        st.metric("Drift?", "Yes" if p < 0.05 else "No")
        st.metric("p-value", round(p, 4))
