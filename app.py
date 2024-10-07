import streamlit as st

# Function to get dosage by weight
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

# Function to get dosage by age
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

# Function to calculate dose
def calculate_dose(dosage_mg, formulation):
    formulations = {
        'Infant drops (50mg/1.25mL)': ('Infant drops', 50 / 1.25, 'liquid'), 
        'Children’s liquid (100mg/5mL)': ('Children’s liquid', 100 / 5, 'liquid'), 
        'Chewable tablets (50mg/tablet)': ('Chewable tablets', 50, 'tablet'), 
        'Junior-strength chewable tablets (100mg/tablet)': ('Junior-strength chewable tablets', 100, 'tablet'), 
        'Adult tablets (200mg/tablet)': ('Adult Tablets', 200, 'tablet')
    }

    if formulation not in formulations:
        return "Formulation not available."

    formulation_name, concentration, form_type = formulations[formulation]

    # Calculate the required dose based on formulation type
    if form_type == 'liquid':
        dose_ml = round(dosage_mg / concentration, 1)  # Round to the tenth place
        return f"Dosage: {dose_ml} mL of {formulation_name}"
    else:
        dose_tablets = round(dosage_mg / concentration, 1)  # Round to the tenth place
        return f"Dosage: {dose_tablets} tablets of {formulation_name}"

# Streamlit app layout
st.title("Ibuprofen Dosing Calculator")

# Ask the user to choose between dosing by weight or age
choice = st.selectbox("Would you like to dose by weight or age?", ["weight", "age"])

if choice == "weight":
    # Input for weight in kg or lbs
    unit = st.selectbox("Choose your units", ["Kilograms", "Pounds"])
    
    # Updated weight input field to start at 0 and allow decimals
    weight = st.number_input(f"Enter the patient's weight in {unit}", min_value=0.0, step=1.0, format="%.1f")
    
    # Convert pounds to kg if necessary
    if unit == "Pounds":
        weight *= 0.453592

    # Ensure weight is greater than zero
    if weight <= 0:
        st.error("Invalid weight. Please enter a weight greater than zero.")
        st.stop()

    # Display formulation options with concentrations
    formulation = st.selectbox("Select the formulation", 
                               ["Infant drops (50mg/1.25mL)", 
                                "Children’s liquid (100mg/5mL)", 
                                "Chewable tablets (50mg/tablet)", 
                                "Junior-strength chewable tablets (100mg/tablet)", 
                                "Adult tablets (200mg/tablet)"])
    
    # Calculate the dose when the button is clicked
    if st.button("Calculate Dosage"):
        result = get_dosage_by_weight(weight, formulation)
        st.write(result)

elif choice == "age":
    # Ask if the user wants to enter the age in years or months
    age_unit = st.selectbox("Would you like to enter the age in years or months?", ["Years", "Months"])

    # Convert years to months if necessary
    if age_unit == "Years":
        age_years = st.number_input("Enter the patient's age in years", min_value=0, step=1)
        age = age_years * 12  # Convert years to months
    else:
        age = st.number_input("Enter the patient's age in months", min_value=0, step=1)

    # Ensure age is within the valid range
    if age < 6:
        st.error("This age does not routinely receive ibuprofen. Please consult a medical provider.")
        st.stop()

    # Display formulation options with concentrations
    formulation = st.selectbox("Select the formulation", 
                               ["Infant drops (50mg/1.25mL)", 
                                "Children’s liquid (100mg/5mL)", 
                                "Chewable tablets (50mg/tablet)", 
                                "Junior-strength chewable tablets (100mg/tablet)", 
                                "Adult tablets (200mg/tablet)"])
    
    # Calculate the dose when the button is clicked
    if st.button("Calculate Dosage"):
        result = get_dosage_by_age(age, formulation)
        st.write(result)
