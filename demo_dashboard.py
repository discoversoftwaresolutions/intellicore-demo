import streamlit as st
import requests
import websocket
import threading
import json

st.set_page_config(page_title="IntelliCore AGI Demo", layout="wide")

st.title("🤖 IntelliCore AGI – Stakeholder Demo")
st.caption("Cortex Decisions • Autonomous Agents • Self-Reflection • Live Telemetry")

# Section: Natural Language Input
st.subheader("🧠 Cortex Reasoning")
input_text = st.text_input("Ask IntelliCore AGI:", placeholder="Should we send a drone to Area B?")

if st.button("Submit to Cortex"):
    try:
        res = requests.post("https://api.intellicore.ai/cortex/decision", json={"text": input_text})
        st.success(res.json().get("decision", "No response"))
    except Exception as e:
        st.error(f"Error: {e}")

# Section: Agent Execution
st.subheader("🤖 Agent Interaction")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Send Drone"):
        r = requests.post("https://api.intellicore.ai/agent/drone", json={"command": "Deploy to Area B"})
        st.write(r.json())

with col2:
    if st.button("Activate Humanoid"):
        r = requests.post("https://api.intellicore.ai/agent/humanoid", json={"command": "Assist with medical"})
        st.write(r.json())

with col3:
    if st.button("Speak with Virtual Agent"):
        r = requests.post("https://api.intellicore.ai/agent/virtual", json={"prompt": "How is the mission going?"})
        st.write(r.json())

# Section: WebSocket Telemetry
st.subheader("📡 Live Telemetry Stream")

log_box = st.empty()

def stream_logs():
    ws = websocket.WebSocketApp(
        "wss://api.intellicore.ai/ws/telemetry?token=demo",
        on_message=lambda ws, msg: log_box.json(json.loads(msg)),
    )
    ws.run_forever()

if st.button("Start Telemetry Stream"):
    threading.Thread(target=stream_logs).start()

# Section: Self-Reflection Logs
st.subheader("🔄 Recent Self-Reflections")

try:
    logs = requests.get("https://api.intellicore.ai/self-reflection/latest").json()
    for entry in logs[-5:][::-1]:
        st.markdown(f"""
        **🕒 {entry['timestamp']}**
        - Suggestion: *{entry['suggestion']}*
        - ✅ Ethics Approved: {entry['ethics_approved']}
        - _Why_: {entry['rationale']}
        """)
except:
    st.warning("Unable to load reflection logs.")
