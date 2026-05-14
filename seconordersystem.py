# ============================================================
# STREAMLIT APP
# DAMPING SYSTEM SIMULATOR WITH CIRCUIT DIAGRAM
# ============================================================

# Run:
# streamlit run app.py

# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Damping System Simulator",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("⚡ Damping System Interactive Simulator")
st.subheader("Underdamped • Critically Damped • Overdamped")

st.markdown("---")

# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.header("System Parameters")

zeta = st.sidebar.slider(
    "Damping Ratio (ζ)",
    0.0,
    3.0,
    0.5,
    0.01
)

wn = st.sidebar.slider(
    "Natural Frequency ωn",
    1.0,
    20.0,
    5.0,
    0.5
)

# ============================================================
# TIME VECTOR
# ============================================================

t = np.linspace(0, 10, 2000)

# ============================================================
# RESPONSE CALCULATION
# ============================================================

if zeta < 1:

    wd = wn * np.sqrt(1 - zeta**2)

    y = 1 - np.exp(-zeta * wn * t) * (
        np.cos(wd * t)
        + (zeta / np.sqrt(1 - zeta**2)) * np.sin(wd * t)
    )

    system_type = "UNDERDAMPED"
    description = "Oscillatory response with overshoot"
    color = "cyan"

elif zeta == 1:

    y = 1 - np.exp(-wn * t) * (1 + wn * t)

    system_type = "CRITICALLY DAMPED"
    description = "Fastest response without oscillation"
    color = "lime"

else:

    s1 = -wn * (zeta - np.sqrt(zeta**2 - 1))
    s2 = -wn * (zeta + np.sqrt(zeta**2 - 1))

    y = 1 - (
        (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t))
        / (s2 - s1)
    )

    system_type = "OVERDAMPED"
    description = "Slow response without oscillation"
    color = "red"

# ============================================================
# METRICS
# ============================================================

col1, col2, col3 = st.columns(3)

col1.metric("Damping Ratio ζ", f"{zeta:.2f}")
col2.metric("Natural Frequency ωn", f"{wn:.2f}")
col3.metric("System Type", system_type)

st.markdown("---")

# ============================================================
# CIRCUIT DIAGRAM + RESPONSE
# ============================================================

col_left, col_right = st.columns([1,2])

# ============================================================
# LEFT SIDE : RLC CIRCUIT DIAGRAM
# ============================================================

with col_left:

    st.subheader("🔌 Series RLC Circuit")

    fig_circuit, axc = plt.subplots(figsize=(5,5))

    fig_circuit.patch.set_facecolor('black')
    axc.set_facecolor('black')

    axc.set_xlim(0,10)
    axc.set_ylim(0,10)

    axc.axis('off')

    # --------------------------------------------------------
    # Wires
    # --------------------------------------------------------

    axc.plot([1,2],[5,5], color='white', linewidth=3)

    # Resistor
    x_res = np.linspace(2,4,9)
    y_res = [5,5.5,4.5,5.5,4.5,5.5,4.5,5.5,5]

    axc.plot(x_res, y_res, color='yellow', linewidth=3)

    # Wire
    axc.plot([4,5],[5,5], color='white', linewidth=3)

    # Inductor
    theta = np.linspace(0,np.pi,100)

    for i in range(4):

        x = 5 + i*0.5 + 0.25*np.cos(theta)
        y = 5 + 0.5*np.sin(theta)

        axc.plot(x,y,color='cyan',linewidth=3)

    # Wire
    axc.plot([7,8],[5,5], color='white', linewidth=3)

    # Capacitor
    axc.plot([8,8],[4,6], color='lime', linewidth=3)
    axc.plot([8.5,8.5],[4,6], color='lime', linewidth=3)

    # Wire return
    axc.plot([8.5,9],[5,5], color='white', linewidth=3)
    axc.plot([9,9],[5,2], color='white', linewidth=3)
    axc.plot([9,1],[2,2], color='white', linewidth=3)
    axc.plot([1,1],[2,5], color='white', linewidth=3)

    # Source
    circle = plt.Circle((1,3.5),0.5,color='red',fill=False,linewidth=3)

    axc.add_patch(circle)

    axc.text(0.7,3.4,"~",color='red',fontsize=18,fontweight='bold')

    # Labels
    axc.text(2.7,6.2,"R",color='yellow',fontsize=16,fontweight='bold')
    axc.text(5.7,6.2,"L",color='cyan',fontsize=16,fontweight='bold')
    axc.text(8.1,6.2,"C",color='lime',fontsize=16,fontweight='bold')

    axc.set_title(
        "RLC Damping Circuit",
        color='white',
        fontsize=16,
        fontweight='bold'
    )

    st.pyplot(fig_circuit)

