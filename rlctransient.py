# ================================
# ⚡ RLC TRANSIENT LAB (PREMIUM UI)
# ================================

import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="RLC Transient Lab", page_icon="logo.png", layout="wide")

# --- CUSTOM STYLE ---
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3 {
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("⚡ RLC Transient Analysis (Series Circuit)")
st.markdown("### 🔬 Visualize damping, oscillation & energy exchange")

# =====================================
# 🔧 SIDEBAR
# =====================================
st.sidebar.header("🔧 Circuit Parameters")

R = st.sidebar.slider("Resistance R (Ω)", 0.1, 100.0, 10.0)
L = st.sidebar.slider("Inductance L (H)", 0.001, 1.0, 0.1)
C_micro = st.sidebar.slider("Capacitance (μF)", 1.0, 1000.0, 100.0)
C = C_micro * 1e-6
V = st.sidebar.slider("Step Voltage (V)", 1.0, 500.0, 100.0)

# NEW: Switch Control
switch_closed = st.sidebar.toggle("🔘 Close Switch", value=True)

# NEW: More Cycles Control
cycles = st.sidebar.slider("📡 Display Cycles", 1, 20, 8)

# =====================================
# ⚙️ CALCULATIONS
# =====================================
alpha = R / (2 * L)
omega_0 = 1 / np.sqrt(L * C)

# More time span based on cycles
T0 = 2 * np.pi / omega_0
t_max = cycles * T0
t = np.linspace(0, t_max, 5000)

# --- INITIALIZE ---
i = np.zeros_like(t)
v_c = np.zeros_like(t)
response = ""
color_resp = ""

# If switch open → no response
if not switch_closed:
    i = np.zeros_like(t)
    v_c = np.zeros_like(t)
    response = "⚪ Switch Open"
    color_resp = "white"

else:
    # --- RESPONSE + WAVEFORMS ---
    if alpha < omega_0:
        # 🟢 UNDERDAMPED
        omega_d = np.sqrt(omega_0**2 - alpha**2)

        i = (V / L) * (1 / omega_d) * np.exp(-alpha * t) * np.sin(omega_d * t)

        v_c = V * (
            1
            - np.exp(-alpha * t)
            * (
                np.cos(omega_d * t)
                + (alpha / omega_d) * np.sin(omega_d * t)
            )
        )

        response = "🟢 Underdamped"
        color_resp = "lime"

    elif abs(alpha - omega_0) < 1e-3:
        # 🟡 CRITICALLY DAMPED
        i = (V / L) * t * np.exp(-alpha * t)

        v_c = V * (1 - (1 + alpha * t) * np.exp(-alpha * t))

        response = "🟡 Critically Damped"
        color_resp = "yellow"

    else:
        # 🔴 OVERDAMPED
        s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
        s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)

        i = (V / L) * (np.exp(s1 * t) - np.exp(s2 * t)) / (s1 - s2)

        v_c = V * (
            1 - ((s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1))
        )

        response = "🔴 Overdamped"
        color_resp = "red"

# --- ENERGY ---
W_L = 0.5 * L * i**2
W_C = 0.5 * C * v_c**2

# =====================================
# 📊 METRICS
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("Damping Factor α", f"{alpha:.2f}")
col2.metric("Natural Frequency ω₀", f"{omega_0:.2f}")
col3.markdown(
    f"<h3 style='color:{color_resp}'>{response}</h3>",
    unsafe_allow_html=True
)

# =====================================
# 🔌 CIRCUIT DIAGRAM
# =====================================
st.subheader("🔌 RLC Circuit with Switch")

fig_circ, ax = plt.subplots(figsize=(12, 3))

# --- SOURCE ---
circle = plt.Circle((0.3, 0.5), 0.1, fill=False, linewidth=2)
ax.add_patch(circle)
ax.text(0.15, 0.75, f"{V:.0f} V", fontsize=11)

# --- LEFT WIRE ---
ax.plot([0, 0], [0.1, 0.5], linewidth=2)
ax.plot([0, 0.3], [0.1, 0.1], linewidth=2)

# --- SWITCH ---
ax.plot([0.4, 0.7], [0.5, 0.5], linewidth=2)

if switch_closed:
    # Closed switch
    ax.plot([0.7, 1.0], [0.5, 0.5], linewidth=2, color='green')
else:
    # Open switch
    ax.plot([0.7, 1.0], [0.5, 0.7], linewidth=2, color='red')

ax.text(0.65, 0.8, "Switch")

