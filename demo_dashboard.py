import streamlit as st
import hashlib
import numpy as np
import time
import threading
import requests
from random import choice
from transformers import pipeline
from scipy.stats import ks_2samp

# Safe audio import
try:
    import sounddevice as sd
    import speech_recognition as sr
    has_audio = True
except OSError:
    has_audio = False

# Page setup
st.set_page_config(page_title="IntelliCore AGI", layout="wide")
PASSWORD = "Stakeholder2025"
API_URL = "https://demo.intellicore.ai"

# Password gate
def check_password():
    def encrypt(p): return hashlib.sha256(p.encode()).hexdigest()
    input_pass = st.sidebar.text_input("🔐 Enter Password:", type="password")
    if encrypt(input_pass) != encrypt(PASSWORD):
        st.warning("🔒 Access denied")
        st.stop()

check_password()
st.sidebar.success("✅ Access Granted")

# Branding
st.image("https://intellicore.ai/assets/logo_dark.png", width=140)
st.title("🤖 IntelliCore AGI — Unified AGI Control & Demo")

if 'last_decision' not in st.session_state:
    st.session_state['last_decision'] = None

# Define all tabs
tabs = st.tabs([
    "🌐 Home", "🛰 Agent Control", "📡 Telemetry",
    "🔄 Reflection", "🎤 Voice", "😊 Emotion", "⚠️ Drift"
])

# 🌐 Home Tab
with tabs[0]:
    st.markdown("### 🧠 Ask IntelliCore")
    question = st.text_input("Prompt", placeholder="e.g. Should we initiate a tactical scan of Zone C?")
    if st.button("🧠 Generate Decision"):
        st.session_state['last_decision'] = choice([
            "Deploy drone to Zone C for tactical scan.",
            "Delay operation due to low visibility.",
            "Initiate satellite imaging of Region 7."
        ])
        st.success("Cortex has responded.")
    if st.session_state['last_decision']:
        st.info(f"**🤖 Decision:** {st.session_state['last_decision']}")
        if st.button("🚀 Execute"):
            st.success("🛰 Executing decision logic…")

# 🛰 Agent Control
with tabs[1]:
    st.markdown("### 🛰 Agent Command Center")
    c1, c2, c3 = st.columns(3)
    if c1.button("Deploy Drone"):
        st.info("🛰 Drone launched to Sector A.")
    if c2.button("Activate Humanoid"):
        st.info("🧍 Humanoid operational in MedBay.")
    if c3.button("Contact Virtual Agent"):
        st.success("💬 Virtual Agent is online.")

# 📡 Telemetry
with tabs[2]:
    st.markdown("### 📡 Live Agent Telemetry")
    telemetry_box = st.empty()
    if st.button("📶 Start Feed"):
        def stream():
            updates = [
                {"agent": "drone", "status": "Scanning", "zone": "Sector A"},
                {"agent": "humanoid", "status": "Assisting", "zone": "Zone B"},
                {"agent": "virtual", "status": "Reporting", "zone": "HQ"}
            ]
            for _ in range(10):
                telemetry_box.json(choice(updates))
                time.sleep(1)
        threading.Thread(target=stream).start()

# 🔄 Reflection
with tabs[3]:
    st.markdown("### 🔄 Self-Reflection Logs")
    logs = [
        {"timestamp": "2025-04-15T12:01Z", "change": "Reduced redundant scans", "why": "Battery preservation"},
        {"timestamp": "2025-04-14T09:22Z", "change": "Switched from GPS to vision nav", "why": "Improved accuracy"}
    ]
    for log in logs:
        st.markdown(f"**🕒 {log['timestamp']}** — *{log['change']}*  \n> _Reason:_ {log['why']}")

# 🎤 Voice
with tabs[4]:
    st.markdown("### 🎤 Voice Transcription")
    if not has_audio:
        st.warning("🔇 Audio recording not supported in this environment.")
        mock_input = st.text_input("Manual transcription (mock):")
        if mock_input:
            st.success(f"🗣 You said: {mock_input}")
    else:
        if st.button("🎙 Start Recording"):
            recognizer = sr.Recognizer()
            with sd.InputStream(samplerate=16000, channels=1) as stream:
                st.info("Listening for 5s...")
                audio = stream.read(16000 * 5)[0]
            audio_data = sr.AudioData(np.array(audio).tobytes(), 16000, 2)
            try:
                result = recognizer.recognize_google(audio_data)
                st.success(f"🔊 {result}")
            except Exception as e:
                st.error(f"Speech recognition error: {e}")

# 😊 Emotion
with tabs[5]:
    st.markdown("### 😊 Emotion Analysis")
    text = st.text_area("Type input for analysis:")
    if st.button("🔍 Analyze"):
        emo = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        st.json(emo(text))

# ⚠️ Drift
with tabs[6]:
    st.markdown("### ⚠️ Data Drift Detection")
    if st.button("🔎 Run Drift Test"):
        ref = np.random.normal(size=500)
        new = np.concatenate([ref, np.random.normal(loc=1.3, size=100)])
        stat, p = ks_2samp(ref, new)
        st.metric("Drift Detected", "Yes" if p < 0.05 else "No")
        st.metric("p-value", round(p, 4))
