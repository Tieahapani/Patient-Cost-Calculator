import streamlit as st
from calculator import calculate_patient_cost

st.set_page_config(
    page_title="Out Of Pocket Cost Calculator", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS to reduce spacing and make layout more compact
st.markdown("""
<style>
    /* Reduce top padding */
    .main > div {
        padding-top: 1rem;
    }
    
    /* Reduce spacing between elements */
    .stMarkdown {
        margin-bottom: 0.5rem;
    }
    
    /* Compact form inputs */
    .stTextInput > div > div > input {
        height: 2.5rem;
    }
    
    .stNumberInput > div > div > input {
        height: 2.5rem;
    }
    
    /* Reduce header spacing */
    h1, h2, h3 {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    /* Compact button styling */
    .stButton > button {
        height: 2.5rem;
        margin-top: 0.5rem;
    }
    
    /* Reduce column gaps */
    .css-1d391kg {
        gap: 1rem;
    }
    
    /* Make results section sticky on larger screens */
    @media (min-width: 768px) {
        .results-container {
            position: sticky;
            top: 1rem;
            max-height: 90vh;
            overflow-y: auto;
        }
    }
</style>
""", unsafe_allow_html=True)

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
col1, col2 = st.columns([3, 2])  # Adjusted ratio for better space usage

# --- TITLE + RESET BUTTON INLINE ---
with col1:
    title_col, reset_button_col = st.columns([6, 1])  # More compact title area
    
    with title_col:
        st.markdown(
            """
            <h1 style='font-family: "Segoe UI", sans-serif;
                       color: #007C91;
                       font-weight: bold;
                       margin-bottom: 0.5rem;
                       font-size: 1.8rem;'>
                🩺 Out Of Pocket Cost Calculator
            </h1>
            """,
            unsafe_allow_html=True
        )
    
    with reset_button_col:
        if st.button("🔄", help="Reset Form"):
            reset_form()

    # --- INPUT SECTIONS ---
    st.markdown("<h3 style='color:#007C91; margin-bottom: 0.5rem;'>Patient Info</h3>", unsafe_allow_html=True)
    
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        patient_name = st.text_input("Patient Name", key="patient_name", placeholder="Enter patient name")
    with row1_col2: 
        insurance_company = st.text_input("Insurance Company", key="insurance_company", placeholder="Insurance provider")
    
    row2_col1, row2_col2 = st.columns(2)
    with row2_col1: 
        mri_number = st.text_input("MRI Number", key="mri_number", placeholder="MRI number")
    with row2_col2: 
        cpt_code = st.text_input("CPT Code", max_chars=6, key="cpt_code", placeholder="5-digit code")
    
    st.markdown("<h3 style='color:#007C91; margin-bottom: 0.5rem; margin-top: 1rem;'>Medical Cost Inputs</h3>", unsafe_allow_html=True)
    
    # Arrange cost inputs in a more compact layout
    cost_col1, cost_col2 = st.columns(2)
    with cost_col1:
        st.number_input("Procedure Cost ($)", key="procedure_cost", min_value=0.0, placeholder="0.00")
        st.number_input("Remaining Deductible ($)", key="remaining_deductible", min_value=0.0, placeholder="0.00")
        st.number_input("Out-of-Pocket Max ($)", key="oop_max", min_value=0.0, placeholder="0.00")
    
    with cost_col2:
        st.slider("Co-Insurance (%)", min_value=0, max_value=100, 
                  value=st.session_state.coinsurance, step=5, key="coinsurance")
        st.number_input("Co-Pay Amount ($)", key="copay", min_value=0.0, placeholder="0.00")
        
        # Add some spacing to align with the left column
        st.write("")
    
    # --- CALCULATE BUTTON (PROMINENT) ---
    st.markdown("<div style= 'margin-top: 1rem;'></div>", unsafe_allow_html=True)
    calculate_pressed = st.button("📋 Calculate Patient Cost", type="primary", use_container_width=True)
    

# --- RESULTS SECTION ---
with col2:
    # Add container for sticky positioning on larger screens
    st.markdown('<div class="results-container">', unsafe_allow_html=True)
    
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
        st.markdown("<h2 style='color: #007C91;'>🧾 Results</h2>", unsafe_allow_html=True)
        st.markdown(f"Patient Name: {patient_name}")
        st.markdown(f"MRI Number: {mri_number}")
        st.markdown(f"Insurance Company: {insurance_company}") 
        st.markdown(f"CPT Code: {cpt_code.upper()}") 
        st.success(f"Patient Pays: ${patient_cost:.2f}")
        st.info(f"Insurance Covers: ${insurance_covers:.2f}")
            
            
                

            
