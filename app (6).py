import streamlit as st
import pandas as pd

# --- 1. Data Storage Initialization ---
if 'patient_records_df' not in st.session_state:
    st.session_state.patient_records_df = pd.DataFrame(columns=[
        'AGE', 'GENDER', 'WEIGHT(kg)', 'HEIGHT(cm)', 'BMI',
        'WAIST CIRCUMFERENCE', 'BP(mmHg)', 'BLOOD SUGAR(mmol/L)',
        'HTN', 'DIABETES', 'BOTH DM+HTN', 'TREATMENT', 'VISIT TYPE'
    ])

# --- 2. BMI Calculation Function ---
def calculate_bmi(weight_kg, height_cm):
    """Calculates BMI given weight in kg and height in cm."""
    try:
        if weight_kg > 0 and height_cm > 0:
            height_m = height_cm / 100.0
            bmi = weight_kg / (height_m ** 2)
            return round(bmi, 2)
        return None
    except:
        return None

# --- 3. Streamlit UI ---

st.title('🏥 Clinical Data Entry Form')

# Use columns for layout
col1, col2 = st.columns(2)

with col1:
    st.header("Patient Details")
    age = st.number_input('Age:', min_value=1, max_value=120, value=1, step=1)
    gender = st.radio('Gender:', ['Male', 'Female'])
    weight = st.number_input('Weight (kg):', min_value=10.0, value=10.0, step=0.1)
    height = st.number_input('Height (cm):', min_value=50.0, value=50.0, step=0.1)
    bmi_val = calculate_bmi(weight, height)
    st.text_input('BMI:', value=str(bmi_val) if bmi_val is not None else '—', disabled=True)
    waist = st.number_input('Waist Circ (cm):', min_value=10.0, value=10.0, step=0.1)

    # ✅ Add Visit Type here
    visit_type = st.selectbox(
        'Visit Type:',
        ['New Visit', 'Follow-up', 'Referral', 'Emergency', 'Routine Checkup']
    )

with col2:
    st.header("Clinical Metrics")
    bp = st.text_input('BP (mmHg):', placeholder='e.g., 140/90')
    sugar = st.number_input('Blood Sugar (mmol/L):', min_value=2.0, value=2.0, step=0.1)
    treatment = st.text_input('Treatment Code:', placeholder='e.g., abe')

    st.header("Diagnosis Status")
    htn = st.checkbox('Hypertension (HTN)')
    dm = st.checkbox('Diabetes (DM)')
    both = st.checkbox('Both DM + HTN')

# --- 4. Button Actions ---
save_button = st.button('Save Record')
clear_button = st.button('Clear Form')
download_button = st.button('Download Records (CSV)')

# Save Record Logic
if save_button:
    if not age or not weight or not height:
        st.error("Error: Age, Weight, and Height are required.")
    else:
        new_record = {
            'AGE': age,
            'GENDER': gender[0],  # 'M' or 'F'
            'WEIGHT(kg)': weight,
            'HEIGHT(cm)': height,
            'BMI': bmi_val,
            'WAIST CIRCUMFERENCE': waist,
            'BP(mmHg)': bp,
            'BLOOD SUGAR(mmol/L)': sugar,
            'HTN': 1 if htn else 0,
            'DIABETES': 1 if dm else 0,
            'BOTH DM+HTN': 1 if both else 0,
            'TREATMENT': treatment,
            'VISIT TYPE': visit_type   # ✅ New field added
        }

        st.session_state.patient_records_df = pd.concat(
            [st.session_state.patient_records_df, pd.DataFrame([new_record])],
            ignore_index=True
        )
        st.success(f"Record for Age {age} saved successfully!")

# Download Records Logic
if download_button:
    if not st.session_state.patient_records_df.empty:
        csv_data = st.session_state.patient_records_df.to_csv(index=False)
        st.download_button(
            label="Click to Download",
            data=csv_data,
            file_name='patient_records_export.csv',
            mime='text/csv'
        )
    else:
        st.info("No records to download yet.")

# Display Saved Records
st.markdown('<hr>', unsafe_allow_html=True)
st.header("Saved Records")
if not st.session_state.patient_records_df.empty:
    st.dataframe(st.session_state.patient_records_df)
    st.write("Total Records:", len(st.session_state.patient_records_df))
else:
    st.write("No records saved yet.")

# Clear Form Logic
if clear_button:
    st.info("Form clear button clicked. Note: Input fields are not automatically reset without a script rerun.")
