import streamlit as st
from calculator import calculate_patient_cost

st.set_page_config(page_title="Patient Medical Cost Calculator", layout="wide")

# --- TOP BAR WITH RESET BUTTON ---
top_col1, top_col2 = st.columns([5, 1])
with top_col1:
    st.title("🩺 Patient Medical Cost Calculator")
with top_col2:
    if st.button("🔄 Reset All (Top)"):
        for key in ["patient_name", "mri_number", "procedure_cost", "remaining_deductible", "copay", "oop_max"]:
            st.session_state[key] = "" if key in ["patient_name", "mri_number"] else 0.0
        # Reset slider separately to 20
        st.session_state["coinsurance"] = 20
        st.rerun()

# Use 2 unequal-width columns: form wider, result narrower
col1, col2 = st.columns([2, 1])  # 2:1 width ratio

# --- LEFT COLUMN: Form Inputs ---
with col1:
    st.header("Patient Info")
    patient_name = st.text_input("Patient Name", key="patient_name")
    mri_number = st.text_input("MRI Number", key="mri_number")

    st.header("Medical Cost Inputs")
    st.number_input("Procedure Cost ($)", key="procedure_cost")
    st.number_input("Remaining Deductible ($)", key="remaining_deductible")
    st.slider("Co-Insurance (%)", min_value=0, max_value=100, value=st.session_state.get("coinsurance", 20), step=1, key="coinsurance")
    st.number_input("Co-Pay Amount ($)", key="copay")
    st.number_input("Out-of-Pocket Max ($)", key="oop_max")

    # Buttons side-by-side
    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        calculate_pressed = st.button("📋 Calculate")
    with button_col2:
        if st.button("🔁 Reset (Below)"):
            for key in ["patient_name", "mri_number", "procedure_cost", "remaining_deductible", "copay", "oop_max"]:
                st.session_state[key] = "" if key in ["patient_name", "mri_number"] else 0.0
            st.session_state["coinsurance"] = 20
            st.rerun()

# --- RIGHT COLUMN: Results ---
with col2:
    if calculate_pressed:
        procedure_cost = st.session_state["procedure_cost"]
        remaining_deductible = st.session_state["remaining_deductible"]
        coinsurance = st.session_state["coinsurance"]
        copay = st.session_state["copay"]
        oop_max = st.session_state["oop_max"]

        patient_cost, insurance_covers = calculate_patient_cost(
            procedure_cost, remaining_deductible, coinsurance, copay, oop_max
        )

        st.header("🧾 Results")
        st.markdown(f"**Patient Name:** {patient_name}")
        st.markdown(f"**MRI Number:** {mri_number}")
        st.success(f"**Patient Pays:** ${patient_cost:.2f}")
        st.info(f"**Insurance Covers:** ${insurance_covers:.2f}")
