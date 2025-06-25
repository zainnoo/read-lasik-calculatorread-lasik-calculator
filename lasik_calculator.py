import streamlit as st

st.title("ZAIN's READ LASIK Calculator")

st.markdown("""
This tool calculates the final refraction and Q value changes for presbyopic LASIK in hypermetropic patients based on your proprietary algorithm.
""")

# Inputs
st.header("🔢 Input Values")
re_od = st.number_input("Right Eye Refraction (OD)", min_value=0.0, max_value=10.0, value=1.50, step=0.25)
re_os = st.number_input("Left Eye Refraction (OS)", min_value=0.0, max_value=10.0, value=2.25, step=0.25)
monovision_tolerance = st.number_input("Max Monovision Tolerance (D)", min_value=0.0, max_value=3.0, value=1.50, step=0.25)
extra_add = st.number_input("Extra Near Add Required (D)", min_value=0.0, max_value=3.0, value=0.50, step=0.25)

# Constants
q_per_d = 0.3 / 1.25

# Calculations
le_q_change = round(q_per_d * monovision_tolerance, 2)
le_final_refraction = round(re_os + monovision_tolerance + extra_add, 2)
re_final_refraction = round(re_od + extra_add, 2)
re_q_change = round(q_per_d * extra_add, 2)

# Output
st.header("📊 Results")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Right Eye (OD)")
    st.write(f"**Final Refraction:** {re_final_refraction} D")
    st.write(f"**Q Value Increase:** {re_q_change}")

with col2:
    st.subheader("Left Eye (OS)")
    st.write(f"**Final Refraction:** {le_final_refraction} D")
    st.write(f"**Q Value Increase (limited to tolerance):** {le_q_change}")

st.markdown("---")
st.caption("Developed for Khatib Eye Clinic | Based on ZAIN's READ LASIK algorithm")
