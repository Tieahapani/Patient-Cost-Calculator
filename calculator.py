def calculate_patient_cost(
    procedure_cost, remaining_deductible, coinsurance, copay, oop_max
):
    # Deductible applied is the lesser of procedure cost or remaining deductible
    deductible_applied = min(procedure_cost, remaining_deductible)

    # What's left after deductible
    remaining_cost = procedure_cost - deductible_applied

    # Coinsurance only applies on the amount after deductible
    coinsurance_amount = remaining_cost * (coinsurance / 100)

    # Total cost to patient: deductible + coinsurance + copay (unless it exceeds OOP max)
    total_patient_cost = deductible_applied + coinsurance_amount + copay
    total_patient_cost = min(total_patient_cost, oop_max)

    # Insurance covers the rest
    insurance_covers = procedure_cost - total_patient_cost

    return round(total_patient_cost, 2), round(insurance_covers, 2)
