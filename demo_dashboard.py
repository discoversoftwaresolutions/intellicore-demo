import streamlit as st
import threading
import hashlib
import time
import requests
from random import choice

# ─── CONFIG ────────────────────────────────────────────────────────────────
API_URL = "http://localhost:8000"  # ← Replace with your real API URL if available

# ─── PAGE SETUP ────────────────────────────────────────────────────────────
st.set_page_config(page_title="IntelliCore AGI Demo", layout="wide")

# ─── PASSWORD GATE ─────────────────────────────────────────────────────────
def check_password():
    def encrypt(p):
        return hashlib.sha256(p.encode()).hexdigest()
    correct_hash = encrypt("Stakeholder2025")
    entered = st.text_input("Enter demo password:", type="password")
    if encrypt(entered) != correct_hash:
        st.warning("🔒 Access denied")
        st.stop()

check_password()

# ─── BRANDING & ONBOARDING ─────────────────────────────────────────────────
st.image("https://intellicore.ai/assets/logo_dark.png", width=180)
st.title("🤖 IntelliCore AGI – Stakeholder Demo")
st.caption("Cortex Decisions • Autonomous Agents • Self-Reflection • Live Telemetry")
with st.expander("📘 What can I do here?"):
    st.markdown("""
    - Ask IntelliCore AGI natural language questions  
    - Trigger autonomous agents with one click  
    - Watch real-time telemetry from the field  
    - See how the system learns from its own decisions  
    """)

# ─── MOCK CORTEX DECISION ───────────────────────────────────────────────────
if 'last_decision' not in st.session_state:
    st.session_state['last_decision'] = None

st.subheader("🧠 Ask IntelliCore AGI")
text = st.text_input("Your question:", placeholder="Should we deploy the drone to Area B?")

if st.button("Submit to Cortex"):
    decision = choice([
        "Deploy drone to Area B for surveillance.",
        "Hold drone deployment, awaiting weather confirmation.",
        "Initiate data link with northern outpost."
    ])
    st.session_state['last_decision'] = decision
    st.success(f"🤖 Cortex Decision: {decision}")

# ─── EXECUTE DECISION WITH ENHANCED MOCK ────────────────────────────────────
if st.session_state['last_decision']:
    st.markdown("**Ready to execute:**")
    exec_col, show_col = st.columns([1, 3])
    with exec_col:
        if st.button("Execute Decision"):
            cmd = st.session_state['last_decision']
            # determine agent
            if "drone" in cmd.lower():
                agent = "drone"
            elif "humanoid" in cmd.lower():
                agent = "humanoid"
            else:
                agent = "virtual"
            # try real API call
            try:
                resp = requests.post(
                    f"{API_URL}/agent/{agent}",
                    json={"command": cmd},
                    timeout=5
                )
                resp.raise_for_status()
                data = resp.json()
                st.success(f"✅ {agent.capitalize()} Agent Response: {data.get('executed', data)}")
            except Exception:
                # ─ Enhanced Mock Fallback ───────────────────────────
                mock_resp = {
                    "drone": [
                        {
                            "executed": f"Drone executed: {cmd}",
                            "status": "en route",
                            "eta_secs": 120,
                            "battery": "83%"
                        },
                        {
                            "executed": "Drone began perimeter scan at Area B",
                            "status": "scanning",
                            "progress": "15%",
                            "battery": "79%"
                        }
                    ],
                    "humanoid": [
                        {
                            "executed": f"Humanoid performing: {cmd}",
                            "status": "assisting",
                            "location": "Zone C",
                            "battery": "67%"
                        },
                        {
                            "executed": "Humanoid completed medical assistance",
                            "status": "idle",
                            "location": "Zone C",
                            "battery": "72%"
                        }
                    ],
                    "virtual": [
                        {
                            "executed": f"Virtual Agent acknowledges: {cmd}",
                            "response_time_ms": 85,
                            "confidence": 0.97
                        },
                        {
                            "executed": "Virtual Agent reports all systems normal",
                            "response_time_ms": 60,
                            "confidence": 0.93
                        }
                    ]
                }
                fake = choice(mock_resp[agent])
                st.info(f"🔄 Mock {agent.capitalize()} Response:")
                st.json(fake)
    with show_col:
        st.write(f"> {st.session_state['last_decision']}")

# ─── QUICK AGENT BUTTONS ────────────────────────────────────────────────────
st.subheader("🤖 Quick Agent Commands")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("Send Drone"):
        st.info("🛰 Drone deployed to Area B")
with c2:
    if st.button("Activate Humanoid"):
        st.info("🧍 Humanoid assisting medical team")
with c3:
    if st.button("Contact Virtual Agent"):
        st.success("💬 Virtual Agent says: 'All systems are operational.'")

# ─── SIMULATED TELEMETRY STREAM ────────────────────────────────────────────
st.subheader("📡 Live Telemetry Feed (Simulated)")
telemetry_box = st.empty()
if st.button("Start Telemetry"):
    def fake_telemetry():
        updates = [
            {"agent": "drone", "status": "Scanning terrain", "location": "Area B"},
            {"agent": "humanoid", "status": "Delivering aid", "location": "Zone C"},
            {"agent": "virtual", "status": "Reporting metrics", "location": "Command"}
        ]
        for _ in range(6):
            telemetry_box.json(choice(updates))
            time.sleep(1.5)
    threading.Thread(target=fake_telemetry, daemon=True).start()

# ─── SELF-REFLECTION LOGS (SIMULATED) ────────────────────────────────────────
st.subheader("🔄 AGI Self-Reflection Logs (Simulated)")
sample_logs = [
    {
        "timestamp": "2025-04-15T12:01:00Z",
        "suggestion": "Refactor memory access pipeline",
        "ethics_approved": True,
        "rationale": "Improves recall consistency without compromising autonomy."
    },
    {
        "timestamp": "2025-04-14T18:47:23Z",
        "suggestion": "Avoid redundancy in drone pathing",
        "ethics_approved": True,
        "rationale": "Reduces energy use and time-to-scan."
    }
]
for entry in sample_logs:
    with st.container():
        st.markdown(f"""
        **🕒 {entry['timestamp']}**  
        - **Suggestion:** *{entry['suggestion']}*  
        - ✅ **Ethics Approved:** {entry['ethics_approved']}  
        - 📘 **Why:** {entry['rationale']}  
        """)
