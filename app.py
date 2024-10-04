import streamlit as st



def get_dosage_by_weight(weight, formulation):
    # Define weight ranges and corresponding dosages
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
    # Define age ranges and corresponding dosages
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
    # Formulation options with numerical choice
    formulations = {
        1: ('Infant drops', 50 / 1.25, 'liquid'),  # mg per mL
        2: ('Children’s liquid', 100 / 5, 'liquid'),  # mg per mL
        3: ('Chewable tablets', 50, 'tablet'),  # mg per tablet
        4: ('Junior-strength chewable tablets', 100, 'tablet'),  # mg per tablet
        5: ('Adult Tablets', 200, 'tablet')  # mg per tablet
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


def restart_prompt():
    # Ask if the user wants to restart or exit
    restart = input("Would you like to restart the calculator? (yes/no): ").strip().lower()
    if restart == 'yes':
        main()  # Restart the calculator
    else:
        st.write("Exiting the calculator. Goodbye!")

st.title("Ibuprofen Dosage Calculator")

def main():
    while True:  # Loop to allow for multiple calculations
        # Ask the user to dose by weight or age
        choice = input("Would you like to dose by (1) weight or (2) age? ").strip()

        if choice == '1':
            try:
                # Ask for units: kg or lbs
                unit = input("Would you like to enter the weight in (1) kg or (2) lbs? ").strip()

                if unit == '1':
                    weight = st.number_input("Enter the patient's weight in kg: ").strip()
                elif unit == '2':
                    weight_in_lbs = st.number_input("Enter the patient's weight in lbs: ").strip()
                    # Convert pounds to kilograms (1 lb = 0.453592 kg)
                    weight = weight_in_lbs * 0.453592
                else:
                    st.write("Invalid unit choice.")
                    restart_prompt()
                    continue

                # Check if weight is within the acceptable range
                if weight < 5.4:  # Assuming 5.4 kg is the minimum for ibuprofen
                    st.write("This weight does not routinely receive ibuprofen, please consult a medical provider.")
                    restart_prompt()
                    continue

                # Display the formulation choices as numbers
                st.write("Select a formulation:")
                st.write("1. Infant drops (50 mg/1.25mL)")
                st.write("2. Children’s liquid (100 mg/5mL)")
                st.write("3. Chewable tablets (50 mg)")
                st.write("4. Junior-strength chewable tablets (100 mg)")
                st.write("5. Adult Tablets (200 mg)")

                formulation = int(input("Enter the number corresponding to the formulation: ").strip())

                if formulation not in range(1, 6):
                    st.write("Invalid formulation choice.")
                    restart_prompt()
                    continue

                result = get_dosage_by_weight(weight, formulation)

            except ValueError:
                st.write("Invalid input for weight or formulation. Please enter a valid number.")
                restart_prompt()
                continue
        elif choice == '2':
            try:
                age = int(input("Enter the patient's age in months: ").strip())

                # Check if age is within the acceptable range
                if age < 6:  # Assuming 6 months is the minimum for ibuprofen
                    st.write("This age does not routinely receive ibuprofen, please consult a medical provider.")
                    restart_prompt()
                    continue

                # Display the formulation choices as numbers
                st.write("Select a formulation:")
                st.write("1. Infant drops (50 mg/1.25mL)")
                st.write("2. Children’s liquid (100 mg/5mL)")
                st.write("3. Chewable tablets (50 mg)")
                st.write("4. Junior-strength chewable tablets (100 mg)")
                st.write("5. Adult Tablets (200 mg)")

                formulation = int(input("Enter the number corresponding to the formulation: ").strip())

                if formulation not in range(1, 6):
                    st.write("Invalid formulation choice.")
                    restart_prompt()
                    continue

                result = get_dosage_by_age(age, formulation)

            except ValueError:
                st.write("Invalid input for age or formulation. Please enter a valid number.")
                restart_prompt()
                continue
        else:
            st.write("Invalid choice. Please enter 1 for weight or 2 for age.")
            restart_prompt()
            continue

        # Print the result only if the dosage calculation is successful
        if "does not routinely receive ibuprofen" not in result:
            st.write(result)
        restart_prompt()  # After displaying the result, ask if they want to restart


if __name__ == "__main__":
    main()
