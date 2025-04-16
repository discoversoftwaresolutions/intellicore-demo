import streamlit as st
import threading
import hashlib
import time
from random import choice

# 1️⃣ Must be first
st.set_page_config(page_title="IntelliCore AGI Demo", layout="wide")

# 2️⃣ Password Gate
def check_password():
    def encrypt(p): return hashlib.sha256(p.encode()).hexdigest()
    correct_hash = encrypt("Stakeholder2025")
    entered = st.text_input("Enter demo password:", type="password")
    if encrypt(entered) != correct_hash:
        st.warning("🔒 Access denied")
        st.stop()
check_password()

# 3️⃣ Branding & Onboarding
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

# 4️⃣ Mock Cortex Decision + Execute Button
if 'last_decision' not in st.session_state:
    st.session_state['last_decision'] = None

st.subheader("🧠 Ask IntelliCore AGI")
text = st.text_input("Your question:", placeholder="Should we deploy the drone to Area B?")

# When clicked, generate and store a mock decision
if st.button("Submit to Cortex"):
    decision = choice([
        "Deploy drone to Area B for surveillance.",
        "Hold drone deployment, awaiting weather confirmation.",
        "Initiate data link with northern outpost."
    ])
    st.session_state['last_decision'] = decision
    st.success(f"🤖 Cortex Decision: {decision}")

# Show "Execute Decision" if we have one
if st.session_state['last_decision']:
    st.markdown("**Ready to execute:**")
    col_exec, col_show = st.columns([1, 3])
    with col_exec:
        if st.button("Execute Decision"):
            cmd = st.session_state['last_decision']
            # Basic routing logic
            if "drone" in cmd.lower():
                agent = "drone"
            elif "humanoid" in cmd.lower():
                agent = "humanoid"
            else:
                agent = "virtual"
            st.info(f"🚀 Executing on `{agent}`: {cmd}")
    with col_show:
        st.write(f"> {st.session_state['last_decision']}")

# 5️⃣ Agent Actions (Quick Buttons)
st.subheader("🤖 Agent Command Center")
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

# 6️⃣ Simulated Telemetry Stream
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

# 7️⃣ Self-Reflection Logs (Simulated)
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

