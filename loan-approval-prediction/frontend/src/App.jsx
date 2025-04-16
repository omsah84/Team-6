import React, { useState } from "react";


const App = () => {
  const [formData, setFormData] = useState({
    Gender: "Male",
    Married: "No",
    Dependents: "0",
    Education: "Graduate",
    Self_Employed: "No",
    ApplicantIncome: "",
    CoapplicantIncome: "",
    LoanAmount: "",
    Loan_Amount_Term: 360.0,
    Credit_History: 1.0,
    Property_Area: "Urban",
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: name === "ApplicantIncome" || name === "CoapplicantIncome" || name === "LoanAmount"
        ? Number(value)
        : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setResult(data.prediction);
    } catch (error) {
      setResult("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>🏦 Loan Approval Prediction</h1>
      <form onSubmit={handleSubmit}>
        {[
          ["Gender", ["Male", "Female"]],
          ["Married", ["Yes", "No"]],
          ["Dependents", ["0", "1", "2", "3+"]],
          ["Education", ["Graduate", "Not Graduate"]],
          ["Self_Employed", ["Yes", "No"]],
          ["Property_Area", ["Urban", "Semiurban", "Rural"]],
        ].map(([field, options]) => (
          <div className="field" key={field}>
            <label>{field}</label>
            <select name={field} value={formData[field]} onChange={handleChange}>
              {options.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
        ))}

        <div className="field">
          <label>Applicant Income</label>
          <input
            type="number"
            name="ApplicantIncome"
            value={formData.ApplicantIncome}
            onChange={handleChange}
            required
          />
        </div>

        <div className="field">
          <label>Coapplicant Income</label>
          <input
            type="number"
            name="CoapplicantIncome"
            value={formData.CoapplicantIncome}
            onChange={handleChange}
          />
        </div>

        <div className="field">
          <label>Loan Amount</label>
          <input
            type="number"
            name="LoanAmount"
            value={formData.LoanAmount}
            onChange={handleChange}
            required
          />
        </div>

        <div className="field">
          <label>Loan Amount Term</label>
          <select name="Loan_Amount_Term" value={formData.Loan_Amount_Term} onChange={handleChange}>
            {[360.0, 180.0, 120.0, 60.0].map((term) => (
              <option key={term} value={term}>{term}</option>
            ))}
          </select>
        </div>

        <div className="field">
          <label>Credit History</label>
          <select name="Credit_History" value={formData.Credit_History} onChange={handleChange}>
            {[1.0, 0.0].map((ch) => (
              <option key={ch} value={ch}>{ch}</option>
            ))}
          </select>
        </div>

        <button type="submit" disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>
      </form>

      {result && (
        <div className={`result ${result === "Approved" ? "approved" : "rejected"}`}>
          {result === "Approved" ? "✅ Loan Approved!" : "❌ Loan Rejected"}
        </div>
      )}
    </div>
  );
};

export default App;
