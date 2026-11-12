
import streamlit as st
from src.data import load_diabetes_data
from src.model import train_model
from src.ui import inject_css

st.set_page_config(page_title="DiaSense", page_icon="🩺", layout="wide", initial_sidebar_state="expanded")
inject_css()

@st.cache_data(show_spinner=False)
def get_data():
    return load_diabetes_data()

@st.cache_resource(show_spinner=False)
def get_model(df):
    return train_model(df)

try:
    df = get_data()
    model_bundle = get_model(df)
    st.session_state["df"] = df
    st.session_state["model_bundle"] = model_bundle
except Exception as e:
    st.error("DiaSense could not prepare the model.")
    st.info("Go to the Data page and upload a compatible diabetes CSV.")
    st.stop()

pages = [
    st.Page("pages/home.py", title="Home", icon="🏠", default=True),
    st.Page("pages/predict.py", title="Risk Prediction", icon="🩺"),
    st.Page("pages/model.py", title="Model Performance", icon="📈"),
    st.Page("pages/insights.py", title="Key Insights", icon="💡"),
    st.Page("pages/data.py", title="Data", icon="📁"),
    st.Page("pages/about.py", title="About", icon="ℹ️"),
]
pg = st.navigation(pages, position="sidebar")

with st.sidebar:
    st.markdown("## 🩺 DiaSense")
    st.caption("Diabetes Risk Prediction")
    st.divider()
    st.metric("Records", f"{len(df):,}")
    st.metric("Model", "Random Forest")
    st.divider()
    st.caption("Decision-support prototype • Not a medical diagnosis")

pg.run()
