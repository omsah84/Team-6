# Flask
from flask import Flask, render_template, request
# Data manipulation
import pandas as pd
# Matrices manipulation
import numpy as np
# Script logging
import logging
# ML model
import joblib
# JSON manipulation
import json
# Utilities
import sys
import os

# --- Critical fix for XGBoost compatibility ---
import xgboost.compat
from sklearn.preprocessing import LabelEncoder

# Monkey-patch missing XGBoostLabelEncoder
if not hasattr(xgboost.compat, 'XGBoostLabelEncoder'):
    xgboost.compat.XGBoostLabelEncoder = LabelEncoder

# Current directory
current_dir = os.path.dirname(__file__)

# Flask app
app = Flask(__name__, static_folder='static', template_folder='template')

# Logging configuration
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

def ValuePredictor(data=pd.DataFrame):
    # Model name
    model_name = 'bin/xgboostModel.pkl'
    # Model directory
    model_dir = os.path.join(current_dir, model_name)
    # Load model
    loaded_model = joblib.load(open(model_dir, 'rb'))
    # Make prediction
    result = loaded_model.predict(data)
    return result[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/prediction', methods=['POST'])
def predict():
    if request.method == 'POST':
        # Extract form data
        form_data = {
            'name': request.form['name'],
            'gender': request.form['gender'],
            'education': request.form['education'],
            'self_employed': request.form['self_employed'],
            'marital_status': request.form['marital_status'],
            'dependents': request.form['dependents'],
            'applicant_income': float(request.form['applicant_income']),
            'coapplicant_income': float(request.form['coapplicant_income']),
            'loan_amount': float(request.form['loan_amount']),
            'loan_term': float(request.form['loan_term']),
            'credit_history': request.form['credit_history'],
            'property_area': request.form['property_area']
        }

        # Load JSON schema
        schema_path = os.path.join(current_dir, 'data/columns_set.json')
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Initialize template with zeros
        template = {k: 0 for k in schema['data_columns']}
        
        # Handle categorical features
        categorical_mappings = {
            'Dependents': form_data['dependents'],
            'Property_Area': form_data['property_area']
        }
        
        for feature, value in categorical_mappings.items():
            col_name = f"{feature}_{value}"
            if col_name in template:
                template[col_name] = 1

        # Handle numerical features
        numerical_mappings = {
            'ApplicantIncome': form_data['applicant_income'],
            'CoapplicantIncome': form_data['coapplicant_income'],
            'LoanAmount': form_data['loan_amount'],
            'Loan_Amount_Term': form_data['loan_term'],
            'Gender_Male': 1 if form_data['gender'] == 'Male' else 0,
            'Married_Yes': 1 if form_data['marital_status'] == 'Yes' else 0,
            'Education_Not Graduate': 1 if form_data['education'] == 'Not Graduate' else 0,
            'Self_Employed_Yes': 1 if form_data['self_employed'] == 'Yes' else 0,
            'Credit_History_1.0': 1 if form_data['credit_history'] == 'Yes' else 0
        }

        # Update template with numerical values
        template.update(numerical_mappings)

        # Create DataFrame
        df = pd.DataFrame([template], dtype=float)

        # Get prediction
        result = ValuePredictor(data=df)

        # Generate response
        name = form_data['name']
        if int(result) == 1:
            prediction = f'Dear Mr/Mrs/Ms {name}, your loan is approved!'
        else:
            prediction = f'Sorry Mr/Mrs/Ms {name}, your loan is rejected!'

        return render_template('prediction.html', prediction=prediction)

    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)