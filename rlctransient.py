# ================================
# ⚡ RLC TRANSIENT LAB (PREMIUM UI)
# ================================

import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="RLC Transient Lab",page_icon="logo.png", layout="wide")

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

# =====================================
# ⚙️ CALCULATIONS
# =====================================
alpha = R / (2 * L)
omega_0 = 1 / np.sqrt(L * C)

t = np.linspace(0, 0.1, 2000)

# --- RESPONSE ---
# --- ENERGY + CAPACITOR VOLTAGE ---

if alpha < omega_0:
    omega_d = np.sqrt(omega_0**2 - alpha**2)

    v_c = V * (
        1
        - np.exp(-alpha*t) * (
            np.cos(omega_d*t)
            + (alpha/omega_d)*np.sin(omega_d*t)
        )
    )

elif abs(alpha - omega_0) < 1e-3:
    v_c = V * (1 - (1 + alpha*t)*np.exp(-alpha*t))

else:
    s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
    s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)

    v_c = V * (
        1 - ( (s2*np.exp(s1*t) - s1*np.exp(s2*t)) / (s2 - s1) )
    )

# --- ENERGY ---
W_L = 0.5 * L * i**2
W_C = 0.5 * C * v_c**2

# =====================================
# 📊 METRICS
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("Damping Factor α", f"{alpha:.2f}")
col2.metric("Natural Frequency ω₀", f"{omega_0:.2f}")
col3.markdown(f"<h3 style='color:{color_resp}'>{response}</h3>", unsafe_allow_html=True)


# --- CIRCUIT DIAGRAM ---
st.subheader("🔌 RLC Circuit")

fig_circ, ax = plt.subplots(figsize=(10, 3))

# --- WIRE START ---
ax.plot([0, 0.5], [0.5, 0.5], linewidth=2)

# --- SOURCE (circle) ---
circle = plt.Circle((0.3, 0.5), 0.1, fill=False, linewidth=2)
ax.add_patch(circle)
ax.text(0.15, 0.75, f"{V:.0f} V", fontsize=11)

# --- RESISTOR (zigzag) ---
x = np.linspace(0.5, 1.5, 10)
y = 0.5 + 0.1 * np.sin(10 * np.pi * (x - 0.5))
ax.plot(x, y, linewidth=2)
ax.text(0.9, 0.8, f"R={R:.1f}Ω")

# --- INDUCTOR (coil) ---
theta = np.linspace(0, 4*np.pi, 200)
x_coil = 1.5 + 0.4 * theta/(4*np.pi)
y_coil = 0.5 + 0.1 * np.sin(theta)
ax.plot(x_coil, y_coil, linewidth=2)
ax.text(1.8, 0.8, f"L={L:.2f}H")

# --- CAPACITOR (plates) ---
ax.plot([2.0, 2.2], [0.5, 0.5], linewidth=2)
ax.plot([2.2, 2.2], [0.3, 0.7], linewidth=2)
ax.plot([2.4, 2.4], [0.3, 0.7], linewidth=2)
ax.plot([2.4, 2.6], [0.5, 0.5], linewidth=2)
ax.text(2.1, 0.8, f"C={C_micro:.0f}μF")

# --- RETURN PATH ---
ax.plot([2.6, 2.6], [0.5, 0.1], linewidth=2)
ax.plot([2.6, 0], [0.1, 0.1], linewidth=2)
ax.plot([0, 0], [0.1, 0.5], linewidth=2)

# --- FINAL SETTINGS ---
ax.set_xlim(-0.2, 3)
ax.set_ylim(0, 1)
ax.axis('off')

st.pyplot(fig_circ, clear_figure=True)

# =====================================
# 📈 CURRENT RESPONSE
# =====================================
st.subheader("📈 Transient Current")

fig1, ax1 = plt.subplots()

ax1.plot(t, i, linewidth=2)
ax1.fill_between(t, i, alpha=0.2)

ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Current (A)")
ax1.set_title("Current Response")
ax1.grid()

# Highlight oscillation decay
ax1.axhline(0, linestyle='--')

st.pyplot(fig1)

# =====================================
# ⚡ ENERGY FLOW
# =====================================
st.subheader("⚡ Energy Exchange")

fig2, ax2 = plt.subplots()

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

if alpha < omega_0:
    msg = "Energy oscillates between L and C → sinusoidal decay."
elif abs(alpha - omega_0) < 1e-3:
    msg = "Fastest return to steady state without oscillation."
else:
    msg = "Highly damped → slow energy dissipation."

st.markdown(
    f"<div style='color:red; font-size:18px; font-weight:bold'>{msg}</div>",
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
""")

# =====================================
# 📌 FOOTER
# =====================================
st.markdown("---")
st.markdown("Built for intuitive learning ⚡ | Explore, visualize, understand.")
