import streamlit as st
import numpy as np
import plotly.graph_objects as go
import schemdraw
import schemdraw.elements as elm

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="RL Circuit DC Transient Visualizer",
    page_icon="⚡",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
    .main { background-color: #f5f9ff; }
    h1, h2, h3 { text-align: center; color: #003366; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #007bff; }
</style>
""", unsafe_allow_html=True)

# ================= CACHED CIRCUIT DRAWING =================
# ================= RL CIRCUIT =================
# active_path = "growth"  -> Supply connected (current growth)
# active_path = "decay"   -> Supply disconnected, RL discharge loop

def draw_circuit(active_path="growth"):
    import schemdraw
    import schemdraw.elements as elm

    d = schemdraw.Drawing(unit=1.2)

    # ---------------- BATTERY ----------------
    d += elm.SourceV().up().label("V")

    # ---------------- TOP NODE ----------------
    d += elm.Line().right()
    d += elm.Dot()

    # ---------------- MAIN SWITCH ----------------
    if active_path == "growth":
        sw = elm.Switch(action='close').right().label("Close")
    else:
        sw = elm.Switch(action='open').right().label("Open")

    d += sw

    # Save position after switch
    d.push()

    # =====================================================
    # RL MAIN BRANCH (Used during growth and visible always)
    # =====================================================
    d += elm.Line().right()
    d += elm.Resistor().down().label("R")
    d += elm.Inductor().down().label("L")

    # Bottom return to source
    d += elm.Line().left(3.6)
    d += elm.Line().up(1.2)

    # =====================================================
    # DECAY / DISCHARGE PATH
    # =====================================================
    if active_path == "decay":
        # Return to node after main switch
        d.pop()

        # Downward branch for discharge loop
        d += elm.Line().down(0.3)

        # Secondary closed discharge switch
        d += elm.Switch(action='close').down().label("Discharge")

        # Connect to lower RL loop
        d += elm.Line().down(0.9)

    return d

# ================= TITLE & SIDEBAR =================
st.title("⚡ RL Circuit DC Transient Analysis")

st.sidebar.header("⚙ Circuit Parameters")
V = st.sidebar.slider("Supply Voltage V (Volts)", 1.0, 500.0, 100.0)
R = st.sidebar.slider("Resistance R (Ω)", 0.1, 100.0, 10.0)
L = st.sidebar.slider("Inductance L (H)", 0.001, 10.0, 1.0)
mode = st.sidebar.radio("Select Operation Mode", ["Growth (Switch ON)", "Decay (Switch OFF)"])

# ================= CALCULATIONS =================
# Safety check to avoid division by zero
R_safe = max(R, 1e-9)
tau = L / R_safe
I_final = V / R_safe
t_max = 5 * tau
t = np.linspace(0, t_max, 500)

if mode == "Growth (Switch ON)":
    i = I_final * (1 - np.exp(-t / tau))
    vL = V * np.exp(-t / tau)
    vR = V - vL
    target_val = I_final * 0.632
    target_label = "63.2% (τ)"
    current_title = "Current Growth: i(t) = I[1 - e^(-t/τ)]"
else:
    i = I_final * np.exp(-t / tau)
    vR = i * R
    vL = -vR
    target_val = I_final * 0.368
    target_label = "36.8% (τ)"
    current_title = "Current Decay: i(t) = I₀e^(-t/τ)"

energy = 0.5 * L * i**2

# ================= METRICS =================
m1, m2, m3 = st.columns(3)
m1.metric("Time Constant (τ)", f"{tau:.4f} s")
m2.metric("Steady State Current", f"{I_final:.2f} A")
m3.metric("Settling Time (5τ)", f"{5*tau:.4f} s")

# ================= VISUALS =================
col_diag, col_theory = st.columns([1, 1])

with col_diag:
    st.subheader("🔌 Circuit Diagram")
    svg = draw_circuit(mode, R, L)
    st.components.v1.html(f"<div style='display:flex;justify-content:center;'>{svg}</div>", height=250)

with col_theory:
    st.subheader("📘 Governing Equations")
    if mode == "Growth (Switch ON)":
        st.latex(r"i(t) = \frac{V}{R}(1 - e^{-t/\tau})")
        st.latex(r"v_L(t) = V e^{-t/\tau}")
    else:
        st.latex(r"i(t) = I_0 e^{-t/\tau}")
        st.latex(r"v_L(t) = -Ri(t)")
    st.latex(r"\tau = \frac{L}{R}")

# ================= GRAPHS =================
# Current Plot
fig_i = go.Figure()
fig_i.add_trace(go.Scatter(x=t, y=i, name="Current i(t)", line=dict(color='#1f77b4', width=3)))
fig_i.add_vline(x=tau, line_dash="dash", line_color="red", annotation_text="τ")
fig_i.add_hline(y=target_val, line_dash="dot", line_color="gray", annotation_text=target_label)
fig_i.update_layout(title=current_title, xaxis_title="Time (s)", yaxis_title="Current (A)", height=400)
st.plotly_chart(fig_i, use_container_width=True)

# Voltage & Energy Plots
c1, c2 = st.columns(2)

with c1:
    fig_v = go.Figure()
    fig_v.add_trace(go.Scatter(x=t, y=vR, name="vR (Resistor)"))
    fig_v.add_trace(go.Scatter(x=t, y=vL, name="vL (Inductor)"))
    fig_v.update_layout(title="Voltage Response", xaxis_title="Time (s)", yaxis_title="Volts (V)", height=400)
    st.plotly_chart(fig_v, use_container_width=True)

with c2:
    fig_e = go.Figure()
    fig_e.add_trace(go.Scatter(x=t, y=energy, name="Energy", fill='tozeroy', line_color='green'))
    fig_e.update_layout(title="Stored Magnetic Energy", xaxis_title="Time (s)", yaxis_title="Joules (J)", height=400)
    st.plotly_chart(fig_e, use_container_width=True)

# ================= FOOTER =================
st.markdown("---")
st.markdown("### 📊 Quick Reference")
st.table({
    "Time": ["1τ", "2τ", "3τ", "4τ", "5τ"],
    "Growth %": ["63.2%", "86.5%", "95.0%", "98.2%", "99.3%"],
    "Decay %": ["36.8%", "13.5%", "5.0%", "1.8%", "0.7%"]
})
