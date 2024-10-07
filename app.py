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
        'Infant Drops': ('Infant Drops', 50 / 1.25, 'liquid', '<2', '<23'),
        'Children’s Liquid': ('Children’s Liquid', 100 / 5, 'liquid', '>2, <12', '>22, <96'),
        'Chewable Tablets': ('Chewable Tablets', 50, 'tablet', '>2, <12', '>22, <96'),
        'Junior-Strength Chewable Tablets': ('Junior-Strength Chewable Tablets', 100, 'tablet', '>2, <12', '>22, <96'),
        'Adult Tablets': ('Adult Tablets', 200, 'tablet', '>10', '>55')
    }

    formulation_cleaned = formulation.split('(')[0].strip()

    if formulation_cleaned not in formulations:
        return "Formulation not available."

    formulation_name, concentration, form_type, age_range, weight_range = formulations[formulation_cleaned]

    if age is not None:
        if (formulation_cleaned == 'Infant Drops' and age >= 24) or \
           (formulation_cleaned in ['Children’s Liquid', 'Chewable Tablets', 'Junior-Strength Chewable Tablets'] and not (24 <= age <= 143)) or \
           (formulation_cleaned == 'Adult Tablets' and age < 120):
            warning = f"{formulation_name} is not typically used for this age. Please make sure you selected the correct formulation."
            st.warning(warning)

    if weight is not None:
        if (formulation_cleaned == 'Infant Drops' and weight >= 23) or \
           (formulation_cleaned in ['Children’s Liquid', 'Chewable Tablets', 'Junior-Strength Chewable Tablets'] and not (22 < weight < 50)) or \
           (formulation_cleaned == 'Adult Tablets' and weight <= 55):
            warning = f"{formulation_name} is not typically used for this weight. Please make sure you selected the correct formulation."
            st.warning(warning)

    if form_type == 'liquid':
        dose_ml = dosage_mg / concentration
        return f"Dosage: {round(dose_ml, 1)} mL of {formulation_name}"
    else:
        dose_tablets = dosage_mg / concentration
        return f"Dosage: {round(dose_tablets, 1)} tablets of {formulation_name}"


# Streamlit app layout
st.title("Ibuprofen Dosing Calculator")

choice = st.selectbox("Select Dosing by Weight or Age", ["Weight", "Age"])

if choice == "Weight":
    unit = st.selectbox("Select Dosing By Kilograms or Pounds", ["Kilograms", "Pounds"])

    weight = st.number_input(f"Enter the Patient's Weight in {unit}", min_value=0.0, step=1.0)

    if unit == "Pounds":
        weight *= 0.453592

    if weight <= 0:
        st.error("Invalid weight. Please enter a weight greater than zero.")
        st.stop()

    formulation = st.selectbox("Select the Formulation", 
                               ["Infant Drops (50mg/1.25mL)", 
                                "Children’s Liquid (100mg/5mL)", 
                                "Chewable Tablets (50mg/tablet)", 
                                "Junior-Strength Chewable Tablets (100mg/tablet)", 
                                "Adult Tablets (200mg/tablet)"])
    
    if st.button("Calculate Dosage"):
        result = get_dosage_by_weight(weight, formulation)
        st.write(result)
        st.write("Dose: Give every 6 hours if needed, for fever or pain. DO NOT GIVE MORE THAN 4 DOSES IN 24 HOURS.")
        st.write("[Dosing in this calculator comes from healthychildren.org](https://www.healthychildren.org/English/safety-prevention/at-home/medication-safety/Pages/Ibuprofen-for-Fever-and-Pain.aspx)")


elif choice == "Age":
    age_unit = st.selectbox("Select Age as Years or Months", ["Years", "Months"])

    if age_unit == "Years":
        age_years = st.number_input("Enter the Patient's Age in Years", min_value=0, step=1)
        age = age_years * 12
    else:
        age = st.number_input("Enter the Patient's Age in Months", min_value=0, step=1)

    if age < 6:
        st.error("This age does not routinely receive ibuprofen. Please consult a medical provider.")
        st.stop()

    formulation = st.selectbox("Select The Formulation", 
                               ["Infant Drops (50mg/1.25mL)", 
                                "Children’s Liquid (100mg/5mL)", 
                                "Chewable Tablets (50mg/tablet)", 
                                "Junior-Strength Chewable Tablets (100mg/tablet)", 
                                "Adult Tablets (200mg/tablet)"])

    if st.button("Calculate Dosage"):
        result = get_dosage_by_age(age, formulation)
        st.write(result)
        st.write("Dose: Give every 6 hours if needed, for fever or pain. DO NOT GIVE MORE THAN 4 DOSES IN 24 HOURS.")
        st.write("[Dosing in this calculator comes from healthychildren.org](https://www.healthychildren.org/English/safety-prevention/at-home/medication-safety/Pages/Ibuprofen-for-Fever-and-Pain.aspx)")
