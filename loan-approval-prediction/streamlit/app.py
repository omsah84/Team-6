import streamlit as st
import pandas as pd
import joblib
import os

# Load model and training data structure
model = joblib.load("./loan_approval_xgboost_model.joblib")
df = pd.read_csv("./data.csv")
X_columns = pd.get_dummies(df.drop(columns=["Loan_Status", "Applicant_ID"]), drop_first=True).columns

# Page Config
st.set_page_config(page_title="Loan Approval Predictor", page_icon="🏦", layout="centered")

# Styling
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Title and Description
st.title("🏦 Loan Approval Prediction App")
st.markdown("#### Enter applicant details to check loan approval status")

# Mode Selection
mode = st.radio("Select Input Mode:", ["🧮 Simple Mode", "✍️ Custom Mode"])

# Input Fields
st.markdown("### 👤 Personal Information")
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
with col2:
    married = st.selectbox("Married", ["Yes", "No"])
with col3:
    dependents = (
        st.selectbox("Dependents", ["0", "1", "2", "3+"])
        if mode == "🧮 Simple Mode"
        else st.text_input("Dependents (e.g., 0, 1, 2, 3+)", "0")
    )

col1, col2 = st.columns(2)
with col1:
    education = st.selectbox("Education", ["Graduate", "Not Graduate"])
with col2:
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])

st.markdown("### 💰 Financial Information")

col1, col2 = st.columns(2)
with col1:
    if mode == "🧮 Simple Mode":
        applicant_income = st.slider("Applicant Income (₹)", 0, 100000, 5000, step=1000)
    else:
        applicant_income = st.number_input("Applicant Income (₹)", min_value=0, value=5000)

with col2:
    if mode == "🧮 Simple Mode":
        coapplicant_income = st.slider("Coapplicant Income (₹)", 0, 50000, 0, step=1000)
    else:
        coapplicant_income = st.number_input("Coapplicant Income (₹)", min_value=0, value=0)

if mode == "🧮 Simple Mode":
    loan_amount = st.slider("Loan Amount (in ₹1000s)", 0, 700, 100, step=10)
else:
    loan_amount = st.number_input("Loan Amount (in ₹1000s)", min_value=0, value=100)

# ✅ Updated Loan Term input
if mode == "🧮 Simple Mode":
    loan_term = st.slider("Loan Term (Months)", min_value=1, max_value=360, step=1, value=1)
else:
    loan_term = st.number_input("Loan Term (Months)", min_value=1, max_value=600, value=1, step=1)

credit_history = st.radio("Credit History", [1.0, 0.0], format_func=lambda x: "Good" if x == 1.0 else "Poor")
property_area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])

# Predict Button
if st.button("🔍 Predict Loan Status"):

    # Gather input
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

    # Show Entered Data
    with st.expander("🧾 Review Entered Details"):
        st.json(input_data)

    # Preprocess
    input_df = pd.DataFrame([input_data])
    input_encoded = pd.get_dummies(input_df, drop_first=True)
    input_encoded = input_encoded.reindex(columns=X_columns, fill_value=0)

    # Prediction and Confidence
    prediction = model.predict(input_encoded)[0]
    probability = model.predict_proba(input_encoded)[0][1]
    result = "✅ Approved" if prediction == 1 else "❌ Rejected"

    # Output
    st.markdown("### 📊 Prediction Result:")
    st.success(result)
    st.info(f"📈 Model Confidence: {probability * 100:.2f}%")

    # Save History (optional)
    input_df["Prediction"] = result
    input_df["Confidence"] = round(probability, 4)
    log_file = "prediction_history.csv"
    if os.path.exists(log_file):
        input_df.to_csv(log_file, mode='a', header=False, index=False)
    else:
        input_df.to_csv(log_file, index=False)
