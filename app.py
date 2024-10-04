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
    
    return calculate_dose(dosage_mg, formulation)

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
    
    return calculate_dose(dosage_mg, formulation)

def calculate_dose(dosage_mg, formulation):
    formulations = {
        'Infant drops': ('Infant drops', 50 / 1.25, 'liquid'), 
        'Children’s liquid': ('Children’s liquid', 100 / 5, 'liquid'), 
        'Chewable tablets': ('Chewable tablets', 50, 'tablet'), 
        'Junior-strength chewable tablets': ('Junior-strength chewable tablets', 100, 'tablet'), 
        'Adult tablets': ('Adult Tablets', 200, 'tablet')
    }

    if formulation not in formulations:
        return "Formulation not available."

    formulation_name, concentration, form_type = formulations[formulation]

    if form_type == 'liquid':
        dose_ml = dosage_mg / concentration
        return f"Dosage: {dose_ml:.2f} mL of {formulation_name}"
    else:
        dose_tablets = dosage_mg / concentration
        return f"Dosage: {dose_tablets:.2f} tablets of {formulation_name}"

# Streamlit app layout
st.title("Ibuprofen Dosing Calculator")

choice = st.selectbox("Would you like to dose by weight or age?", ["weight", "age"])

if choice == "weight":
    unit = st.selectbox("Choose your units", ["kg", "pounds"])

    weight = st.number_input(f"Enter the patient's weight in {unit}", min_value=0.0, step=0.1)
    
    if unit == "pounds":
        weight *= 0.453592

    if weight <= 0:
        st.error("Invalid weight. Please enter a weight greater than zero.")
        st.stop()

    formulation = st.selectbox("Select the formulation", 
                               ["Infant drops", "Children’s liquid", 
                                "Chewable tablets", "Junior-strength chewable tablets", 
                                "Adult tablets"])
    
    if st.button("Calculate Dosage"):
        result = get_dosage_by_weight(weight, formulation)
        st.write(result)

elif choice == "age":
    age = st.number_input("Enter the patient's age in months", min_value=0, step=1)

    if age < 6:
        st.error("This age does not routinely receive ibuprofen. Please consult a medical provider.")
        st.stop()
    
    formulation = st.selectbox("Select the formulation", 
                               ["Infant drops", "Children’s liquid", 
                                "Chewable tablets", "Junior-strength chewable tablets", 
                                "Adult tablets"])
    
    if st.button("Calculate Dosage"):
        result = get_dosage_by_age(age, formulation)
        st.write(result)
