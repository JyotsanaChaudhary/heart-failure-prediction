import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Smart Traffic Monitoring & Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PROFESSIONAL UI CSS ----------
st.markdown("""
<style>

/* Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* Hide default Streamlit UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Global */
.stApp {
    background-color: #0e1117;
    font-family: 'Inter', sans-serif;
    color: #e5e7eb;
}

/* Metric Cards */
[data-testid="stMetric"] {
    background: linear-gradient(145deg, #151a21, #1a1f26);
    border: 1px solid #2a303a;
    padding: 28px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 30px rgba(0,0,0,0.5);
}

/* Metric Value */
div[data-testid="stMetricValue"] {
    font-size: 54px !important;
    font-weight: 900 !important;
    letter-spacing: -1px;
    color: #ffffff !important;
}

/* Metric Label */
div[data-testid="stMetricLabel"] {
    font-size: 15px !important;
    font-weight: 600;
    letter-spacing: 0.7px;
    text-transform: uppercase;
    color: #9ca3af !important;
}

/* Title */
.main-title {
    font-size: 58px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
    margin-bottom: 10px;
}

/* Status */
.status-text {
    color: #22c55e;
    font-weight: 600;
    font-size: 14px;
}

/* Signal Simulator Card */
.signal-card {
    border-radius: 16px;
    padding: 25px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.6);
    text-align: center;
    margin-bottom: 20px;
    color: white;
}

.signal-text {
    font-size: 32px;
    font-weight: 800;
    margin-bottom: 10px;
}

.countdown {
    font-size: 22px;
    color: #e5e7eb;
}

.button-style {
    background-color: #3b82f6;
    color: white;
    font-weight: 600;
    border-radius: 12px;
    padding: 8px 18px;
}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("Control Panel")
    st.write("---")
    st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])
    st.file_uploader("Upload Video", type=["mp4", "mov"])
    st.write("---")
    st.markdown("**Signal Simulation Settings**")
    green = st.number_input("Green Duration (s)", min_value=1, value=5)
    yellow = st.number_input("Yellow Duration (s)", min_value=1, value=2)
    red = st.number_input("Red Duration (s)", min_value=1, value=4)

# ---------- HEADER ----------
st.markdown(
    "<h2 class='main-title'>Smart Traffic Monitoring & Analytics</h2>",
    unsafe_allow_html=True
)

st.markdown(
    f"""
    System Node: <b>Vadodara-04</b> |
    Status: <span class="status-text">Operational</span> |
    Time: {time.strftime('%H:%M:%S')}
    """,
    unsafe_allow_html=True
)

st.write("")

# ---------- DATA ----------
total_v = 42
car, bike, bus, truck = 25, 12, 3, 2

# ---------- METRICS ----------
col1, col2, col3, col4 = st.columns(4, gap="medium")
col1.metric("Total Vehicles", total_v)
col2.metric("Cars", car)
col3.metric("Two-Wheelers", bike)
col4.metric("Heavy Vehicles", bus + truck)

st.write("---")

# ---------- ANALYTICS ----------
col_gauge, col_bar = st.columns(2, gap="medium")

with col_gauge:
    st.subheader("Traffic Density Index")
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=total_v,
        gauge={
            "axis": {"range": [0, 60]},
            "bar": {"color": "#3b82f6"},
            "steps": [
                {"range": [0, 20], "color": "#065f46"},
                {"range": [20, 40], "color": "#92400e"},
                {"range": [40, 60], "color": "#991b1b"},
            ],
        }
    ))
    fig_gauge.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "white"},
        height=380
    )
    st.plotly_chart(fig_gauge, use_container_width=True)

with col_bar:
    st.subheader("Vehicle Category Distribution")
    df = pd.DataFrame({
        "Vehicle Type": ["Cars", "Two-Wheelers", "Buses", "Trucks"],
        "Count": [car, bike, bus, truck]
    })
    fig_bar = px.bar(
        df,
        x="Vehicle Type",
        y="Count",
        color="Vehicle Type",
        template="plotly_dark",
        color_discrete_sequence=["#2563eb", "#f97316", "#10b981", "#8b5cf6"]
    )
    fig_bar.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=380,
        showlegend=False
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.write("---")

# ---------- TRAFFIC SIGNAL SIMULATOR ----------
st.subheader("🚦 Live Traffic Signal Simulation")

# Signal container
signal_box = st.empty()

# Start / Stop Buttons
start_col, stop_col = st.columns(2)
start = start_col.button("Start Simulation")
stop = stop_col.button("Stop Simulation")

# Session state for simulation
if "running" not in st.session_state:
    st.session_state.running = False

if start:
    st.session_state.running = True
if stop:
    st.session_state.running = False

# Signal loop
while st.session_state.running:
    # GREEN
    for i in range(green, 0, -1):
        if not st.session_state.running:
            break
        signal_box.markdown(f"""
        <div class="signal-card" style="background-color:#065f46;">
            <div class="signal-text">🟢 GREEN</div>
            <div class="countdown">{i} s remaining</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)

    # YELLOW
    for i in range(yellow, 0, -1):
        if not st.session_state.running:
            break
        signal_box.markdown(f"""
        <div class="signal-card" style="background-color:#b45309;">
            <div class="signal-text">🟡 YELLOW</div>
            <div class="countdown">{i} s remaining</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)

    # RED
    for i in range(red, 0, -1):
        if not st.session_state.running:
            break
        signal_box.markdown(f"""
        <div class="signal-card" style="background-color:#991b1b;">
            <div class="signal-text">🔴 RED</div>
            <div class="countdown">{i} s remaining</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
