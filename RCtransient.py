import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
import time

# ================= PAGE CONFIG =================
st.set_page_config(page_title="Animated SPDT Switch", layout="wide")
st.title("⚡ RC Circuit with Animated SPDT Switch")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Parameters")

V = st.sidebar.slider("Voltage (V)", 1.0, 50.0, 10.0)
R = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)
C = st.sidebar.slider("Capacitance (F)", 0.01, 5.0, 1.0)

mode = st.sidebar.radio("Mode", ["Charging", "Discharging"])
animate = st.sidebar.button("▶ Animate Switch")

# ================= CIRCUIT =================
def draw_spdt(position):
    d = schemdraw.Drawing()

    # RC branch
    d += elm.Resistor().right().label("R")
    d += elm.Capacitor().down().label("C")
    d += elm.Line().left(2)
    d += elm.Line().up()

    # Common node
    d += elm.Dot()

    if position == "charging":
        # Switch tilted to battery
        d += elm.Switch(action='close').up().label("To V")
        d += elm.SourceV().down().label("V")
        d += elm.Line().left()
        d += elm.Line().up()

        # Other side open
        d.push()
        d += elm.Line().down(0.5)
        d += elm.Switch(action='open').right()
        d.pop()

    elif position == "middle":
        # Transition state (both open)
        d += elm.Switch(action='open').up()
        d.push()
        d += elm.Line().down(0.5)
        d += elm.Switch(action='open').right()
        d.pop()

    else:
        # Switch tilted to loop
        d += elm.Switch(action='close').down().label("To Loop")
        d += elm.Line().right(1.5)
        d += elm.Line().up(2)
        d += elm.Line().left(2)

        # Other side open
        d.push()
        d += elm.Line().right(0.5)
        d += elm.Switch(action='open')
        d.pop()

    return d

# ================= GRAPH =================
def plot_graph(mode):
    tau = R * C
    t = np.linspace(0, 5 * tau, 400)

    if mode == "Charging":
        Vc = V * (1 - np.exp(-t / tau))
    else:
        Vc = V * np.exp(-t / tau)

    fig, ax = plt.subplots()
    ax.plot(t, Vc, linewidth=2)
    ax.set_xlabel("Time")
    ax.set_ylabel("Vc")
    ax.set_title(mode)
    ax.grid(True)
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    return fig

# ================= PLACEHOLDERS =================
col1, col2 = st.columns(2)
circuit_placeholder = col1.empty()
graph_placeholder = col2.empty()

# ================= STATIC DISPLAY =================
position_map = {
    "Charging": "charging",
    "Discharging": "discharging"
}

d = draw_spdt(position_map[mode])
d.draw()
fig = plt.gcf()
fig.set_size_inches(4, 3)
circuit_placeholder.pyplot(fig)
plt.clf()

graph_placeholder.pyplot(plot_graph(mode))

# ================= ANIMATION =================
if animate:
    sequence = ["charging", "middle", "discharging"] if mode == "Discharging" else ["discharging", "middle", "charging"]

    for pos in sequence:
        d = draw_spdt(pos)
        d.draw()
        fig = plt.gcf()
        fig.set_size_inches(4, 3)

        circuit_placeholder.pyplot(fig)
        plt.clf()

        time.sleep(0.5)
