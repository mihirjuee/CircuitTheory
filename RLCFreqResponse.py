# ============================================================
# RLC CIRCUIT RESPONSE SIMULATOR
# STREAMLIT APP
# ============================================================

# Run using:
# streamlit run app.py

# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RLC Circuit Simulator",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("⚡ RLC Circuit Response Simulator")
st.subheader("Series RLC Circuit • Resonance • Damping • Phasor")

st.markdown("---")

# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.header("Circuit Parameters")

R = st.sidebar.slider(
    "Resistance R (Ω)",
    1.0,
    100.0,
    10.0
)

L = st.sidebar.slider(
    "Inductance L (H)",
    0.001,
    1.0,
    0.1
)

C = st.sidebar.slider(
    "Capacitance C (F)",
    0.000001,
    0.01,
    0.001,
    format="%.6f"
)

V = st.sidebar.slider(
    "Supply Voltage (V)",
    1.0,
    400.0,
    230.0
)

f = st.sidebar.slider(
    "Frequency (Hz)",
    1.0,
    500.0,
    50.0
)

# ============================================================
# CALCULATIONS
# ============================================================

w = 2 * np.pi * f

XL = w * L
XC = 1 / (w * C)

Z = np.sqrt(R**2 + (XL - XC)**2)

I = V / Z

pf_angle = np.degrees(np.arctan((XL - XC)/R))

pf = np.cos(np.radians(pf_angle))

fr = 1 / (2 * np.pi * np.sqrt(L*C))

bandwidth = R / (2 * np.pi * L)

Q = fr / bandwidth

# ============================================================
# DAMPING CONDITION
# ============================================================

alpha = R / (2 * L)
omega0 = 1 / np.sqrt(L*C)

if alpha < omega0:
    damping = "UNDERDAMPED"
    damping_color = "cyan"

elif alpha == omega0:
    damping = "CRITICALLY DAMPED"
    damping_color = "lime"

else:
    damping = "OVERDAMPED"
    damping_color = "red"

# ============================================================
# METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Impedance Z", f"{Z:.2f} Ω")
col2.metric("Current I", f"{I:.2f} A")
col3.metric("Power Factor", f"{pf:.2f}")
col4.metric("Resonant Frequency", f"{fr:.2f} Hz")

st.markdown("---")

# ============================================================
# CIRCUIT DIAGRAM
# ============================================================

col_left, col_right = st.columns([1,2])

with col_left:

    st.subheader("🔌 Series RLC Circuit")

    fig1, ax1 = plt.subplots(figsize=(5,5))

    fig1.patch.set_facecolor('black')
    ax1.set_facecolor('black')

    ax1.set_xlim(0,10)
    ax1.set_ylim(0,10)

    ax1.axis('off')

    # --------------------------------------------------------
    # WIRES
    # --------------------------------------------------------

    ax1.plot([1,2],[5,5], color='white', linewidth=3)

    # --------------------------------------------------------
    # RESISTOR
    # --------------------------------------------------------

    x_res = np.linspace(2,4,9)
    y_res = [5,5.5,4.5,5.5,4.5,5.5,4.5,5.5,5]

    ax1.plot(x_res, y_res,
             color='yellow',
             linewidth=3)

    # --------------------------------------------------------
    # WIRE
    # --------------------------------------------------------

    ax1.plot([4,5],[5,5], color='white', linewidth=3)

    # --------------------------------------------------------
    # INDUCTOR
    # --------------------------------------------------------

    theta = np.linspace(0,np.pi,100)

    for i in range(4):

        x = 5 + i*0.5 + 0.25*np.cos(theta)
        y = 5 + 0.5*np.sin(theta)

        ax1.plot(x,y,color='cyan',linewidth=3)

    # --------------------------------------------------------
    # WIRE
    # --------------------------------------------------------

    ax1.plot([7,8],[5,5], color='white', linewidth=3)

    # --------------------------------------------------------
    # CAPACITOR
    # --------------------------------------------------------

    ax1.plot([8,8],[4,6], color='lime', linewidth=3)
    ax1.plot([8.5,8.5],[4,6], color='lime', linewidth=3)

    # --------------------------------------------------------
    # RETURN PATH
    # --------------------------------------------------------

    ax1.plot([8.5,9],[5,5], color='white', linewidth=3)
    ax1.plot([9,9],[5,2], color='white', linewidth=3)
    ax1.plot([9,1],[2,2], color='white', linewidth=3)
    ax1.plot([1,1],[2,5], color='white', linewidth=3)

    # --------------------------------------------------------
    # SOURCE
    # --------------------------------------------------------

    circle = plt.Circle(
        (1,3.5),
        0.5,
        color='red',
        fill=False,
        linewidth=3
    )

    ax1.add_patch(circle)

    ax1.text(
        0.7,
        3.4,
        "~",
        color='red',
        fontsize=18,
        fontweight='bold'
    )

    # --------------------------------------------------------
    # LABELS
    # --------------------------------------------------------

    ax1.text(2.7,6.2,"R",
             color='yellow',
             fontsize=16,
             fontweight='bold')

    ax1.text(5.7,6.2,"L",
             color='cyan',
             fontsize=16,
             fontweight='bold')

    ax1.text(8.1,6.2,"C",
             color='lime',
             fontsize=16,
             fontweight='bold')

    ax1.set_title(
        "Series RLC Circuit",
        color='white',
        fontsize=16,
        fontweight='bold'
    )

    st.pyplot(fig1)

