# Telemetry Tab
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
        thread = threading.Thread(target=stream)
        thread.start()

# Reflection Tab
with tabs[3]:
    st.markdown("### 🔄 Self-Reflection Logs")
    logs = [
        {"timestamp": "2025-04-15T12:01Z", "change": "Reduced redundant scans", "why": "Battery preservation"},
        {"timestamp": "2025-04-14T09:22Z", "change": "Switched from GPS to vision nav", "why": "Improved accuracy"}
    ]
    if logs:
        for log in logs:
            st.markdown(
                f"**🕒 {log['timestamp']}** — *{log['change']}*  \n> _Reason:_ {log['why']}"
            )
    else:
        st.info("🤔 No recent reflection logs.")

# Speech Tab
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
# Telemetry Tab
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
        thread = threading.Thread(target=stream)
        thread.start()

# Reflection Tab
with tabs[3]:
    st.markdown("### 🔄 Self-Reflection Logs")
    logs = [
        {"timestamp": "2025-04-15T12:01Z", "change": "Reduced redundant scans", "why": "Battery preservation"},
        {"timestamp": "2025-04-14T09:22Z", "change": "Switched from GPS to vision nav", "why": "Improved accuracy"}
    ]
    if logs:
        for log in logs:
            st.markdown(
                f"**🕒 {log['timestamp']}** — *{log['change']}*  \n> _Reason:_ {log['why']}"
            )
    else:
        st.info("🤔 No recent reflection logs.")

# Speech Tab
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
# Emotion Tab
with tabs[5]:
    st.markdown("### 😊 Emotion Analysis")
    text = st.text_area("Type input for analysis:")
    if st.button("🔍 Analyze"):
        emo = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
        res = emo(text)
        st.json(res)

# Drift Tab
with tabs[6]:
    st.markdown("### ⚠️ Data Drift Detection")
    if st.button("🔎 Run Drift Test"):
        ref = np.random.normal(size=500)
        new = np.concatenate([ref, np.random.normal(loc=1.3, size=100)])
        stat, p = ks_2samp(ref, new)
        st.metric("Drift Detected", "Yes" if p < 0.05 else "No")
        st.metric("p-value", round(p, 4))
