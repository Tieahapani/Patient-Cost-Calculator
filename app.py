import streamlit as st
from calculator import calculate_patient_cost

st.set_page_config(page_title="Patient Medical Cost Calculator", layout="wide")

# --- INITIALIZE SESSION STATE ---
def initialize_session_state():
    """Initialize session state variables with default values"""
    defaults = {
        "patient_name": "",
        "mri_number": "",
        "insurance_company": "",
        "cpt_code": "",
        "procedure_cost": 0.0,
        "remaining_deductible": 0.0,
        "copay": 0.0,
        "oop_max": 0.0,
        "coinsurance": 20
    }
    
    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

# --- RESET FUNCTION ---
def reset_form():
    """Reset all form fields to their default values"""
    st.session_state.patient_name = ""
    st.session_state.mri_number = ""
    st.session_state.insurance_company = ""
    st.session_state.cpt_code = ""
    st.session_state.procedure_cost = 0.0
    st.session_state.remaining_deductible = 0.0
    st.session_state.copay = 0.0
    st.session_state.oop_max = 0.0
    st.session_state.coinsurance = 20
    st.rerun()

# Initialize session state before using it
initialize_session_state()

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
        cpt_code = st.text_input("CPT Code (5 characters)", max_chars=6, key="cpt_code")
    
    st.markdown("<h2 style='color:#007C91;'>Medical Cost Inputs</h2>", unsafe_allow_html=True)
    
    st.number_input("Procedure Cost ($)", key="procedure_cost", min_value=0.0)
    st.number_input("Remaining Deductible ($)", key="remaining_deductible", min_value=0.0)
    st.slider("Co-Insurance (%)", min_value=0, max_value=100, 
              value=st.session_state.coinsurance, step=1, key="coinsurance")
    st.number_input("Co-Pay Amount ($)", key="copay", min_value=0.0)
    st.number_input("Out-of-Pocket Max ($)", key="oop_max", min_value=0.0)
    
    # --- BUTTONS: CALCULATE & RESET (BOTTOM) ---
    button_col1, button_col2 = st.columns([1, 1])
    with button_col1:
        calculate_pressed = st.button("📋 Calculate")
    with button_col2:
        if st.button("🔁 Reset (Below)"):
            reset_form()

# --- RESULTS SECTION ---
with col2:
    if calculate_pressed:
        # Get values from session state
        procedure_cost = st.session_state.procedure_cost
        remaining_deductible = st.session_state.remaining_deductible
        coinsurance = st.session_state.coinsurance
        copay = st.session_state.copay
        oop_max = st.session_state.oop_max
        
        # Only calculate if we have a valid procedure cost
        if procedure_cost > 0:
            patient_cost, insurance_covers = calculate_patient_cost(
                procedure_cost, remaining_deductible, coinsurance, copay, oop_max
            )
            
            st.markdown("<h2 style='color:#007C91;'>🧾 Results</h2>", unsafe_allow_html=True)
            st.markdown(f"**Patient Name:** {st.session_state.patient_name}")
            st.markdown(f"**MRI Number:** {st.session_state.mri_number}")
            st.markdown(f"**Insurance Company:** {st.session_state.insurance_company}") 
            st.markdown(f"**CPT Code:** {st.session_state.cpt_code.upper()}") 
            st.success(f"**Patient Pays:** ${patient_cost:.2f}")
            st.info(f"**Insurance Covers:** ${insurance_covers:.2f}")
        else:
            st.warning("Please enter a valid procedure cost to calculate results.")
