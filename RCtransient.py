import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import time

# ================= PAGE =================
st.set_page_config(page_title="RC Lab Simulator",page_icon="logo.png", layout="wide")
st.title("⚡  RC Circuit Transient Behavior")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Controls")

V = st.sidebar.slider("Voltage (V)", 1.0, 50.0, 10.0)
R = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)
C = st.sidebar.slider("Capacitance (F)", 0.01, 5.0, 1.0)

mode = st.sidebar.toggle("Switch → Charging (ON) / Discharging (OFF)")
run = st.sidebar.button("▶ Run Simulation")

# ================= CIRCUIT =================
def draw_circuit(active_path="charge"):
    d = schemdraw.Drawing(unit=1.2)

    # Battery
    d += elm.SourceV().up().label("V")

    # Node
    d += elm.Line().right()
    d += elm.Dot()

    # Switch
    if active_path == "charge":
        sw = elm.Switch(action='close').right().label("Close")
    else:
        sw = elm.Switch(action='open').right().label("Open")

    d += sw   # ✅ correct usage

    # Save position AFTER switch
    d.push()

    # RC branch
    d += elm.Line().right()
    d += elm.Resistor().down().label("R")
    d += elm.Capacitor().down().label("C")

    d += elm.Line().left(3.6)
    d += elm.Line().up(1.2)

    # Discharge branch
    if active_path == "discharge":
        d.pop()
        d += elm.Line().down(0.2)
        d += elm.Switch(action='close').down().label("Close")
        d += elm.Line().down(1)

    return d

# ================= GRAPH =================
def simulate(mode):
    tau = R * C
    t = np.linspace(0, 5*tau, 200)

    if mode:  # Charging
        Vc = V * (1 - np.exp(-t/tau))
    else:     # Discharging
        Vc = V * np.exp(-t/tau)

    return t, Vc

# ================= LAYOUT =================
col1, col2 = st.columns([1,1])

circuit_placeholder = col1.empty()
graph_placeholder = col2.empty()
value_placeholder = st.empty()

# ================= INITIAL =================
state = "charge" if mode else "discharge"
d = draw_circuit(state)
d.draw()
fig = plt.gcf()
fig.set_size_inches(4,3)
circuit_placeholder.pyplot(fig)
plt.clf()

t, Vc = simulate(mode)
fig2, ax = plt.subplots()
ax.plot(t, Vc, linewidth=2)
ax.set_xlabel("Time")
ax.set_ylabel("Vc")
ax.set_title("Charging" if mode else "Discharging")
ax.grid(True)
ax.set_xlim(left=0)
ax.set_ylim(bottom=0)
graph_placeholder.pyplot(fig2)

value_placeholder.metric("Capacitor Voltage", f"{Vc[-1]:.2f} V")
value_placeholder.metric("Time Constant", f"{tau[-1]:.2f} s")

# ================= REAL-TIME SIM =================
if run:
    tau = R * C
    t = np.linspace(0, 5*tau, 200)

    for i in range(len(t)):
        if mode:
            vc = V * (1 - np.exp(-t[i]/tau))
            state = "charge"
        else:
            vc = V * np.exp(-t[i]/tau)
            state = "discharge"

        # Update circuit
        d = draw_circuit(state)
        d.draw()
        fig = plt.gcf()
        fig.set_size_inches(4,3)
        circuit_placeholder.pyplot(fig)
        plt.clf()

        # Update graph dynamically
        fig2, ax = plt.subplots()
        ax.plot(t[:i+1], 
                V * (1 - np.exp(-t[:i+1]/tau)) if mode 
                else V * np.exp(-t[:i+1]/tau),
                linewidth=2)

        ax.set_xlim(0, max(t))
        ax.set_ylim(0, V)
        ax.set_xlabel("Time")
        ax.set_ylabel("Vc")
        ax.grid(True)

        graph_placeholder.pyplot(fig2)

        # Live voltage
        value_placeholder.metric("Capacitor Voltage", f"{vc:.2f} V")
        value_placeholder.metric("Time Constant", f"{tau:.2f} s")

        time.sleep(0.05)
