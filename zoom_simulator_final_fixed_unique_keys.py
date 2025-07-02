
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="ZOOM Simulator - CAMP Algorithm", layout="wide")

# App Title and Subtitle
st.title("🔍 ZOOM Simulator")
st.subheader("Based on the CAMP Algorithm (Controlled Asphericity Modulation for Presbyopia)")

# Sidebar Inputs

# Sidebar Inputs
st.sidebar.header("🔢 Spherical Equivalent (Before Q Modulation)")
se_re = st.sidebar.number_input("RE Spherical Equivalent (D)", 0.0, 6.0, 0.0, 0.25, key="se_re")
se_le = st.sidebar.number_input("LE Spherical Equivalent (D)", 0.0, 6.0, 0.0, 0.25, key="se_le")

st.sidebar.header("🌀 Preop Corneal SA (6mm)")
sa_re = st.sidebar.number_input("RE Spherical Aberration (SA)", 0.0, 0.6, 0.0, 0.01, key="sa_re")
sa_le = st.sidebar.number_input("LE Spherical Aberration (SA)", 0.0, 0.6, 0.0, 0.01, key="sa_le")

st.sidebar.header("🔎 Actual RE Refraction Sphere and Actual LE Refraction Sphere")
actual_re = st.sidebar.number_input("RE Actual Refraction (D)", 0.0, 6.0, 0.0, 0.25)
actual_le = st.sidebar.number_input("LE Actual Refraction (D)", 0.0, 6.0, 0.0, 0.25)

st.sidebar.header("🔍 BIA and Q Modulation Settings")
bia = st.sidebar.slider("Binocular Inherent Accommodation (BIA)", 0.0, 2.5, 0.0, 0.25)
re_q = st.sidebar.slider("RE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.00, 0.06)
le_q = st.sidebar.slider("LE Q Value Δ (Max 0.36)", 0.00, 0.36, 0.00, 0.06)

st.sidebar.header("🔧 Refraction Changes")
re_refraction = st.sidebar.slider("Right Eye Refraction Add (D)", 0.0, 6.0, 0.0, 0.25)
le_refraction = st.sidebar.slider("Left Eye Refraction Add (D)", 0.0, 6.0, 0.0, 0.25)

st.sidebar.header("👓 Monovision Adjustments")
monovision_eye = st.sidebar.selectbox("Eye for Monovision", ["None", "Right Eye", "Left Eye"])
monovision_add = st.sidebar.slider("Monovision Add (D)", 0.0, 1.5, 0.0, 0.25)

show_overlap = st.sidebar.checkbox("🔷 Show Binocular Overlap", value=False)

se_re = st.sidebar.number_input("RE Spherical Equivalent (D)", 0.0, 6.0, 0.0, 0.25, key="se_re")
se_le = st.sidebar.number_input("LE Spherical Equivalent (D)", 0.0, 6.0, 0.0, 0.25, key="se_le")

st.sidebar.header("🌀 Preop Corneal SA (6mm)")
sa_re = st.sidebar.number_input("RE Spherical Aberration (SA)", 0.0, 0.6, 0.0, 0.01, key="sa_re")
sa_le = st.sidebar.number_input("LE Spherical Aberration (SA)", 0.0, 0.6, 0.0, 0.01, key="sa_le")


# Q to DOF conversion
def get_dof_from_se(se, sa_preop, pupil=3.0, k=1.5):
    if se == 0:
        return 0
    dof = (0.25 * se) * (4 / pupil)**2 * (1 - k * sa_preop)
    dof = max(dof, 0)
    return round(dof * 4) / 4

q_to_dof = 1.25 / 0.3



def plot_eye(ax, label, q_delta, bia, refraction, monovision, show_overlap=False, other_eye_dof=None, se_dof=0):
    q_dof = q_delta * q_to_dof
    net_shift = refraction + monovision

    retina_x = 0
    se_start = retina_x - net_shift
    se_end = se_start - se_dof

    bia_start = se_end
    bia_end = bia_start - bia

    q_start = retina_x - net_shift
    q_end = q_start + q_dof

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
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)
    ax.text(-2.5, 1.7, label, fontsize=11, weight='bold')

    if show_overlap:
        return (bia_end, q_end)
    return None


    retina_x = 0
    se_start = retina_x - net_shift
    se_end = se_start - se_dof

    bia_start = retina_x - net_shift
    bia_end = bia_start - bia

    q_start = retina_x - net_shift
    q_end = q_start + q_dof

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
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)
    ax.text(-2.5, 1.7, label, fontsize=11, weight='bold')

    if show_overlap:
        return (bia_end, q_end)
    return None


    retina_x = 0
    bia_start = retina_x - net_shift
    bia_end = bia_start - bia

    q_start = retina_x - net_shift
    q_end = q_start + q_dof

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

    ax.fill_betweenx([-0.4, 0.4], bia_end, bia_start, color='yellow', alpha=0.4)
    ax.fill_betweenx([-0.4, 0.4], q_start, q_end, color='green', alpha=0.3)
    ax.text(-2.5, 1.7, label, fontsize=11, weight='bold')

    if show_overlap:
        return (bia_end, q_end)
    return None

