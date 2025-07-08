import streamlit as st
from calculator import calculate_patient_cost

st.set_page_config(page_title="Patient Medical Cost Calculator", layout="wide")

# --- RESET FUNCTION ---
def reset_form():
    keys_to_clear = [
        "patient_name", "mri_number", "insurance_company", "cpt_code", "procedure_cost",
        "remaining_deductible", "copay", "oop_max", "coinsurance"
    ]
    for key in keys_to_clear:
        if key in st.session_state:
            if key in ["patient_name", "mri_number","insurance_company", "cpt_code"]:
                st.session_state[key] = ""
            elif key == "coinsurance":
                st.session_state[key] = 20
            else:
                st.session_state[key] = 0.0
    st.rerun()

# --- MAIN LAYOUT COLUMNS ---
col1, col2 = st.columns([2, 1])  # Left: form, Right: results

# --- TITLE + RESET BUTTON INLINE ---
with col1:
    title_col, reset_button_col = st.columns([8, 1])  # Wider title area
    with title_col:
        st.markdown(
            """
            <h2 style='font-family: "Segoe UI", sans-serif;
                       color: #007C91;
                       font-weight: bold;
                       margin-bottom: 0;'>
                🩺 Patient Medical Cost Calculator
            </h2>
            """,
            unsafe_allow_html=True
        )
    with reset_button_col:
        if st.button("🔄 Reset"):
            reset_form()

    # --- INPUT SECTIONS ---
    st.markdown("<h2 style='color:#007C91;'>Patient Info</h2>", unsafe_allow_html=True)
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
         patient_name = st.text_input("Patient Name", key="patient_name")
    with row1_col2: 
        insurance_company = st.text_input("Insurance Company", key="insurance_company")
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1: 
         mri_number = st.text_input("MRI Number", key="mri_number")
    with row2_col2: 
        cpt_code = st.text_input("CPT Code (5 characters)", max_chars= 6, key="cpt_code")

    st.markdown("<h2 style='color:#007C91;'>Medical Cost Inputs</h2>", unsafe_allow_html=True)
    st.number_input("Procedure Cost ($)", key="procedure_cost")
    st.number_input("Remaining Deductible ($)", key="remaining_deductible")
    st.slider("Co-Insurance (%)", min_value=0, max_value=100, value=st.session_state.get("coinsurance", 20), step=1, key="coinsurance")
    st.number_input("Co-Pay Amount ($)", key="copay")
    st.number_input("Out-of-Pocket Max ($)", key="oop_max") 
    st.markdown("---")

    # --- BUTTONS: CALCULATE & RESET (BOTTOM) ---
    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        calculate_pressed = st.button("📋 Calculate")
    with button_col2:
        if st.button("🔁 Reset (Below)"):
            reset_form()

# --- RESULTS SECTION ---
with col2:
    if 'calculate_pressed' in locals() and calculate_pressed:
        procedure_cost = st.session_state["procedure_cost"]
        remaining_deductible = st.session_state["remaining_deductible"]
        coinsurance = st.session_state["coinsurance"]
        copay = st.session_state["copay"]
        oop_max = st.session_state["oop_max"]

        patient_cost, insurance_covers = calculate_patient_cost(
            procedure_cost, remaining_deductible, coinsurance, copay, oop_max
        )

        st.markdown("<h2 style='color:#007C91;'>🧾 Results</h2>", unsafe_allow_html=True)
        st.markdown(f"**Patient Name:** {patient_name}")
        st.markdown(f"**MRI Number:** {mri_number}")
        st.markdown(f"**Insurance Company:** {insurance_company}") 
        st.markdown(f"**CPT Code:** {cpt_code.upper()}") 
        st.success(f"**Patient Pays:** ${patient_cost:.2f}")
        st.info(f"**Insurance Covers:** ${insurance_covers:.2f}")
