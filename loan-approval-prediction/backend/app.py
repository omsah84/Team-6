from flask import Flask, request, jsonify
import joblib
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load trained model
try:
    model = joblib.load("../model/loan_approval_xgboost_model.joblib")
    print("Model loaded successfully.")
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Load column structure from training data
try:
    df = pd.read_csv("../model/data.csv")
    X_columns = pd.get_dummies(df.drop(columns=["Loan_Status", "Applicant_ID"]), drop_first=True).columns
    print("Data columns loaded successfully.")
except Exception as e:
    X_columns = pd.Index([])
    print(f"Error loading columns: {e}")

@app.route("/")
def home():
    return "Loan Approval Prediction API is running!"

@app.route("/predict", methods=["POST"])
def predict():
    if model is None or X_columns.empty:
        return jsonify({"error": "Model or data columns not loaded properly."})

    try:
        # JSON input from Postman
        input_data = request.get_json()
        input_df = pd.DataFrame([input_data])

        # One-hot encode and align with training columns
        input_encoded = pd.get_dummies(input_df, drop_first=True)
        input_encoded = input_encoded.reindex(columns=X_columns, fill_value=0)

        # Predict
        prediction = model.predict(input_encoded)[0]
        result = "Approved" if prediction == 1 else "Rejected"

        return jsonify({"prediction": result})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
