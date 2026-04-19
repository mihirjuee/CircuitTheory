import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# ================= PAGE CONFIG =================
st.set_page_config(page_title="RC Circuit (Two Switches)", layout="wide")
st.title("⚡ RC Circuit with Two Switches (Textbook Style)")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Parameters")

V = st.sidebar.slider("Voltage (V)", 1.0, 50.0, 10.0)
R = st.sidebar.slider("Resistance (Ω)", 1.0, 100.0, 10.0)
C = st.sidebar.slider("Capacitance (F)", 0.01, 5.0, 1.0)

st.sidebar.markdown("### 🔘 Switch Control")
S1 = st.sidebar.toggle("S1 → Charging Switch", True)
S2 = st.sidebar.toggle("S2 → Discharge Switch", False)

# ================= CIRCUIT =================
def rc_circuit(S1, S2):
    d = schemdraw.Drawing(unit=1.2)

    # ---- TOP NODE ----
    d += elm.Dot()
    
    # ---- LEFT BRANCH (Battery + S1) ----
    d.push()
    if S1:
        d += elm.Switch().left().label("S1")
        d += elm.SourceV().down().label("V")
        d += elm.Line().right()
    else:
        d += elm.Gap().left().label("S1 Open")
    d.pop()

    # ---- RIGHT BRANCH (R-C) ----
    d += elm.Resistor().right().label("R")
    d += elm.Capacitor().down().label("C")

    # ---- BOTTOM NODE ----
    d += elm.Line().left()
    
    # ---- S2 (Discharge Switch) ----
    if S2:
        d += elm.Switch().left().label("S2")
    else:
        d += elm.Gap().label("S2 Open")

    # ---- CLOSE LOOP ----
    d += elm.Line().up()

    return d

# ================= CALCULATIONS =================
tau = R * C
t = np.linspace(0, 5 * tau, 500)

# Mode logic
if S1 and not S2:
    mode = "Charging"
    Vc = V * (1 - np.exp(-t / tau))

elif S2 and not S1:
    mode = "Discharging"
    Vc = V * np.exp(-t / tau)

elif S1 and S2:
    mode = "⚠️ Invalid (Both Closed)"
    Vc = np.zeros_like(t)

else:
    mode = "Open Circuit"
    Vc = np.zeros_like(t)

# ================= LAYOUT =================
col1, col2 = st.columns([1, 1])

# -------- CIRCUIT --------
with col1:
    st.subheader("🔌 Circuit Diagram")

    d = rc_circuit(S1, S2)
    d.draw()

    fig = plt.gcf()
    fig.set_size_inches(4.2, 3.2)
    st.pyplot(fig)
    plt.clf()

    st.caption(f"Mode: {mode}")

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
### ⚡ Operation

- **S1 ON, S2 OFF → Charging**
- **S1 OFF, S2 ON → Discharging**
- **Both OFF → Open circuit**
- **Both ON → Invalid condition**

### ⏱ Time Constant
τ = R × C = **{tau:.2f} s**
""")
