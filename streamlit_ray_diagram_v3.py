
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dr Zain's Presbyopic LASIK Ray Diagram", layout="wide")

st.title("👁 Dr Zain's Presbyopic LASIK Ray Diagram Simulator")

st.markdown("""
### Visualize the Depth of Focus and Binocular Overlap  
This simulator demonstrates how BIA, Q modulation, refraction, and monovision affect vision range.

- 🔴 Retina line at 0D
- 📘 Near line 2.5D in front (left) of retina
- 🟡 BIA DOF: starts at retina and extends left
- 🟢 Q-induced DOF: starts at retina and extends right (away from near)
- Changes in **refraction** and **monovision** shift both DOF bars proportionately to the left
- Optional 🔷 Binocular overlap zone shown only if selected
""")

st.sidebar.header("👁 Input Refraction")
re_refraction = st.sidebar.slider("Right Eye Refraction (D)", 0.0, 6.0, 2.0, 0.25)
le_refraction = st.sidebar.slider("Left Eye Refraction (D)", 0.0, 6.0, 1.0, 0.25)

st.sidebar.header("👓 Monovision Settings")
monovision_eye = st.sidebar.selectbox("Eye for Monovision", ["None", "Right Eye", "Left Eye"])
monovision_add = st.sidebar.slider("Monovision Add (D)", 0.0, 1.5, 0.0, 0.25)

st.sidebar.header("🔍 BIA and Q Modulation")
bia = st.sidebar.slider("Binocular Inherent Accommodation (BIA)", 0.0, 2.5, 1.0, 0.25)
re_q = st.sidebar.slider("RE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.12, 0.06)
le_q = st.sidebar.slider("LE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.36, 0.06)

show_overlap = st.sidebar.checkbox("🔷 Show Binocular Overlap", value=False)

# Q to DOF conversion
q_to_dof = 1.25 / 0.3

def plot_eye(ax, label, refraction, q_delta, bia, monovision, show_overlap=False, other_eye_dof=None):
    # DOF calculations
    q_dof = q_delta * q_to_dof

    # Shift all bars by total power added (refraction + monovision)
    net_shift = refraction + monovision

    # BIA is to the left (near)
    bia_start = 0 - net_shift
    bia_end = bia_start - bia

    # Q DOF is to the right (far)
    q_start = 0 - net_shift
    q_end = q_start + q_dof

    # Near reading line (2.5D left)
    near_line = -2.5

    # Eye illustration
    eye_x = np.linspace(-3, 3, 500)
    eye_y_upper = 1.2 * np.sin(np.pi * eye_x / 6)
    eye_y_lower = -1.2 * np.sin(np.pi * eye_x / 6)
    ax.plot(eye_x, eye_y_upper, color='black')
    ax.plot(eye_x, eye_y_lower, color='black')

    ax.axvline(0 - net_shift, color='red', lw=2)
    ax.text(0 - net_shift - 0.2, 1.4, "👁 Retina", color='red')
    ax.axvline(near_line, color='purple', linestyle='--', lw=1.5)
    ax.text(near_line - 0.3, 1.4, "📖 Near", color='purple')

    ax.fill_betweenx([-0.4, 0.4], bia_end, bia_start, color='yellow', alpha=0.4)
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)

    ax.text(-2.5, 1.7, label, fontsize=11, weight='bold')

    # Return DOF zone if needed
    if show_overlap:
        return (bia_end, q_end)
    return None

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
for ax in axs:
    ax.set_xlim(-4.5, 1.5)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

re_mono = monovision_add if monovision_eye == "Right Eye" else 0
le_mono = monovision_add if monovision_eye == "Left Eye" else 0

# Draw eyes
re_dof = plot_eye(axs[0], f"Right Eye (RE +{re_refraction:.2f}D, Q Δ {re_q:.2f})",
                  re_refraction, re_q, bia, re_mono, show_overlap)
le_dof = plot_eye(axs[1], f"Left Eye (LE +{le_refraction:.2f}D, Q Δ {le_q:.2f})",
                  le_refraction, le_q, bia, le_mono, show_overlap)

# Draw binocular overlap
if show_overlap and re_dof and le_dof:
    start_overlap = max(re_dof[0], le_dof[0])
    end_overlap = min(re_dof[1], le_dof[1])
    binocular_overlap = max(0, end_overlap - start_overlap)
    for ax in axs:
        if binocular_overlap > 0.01:
            ax.axvspan(start_overlap, end_overlap, ymin=0.15, ymax=0.85, facecolor='cyan', alpha=0.4)
            ax.text(-4.0, -2.1,
                    f"👓 Binocular Overlap = {binocular_overlap:.2f}D",
                    fontsize=10, color='blue')
            if binocular_overlap < 0.75:
                ax.text(-3.0, -2.2, "⚠️ Poor Binocular Fusion", fontsize=11, color='red')

plt.tight_layout()
st.pyplot(fig)
