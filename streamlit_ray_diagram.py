
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dr Zain's Presbyopic LASIK Simulator", layout="wide")

st.title("👁 Dr Zain's Presbyopic LASIK Ray Diagram Simulator")

st.markdown("""
This simulator helps visualize the effects of **refraction**, **Q value modulation**, and **monovision** on the depth of focus and binocular overlap.
- **BIA (yellow)** = Natural accommodation
- **Q DOF (green)** = Additional focus range due to Q modulation
- **Binocular Overlap (cyan)** = Zone seen clearly by both eyes
- **Red line** = Retina  
- **Purple dashed line** = Near point (25 cm, ~2.5D)
""")

st.sidebar.header("Right Eye (RE)")
re_refraction = st.sidebar.slider("RE Refraction (D)", 2.5, 5.0, 3.5, 0.25)
re_q = st.sidebar.slider("RE Q value change", 0.0, 0.4, 0.12, 0.01)

st.sidebar.header("Left Eye (LE)")
le_refraction = st.sidebar.slider("LE Refraction (D)", 2.5, 6.0, 4.75, 0.25)
le_q = st.sidebar.slider("LE Q value change", 0.0, 0.5, 0.36, 0.01)

# Constants
retina_x = 8
reading_x = retina_x - 2.5
q_to_dof = 1.25 / 0.3  # ~4.1667 D per Q value

def plot_eye(ax, label, refraction, q_delta, is_left):
    q_dof = q_delta * q_to_dof
    monovision_shift = refraction - 3.5
    q_start = retina_x - q_dof - monovision_shift
    q_end = retina_x - monovision_shift
    bia_dof = 2.5 - monovision_shift
    bia_start = q_start - bia_dof
    bia_end = q_start

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

    # Fill zones
    ax.fill_betweenx([-0.4, 0.4], bia_start, bia_end, color='yellow', alpha=0.4)
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)

    ax.text(5, 1.8, label, fontsize=11, weight='bold')
    return q_start, q_end

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
for ax in axs:
    ax.set_xlim(4.5, 10)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

re_start, re_end = plot_eye(axs[0], f"Right Eye (RE {re_refraction:.2f}D, Q Δ {re_q:.2f})", re_refraction, re_q, False)
le_start, le_end = plot_eye(axs[1], f"Left Eye (LE {le_refraction:.2f}D, Q Δ {le_q:.2f})", le_refraction, le_q, True)

# Binocular overlap
overlap_start = max(re_start, le_start)
overlap_end = min(re_end, le_end)
overlap_width = max(0, overlap_end - overlap_start)

for ax in axs:
    if overlap_width > 0.01:
        ax.axvspan(overlap_start, overlap_end, ymin=0.15, ymax=0.85, facecolor='cyan', alpha=0.4)
        ax.plot([overlap_start, overlap_start], [-0.5, 0.5], color='cyan', linestyle='--', lw=2)
        ax.plot([overlap_end, overlap_end], [-0.5, 0.5], color='cyan', linestyle='--', lw=2)

        ax.text((overlap_start + overlap_end)/2 - 0.3, -2.1,
                f"👓 Binocular Overlap = {overlap_width:.2f}D",
                fontsize=10, color='blue')
        if overlap_width < 0.75:
            ax.text(5.5, -2.2, "⚠️ Warning: Poor binocular fusion!", fontsize=11, color='red')

plt.tight_layout()
st.pyplot(fig)
