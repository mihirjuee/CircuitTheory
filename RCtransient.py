import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RC Circuit (SPDT Switch)", layout="wide")

st.title("⚡ RC Circuit with SPDT Switch")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Parameters")

V = st.sidebar.slider("Voltage (V)", 1.0, 50.0, 10.0)
R = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)
C = st.sidebar.slider("Capacitance (F)", 0.01, 5.0, 1.0)

mode = st.sidebar.radio("🔘 Switch Position", ["Charging", "Discharging"])

# ================= CIRCUIT =================
def rc_spdt(mode):
    d = schemdraw.Drawing(unit=1.0)

    # Common RC branch
    d += elm.Resistor().right().label("R")
    d += elm.Capacitor().down().label("C")

    # Bottom return
    d += elm.Line().left(2)
    d += elm.Line().up()

    # SPDT switch (manual drawing)
    d += elm.Dot()  # common node

    if mode == "Charging":
        # Switch connects to battery
        d += elm.Line().up(0.5)
        d += elm.Switch().right().label("S → V")
        d += elm.SourceV().down().label("V")
        d += elm.Line().left(2)
        d += elm.Line().up()
    else:
        # Switch connects to discharge loop
        d += elm.Line().down(0.5)
        d += elm.Switch().right().label("S → Loop")
        d += elm.Line().right(1)
        d += elm.Line().up(2)
        d += elm.Line().left(3)

    return d


# ================= CALCULATIONS =================
tau = R * C
t = np.linspace(0, 5 * tau, 500)

if mode == "Charging":
    Vc = V * (1 - np.exp(-t / tau))
else:
    Vc = V * np.exp(-t / tau)

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# -------- CIRCUIT --------
with col1:
    st.subheader("🔌 Circuit Diagram")

    d = rc_spdt(mode)
    d.draw()

    fig = plt.gcf()
    fig.set_size_inches(4, 3)
    st.pyplot(fig)
    plt.clf()

    st.caption(f"Switch Position: {mode}")

# -------- GRAPH --------
with col2:
    st.subheader("📉 Capacitor Voltage")

    fig2, ax = plt.subplots()

    ax.plot(t, Vc, linewidth=2)

    ax.set_xlabel("Time (t)")
    ax.set_ylabel("Vc")
    ax.set_title(mode)
    ax.grid(True)

    ax.set_xlim(left=0)
    ax.set_ylim(bottom=0)

    st.pyplot(fig2)

# ================= INFO =================
st.markdown("---")

st.markdown(f"""
### ⚡ SPDT Switch Operation

- **Charging Mode** → Switch connects capacitor to battery  
- **Discharging Mode** → Switch connects capacitor to closed loop  

### ⏱ Time Constant
τ = R × C = **{tau:.2f} s**
""")
