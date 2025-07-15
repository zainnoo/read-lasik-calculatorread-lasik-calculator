
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="ZOOM Simulator - Myopic LASIK Model", layout="wide")

st.title("🔍 ZOOM Simulator – Myopic LASIK (No Q Modulation)")
st.subheader("Controlled Spherical Aberration from Myopic Treatment – 6.0 mm Optic Zone Only")

st.sidebar.header("🔎 Refraction (RE & LE)")
# Right Eye
re_sphere = st.sidebar.number_input("RE Sphere (D)", -10.0, 0.0, 0.0, 0.25, key="re_sphere")
re_cyl = st.sidebar.number_input("RE Cylinder (D)", -6.0, 0.0, 0.0, 0.25, key="re_cyl")

# Left Eye
le_sphere = st.sidebar.number_input("LE Sphere (D)", -10.0, 0.0, 0.0, 0.25, key="le_sphere")
le_cyl = st.sidebar.number_input("LE Cylinder (D)", -6.0, 0.0, 0.0, 0.25, key="le_cyl")

st.sidebar.header("🌀 Preop Corneal Spherical Aberration (6mm)")
sa_re = st.sidebar.number_input("RE Corneal SA (μm)", min_value=0.00, max_value=1.00, value=0.00, step=0.01, key="sa_re")
sa_le = st.sidebar.number_input("LE Corneal SA (μm)", min_value=0.00, max_value=1.00, value=0.00, step=0.01, key="sa_le")

st.sidebar.header("🔍 BIA and Refraction Additions")
bia = st.sidebar.slider("Binocular Inherent Accommodation (BIA)", 0.0, 2.5, 0.0, 0.25)
re_refraction = st.sidebar.slider("Right Eye Refraction Add (D)", 0.0, 6.0, 0.0, 0.25)
le_refraction = st.sidebar.slider("Left Eye Refraction Add (D)", 0.0, 6.0, 0.0, 0.25)

st.sidebar.header("👓 Monovision Adjustments")
monovision_eye = st.sidebar.selectbox("Eye for Monovision", ["None", "Right Eye", "Left Eye"])
monovision_add = st.sidebar.slider("Monovision Add (D)", 0.0, 1.5, 0.0, 0.25)

show_overlap = st.sidebar.checkbox("🔷 Show Binocular Overlap", value=False)

def get_dof_myopia(sphere, cyl, preop_SA):
    total_myopia = abs(sphere) + abs(cyl)
    induced_SA = total_myopia * 0.045
    postop_SA = min(preop_SA + induced_SA, 0.60)
    dof = 3.0 * postop_SA
    return round(dof * 4) / 4

def plot_eye(ax, label, bia, refraction, monovision, show_overlap=False, se_dof=0):
    net_shift = refraction + monovision
    retina_x = 0
    se_start = retina_x - net_shift
    se_end = se_start - se_dof
    bia_start = se_end
    bia_end = bia_start - bia
    near_line = -2.5

    eye_x = np.linspace(-3, 3, 500)
    eye_y_upper = 1.2 * np.sin(np.pi * eye_x / 6)
    eye_y_lower = -1.2 * np.sin(np.pi * eye_x / 6)
    ax.plot(eye_x, eye_y_upper, color='black')
    ax.plot(eye_x, eye_y_lower, color='black')

    ax.axvline(retina_x, color='red', lw=2)
    ax.text(retina_x - 0.2, 1.4, "👁 Retina", color='red')
    ax.axvline(near_line, color='purple', linestyle='--', lw=1.5)
    ax.text(near_line - 0.3, 1.4, "📖 Near", color='purple')

    ax.fill_betweenx([-0.4, 0.4], se_end, se_start, color='red', alpha=0.4)
    ax.fill_betweenx([-0.4, 0.4], bia_end, bia_start, color='yellow', alpha=0.4)
    ax.text(-2.5, 1.7, label, fontsize=11, weight='bold')

    if show_overlap:
        return (bia_end, se_start)
    return None

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
for ax in axs:
    ax.set_xlim(-5, 2)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

re_mono = monovision_add if monovision_eye == "Right Eye" else 0
le_mono = monovision_add if monovision_eye == "Left Eye" else 0

re_dof_val = get_dof_myopia(re_sphere, re_cyl, sa_re)
le_dof_val = get_dof_myopia(le_sphere, le_cyl, sa_le)

re_dof = plot_eye(axs[0], f"Right Eye", bia, re_refraction, re_mono, show_overlap, se_dof=re_dof_val)
le_dof = plot_eye(axs[1], f"Left Eye", bia, le_refraction, le_mono, show_overlap, se_dof=le_dof_val)

if show_overlap and re_dof and le_dof:
    start_overlap = max(re_dof[0], le_dof[0])
    end_overlap = min(re_dof[1], le_dof[1])
    binocular_overlap = max(0, end_overlap - start_overlap)
    for ax in axs:
        if binocular_overlap > 0.01:
            ax.axvspan(start_overlap, end_overlap, ymin=0.15, ymax=0.85, facecolor='cyan', alpha=0.4)
            ax.text(-4.2, -2.1, f"👓 Binocular Overlap = {binocular_overlap:.2f}D", fontsize=10, color='blue')
            if binocular_overlap < 0.75:
                ax.text(-3.0, -2.2, "⚠️ Poor Binocular Fusion", fontsize=11, color='red')

plt.tight_layout()
st.pyplot(fig)

st.markdown("#### ⚠️ Disclaimer")
st.markdown("This simulator models DOF induced by myopic treatment based on corneal spherical aberration changes. Valid for 6.0 mm OZ only. Not to be used for hyperopic or Q-modulated treatments.")

st.markdown("### 🧾 Final Treatment Plan")
final_re_sphere = re_sphere + re_refraction + re_mono
final_le_sphere = le_sphere + le_refraction + le_mono
st.write(f"**Right Eye Final Sphere:** {final_re_sphere:.2f} D")
st.write(f"**Left Eye Final Sphere:** {final_le_sphere:.2f} D")

st.markdown("---")
st.markdown("**Developed by Dr. Zain Khatib, Mumbai**  
**Algorithm:** ZOOM Myopia Model")
