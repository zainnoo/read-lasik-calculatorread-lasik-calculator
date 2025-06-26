
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dr Zain's Presbyopic LASIK Ray Diagram", layout="wide")

st.title("👁 Dr Zain's Presbyopic LASIK Ray Diagram Simulator")

st.markdown("""
### Visualize the Depth of Focus and Binocular Overlap
Use this tool to simulate:
- Effects of **refraction**, **BIA (binocular inherent accommodation)**, **Q value modulation**, and **monovision**
- **Yellow bar**: DOF from BIA (to the right of retina)
- **Green bar**: DOF from Q modulation (to the left of retina)
- **Cyan bar**: Binocular Overlap (visible in both eyes)
- **Red line**: Retina | **Purple dashed line**: Near vision (25 cm or 2.5D)
""")

st.sidebar.header("👁 Input Refraction")
re_refraction = st.sidebar.slider("Right Eye Refraction (D)", 0.0, 6.0, 2.0, 0.25)
le_refraction = st.sidebar.slider("Left Eye Refraction (D)", 0.0, 6.0, 1.0, 0.25)

st.sidebar.header("👓 Monovision Settings")
monovision_eye = st.sidebar.selectbox("Eye for Monovision", ["None", "Right Eye", "Left Eye"])
monovision_add = st.sidebar.slider("Monovision Add (D)", 0.0, 1.5, 0.0, 0.25)

st.sidebar.header("🔍 Accommodation & Q Modulation")
bia = st.sidebar.slider("Binocular Inherent Accommodation (BIA)", 0.0, 2.5, 1.0, 0.25)
re_q = st.sidebar.slider("RE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.12, 0.06)
le_q = st.sidebar.slider("LE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.36, 0.06)

# Apply monovision
if monovision_eye == "Right Eye":
    re_refraction += monovision_add
elif monovision_eye == "Left Eye":
    le_refraction += monovision_add

# Constants
retina_x = 8
reading_x = retina_x - 2.5
q_to_dof = 1.25 / 0.3  # ~4.1667 D per Q value

def plot_eye(ax, label, refraction, q_delta, bia, is_left):
    # BIA DOF: to the right of retina
    bia_start = retina_x
    bia_end = retina_x + bia

    # Q DOF: to the left of retina
    q_dof = q_delta * q_to_dof
    q_start = retina_x - q_dof
    q_end = retina_x

    # Eye shape
    eye_x = np.linspace(0, retina_x, 500)
    eye_y_upper = 1.2 * np.sin(0.5 * np.pi * eye_x / retina_x)
    eye_y_lower = -1.2 * np.sin(0.5 * np.pi * eye_x / retina_x)
    ax.plot(eye_x, eye_y_upper, color='black')
    ax.plot(eye_x, eye_y_lower, color='black')

    # Reference lines
    ax.plot([retina_x, retina_x], [-1.2, 1.2], color='red', lw=2)
    ax.text(retina_x - 0.2, 1.4, "👁 Retina", fontsize=10, color='red')
    ax.plot([reading_x, reading_x], [-1.2, 1.2], color='purple', linestyle='--', lw=1.5)
    ax.text(reading_x - 0.3, 1.4, "📖 Near", fontsize=10, color='purple')

    # DOF zones
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)
    ax.fill_betweenx([-0.4, 0.4], bia_start, bia_end, color='yellow', alpha=0.4)

    ax.text(5, 1.8, label, fontsize=11, weight='bold')

    return q_start, q_end, bia_start, bia_end

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
for ax in axs:
    ax.set_xlim(4.5, 10.5)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

re_qs, re_qe, re_bs, re_be = plot_eye(axs[0], f"Right Eye (RE {re_refraction:.2f}D, Q Δ {re_q:.2f})", re_refraction, re_q, bia, False)
le_qs, le_qe, le_bs, le_be = plot_eye(axs[1], f"Left Eye (LE {le_refraction:.2f}D, Q Δ {le_q:.2f})", le_refraction, le_q, bia, True)

# Binocular overlap
dof_start = max(re_qs, le_qs)
dof_end = min(re_be, le_be)
overlap = max(0, dof_end - dof_start)

for ax in axs:
    if overlap > 0.01:
        ax.axvspan(dof_start, dof_end, ymin=0.15, ymax=0.85, facecolor='cyan', alpha=0.4)
        ax.plot([dof_start, dof_start], [-0.5, 0.5], color='cyan', linestyle='--', lw=2)
        ax.plot([dof_end, dof_end], [-0.5, 0.5], color='cyan', linestyle='--', lw=2)
        ax.text((dof_start + dof_end)/2 - 0.3, -2.1,
                f"👓 Binocular Overlap = {overlap:.2f}D",
                fontsize=10, color='blue')
        if overlap < 0.75:
            ax.text(5.5, -2.2, "⚠️ Poor Binocular Fusion", fontsize=11, color='red')

plt.tight_layout()
st.pyplot(fig)
