# DiaSense

Streamlit-based diabetes risk prediction project using Random Forest.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app can automatically retrieve the public Pima Indians Diabetes dataset if no local `data/diabetes.csv` exists and internet access is available. You can also upload a compatible CSV from the Data page.

## Input columns

Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Outcome.

## Important

This is an educational machine-learning project and not a medical diagnostic tool.
