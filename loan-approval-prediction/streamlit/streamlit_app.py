import streamlit as st
import pandas as pd
import joblib

# Load the model and training structure
model = joblib.load("../model/loan_approval_xgboost_model.joblib")
df = pd.read_csv("../model/data.csv")
X_columns = pd.get_dummies(df.drop(columns=["Loan_Status", "Applicant_ID"]), drop_first=True).columns

st.title("🏦 Loan Approval Prediction App")
st.write("Enter applicant details to predict loan approval.")

# User input fields
gender = st.selectbox("Gender", ["Male", "Female"])
married = st.selectbox("Married", ["Yes", "No"])
dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
education = st.selectbox("Education", ["Graduate", "Not Graduate"])
self_employed = st.selectbox("Self Employed", ["Yes", "No"])
applicant_income = st.number_input("Applicant Income", min_value=0)
coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
loan_amount = st.number_input("Loan Amount", min_value=0)
loan_term = st.selectbox("Loan Amount Term", [360.0, 180.0, 120.0, 60.0])
credit_history = st.selectbox("Credit History", [1.0, 0.0])
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

if st.button("Predict"):
    input_data = {
        "Gender": gender,
        "Married": married,
        "Dependents": dependents,
        "Education": education,
        "Self_Employed": self_employed,
        "ApplicantIncome": applicant_income,
        "CoapplicantIncome": coapplicant_income,
        "LoanAmount": loan_amount,
        "Loan_Amount_Term": loan_term,
        "Credit_History": credit_history,
        "Property_Area": property_area
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # One-hot encode and align with training columns
    input_encoded = pd.get_dummies(input_df, drop_first=True)
    input_encoded = input_encoded.reindex(columns=X_columns, fill_value=0)

    # Predict
    prediction = model.predict(input_encoded)[0]
    result = "✅ Approved" if prediction == 1 else "❌ Rejected"

    st.subheader("Prediction Result:")
    st.success(result if prediction == 1 else "Rejected")
