import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import xgboost as xgb
import joblib

# Load the cleaned dataset
df = pd.read_csv("data.csv")

# Feature columns and target column
X = df.drop(columns=["Loan_Status", "Applicant_ID"])  # Drop target and ID column
y = df["Loan_Status"].apply(lambda x: 1 if x == "Y" else 0)  # Convert target to binary (Y -> 1, N -> 0)

# Convert categorical columns using one-hot encoding
X = pd.get_dummies(X, drop_first=True)

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize XGBoost classifier
model = xgb.XGBClassifier(
    objective='binary:logistic',  # Binary classification
    eval_metric='logloss',        # Logarithmic loss for evaluation
    use_label_encoder=False,      # Prevent warning on label encoder
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the trained model to a file
model_filename = "loan_approval_xgboost_model.joblib"
joblib.dump(model, model_filename)
print(f"Model saved to {model_filename}")
