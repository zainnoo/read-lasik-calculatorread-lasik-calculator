
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Dr Zain's Presbyopic LASIK Ray Diagram", layout="wide")

st.title("👁 Dr Zain's Presbyopic LASIK Ray Diagram Simulator")

st.markdown("""
### Visualize the Depth of Focus and Binocular Overlap  
This simulator demonstrates how BIA, Q modulation, refraction changes, and monovision affect vision range.

- 🔴 Retina line is fixed at 0D
- 📘 Near line is 2.5D in front (left) of retina
- 🟡 BIA DOF: extends left of retina
- 🟢 Q-induced DOF: extends right of retina
- Refraction and Monovision shift convergence point leftward
- Optional 🔷 Binocular overlap zone shown only if selected
""")

# Actual Refraction Entry (for reference only)
st.sidebar.header("🔎 Actual Distance Refraction (Input only, no diagram effect)")
actual_re = st.sidebar.number_input("RE Actual Refraction (D)", 0.0, 6.0, 2.0, 0.25)
actual_le = st.sidebar.number_input("LE Actual Refraction (D)", 0.0, 6.0, 1.0, 0.25)

# BIA & Q Modulation
st.sidebar.header("🔍 BIA and Q Modulation Settings")
bia = st.sidebar.slider("Binocular Inherent Accommodation (BIA)", 0.0, 2.5, 1.0, 0.25)
re_q = st.sidebar.slider("RE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.12, 0.06)
le_q = st.sidebar.slider("LE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.36, 0.06)

# Refraction Shift
st.sidebar.header("🔧 Refraction Changes")
re_refraction = st.sidebar.slider("Right Eye Refraction Add (D)", 0.0, 6.0, 0.0, 0.25)
le_refraction = st.sidebar.slider("Left Eye Refraction Add (D)", 0.0, 6.0, 0.0, 0.25)

# Monovision Settings
st.sidebar.header("👓 Monovision Adjustments")
monovision_eye = st.sidebar.selectbox("Eye for Monovision", ["None", "Right Eye", "Left Eye"])
monovision_add = st.sidebar.slider("Monovision Add (D)", 0.0, 1.5, 0.0, 0.25)

# Binocular Overlap Option
show_overlap = st.sidebar.checkbox("🔷 Show Binocular Overlap", value=False)

# Q to DOF conversion
q_to_dof = 1.25 / 0.3

def plot_eye(ax, label, q_delta, bia, refraction, monovision, show_overlap=False, other_eye_dof=None):
    # Q DOF is to the right of retina
    q_dof = q_delta * q_to_dof

    # Total net shift from refraction + monovision
    net_shift = refraction + monovision

    # Retina stays at 0
    retina_x = 0
    bia_start = retina_x
    bia_end = bia_start - bia

    q_start = retina_x
    q_end = q_start + q_dof

    # Shift all DOF bars leftward to simulate improved near vision
    bia_start -= net_shift
    bia_end -= net_shift
    q_start -= net_shift
    q_end -= net_shift

    # Near line (2.5D anterior)
    near_line = -2.5

    # Draw eye shape
    eye_x = np.linspace(-3, 3, 500)
    eye_y_upper = 1.2 * np.sin(np.pi * eye_x / 6)
    eye_y_lower = -1.2 * np.sin(np.pi * eye_x / 6)
    ax.plot(eye_x, eye_y_upper, color='black')
    ax.plot(eye_x, eye_y_lower, color='black')

    ax.axvline(retina_x, color='red', lw=2)
    ax.text(retina_x - 0.2, 1.4, "👁 Retina", color='red')
    ax.axvline(near_line, color='purple', linestyle='--', lw=1.5)
    ax.text(near_line - 0.3, 1.4, "📖 Near", color='purple')

    ax.fill_betweenx([-0.4, 0.4], bia_end, bia_start, color='yellow', alpha=0.4)
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)

    ax.text(-2.5, 1.7, label, fontsize=11, weight='bold')

    if show_overlap:
        return (bia_end, q_end)
    return None

# Prepare figure and axes
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
for ax in axs:
    ax.set_xlim(-5, 2)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

# Monovision values
re_mono = monovision_add if monovision_eye == "Right Eye" else 0
le_mono = monovision_add if monovision_eye == "Left Eye" else 0

# Plotting each eye
re_dof = plot_eye(axs[0], f"Right Eye (Q Δ {re_q:.2f})", re_q, bia, re_refraction, re_mono, show_overlap)
le_dof = plot_eye(axs[1], f"Left Eye (Q Δ {le_q:.2f})", le_q, bia, le_refraction, le_mono, show_overlap)

# Show binocular overlap
if show_overlap and re_dof and le_dof:
    start_overlap = max(re_dof[0], le_dof[0])
    end_overlap = min(re_dof[1], le_dof[1])
    binocular_overlap = max(0, end_overlap - start_overlap)
    for ax in axs:
        if binocular_overlap > 0.01:
            ax.axvspan(start_overlap, end_overlap, ymin=0.15, ymax=0.85, facecolor='cyan', alpha=0.4)
            ax.text(-4.2, -2.1,
                    f"👓 Binocular Overlap = {binocular_overlap:.2f}D",
                    fontsize=10, color='blue')
            if binocular_overlap < 0.75:
                ax.text(-3.0, -2.2, "⚠️ Poor Binocular Fusion", fontsize=11, color='red')

plt.tight_layout()
st.pyplot(fig)
