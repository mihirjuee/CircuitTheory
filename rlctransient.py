# ================================
# ⚡ RLC TRANSIENT LAB (PREMIUM UI)
# ================================

import matplotlib
matplotlib.use('Agg')

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- PAGE CONFIG ---
st.set_page_config(page_title="RLC Transient Lab", layout="wide")

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
if alpha < omega_0:
    omega_d = np.sqrt(omega_0**2 - alpha**2)
    i = (V / L) * (1/omega_d) * np.exp(-alpha*t) * np.sin(omega_d*t)
    response = "🟢 Underdamped"
    color_resp = "lime"

elif abs(alpha - omega_0) < 1e-3:
    i = (V / L) * t * np.exp(-alpha*t)
    response = "🟡 Critically Damped"
    color_resp = "yellow"

else:
    s1 = -alpha + np.sqrt(alpha**2 - omega_0**2)
    s2 = -alpha - np.sqrt(alpha**2 - omega_0**2)
    i = (V / L) * (np.exp(s1*t) - np.exp(s2*t)) / (s1 - s2)
    response = "🔴 Overdamped"
    color_resp = "red"

# --- ENERGY ---
W_L = 0.5 * L * i**2
v_c = V * (1 - np.exp(-alpha*t))
W_C = 0.5 * C * v_c**2

# =====================================
# 📊 METRICS
# =====================================
col1, col2, col3 = st.columns(3)

col1.metric("Damping Factor α", f"{alpha:.2f}")
col2.metric("Natural Frequency ω₀", f"{omega_0:.2f}")
col3.markdown(f"<h3 style='color:{color_resp}'>{response}</h3>", unsafe_allow_html=True)


# --- CIRCUIT DIAGRAM ---
st.subheader("🔌 RLC Series Circuit")

def draw_circuit(V, R, L, C_m):
    # Create figure and axis explicitly
    fig, ax = plt.subplots(figsize=(10, 2))
    
    # Helper function for components to keep code clean
    def draw_comp(x1, x2, label):
        ax.plot([x1, x2], [0.5, 0.5], 'k-', lw=2)
        ax.text((x1+x2)/2, 0.6, label, ha='center', fontweight='bold')

    # Draw circuit components
    draw_comp(0, 1, f"{V:.0f}V")
    draw_comp(1, 2, f"R={R:.1f}Ω")
    draw_comp(2, 3, f"L={L:.2f}H")
    draw_comp(3, 4, f"C={C_m:.0f}μF")
    
    # Draw closing wire
    ax.plot([4, 4, 0, 0], [0.5, 0, 0, 0.5], 'k-', lw=2)
    
    # Finalize axis
    ax.axis('off')
    return fig

# Render the circuit figure
st.pyplot(draw_circuit(V, R, L, C_micro))

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
    st.success("Energy oscillates between L and C → sinusoidal decay.")
elif abs(alpha - omega_0) < 1e-3:
    st.warning("Fastest return to steady state without oscillation.")
else:
    st.error("Highly damped → slow energy dissipation.")

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
