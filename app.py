import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# These modules are uploaded at the repository root (not inside a src/ folder).
from data import load_diabetes_data
from model import train_model, FEATURES
from ui import inject_css


st.set_page_config(
    page_title="DiaSense | Diabetes Prediction",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

# -------------------------------------------------------------------
# Data and model
# -------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_default_data():
    return load_diabetes_data()


@st.cache_data(show_spinner=False)
def get_uploaded_data(file_bytes):
    from io import BytesIO
    return load_diabetes_data(BytesIO(file_bytes))


@st.cache_resource(show_spinner=False)
def get_model(dataframe):
    # The model module trains a Random Forest pipeline and returns
    # evaluation metrics, confusion matrix, feature importance and pipeline.
    return train_model(dataframe)


st.sidebar.markdown("## 🩺 DiaSense")
st.sidebar.caption("Diabetes Risk Prediction")
st.sidebar.divider()

uploaded_csv = st.sidebar.file_uploader(
    "Optional: upload a compatible diabetes CSV",
    type=["csv"],
    help="The CSV must contain the 8 clinical features and an Outcome/target column.",
)

try:
    if uploaded_csv is not None:
        df = get_uploaded_data(uploaded_csv.getvalue())
        data_source = "Uploaded CSV"
    else:
        df = get_default_data()
        data_source = "Default dataset"

    if len(df) < 10:
        st.error("The dataset contains too few valid records to train and evaluate the model.")
        st.stop()

    model_bundle = get_model(df)
    pipeline = model_bundle["pipeline"]

except Exception as exc:
    st.error("DiaSense could not load the dataset or prepare the prediction model.")
    st.warning(
        "Check that data.py, model.py and ui.py are uploaded beside app.py, "
        "and that requirements.txt contains the required libraries."
    )
    st.exception(exc)
    st.stop()

st.sidebar.metric("Dataset records", f"{len(df):,}")
st.sidebar.metric("Model", "Random Forest")
st.sidebar.caption(f"Data source: {data_source}")
st.sidebar.divider()
st.sidebar.caption("Educational decision-support prototype. Not a medical diagnosis.")

# -------------------------------------------------------------------
# Navigation
# -------------------------------------------------------------------
page = st.sidebar.radio(
    "Navigation",
    ["Home", "Risk Prediction", "Model Performance", "Key Insights", "About"],
)

# -------------------------------------------------------------------
# Home
# -------------------------------------------------------------------
if page == "Home":
    st.markdown(
        """
        <div class="hero">
          <div class="hero-content">
            <span class="badge">MACHINE LEARNING • HEALTH ANALYTICS</span>
            <h1>DiaSense</h1>
            <p>
              An interactive diabetes risk prediction application using
              patient health parameters and a Random Forest machine learning model.
            </p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    st.subheader("Project overview")
    st.write(
        "DiaSense analyses eight clinical input features and estimates the likelihood "
        "of a positive diabetes outcome using a Random Forest classifier."
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("Records available", f"{len(df):,}")
    c2.metric("Input features", len(FEATURES))
    c3.metric("Algorithm", "Random Forest")

    st.subheader("How it works")
    st.markdown(
        """
        1. Enter the patient's health measurements on the **Risk Prediction** page.
        2. The application processes the values using the trained machine learning pipeline.
        3. DiaSense displays the predicted class and estimated model probability.
        4. Review the **Model Performance** and **Key Insights** pages for evaluation information.
        """
    )

# -------------------------------------------------------------------
# Risk prediction
# -------------------------------------------------------------------
elif page == "Risk Prediction":
    st.title("🩺 Diabetes Risk Prediction")
    st.write("Enter the health measurements below to generate a model prediction.")

    with st.form("prediction_form"):
        col1, col2 = st.columns(2)

        with col1:
            pregnancies = st.number_input("Pregnancies", min_value=0, max_value=20, value=1, step=1)
            glucose = st.number_input("Glucose (mg/dL)", min_value=0.0, max_value=300.0, value=120.0, step=1.0)
            bloodpressure = st.number_input("Blood Pressure (mmHg)", min_value=0.0, max_value=200.0, value=70.0, step=1.0)
            skinthickness = st.number_input("Skin Thickness (mm)", min_value=0.0, max_value=100.0, value=20.0, step=1.0)

        with col2:
            insulin = st.number_input("Insulin (µU/mL)", min_value=0.0, max_value=900.0, value=79.0, step=1.0)
            bmi = st.number_input("BMI (kg/m²)", min_value=0.0, max_value=100.0, value=25.0, step=0.1)
            pedigree = st.number_input(
                "Diabetes Pedigree Function",
                min_value=0.0,
                max_value=3.0,
                value=0.5,
                step=0.01,
            )
            age = st.number_input("Age (years)", min_value=1, max_value=120, value=30, step=1)

        submitted = st.form_submit_button("Predict Diabetes Risk", type="primary", use_container_width=True)

    if submitted:
        input_df = pd.DataFrame(
            [[pregnancies, glucose, bloodpressure, skinthickness, insulin, bmi, pedigree, age]],
            columns=FEATURES,
        )
        prediction = int(pipeline.predict(input_df)[0])
        probabilities = pipeline.predict_proba(input_df)[0]
        positive_probability = float(probabilities[1])

        st.divider()
        st.subheader("Prediction result")

        if prediction == 1:
            st.error("Model prediction: Higher likelihood of diabetes")
        else:
            st.success("Model prediction: Lower likelihood of diabetes")

        left, right = st.columns(2)
        left.metric("Estimated positive-class probability", f"{positive_probability:.1%}")
        right.metric("Predicted class", "Positive" if prediction == 1 else "Negative")

        st.progress(min(max(positive_probability, 0.0), 1.0))
        st.caption(
            "This probability is the model's estimate for the positive class, "
            "not a clinical diagnosis or an individual's confirmed disease risk."
        )
        st.info(
            "Please consult a qualified healthcare professional for medical interpretation, "
            "screening, testing, or treatment decisions. Do not use this application alone "
            "to make healthcare decisions."
        )

# -------------------------------------------------------------------
# Model performance
# -------------------------------------------------------------------
elif page == "Model Performance":
    st.title("📈 Model Performance")
    st.write("Evaluation results from the model's held-out test split.")

    metrics = model_bundle["metrics"]
    metric_cols = st.columns(len(metrics))
    for col, (name, value) in zip(metric_cols, metrics.items()):
        col.metric(name, f"{value:.3f}")

    st.subheader("Confusion matrix")
    cm = model_bundle["cm"]
    fig_cm = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=["Predicted negative", "Predicted positive"],
            y=["Actual negative", "Actual positive"],
            text=cm,
            texttemplate="%{text}",
            colorscale="Teal",
            showscale=True,
        )
    )
    fig_cm.update_layout(
        xaxis_title="Predicted label",
        yaxis_title="Actual label",
        height=420,
        margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig_cm, use_container_width=True)

    st.caption(
        "Metrics are calculated from the 20% test split created by the training code. "
        "Results depend on the dataset and split."
    )

# -------------------------------------------------------------------
# Key insights
# -------------------------------------------------------------------
elif page == "Key Insights":
    st.title("💡 Key Insights")

    importance = model_bundle["importance"].copy()
    importance["Feature"] = importance["Feature"].str.replace("_", " ").str.title()

    st.subheader("Feature importance")
    fig = px.bar(
        importance.sort_values("Importance", ascending=True),
        x="Importance",
        y="Feature",
        orientation="h",
        title="Random Forest feature importance",
    )
    fig.update_layout(height=450, yaxis_title="", xaxis_title="Importance")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dataset outcome distribution")
    outcome_counts = (
        df["outcome"]
        .map({0: "Negative outcome", 1: "Positive outcome"})
        .value_counts()
        .rename_axis("Outcome")
        .reset_index(name="Records")
    )
    fig_outcome = px.pie(
        outcome_counts,
        names="Outcome",
        values="Records",
        hole=0.55,
        title="Distribution of target classes",
    )
    st.plotly_chart(fig_outcome, use_container_width=True)

    st.caption(
        "Feature importance describes how the fitted Random Forest used features "
        "within this dataset; it does not establish medical causation."
    )

# -------------------------------------------------------------------
# About
# -------------------------------------------------------------------
else:
    st.title("ℹ️ About DiaSense")
    st.write(
        "DiaSense is an educational machine learning project that demonstrates "
        "a Streamlit interface for diabetes outcome prediction."
    )
    st.subheader("Technology stack")
    st.markdown(
        """
        - **Python** – application development
        - **Streamlit** – interactive web interface
        - **Pandas and NumPy** – data handling
        - **Scikit-learn** – preprocessing, Random Forest training and evaluation
        - **Plotly** – interactive charts
        """
    )
    st.subheader("Model inputs")
    st.write(
        "Pregnancies, Glucose, Blood Pressure, Skin Thickness, Insulin, BMI, "
        "Diabetes Pedigree Function and Age."
    )
    st.warning(
        "DiaSense is for educational and demonstration purposes only. "
        "It is not intended to diagnose diabetes, replace laboratory testing, "
        "or provide medical advice."
    )

