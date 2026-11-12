
import streamlit as st
import pandas as pd
from src.model import FEATURES

st.title("🩺 Check Your Diabetes Risk")
st.caption("Enter a few health details you are likely to know. The model handles the remaining technical features automatically.")

m = st.session_state["model_bundle"]
pipe = m["pipeline"]

with st.form("simple_prediction"):
    c1, c2 = st.columns(2)

    with c1:
        age = st.number_input("Age", min_value=1, max_value=120, value=30)
        glucose = st.number_input(
            "Glucose Level (mg/dL)",
            min_value=40.0, max_value=350.0, value=120.0,
            help="Use a recent blood-test value if available."
        )

    with c2:
        bmi = st.number_input(
            "BMI",
            min_value=10.0, max_value=70.0, value=24.0,
            help="You can calculate BMI from your height and weight."
        )
        bp = st.number_input(
            "Blood Pressure (systolic)",
            min_value=70.0, max_value=250.0, value=120.0,
            help="Enter the upper/systolic blood-pressure value."
        )

    submitted = st.form_submit_button("🔍 Check Risk", use_container_width=True)

if submitted:
    # The trained model expects all eight Pima-style features.
    # For features not collected in the simple UI, use neutral dataset
    # medians rather than asking the user for technical measurements.
    df = st.session_state["df"]

    values = {
        "pregnancies": 0,
        "glucose": glucose,
        "bloodpressure": bp,
        "skinthickness": float(df["skinthickness"].median()),
        "insulin": float(df["insulin"].median()),
        "bmi": bmi,
        "diabetespedigreefunction": float(df["diabetespedigreefunction"].median()),
        "age": age,
    }

    X = pd.DataFrame([values], columns=FEATURES)
    probability = float(pipe.predict_proba(X)[0, 1])

    if probability >= 0.50:
        title = "Higher Estimated Risk"
        icon = "⚠️"
    else:
        title = "Lower Estimated Risk"
        icon = "✅"

    st.markdown(
        f"""
        <div class="result">
            <h2>{icon} {title}</h2>
            <h1>{probability * 100:.1f}%</h1>
            <p class="muted">
                Estimated probability produced by the Random Forest model.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.info(
        "This is an ML-based screening estimate, not a medical diagnosis. "
        "Please consult a qualified healthcare professional for clinical interpretation."
    )