# ============================================================
# PHASOR DIAGRAM
# ============================================================

with col_right:

    st.subheader("🌀 Phasor Diagram")

    fig2, ax2 = plt.subplots(figsize=(7,7))

    fig2.patch.set_facecolor('black')
    ax2.set_facecolor('black')

    ax2.set_xlim(-2,2)
    ax2.set_ylim(-2,2)

    ax2.axhline(0,color='white')
    ax2.axvline(0,color='white')

    ax2.grid(alpha=0.3)

    ax2.set_aspect('equal')

    # Current reference
    ax2.arrow(
        0,0,
        1,0,
        color='white',
        width=0.02,
        head_width=0.08,
        length_includes_head=True
    )

    # VR
    ax2.arrow(
        0,0,
        1,0,
        color='yellow',
        width=0.02,
        head_width=0.08,
        length_includes_head=True
    )

    # VL
    ax2.arrow(
        1,0,
        0,XL/Z,
        color='cyan',
        width=0.02,
        head_width=0.08,
        length_includes_head=True
    )

    # VC
    ax2.arrow(
        1,0,
        0,-XC/Z,
        color='lime',
        width=0.02,
        head_width=0.08,
        length_includes_head=True
    )

    # Resultant voltage
    ax2.arrow(
        0,0,
        1,
        (XL-XC)/Z,
        color='red',
        width=0.02,
        head_width=0.08,
        length_includes_head=True
    )

    ax2.text(1.1,0,"VR",color='yellow',fontsize=14)
    ax2.text(1,(XL/Z)+0.1,"VL",color='cyan',fontsize=14)
    ax2.text(1,-(XC/Z)-0.1,"VC",color='lime',fontsize=14)
    ax2.text(1.1,(XL-XC)/Z,"V",color='red',fontsize=14)

    ax2.set_title(
        "Voltage Phasors",
        color='white',
        fontsize=18,
        fontweight='bold'
    )

    ax2.tick_params(colors='white')

    st.pyplot(fig2)

# ============================================================
# RESONANCE CURVE
# ============================================================

st.markdown("---")
st.subheader("📈 Resonance Curve")

freqs = np.linspace(1,500,1000)

currents = []

for freq in freqs:

    w_temp = 2*np.pi*freq

    XL_temp = w_temp * L
    XC_temp = 1/(w_temp*C)

    Z_temp = np.sqrt(R**2 + (XL_temp-XC_temp)**2)

    currents.append(V/Z_temp)

fig3, ax3 = plt.subplots(figsize=(12,5))

fig3.patch.set_facecolor('black')
ax3.set_facecolor('black')

ax3.plot(
    freqs,
    currents,
    color='cyan',
    linewidth=3
)

ax3.axvline(
    fr,
    color='yellow',
    linestyle='--',
    linewidth=2
)

ax3.set_title(
    "Resonance Characteristics",
    color='white',
    fontsize=18,
    fontweight='bold'
)

ax3.set_xlabel(
    "Frequency (Hz)",
    color='white'
)

ax3.set_ylabel(
    "Current (A)",
    color='white'
)

ax3.grid(alpha=0.3)

ax3.tick_params(colors='white')

st.pyplot(fig3)

# ============================================================
# DAMPING STATUS
# ============================================================

st.markdown("---")

st.subheader("📘 Damping Condition")

st.markdown(
    f"""
    <h2 style='color:{damping_color};'>
    {damping}
    </h2>
    """,
    unsafe_allow_html=True
)

st.write(description := f"""
For this RLC circuit:

- α = {alpha:.2f}
- ω₀ = {omega0:.2f}

The circuit behaves as:
### {damping}
""")

# ============================================================
# THEORY
# ============================================================

st.markdown("---")

st.subheader("📖 Important Equations")

st.latex(r'''
X_L = \omega L
''')

st.latex(r'''
X_C = \frac{1}{\omega C}
''')

st.latex(r'''
Z = \sqrt{R^2 + (X_L - X_C)^2}
''')

st.latex(r'''
f_r = \frac{1}{2\pi\sqrt{LC}}
''')

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    "<center><h3 style='color:cyan;'>Learn EE Interactive</h3></center>",
    unsafe_allow_html=True
)
