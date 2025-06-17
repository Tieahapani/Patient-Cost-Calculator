# calculator.py

def calculate_patient_cost(
    procedure_cost, deductible, paid_so_far, coinsurance, copay, oop_max
):
    remaining_deductible = max(deductible - paid_so_far, 0)
    after_deductible = max(procedure_cost - remaining_deductible, 0)
    coinsurance_amount = after_deductible * (coinsurance / 100)
    
    total_patient_cost = remaining_deductible + coinsurance_amount + copay
    total_patient_cost = min(total_patient_cost, oop_max)
    #if the patient cost reaches above the oop_max then it is covered by the insurance 
    insurance_covers = procedure_cost - total_patient_cost
    return total_patient_cost, insurance_covers
