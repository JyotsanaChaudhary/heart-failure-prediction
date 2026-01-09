# app.py
import streamlit as st
import joblib
import numpy as np

st.set_page_config(page_title="Heart Failure Prediction", page_icon="❤️", layout="centered")

st.title("❤️ Heart Failure Prediction App")
st.write("Enter the patient details below:")

# --- USER INPUT ---
age = st.number_input("Age", min_value=1, max_value=120, value=60)
anaemia = st.selectbox("Anaemia", ["No", "Yes"])
creatinine_phosphokinase = st.number_input("Creatinine Phosphokinase (mcg/L)", min_value=0, max_value=10000, value=250)
diabetes = st.selectbox("Diabetes", ["No", "Yes"])
ejection_fraction = st.number_input("Ejection Fraction (%)", min_value=10, max_value=100, value=40)
high_blood_pressure = st.selectbox("High Blood Pressure", ["No", "Yes"])
platelets = st.number_input("Platelets (kiloplatelets/mL)", min_value=0, max_value=1000000, value=300000)
serum_creatinine = st.number_input("Serum Creatinine (mg/dL)", min_value=0.0, max_value=20.0, value=1.0)
serum_sodium = st.number_input("Serum Sodium (mEq/L)", min_value=100, max_value=160, value=135)
sex = st.selectbox("Sex", ["Female", "Male"])
smoking = st.selectbox("Smoking", ["No", "Yes"])
time = st.number_input("Follow-up period (days)", min_value=0, max_value=5000, value=100)

# Convert categorical inputs to numerical (0/1)
anaemia_val = 1 if anaemia == "Yes" else 0
diabetes_val = 1 if diabetes == "Yes" else 0
high_blood_pressure_val = 1 if high_blood_pressure == "Yes" else 0
sex_val = 1 if sex == "Male" else 0
smoking_val = 1 if smoking == "Yes" else 0

# Load model and scaler
model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

# --- PREDICTION ---
if st.button("Predict"):
    # Arrange input in the same order as dataset
    user_input = np.array([[age, anaemia_val, creatinine_phosphokinase, diabetes_val,
                            ejection_fraction, high_blood_pressure_val, platelets,
                            serum_creatinine, serum_sodium, sex_val, smoking_val, time]])
    
    # Scale input
    user_input_scaled = scaler.transform(user_input)
    
    # Predict
    prediction = model.predict(user_input_scaled)
    
    if prediction[0] == 1:
        st.error("⚠️ Prediction: High risk of Heart Failure!")
    else:
        st.success("✅ Prediction: No Heart Failure risk detected!")