fig, axs = plt.subplots(2, 1, figsize=(10, 8))
for ax in axs:
    ax.set_xlim(-5, 2)
    ax.set_ylim(-2.5, 2.5)
    ax.axis('off')

re_mono = monovision_add if monovision_eye == "Right Eye" else 0
le_mono = monovision_add if monovision_eye == "Left Eye" else 0


re_se_dof = get_dof_from_se(se_re, sa_re)
le_se_dof = get_dof_from_se(se_le, sa_le)

re_dof = plot_eye(axs[0], f"Right Eye (Q Δ {re_q:.2f})", re_q, bia, re_refraction, re_mono, show_overlap, se_dof=re_se_dof)
le_dof = plot_eye(axs[1], f"Left Eye (Q Δ {le_q:.2f})", le_q, bia, le_refraction, le_mono, show_overlap, se_dof=le_se_dof)


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


# Final Treatment Summary
st.markdown("### 🧾 Final Treatment Plan")

final_re_sphere = actual_re + re_refraction + (monovision_add if monovision_eye == "Right Eye" else 0)
final_le_sphere = actual_le + le_refraction + (monovision_add if monovision_eye == "Left Eye" else 0)

st.write(f"**Right Eye Final Refraction Sphere:** {final_re_sphere:.2f} D")
st.write(f"**Left Eye Final Refraction Sphere:** {final_le_sphere:.2f} D")

st.write(f"**Right Eye Final Q Value Change:** ΔQ = {re_q:.2f}")
st.write(f"**Left Eye Final Q Value Change:** ΔQ = {le_q:.2f}")


st.markdown('''
### 📝 Instructions for Using the Presbyopic LASIK Simulator

**Use case:** This simulator is intended only for Hypermetropia / Hypermetropic Astigmatism cases.  
**Platform limitation:** It is to be used only with the Wavelight EX500 excimer laser system.  
**Optic Zone:** Applicable only for 6.0 mm Optic Zone.  
Topolyzer images should be captured to identify baseline Q values, Q value modulation should be done using Custom Q mode.  
The simulation does not alter the Q value directly but shows changes as offsets (ΔQ).

---

### 👁️ Visual Simulator Controls:

- **Refraction (RE/LE):** Set the actual hypermetropic spherical power for each eye. This sets the base retinal focus.
- **BIA (Binocular Inherent Accommodation):** Enter BIA manually (formula: BIA = 2.5 - Reading Add required binocularly). This creates a natural depth of focus toward near.
- **Q Value Modulation:** Simulates extended depth of focus by increasing negative asphericity.
- **Refraction Changes:** Allows refraction to be increased for each eye, shifting "Q value modulated" depth of focus to move forward.
- **Monovision Add:** Adds extra refraction to one eye (user selectable), simulating monovision configuration.
- **Binocular Overlap Option:** Displays a cyan-shaded area where both eyes' DOF overlap. Ideal overlap: 1.0–1.5 D.

---

### 📌 Notes:

- You do not need to cross the 2.5D near vision line, as this represents normal reading distance (25 cm).
- If binocular overlap is <0.75D, fusion and visual comfort may be compromised.
- All ranges are dynamically updated and proportional to Q-value or refraction changes.
- End result should be a focus ranging from retinal focus until near focus, keeping binocular balance between 1 to 1.5D.
- Maximum Q value modulation allowed is 0.36, as greater than this will cause loss of contrast.
''')

# Footer Credits
st.markdown("---")
st.markdown("""
**Developed by Dr. Zain Khatib, Mumbai**  
**Algorithm:** CAMP (Controlled Asphericity Modulation for Presbyopia)  
**Simulator:** ZOOM (Zain's Optical Overlap Model)
""")
