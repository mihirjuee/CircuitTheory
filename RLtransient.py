# rl_dc_transient_complete_app.py
# ==========================================================
# RL CIRCUIT DC TRANSIENT ANALYSIS APP
# Complete with:
# ✔ Mobile Responsive Layout
# ✔ RL Circuit Diagram (Schemdraw)
# ✔ Current Growth / Decay
# ✔ Voltage Across R & L
# ✔ Energy Storage
# ✔ Time Constant Visualization
# ==========================================================

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm
from io import BytesIO

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="RL Circuit DC Transient Visualizer",
    page_icon="⚡",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: 'Arial', sans-serif;
}
.main {
    background-color: #f5f9ff;
}
h1, h2, h3 {
    text-align: center;
    color: #003366;
}
.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
}
[data-testid="stMetricValue"] {
    font-size: 28px;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("⚡ RL Circuit DC Transient Analysis")
st.markdown("### Interactive Visualization of Current Growth and Decay in RL Circuit")

# ================= SIDEBAR =================
st.sidebar.header("⚙ Circuit Parameters")

V = st.sidebar.slider("Supply Voltage V (Volts)", 1.0, 500.0, 100.0)
R = st.sidebar.slider("Resistance R (Ω)", 0.1, 100.0, 10.0)
L = st.sidebar.slider("Inductance L (H)", 0.001, 10.0, 1.0)

mode = st.sidebar.radio(
    "Select Operation Mode",
    ["Growth (Switch ON)", "Decay (Switch OFF)"]
)

# ================= CALCULATIONS =================
tau = L / R
I_final = V / R

t_max = 5 * tau
t = np.linspace(0, t_max, 500)

if mode == "Growth (Switch ON)":
    i = I_final * (1 - np.exp(-t / tau))
    vL = V * np.exp(-t / tau)
    vR = V - vL
    current_title = "Current Growth in RL Circuit"
else:
    i0 = I_final
    i = i0 * np.exp(-t / tau)
    vR = i * R
    vL = -vR
    current_title = "Current Decay in RL Circuit"

energy = 0.5 * L * i**2

# ================= METRICS =================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Time Constant (τ=L/R)", f"{tau:.4f} s")

with col2:
    st.metric("Final Current (V/R)", f"{I_final:.4f} A")

with col3:
    st.metric("Transient Completion (5τ)", f"{5*tau:.4f} s")

# ================= RL CIRCUIT DIAGRAM =================
# ================= RL CIRCUIT DIAGRAM WITH DECAY DISCHARGE PATH =================
# Replace your existing circuit diagram block with this

st.subheader("🔌 RL Circuit Diagram")

d = schemdraw.Drawing(show=False)

if mode == "Growth (Switch ON)":
    # ---------------- GROWTH MODE ----------------
    d += elm.SourceV().up().label("V")
    d += elm.Switch(action='close').right().label("S")
    d += elm.Resistor().right().label(f"R = {R} Ω")
    d += elm.Inductor().right().label(f"L = {L} H")
    d += elm.Line().down()
    d += elm.Line().left().left().left()

else:
    # ---------------- DECAY MODE ----------------
    # Battery disconnected, RL closed loop discharge path
    d += elm.Switch(action='open').right().label("S")
    d += elm.Resistor().right().label(f"R = {R} Ω")
    d += elm.Inductor().right().label(f"L = {L} H")
    d += elm.Line().down()
    d += elm.Line().left().left()

    # Complete decay loop
    d += elm.Line().left().up()

    # Current arrow in decay loop
    d += elm.Arrow().right().at((1.8, -1)).label("Discharge Current", loc="bottom")

# Get SVG safely
svg_data = d.get_imagedata("svg").decode()

# Display
st.components.v1.html(svg_data, height=350, scrolling=False)
# ================= THEORY =================
st.subheader("📘 Governing Equations")

if mode == "Growth (Switch ON)":
    st.latex(r"i(t)=\frac{V}{R}\left(1-e^{-t/\tau}\right)")
    st.latex(r"v_L(t)=Ve^{-t/\tau}")
    st.latex(r"v_R(t)=V(1-e^{-t/\tau})")
else:
    st.latex(r"i(t)=I_0e^{-t/\tau}")
    st.latex(r"v_R(t)=Ri(t)")
    st.latex(r"v_L(t)=-Ri(t)")

st.latex(r"\tau=\frac{L}{R}")

# ================= CURRENT GRAPH =================
st.subheader("📈 Current Response")

fig_current = go.Figure()

fig_current.add_trace(go.Scatter(
    x=t,
    y=i,
    mode='lines',
    name='Current i(t)'
))

# Mark tau point
tau_current = I_final * (1 - np.exp(-1)) if mode == "Growth (Switch ON)" else I_final * np.exp(-1)

fig_current.add_vline(
    x=tau,
    line_dash="dash",
    annotation_text="τ"
)

fig_current.update_layout(
    title=current_title,
    xaxis_title="Time (seconds)",
    yaxis_title="Current (Amps)",
    height=500
)

st.plotly_chart(fig_current, use_container_width=True)

# ================= VOLTAGE GRAPH =================
st.subheader("⚡ Voltage Across Resistor and Inductor")

fig_voltage = go.Figure()

fig_voltage.add_trace(go.Scatter(
    x=t,
    y=vR,
    mode='lines',
    name='Voltage Across R'
))

fig_voltage.add_trace(go.Scatter(
    x=t,
    y=vL,
    mode='lines',
    name='Voltage Across L'
))

fig_voltage.add_vline(
    x=tau,
    line_dash="dash",
    annotation_text="τ"
)

fig_voltage.update_layout(
    title="Voltage Transient Response",
    xaxis_title="Time (seconds)",
    yaxis_title="Voltage (Volts)",
    height=500
)

st.plotly_chart(fig_voltage, use_container_width=True)

# ================= ENERGY GRAPH =================
st.subheader("⚙ Energy Stored in Inductor")

fig_energy = go.Figure()

fig_energy.add_trace(go.Scatter(
    x=t,
    y=energy,
    mode='lines',
    name='Energy Stored'
))

fig_energy.update_layout(
    title="Magnetic Energy Storage",
    xaxis_title="Time (seconds)",
    yaxis_title="Energy (Joules)",
    height=500
)

st.plotly_chart(fig_energy, use_container_width=True)

# ================= TRANSIENT STAGES =================
st.subheader("🧠 RL Transient Stages")

st.markdown("""
### During Switching ON:
- Current starts from **0 A**
- Inductor opposes sudden rise
- Current reaches **63.2%** at **t = τ**
- Current reaches steady state at **5τ**

### During Switching OFF:
- Current decays exponentially
- Inductor releases stored magnetic energy
- Opposes sudden drop
- Current approaches zero after **5τ**
""")

# ================= TIME CONSTANT TABLE =================
st.subheader("📊 Time Constant Summary")

percentages = {
    "1τ": "63.2%",
    "2τ": "86.5%",
    "3τ": "95.0%",
    "4τ": "98.2%",
    "5τ": "99.3%"
}

st.table(percentages)

# ================= APPLICATIONS =================
st.subheader("🏭 Applications of RL Circuits")

st.markdown("""
✔ DC Motor Starters  
✔ Relay Coils  
✔ Electromagnetic Systems  
✔ Switching Circuits  
✔ Filters  
✔ Power Electronics  
""")

# ================= FOOTER =================
st.markdown("---")
st.markdown("### Developed for Electrical Engineering Visualization ⚡")
