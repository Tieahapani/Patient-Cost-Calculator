import streamlit as st
from calculator import calculate_patient_cost

# --- RESET LOGIC ---
if "reset_trigger" in st.session_state and st.session_state["reset_trigger"]:
    for key in ["procedure_cost", "deductible", "paid_so_far", "coinsurance", "copay", "oop_max"]:
        st.session_state[key] = 0.0 if key != "coinsurance" else 0  # Float for inputs, int for slider
    st.session_state["reset_trigger"] = False
    st.rerun()  # Requires Streamlit v1.25 or higher

# --- UI ---
st.title("🩺 Patient Medical Cost Calculator")

st.number_input("Procedure Cost ($)", key="procedure_cost")
st.number_input("Annual Deductible ($)", key="deductible")
st.number_input("Amount Paid Toward Deductible ($)", key="paid_so_far")
st.slider("Co-Insurance (%)", min_value=0, max_value=100, step=1, key="coinsurance")
st.number_input("Co-Pay Amount ($)", key="copay")
st.number_input("Out-of-Pocket Max ($)", key="oop_max")

# --- CALCULATE + TRIGGER RESET ---
if st.button("📋 Calculate"):
    # Extract values from session state
    procedure_cost = st.session_state["procedure_cost"]
    deductible = st.session_state["deductible"]
    paid_so_far = st.session_state["paid_so_far"]
    coinsurance = st.session_state["coinsurance"]
    copay = st.session_state["copay"]
    oop_max = st.session_state["oop_max"]

    # Perform calculation
    patient_cost, insurance_covers = calculate_patient_cost(
        procedure_cost, deductible, paid_so_far, coinsurance, copay, oop_max
    )
    st.success(f"Patient Pays: ${patient_cost:.2f}")
    st.info(f"Insurance Covers: ${insurance_covers:.2f}")

    # Set trigger for reset on next rerun
    st.session_state["reset_trigger"] = True
