# --- FIX STREAMLIT RENDERING ---
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="RLC Transient Lab", layout="wide")

st.title("⚡ RLC Transient Analysis")

# =========================================================
# 🔧 INPUTS
# =========================================================
st.sidebar.header("Circuit Parameters")

R = st.sidebar.slider("Resistance R (Ω)", 0.1, 100.0, 10.0)
L = st.sidebar.slider("Inductance L (H)", 0.001, 1.0, 0.1)
C_micro = st.sidebar.slider("Capacitance (μF)", 1.0, 1000.0, 100.0)
C = C_micro * 1e-6

V = st.sidebar.slider("Step Voltage (V)", 1.0, 500.0, 100.0)

# =========================================================
# ⚙️ CALCULATIONS
# =========================================================
alpha = R / (2 * L)
omega_0 = 1 / np.sqrt(L * C)

t = np.linspace(0, 0.1, 1000)

# --- RESPONSE ---
if alpha < omega_0:
    omega_d = np.sqrt(omega_0**2 - alpha**2)
    i = (V / L) * (1/omega_d) * np.exp(-alpha*t) * np.sin(omega_d*t)
    response = "🟢 Underdamped"

elif abs(alpha - omega_0) < 1e-3:
    i = (V / L) * t * np.exp(-alpha*t)
    response = "🟡 Critically Damped"

else:
    s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
    s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)
    i = (V / L) * (np.exp(s1*t) - np.exp(s2*t)) / (s1 - s2)
    response = "🔴 Overdamped"

# =========================================================
# 🔌 SIMPLE CIRCUIT (NO SCHEMDRAW → NO ERROR)
# =========================================================
st.subheader("🔌 RLC Series Circuit")

fig_c, ax_c = plt.subplots()

ax_c.text(0.1, 0.5, "V", fontsize=14)
ax_c.text(0.3, 0.5, f"R = {R:.1f}Ω", fontsize=12)
ax_c.text(0.5, 0.5, f"L = {L:.3f}H", fontsize=12)
ax_c.text(0.7, 0.5, f"C = {C_micro:.1f}μF", fontsize=12)

ax_c.plot([0.05, 0.85], [0.5, 0.5])  # wire
ax_c.set_title("Series RLC Circuit (Conceptual)")
ax_c.axis('off')

st.pyplot(fig_c)

# =========================================================
# 📊 METRICS
# =========================================================
col1, col2, col3 = st.columns(3)
col1.metric("Damping α", f"{alpha:.2f}")
col2.metric("Natural Frequency ω₀", f"{omega_0:.2f}")
col3.metric("Response", response)

# =========================================================
# 📈 CURRENT RESPONSE
# =========================================================
st.subheader("📈 Current Response")

fig1, ax1 = plt.subplots()
ax1.plot(t, i)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Current (A)")
ax1.grid()

st.pyplot(fig1)

# =========================================================
# ⚡ ENERGY
# =========================================================
W_L = 0.5 * L * i**2
v_c = V * (1 - np.exp(-alpha*t))
W_C = 0.5 * C * v_c**2

st.subheader("⚡ Energy Exchange")

fig2, ax2 = plt.subplots()
ax2.plot(t, W_L, label="Inductor")
ax2.plot(t, W_C, label="Capacitor")
ax2.legend()
ax2.grid()

st.pyplot(fig2)

# =========================================================
# 🧠 INTERPRETATION
# =========================================================
st.subheader("🧠 Interpretation")

if alpha < omega_0:
    st.success("Oscillatory (Underdamped)")
elif abs(alpha - omega_0) < 1e-3:
    st.warning("Fastest without oscillation")
else:
    st.error("Slow non-oscillatory response")
