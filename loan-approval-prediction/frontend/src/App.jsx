import React, { useState } from "react";
import {
  Container,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Button,
  CircularProgress,
  Box,
  Alert,
  Card,
  CardContent,
  Grid,
  Fade,
} from "@mui/material";

const App = () => {
  const [mode, setMode] = useState("Simple");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const [formData, setFormData] = useState({
    Gender: "Male",
    Married: "No",
    Dependents: "0",
    Education: "Graduate",
    Self_Employed: "No",
    ApplicantIncome: 5000,
    CoapplicantIncome: 0,
    LoanAmount: 100,
    Loan_Amount_Term: 360,
    Credit_History: 1.0,
    Property_Area: "Urban",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    const floatFields = ["Loan_Amount_Term", "Credit_History"];
    const numberFields = ["ApplicantIncome", "CoapplicantIncome", "LoanAmount"];

    setFormData((prev) => ({
      ...prev,
      [name]: floatFields.includes(name)
        ? parseFloat(value)
        : numberFields.includes(name)
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
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await response.json();
      setResult(data.prediction);
    } catch (err) {
      setResult("Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  const dropdownFields = [
    ["Gender", ["Male", "Female"]],
    ["Married", ["Yes", "No"]],
    ["Dependents", ["0", "1", "2", "3+"]],
    ["Education", ["Graduate", "Not Graduate"]],
    ["Self_Employed", ["Yes", "No"]],
    ["Property_Area", ["Urban", "Semiurban", "Rural"]],
  ];

  return (
    <Box
      sx={{
        background: "linear-gradient(135deg, #dbeafe, #f0f9ff)",
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        py: 6,
        px: 2,
      }}
    >
      <Container maxWidth="md">
        <Card
          elevation={8}
          sx={{
            borderRadius: 4,
            background: "linear-gradient(145deg, #ffffff, #f0f4f8)",
            boxShadow: "0 12px 30px rgba(0,0,0,0.1)",
          }}
        >
          <CardContent sx={{ p: { xs: 3, sm: 4 } }}>
            <Typography
              variant="h4"
              gutterBottom
              align="center"
              sx={{
                fontWeight: "bold",
                background: "linear-gradient(to right, #2563eb, #1d4ed8)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              💡 AI-Powered Loan Predictor
            </Typography>

            <Typography
              variant="subtitle1"
              align="center"
              sx={{ mb: 3, color: "#475569" }}
            >
              Enter your details to see if your loan gets approved
            </Typography>

            <FormControl fullWidth sx={{ mb: 3 }}>
              <InputLabel>Input Mode</InputLabel>
              <Select value={mode} onChange={(e) => setMode(e.target.value)} label="Input Mode">
                <MenuItem value="Simple">🌱 Simple Mode</MenuItem>
                <MenuItem value="Custom">🛠️ Custom Mode</MenuItem>
              </Select>
            </FormControl>

            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                {dropdownFields.map(([field, options]) => (
                  <Grid item xs={12} sm={6} key={field}>
                    <FormControl fullWidth>
                      <InputLabel>{field}</InputLabel>
                      <Select name={field} value={formData[field]} onChange={handleChange} label={field}>
                        {options.map((opt) => (
                          <MenuItem key={opt} value={opt}>
                            {opt}
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  </Grid>
                ))}

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Applicant Income"
                    name="ApplicantIncome"
                    type="number"
                    value={formData.ApplicantIncome}
                    onChange={handleChange}
                    required
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Coapplicant Income"
                    name="CoapplicantIncome"
                    type="number"
                    value={formData.CoapplicantIncome}
                    onChange={handleChange}
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Loan Amount (₹)"
                    name="LoanAmount"
                    type="number"
                    value={formData.LoanAmount}
                    onChange={handleChange}
                    required
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  {mode === "Simple" ? (
                    <FormControl fullWidth>
                      <InputLabel>Loan Term</InputLabel>
                      <Select
                        name="Loan_Amount_Term"
                        value={formData.Loan_Amount_Term}
                        onChange={handleChange}
                        label="Loan Term"
                      >
                        {[360, 180, 120, 60].map((term) => (
                          <MenuItem key={term} value={term}>
                            {term} months
                          </MenuItem>
                        ))}
                      </Select>
                    </FormControl>
                  ) : (
                    <TextField
                      fullWidth
                      label="Loan Term (months)"
                      name="Loan_Amount_Term"
                      type="number"
                      value={formData.Loan_Amount_Term}
                      onChange={handleChange}
                      required
                    />
                  )}
                </Grid>

                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel>Credit History</InputLabel>
                    <Select
                      name="Credit_History"
                      value={formData.Credit_History}
                      onChange={handleChange}
                      label="Credit History"
                    >
                      <MenuItem value={1.0}>✔️ Good (1.0)</MenuItem>
                      <MenuItem value={0.0}>❌ Poor (0.0)</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>

              <Box display="flex" justifyContent="center" sx={{ mt: 4 }}>
                <Button
                  variant="contained"
                  size="large"
                  type="submit"
                  disabled={loading}
                  sx={{
                    background: "linear-gradient(to right, #1e3a8a, #3b82f6)",
                    color: "#fff",
                    px: 5,
                    py: 1.5,
                    fontWeight: 600,
                    textTransform: "none",
                    "&:hover": {
                      background: "linear-gradient(to right, #3b82f6, #60a5fa)",
                    },
                  }}
                >
                  {loading ? <CircularProgress size={26} color="inherit" /> : "🔍 Predict Now"}
                </Button>
              </Box>
            </form>

            <Fade in={!!result}>
              <Box mt={4}>
                {result && (
                  <Alert
                    severity={result === "Approved" ? "success" : "error"}
                    sx={{
                      fontSize: "1.1rem",
                      fontWeight: 500,
                      p: 2,
                      borderRadius: 2,
                      backgroundColor: result === "Approved" ? "#d1fae5" : "#fee2e2",
                    }}
                  >
                    {result === "Approved" ? "✅ Congratulations! Loan Approved." : "❌ Sorry, Loan Rejected."}
                  </Alert>
                )}
              </Box>
            </Fade>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
};

export default App;
