
import streamlit as st

st.set_page_config(page_title="ZOOM LASIK Simulator Hub", page_icon="🧿", layout="centered")

st.title("🧿 ZOOM LASIK Simulator Hub")
st.markdown("Welcome to the LASIK simulation platform powered by the ZOOM model.")

st.markdown("""
### 👁 Available Simulators:
- **Hyperopic LASIK Model** (based on the CAMP algorithm)
- **Myopic LASIK Model** (Q-free, SA-controlled)

Use the **sidebar** to switch between models.
""")

st.success("Choose a model from the sidebar ➡️")
