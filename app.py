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
        'Infant drops': ('Infant drops', 50 / 1.25, 'liquid', '<2', '<23'),
        'Children’s liquid': ('Children’s liquid', 100 / 5, 'liquid', '>2, <12', '>22, <96'),
        'Chewable tablets': ('Chewable tablets', 50, 'tablet', '>2, <12', '>22, <96'),
        'Junior-strength chewable tablets': ('Junior-strength chewable tablets', 100, 'tablet', '>2, <12', '>22, <96'),
        'Adult tablets': ('Adult Tablets', 200, 'tablet', '>10', '>55')
    }

    if formulation not in formulations:
        return "Formulation not available."

    formulation_name, concentration, form_type, age_range, weight_range = formulations[formulation]

    # Warning if age or weight does not match typical use
    if age is not None:
        if (formulation == 'Infant drops' and age >= 24) or \
           (formulation in ['Children’s liquid', 'Chewable tablets', 'Junior-strength chewable tablets'] and not (24 <= age <= 143)) or \
           (formulation == 'Adult tablets' and age < 120):
            warning = f"{formulation_name} is not typically used for this age. Please make sure you selected the correct formulation."
            st.warning(warning)

    if weight is not None:
        if (formulation == 'Infant drops' and weight >= 23) or \
           (formulation in ['Children’s liquid', 'Chewable tablets', 'Junior-strength chewable tablets'] and not (22 < weight < 96)) or \
           (formulation == 'Adult tablets' and weight <= 55):
            warning = f"{formulation_name} is not typically used for this weight. Please make sure you selected the correct formulation."
            st.warning(warning)

    # Calculate the required dose based on formulation type
    if form_type == 'liquid':
        dose_ml = dosage_mg / concentration
        return f"Dosage: {round(dose_ml, 1)} mL of {formulation_name}"
    else:
        dose_tablets = dosage_mg / concentration
        return f"Dosage: {round(dose_tablets, 1)} tablets of {formulation_name}"


# Streamlit app layout
st.title("Ibuprofen Dosing Calculator")

choice = st.selectbox("Would You Like To Dose By Weight Or Age?", ["Weight", "Age"])

if choice == "Weight":
    unit = st.selectbox("Choose Your Units", ["Kilograms", "Pounds"])

    weight = st.number_input(f"Enter The Patient's Weight In {unit}", min_value=0.0, step=0.1)

    if unit == "Pounds":
        weight *= 0.453592

    if weight <= 0:
        st.error("Invalid weight. Please enter a weight greater than zero.")
        st.stop()

    formulation = st.selectbox("Select The Formulation", 
                               ["Infant drops (50mg/1.25mL)", 
                                "Children’s liquid (100mg/5mL)", 
                                "Chewable tablets (50mg/tablet)", 
                                "Junior-strength chewable tablets (100mg/tablet)", 
                                "Adult tablets (200mg/tablet)"])
    
    if st.button("Calculate Dosage"):
        result = get_dosage_by_weight(weight, formulation.split()[0])
        st.write(result)

elif choice == "Age":
    age_unit = st.selectbox("Would You Like To Enter The Age In Years Or Months?", ["Years", "Months"])

    if age_unit == "Years":
        age_years = st.number_input("Enter The Patient's Age In Years", min_value=0, step=1)
        age = age_years * 12
    else:
        age = st.number_input("Enter The Patient's Age In Months", min_value=0, step=1)

    if age < 6:
        st.error("This age does not routinely receive ibuprofen. Please consult a medical provider.")
        st.stop()

    formulation = st.selectbox("Select The Formulation", 
                               ["Infant drops (50mg/1.25mL)", 
                                "Children’s liquid (100mg/5mL)", 
                                "Chewable tablets (50mg/tablet)", 
                                "Junior-strength chewable tablets (100mg/tablet)", 
                                "Adult tablets (200mg/tablet)"])

    if st.button("Calculate Dosage"):
        result = get_dosage_by_age(age, formulation.split()[0])
        st.write(result)


