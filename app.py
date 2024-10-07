import streamlit as st

def get_dosage_by_weight(weight, formulation):
    if 5.4 <= weight <= 8.1:
        dosage_mg = 50
    elif 8.2 <= weight <= 10.8:
        dosage_mg = 75
    elif 10.9 <= weight <= 16.3:
        dosage_mg = 100
    elif 16.4 <= weight <= 21.7:
        dosage_mg = 150
    elif 21.8 <= weight <= 27.2:
        dosage_mg = 200
    elif 27.3 <= weight <= 32.6:
        dosage_mg = 225
    elif 32.7 <= weight <= 43.2:
        dosage_mg = 300
    elif weight > 43.2:
        dosage_mg = 400
    else:
        return "This weight does not routinely receive ibuprofen, please consult a medical provider."
    
    return calculate_dose(dosage_mg, formulation, weight=weight)


def get_dosage_by_age(age, formulation):
    if 6 <= age <= 11:
        dosage_mg = 50
    elif 12 <= age <= 23:
        dosage_mg = 75
    elif 24 <= age <= 35:
        dosage_mg = 100
    elif 36 <= age <= 47:
        dosage_mg = 150
    elif 48 <= age <= 59:
        dosage_mg = 200
    elif 60 <= age <= 71:
        dosage_mg = 225
    elif age == 72 or age == 95:
        dosage_mg = 300
    elif age >= 96:
        dosage_mg = 400
    else:
        return "This age does not routinely receive ibuprofen, please consult a medical provider."
    
    return calculate_dose(dosage_mg, formulation, age=age)


def calculate_dose(dosage_mg, formulation, age=None, weight=None):
    formulations = {
        'Infant drops': ('Infant drops', 50 / 1.25, 'liquid', (0, 23), (0, 2)),
        'Children’s liquid': ('Children’s liquid', 100 / 5, 'liquid', (23, 96), (2, 12)),
        'Chewable tablets (50mg)': ('Chewable tablets', 50, 'tablet', (23, 96), (2, 12)),
        'Junior-strength chewable tablets (100mg)': ('Junior-strength chewable tablets', 100, 'tablet', (23, 96), (2, 12)),
        'Adult tablets (200mg)': ('Adult Tablets', 200, 'tablet', (55, float('inf')), (10, float('inf')))
    }

    if formulation not in formulations:
        return "Formulation not available."

    formulation_name, concentration, form_type, weight_range, age_range = formulations[formulation]

    warning = ""
    
    # Check for atypical formulation use
    if weight is not None and not (weight_range[0] <= weight <= weight_range[1]):
        warning = f"{formulation_name} is not typically used for this weight. Please make sure you selected the correct formulation."
    if age is not None and not (age_range[0] <= age/12 <= age_range[1]):
        warning = f"{formulation_name} is not typically used for this age. Please make sure you selected the correct formulation."

    if form_type == 'liquid':
        dose_ml = dosage_mg / concentration
        result = f"Dosage: {dose_ml:.1f} mL of {formulation_name}"
    else:
        dose_tablets = dosage_mg / concentration
        result = f"Dosage: {dose_tablets:.1f} tablets of {formulation_name}"

    return f"{warning}\n{result}" if warning else result


# Streamlit app layout
st.title("Ibuprofen Dosing Calculator")

# Capitalize the options in selection
choice = st.selectbox("Would you like to dose by Weight or Age?", ["Weight", "Age"])

if choice == "Weight":
    unit = st.selectbox("Choose your units", ["Kilograms", "Pounds"])

    weight = st.number_input(f"Enter the patient's weight in {unit}", min_value=0, step=1)
    
    if unit == "Pounds":
        weight *= 0.453592  # Convert pounds to kilograms

    if weight <= 0:
        st.error("Invalid weight. Please enter a weight greater than zero.")
        st.stop()

    formulation = st.selectbox("Select the formulation", 
                               ["Infant drops (50mg/1.25mL)", 
                                "Children’s liquid (100mg/5mL)", 
                                "Chewable tablets (50mg)", 
                                "Junior-strength chewable tablets (100mg)", 
                                "Adult tablets (200mg)"])
    
    if st.button("Calculate Dosage"):
        result = get_dosage_by_weight(weight, formulation.split()[0])  # Pass the formulation name without concentration
        st.write(result)

elif choice == "Age":
    # Add a selection for years or months
    age_unit = st.selectbox("Would you like to enter the age in Years or Months?", ["Years", "Months"])

    if age_unit == "Years":
        age_years = st.number_input("Enter the patient's age in years", min_value=0, step=1)
        age = age_years * 12  # Convert years to months
    else:
        age = st.number_input("Enter the patient's age in months", min_value=0, step=1)

    if age < 6:
        st.error("This age does not routinely receive ibuprofen. Please consult a medical provider.")
        st.stop()

    formulation = st.selectbox("Select the formulation", 
                               ["Infant drops (50mg/1.25mL)", 
                                "Children’s liquid (100mg/5mL)", 
                                "Chewable tablets (50mg)", 
                                "Junior-strength chewable tablets (100mg)", 
                                "Adult tablets (200mg)"])

    if st.button("Calculate Dosage"):
        result = get_dosage_by_age(age, formulation.split()[0])  # Pass the formulation name without concentration
        st.write(result)

