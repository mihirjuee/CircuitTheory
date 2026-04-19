import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

st.title("⚡ RC Transient Response with Circuit Diagram")

# ================= SIDEBAR =================
st.sidebar.header("Parameters")

V = st.sidebar.slider("Supply Voltage (V)", 1, 100, 10)
R = st.sidebar.slider("Resistance (Ω)", 1, 100, 10)
C = st.sidebar.slider("Capacitance (F)", 0.001, 1.0, 0.1)

mode = st.sidebar.radio("Mode", ["Charging", "Discharging"])

# ================= CIRCUIT =================
def rc_circuit():
    d = schemdraw.Drawing()

    d += elm.SourceV().label("V")

    d += elm.Resistor().right().label("R")

    d += elm.Capacitor().down().label("C")

    d += elm.Line().left()
    d += elm.Line().up()

    return d

# ================= TIME RESPONSE =================
t = np.linspace(0, 5 * R * C, 500)
tau = R * C

if mode == "Charging":
    Vc = V * (1 - np.exp(-t / tau))
else:
    Vc = V * np.exp(-t / tau)

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# -------- CIRCUIT --------
with col1:
    st.subheader("🔌 Circuit Diagram")

    d = rc_circuit()
    d.draw()

    fig = plt.gcf()
    fig.set_size_inches(4, 3)
    st.pyplot(fig)
    plt.clf()

# -------- GRAPH --------
with col2:
    st.subheader("📉 Voltage Response")

    fig2, ax = plt.subplots()

    ax.plot(t, Vc, linewidth=2)
    ax.set_xlabel("Time (t)")
    ax.set_ylabel("Capacitor Voltage (Vc)")
    ax.set_title(f"RC {mode}")
    ax.grid(True)

    st.pyplot(fig2)

# ================= INFO =================
st.info(f"Time constant τ = RC = {tau:.3f} seconds")