# --- RESISTOR ---
x = np.linspace(1.0, 2.0, 10)
y = 0.5 + 0.1 * np.sin(10 * np.pi * (x - 1.0))
ax.plot(x, y, linewidth=2)
ax.text(1.4, 0.8, f"R={R:.1f}Ω")

# --- INDUCTOR ---
theta = np.linspace(0, 4 * np.pi, 200)
x_coil = 2.0 + 0.6 * theta / (4 * np.pi)
y_coil = 0.5 + 0.1 * np.sin(theta)
ax.plot(x_coil, y_coil, linewidth=2)
ax.text(2.2, 0.8, f"L={L:.2f}H")

# --- CAPACITOR ---
ax.plot([2.6, 2.8], [0.5, 0.5], linewidth=2)
ax.plot([2.8, 2.8], [0.3, 0.7], linewidth=2)
ax.plot([3.0, 3.0], [0.3, 0.7], linewidth=2)
ax.plot([3.0, 3.2], [0.5, 0.5], linewidth=2)
ax.text(2.75, 0.8, f"C={C_micro:.0f}μF")

# --- RETURN PATH ---
ax.plot([3.2, 3.2], [0.5, 0.1], linewidth=2)
ax.plot([3.2, 0], [0.1, 0.1], linewidth=2)

# --- CURRENT ARROW ---
if switch_closed:
    ax.arrow(
        1.2, 0.95, 1.0, 0,
        head_width=0.05,
        head_length=0.1,
        linewidth=2
    )
    ax.text(1.6, 1.05, "i(t)", fontsize=12)

# --- FINAL SETTINGS ---
ax.set_xlim(-0.2, 3.5)
ax.set_ylim(0, 1.2)
ax.axis('off')

st.pyplot(fig_circ, clear_figure=True)

# =====================================
# 📈 CURRENT RESPONSE
# =====================================
st.subheader("📈 Transient Current")

fig1, ax1 = plt.subplots(figsize=(10, 5))

ax1.plot(t, i, linewidth=2, label="Current i(t)")
ax1.fill_between(t, i, alpha=0.2)

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Current (A)")
ax1.set_title("Current Response Over Multiple Cycles")
ax1.grid()
ax1.axhline(0, linestyle='--')
ax1.legend()

st.pyplot(fig1)

# =====================================
# ⚡ CAPACITOR VOLTAGE
# =====================================
st.subheader("⚡ Capacitor Voltage")

figv, axv = plt.subplots(figsize=(10, 5))

axv.plot(t, v_c, linewidth=2, label="Vc(t)")
axv.fill_between(t, v_c, alpha=0.2)

axv.set_xlabel("Time (s)")
axv.set_ylabel("Voltage (V)")
axv.set_title("Capacitor Voltage Response")
axv.grid()
axv.legend()

st.pyplot(figv)

# =====================================
# ⚡ ENERGY FLOW
# =====================================
st.subheader("⚡ Energy Exchange")

fig2, ax2 = plt.subplots(figsize=(10, 5))

ax2.plot(t, W_L, label="Inductor Energy")
ax2.plot(t, W_C, label="Capacitor Energy")

ax2.fill_between(t, W_L, alpha=0.1)
ax2.fill_between(t, W_C, alpha=0.1)

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Energy (J)")
ax2.set_title("Energy Oscillation")
ax2.legend()
ax2.grid()

st.pyplot(fig2)

# =====================================
# 🎯 INTERPRETATION PANEL
# =====================================
st.subheader("🧠 Concept Insight")

if not switch_closed:
    msg = "Switch open → No transient response because circuit is incomplete."
elif alpha < omega_0:
    msg = "Energy oscillates between L and C → sinusoidal decay over multiple cycles."
elif abs(alpha - omega_0) < 1e-3:
    msg = "Fastest return to steady state without oscillation."
else:
    msg = "Highly damped → slow energy dissipation."

st.markdown(
    f"<div style='color:cyan; font-size:18px; font-weight:bold'>{msg}</div>",
    unsafe_allow_html=True
)

# =====================================
# 🧪 INTERACTIVE QUESTION
# =====================================
st.subheader("❓ Think & Explore")

st.markdown("""
👉 Why does oscillation disappear when resistance increases?  

👉 What happens if R → 0?  

👉 Where is energy stored at peak current?  

👉 How does opening the switch affect current flow?
""")

# =====================================
# 📌 FOOTER
# =====================================
st.markdown("---")
st.markdown("Built for intuitive learning ⚡ | Explore, visualize, understand.")
