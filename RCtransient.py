import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RC Transient Simulator", layout="wide")

st.title("⚡ RC Circuit: Charging & Discharging")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Parameters")

V = st.sidebar.slider("Supply Voltage (V)", 1.0, 50.0, 10.0)
R = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)
C = st.sidebar.slider("Capacitance (F)", 0.01, 5.0, 1.0)

switch = st.sidebar.toggle("🔘 Switch ON (Charging)", value=True)

# ================= CIRCUIT FUNCTION =================
def rc_circuit(switch_on):
    d = schemdraw.Drawing(unit=1.0)

    if switch_on:
        # 🔋 Charging circuit
        d += elm.SourceV().up().label("V")
        d += elm.Line().right()
        d += elm.Resistor().right().label("R")
        d += elm.Capacitor().down().label("C")
        d += elm.Line().left()
        d += elm.Line().up()

    else:
        # 🔁 Discharging loop (closed path, no source)
        d += elm.Capacitor().right().label("C")
        d += elm.Resistor().down().label("R")
        d += elm.Line().left()
        d += elm.Line().up()

    return d


# ================= CALCULATIONS =================
tau = R * C
t = np.linspace(0, 5 * tau, 500)

if switch:
    # Charging
    Vc = V * (1 - np.exp(-t / tau))
    title = "Charging"
else:
    # Discharging
    Vc = V * np.exp(-t / tau)
    title = "Discharging"

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# -------- CIRCUIT --------
with col1:
    st.subheader("🔌 Circuit Diagram")

    d = rc_circuit(switch)
    d.draw()

    fig = plt.gcf()
    fig.set_size_inches(4, 3)   # 👈 compact diagram
    st.pyplot(fig)
    plt.clf()

    if switch:
        st.caption("🔘 Switch ON → Battery connected → Charging")
    else:
        st.caption("🔘 Switch OFF → Closed R-C loop → Discharging")

# -------- GRAPH --------
with col2:
    st.subheader("📉 Capacitor Voltage")

    fig2, ax = plt.subplots()

    ax.plot(t, Vc, linewidth=2)

    ax.set_xlabel("Time (t)")
    ax.set_ylabel("Capacitor Voltage (Vc)")
    ax.set_title(title)
    ax.grid(True)

    # Start axes from zero
    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    st.pyplot(fig2)

# ================= INFO =================
st.markdown("---")

st.markdown(f"""
### ⚡ Key Concepts

- Time constant: τ = R × C = **{tau:.2f} s**
- Charging: Capacitor voltage rises exponentially
- Discharging: Capacitor releases stored energy through resistor

**Equations:**
- Charging: Vc = V(1 - e^(-t/RC))
- Discharging: Vc = V₀ e^(-t/RC)
""")
