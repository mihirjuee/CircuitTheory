# --- IMPORTANT (fixes Streamlit cloud errors) ---
import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# --- PAGE CONFIG ---
st.set_page_config(page_title="RLC Transient Lab", layout="wide")

st.title("⚡ RLC Transient Analysis (Series Circuit)")

# --- SIDEBAR ---
st.sidebar.header("🔧 Circuit Parameters")

R = st.sidebar.slider("Resistance R (Ω)", 0.1, 100.0, 10.0)
L = st.sidebar.slider("Inductance L (H)", 0.001, 1.0, 0.1)
C_micro = st.sidebar.slider("Capacitance (μF)", 1.0, 1000.0, 100.0)
C = C_micro * 1e-6

V = st.sidebar.slider("Step Voltage (V)", 1.0, 500.0, 100.0)

# --- CALCULATIONS ---
alpha = R / (2 * L)
omega_0 = 1 / np.sqrt(L * C)

# Time axis
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

# --- ENERGY ---
W_L = 0.5 * L * i**2
v_c = V * (1 - np.exp(-alpha*t))  # approx
W_C = 0.5 * C * v_c**2

# --- METRICS ---
col1, col2, col3 = st.columns(3)
col1.metric("Damping Factor α", f"{alpha:.2f}")
col2.metric("Natural Frequency ω₀", f"{omega_0:.2f}")
col3.metric("Response Type", response)

# =========================================================
# 🔌 CIRCUIT DIAGRAM (ERROR-FREE)
# =========================================================
st.subheader("🔌 RLC Circuit")

d = schemdraw.Drawing(unit=2.5)

d += elm.SourceSin().label(f"{V:.1f} V (Step)")
d += elm.Resistor().right().label(f"R = {R:.1f} Ω")
d += elm.Inductor().right().label(f"L = {L:.3f} H")
d += elm.Capacitor().right().label(f"C = {C_micro:.1f} μF")

d += elm.Line().down()
d += elm.Line().left().length(6)
d += elm.Ground()

# --- SAFE DRAW ---
fig_circuit = d.draw()

# Ensure matplotlib figure
if hasattr(fig_circuit, "figure"):
    fig_circuit = fig_circuit.figure

# Resize safely
try:
    fig_circuit.set_size_inches(10, 3)
except:
    pass

st.pyplot(fig_circuit)

# =========================================================
# 📈 CURRENT RESPONSE
# =========================================================
st.subheader("📈 Current Response")

fig1, ax1 = plt.subplots()
ax1.plot(t, i, linewidth=2)
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("Current (A)")
ax1.set_title("Transient Current")
ax1.grid()

st.pyplot(fig1)

# =========================================================
# ⚡ ENERGY PLOT
# =========================================================
st.subheader("⚡ Energy Exchange")

fig2, ax2 = plt.subplots()
ax2.plot(t, W_L, label="Inductor Energy")
ax2.plot(t, W_C, label="Capacitor Energy")

ax2.set_xlabel("Time (s)")
ax2.set_ylabel("Energy (J)")
ax2.set_title("Energy Storage")
ax2.legend()
ax2.grid()

st.pyplot(fig2)

# =========================================================
# 🧠 INTERPRETATION
# =========================================================
st.subheader("🧠 Interpretation")

if alpha < omega_0:
    st.success("Oscillatory response → Energy exchanges between L and C.")
elif abs(alpha - omega_0) < 1e-3:
    st.warning("Fastest response without oscillation.")
else:
    st.error("Slow response, no oscillation.")

# =========================================================
# 🎯 EXTRA INFO
# =========================================================
st.markdown("### 📌 Key Concepts")

st.markdown(f"""
- Damping Factor (α) = {alpha:.3f}  
- Natural Frequency (ω₀) = {omega_0:.3f} rad/s  

👉 **Condition:**
- Underdamped → α < ω₀  
- Critically damped → α = ω₀  
- Overdamped → α > ω₀  
""")