# ============================================================
# RIGHT SIDE : RESPONSE PLOT
# ============================================================

with col_right:

    st.subheader("📈 System Response")

    fig, ax = plt.subplots(figsize=(10,5))

    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')

    ax.plot(
        t,
        y,
        linewidth=3,
        color=color,
        label=system_type
    )

    ax.axhline(
        1,
        linestyle='--',
        linewidth=2,
        color='yellow',
        label='Final Value'
    )

    ax.set_title(
        "Second Order System Response",
        fontsize=18,
        color='white',
        fontweight='bold'
    )

    ax.set_xlabel(
        "Time",
        fontsize=12,
        color='white'
    )

    ax.set_ylabel(
        "Response",
        fontsize=12,
        color='white'
    )

    ax.grid(True, alpha=0.3)

    ax.tick_params(colors='white')

    legend = ax.legend(facecolor='black')

    for text in legend.get_texts():
        text.set_color("white")

    st.pyplot(fig)

# ============================================================
# SPRING MASS VISUALIZATION
# ============================================================

st.markdown("---")
st.subheader("🔄 Mechanical Analogy")

if zeta < 1:
    animation_speed = 1
elif zeta == 1:
    animation_speed = 2
else:
    animation_speed = 4

html_code = f"""
<div style="
display:flex;
justify-content:center;
align-items:center;
height:250px;
background-color:black;
border-radius:15px;
overflow:hidden;
">

<div style="
position:relative;
width:500px;
height:100px;
">

<div style="
position:absolute;
top:45px;
left:0;
width:250px;
height:10px;
background:repeating-linear-gradient(
90deg,
cyan 0px,
cyan 10px,
black 10px,
black 20px
);
">
</div>

<div style="
position:absolute;
top:20px;
left:250px;
width:80px;
height:60px;
background:{color};
border-radius:10px;
animation:move {animation_speed}s infinite alternate;
">
</div>

</div>

</div>

<style>

@keyframes move {{

0% {{
transform: translateX(-50px);
}}

100% {{
transform: translateX(50px);
}}

}}

</style>
"""

st.markdown(html_code, unsafe_allow_html=True)

# ============================================================
# THEORY
# ============================================================

st.markdown("---")

st.subheader("📘 Theory")

st.write("""
The damping response depends on the damping ratio ζ.

### Underdamped (ζ < 1)
- Oscillatory response
- Overshoot present

### Critically Damped (ζ = 1)
- Fastest response
- No oscillation

### Overdamped (ζ > 1)
- Slow response
- No oscillation

In an RLC circuit:
- Resistance causes damping
- Inductor stores magnetic energy
- Capacitor stores electric energy
""")

# ============================================================
# EQUATION
# ============================================================

st.markdown("---")

st.latex(r'''
\frac{d^2x}{dt^2}
+
2\zeta\omega_n\frac{dx}{dt}
+
\omega_n^2x = 0
''')

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    "<center><h3 style='color:cyan;'>Learn EE Interactive</h3></center>",
    unsafe_allow_html=True
)
