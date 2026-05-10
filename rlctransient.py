# ================================
# ⚡ RLC TRANSIENT LAB (PREMIUM UI)
# ================================

import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="RLC Transient Lab",
    page_icon="logo.png",
    layout="wide"
)

# =====================================
# 🎨 CUSTOM STYLE
# =====================================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
h1, h2, h3 {
    text-align: center;
}
div[data-testid="stMetricValue"] {
    color: cyan;
}
</style>
""", unsafe_allow_html=True)

# =====================================
# 🏷️ TITLE
# =====================================
st.title("⚡ RLC Transient Analysis (Series Circuit)")
st.markdown("### 🔬 Visualize damping, oscillation, instability & energy exchange")

# =====================================
# 🔧 SIDEBAR
# =====================================
st.sidebar.header("🔧 Circuit Parameters")

R = st.sidebar.slider("Resistance R (Ω)", 0.0, 100.0, 10.0, 0.01)
L = st.sidebar.slider("Inductance L (H)", 0.001, 1.0, 0.1)
C_micro = st.sidebar.slider("Capacitance (μF)", 1.0, 1000.0, 100.0)

C = C_micro * 1e-6

V = st.sidebar.slider("Step Voltage (V)", 1.0, 500.0, 100.0)

switch_closed = st.sidebar.toggle("🔘 Close Switch", value=True)

cycles = st.sidebar.slider("📡 Display Cycles", 1, 20, 8)

# =====================================
# ⚙️ CALCULATIONS
# =====================================
alpha = R / (2 * L)
omega_0 = 1 / np.sqrt(L * C)

R_critical = 2 * np.sqrt(L / C)

# Time base
T0 = 2 * np.pi / omega_0
t_max = cycles * T0
t = np.linspace(0, t_max, 5000)

# Initialize
i = np.zeros_like(t)
v_c = np.zeros_like(t)

response = ""
color_resp = ""

# =====================================
# 🔍 RESPONSE CLASSIFICATION
# =====================================
if not switch_closed:
    response = "⚪ Switch Open"
    color_resp = "white"

elif R <= 0.05:
    # 🔵 Ideal LC sustained oscillation
    omega = omega_0

    i = (V / L) * (1 / omega) * np.sin(omega * t)

    v_c = V * (1 - np.cos(omega * t))

    response = "🔵 Unstable / Sustained Oscillation"
    color_resp = "cyan"

elif alpha < omega_0:
    # 🟢 Oscillatory underdamped
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

    response = "🟢 Oscillatory / Underdamped"
    color_resp = "lime"

elif abs(R - R_critical) <= 0.5:
    # 🟡 Critically damped
    i = (V / L) * t * np.exp(-alpha * t)

    v_c = V * (1 - (1 + alpha * t) * np.exp(-alpha * t))

    response = "🟡 Critically Damped"
    color_resp = "yellow"

else:
    # 🔴 Overdamped
    s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
    s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)

    i = (V / L) * (np.exp(s1 * t) - np.exp(s2 * t)) / (s1 - s2)

    v_c = V * (
        1 - ((s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s2 - s1))
    )

    response = "🔴 Overdamped"
    color_resp = "red"

# =====================================
# ⚡ ENERGY
# =====================================
W_L = 0.5 * L * i**2
W_C = 0.5 * C * v_c**2

# =====================================
# 📊 METRICS
# =====================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Damping Factor α", f"{alpha:.3f}")
col2.metric("Natural Frequency ω₀", f"{omega_0:.2f}")
col3.metric("Critical Resistance", f"{R_critical:.2f} Ω")

col4.markdown(
    f"<h3 style='color:{color_resp}'>{response}</h3>",
    unsafe_allow_html=True
)

# =====================================
# 🔌 CIRCUIT DIAGRAM
# =====================================
st.subheader("🔌 RLC Circuit with Switch")

fig_circ, ax = plt.subplots(figsize=(14, 3))

# Source
circle = plt.Circle((0.3, 0.5), 0.1, fill=False, linewidth=2)
ax.add_patch(circle)
ax.text(0.15, 0.75, f"{V:.0f} V", fontsize=11)

# Left vertical wire
ax.plot([0, 0], [0.1, 0.5], linewidth=2)

# Bottom wire
ax.plot([0, 0.3], [0.1, 0.1], linewidth=2)

# Switch wire
ax.plot([0.4, 0.7], [0.5, 0.5], linewidth=2)

if switch_closed:
    ax.plot([0.7, 1.0], [0.5, 0.5], linewidth=3, color='green')
else:
    ax.plot([0.7, 1.0], [0.5, 0.7], linewidth=3, color='red')

ax.text(0.65, 0.82, "Switch")

# Resistor
x = np.linspace(1.0, 2.0, 12)
y = 0.5 + 0.1 * np.sin(12 * np.pi * (x - 1.0))
ax.plot(x, y, linewidth=2)
ax.text(1.35, 0.82, f"R={R:.2f}Ω")

# Inductor
theta = np.linspace(0, 4 * np.pi, 300)
x_coil = 2.0 + 0.7 * theta / (4 * np.pi)
y_coil = 0.5 + 0.1 * np.sin(theta)
ax.plot(x_coil, y_coil, linewidth=2)
ax.text(2.25, 0.82, f"L={L:.3f}H")

# Capacitor
ax.plot([2.7, 2.9], [0.5, 0.5], linewidth=2)
ax.plot([2.9, 2.9], [0.3, 0.7], linewidth=2)
ax.plot([3.1, 3.1], [0.3, 0.7], linewidth=2)
ax.plot([3.1, 3.3], [0.5, 0.5], linewidth=2)

ax.text(2.85, 0.82, f"C={C_micro:.0f}μF")

# Return path
ax.plot([3.3, 3.3], [0.5, 0.1], linewidth=2)
ax.plot([3.3, 0], [0.1, 0.1], linewidth=2)

# Current arrow
if switch_closed:
    ax.arrow(
        1.2, 1.0, 1.0, 0,
        head_width=0.05,
        head_length=0.08,
        linewidth=2
    )
    ax.text(1.65, 1.08, "i(t)", fontsize=12)

# Final settings
ax.set_xlim(-0.2, 3.6)
ax.set_ylim(0, 1.2)
ax.axis('off')

st.pyplot(fig_circ)

# =====================================
# 📈 CURRENT RESPONSE
# =====================================
st.subheader("📈 Transient Current Response")

fig1, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(t, i, linewidth=2, label="Current i(t)")
ax1.fill_between(t, i, alpha=0.2)

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Current (A)")
ax1.set_title("Current vs Time")
ax1.grid()
ax1.axhline(0, linestyle='--')
ax1.legend()

st.pyplot(fig1)

# =====================================
# ⚡ CAPACITOR VOLTAGE
# =====================================
st.subheader("⚡ Capacitor Voltage Response")

figv, axv = plt.subplots(figsize=(12, 5))

axv.plot(t, v_c, linewidth=2, label="Vc(t)")
axv.fill_between(t, v_c, alpha=0.2)

axv.set_xlabel("Time (s)")
axv.set_ylabel("Voltage (V)")
axv.set_title("Capacitor Voltage vs Time")
axv.grid()
axv.legend()

st.pyplot(figv)

# =====================================
# ⚡ ENERGY EXCHANGE
# =====================================
st.subheader("⚡ Energy Exchange Between L & C")

fig2, ax2 = plt.subplots(figsize=(12, 5))

ax2.plot(t, W_L, label="Inductor Energy")
ax2.plot(t, W_C, label="Capacitor Energy")

ax2.fill_between(t, W_L, alpha=0.1)
ax2.fill_between(t, W_C, alpha=0.1)

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Energy (J)")
ax2.set_title("Energy Oscillation")
ax2.grid()
ax2.legend()

st.pyplot(fig2)

# =====================================
# 🧠 INSIGHT PANEL
# =====================================
st.subheader("🧠 Concept Insight")

if not switch_closed:
    msg = "Switch open → Circuit incomplete → No transient."
elif R <= 0.05:
    msg = "Zero resistance → Pure LC resonance → Sustained oscillation (ideal instability)."
elif alpha < omega_0:
    msg = "Underdamped → Energy oscillates between inductor and capacitor with gradual decay."
elif abs(R - R_critical) <= 0.5:
    msg = "Critical damping → Fastest response without oscillation."
else:
    msg = "Overdamped → Heavy resistance suppresses oscillation."

st.markdown(
    f"<div style='color:cyan; font-size:20px; font-weight:bold'>{msg}</div>",
    unsafe_allow_html=True
)

# =====================================
# ❓ THINK & EXPLORE
# =====================================
st.subheader("❓ Think & Explore")

st.markdown("""
👉 Why does oscillation disappear as resistance increases?  

👉 Why is critical damping considered optimal?  

👉 What happens when resistance becomes zero?  

👉 At peak current, where is most energy stored?  

👉 How does capacitor voltage behave in overdamped response?
""")

# =====================================
# 📌 FOOTER
# =====================================
st.markdown("---")
st.markdown("### Built for intuitive learning ⚡ | Explore • Visualize • Understand")
