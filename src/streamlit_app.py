import streamlit as st
import pandas as pd
from model import DiabetesModel

st.title(" Diabetes Risk Predictor")

st.write("Enter your health information to predict diabetes risk:")

# Input fields
age = st.number_input("Age", min_value=20, max_value=100, value=40)
pregnancies = st.number_input("Pregnancies", min_value=0, max_value=17, value=0)
glucose = st.number_input("Glucose Level", min_value=40, max_value=600, value=110)
blood_pressure = st.number_input("Blood Pressure", min_value=20, max_value=200, value=80)
skin_thickness = st.number_input("Skin Thickness", min_value=3, max_value=150, value=5)
insulin = st.number_input("Insulin Level", min_value=10, max_value=1000, value=100)
bmi = st.number_input("BMI", min_value=15.0, max_value=100.0, value=25.0, step=0.1)
diabetes_pedigree = st.number_input("Diabetes Pedigree Function", min_value=0.000, max_value=3.000, value=0.000, step=0.001)

if st.button("Predict Diabetes Risk"):
    # Prepare input data
    input_data = {
        'Age': age,
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': diabetes_pedigree
    }
    
    try:
        model = DiabetesModel()
        result = model.predict(input_data)
        
        if isinstance(result[0], dict) and 'errors' in result[0]:
            st.error("Validation Errors:")
            for error in result[0]['errors']:
                st.write(f" {error}")
        else:
            prediction = int(result[0])
            if prediction == 1:
                st.error(" HIGH RISK: The model indicates a higher likelihood of diabetes.")
            else:
                st.success(" LOW RISK: The model indicates a lower likelihood of diabetes.")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

st.write("---")
st.write("Built with Streamlit | Model: XGBoost")
