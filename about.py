
import streamlit as st

st.title("ℹ️ About DiaSense")

st.markdown("""
### How it works

**Health details → preprocessing → Random Forest → estimated risk**

DiaSense is designed to keep the user experience simple while retaining a proper
machine-learning workflow behind the scenes.

### Why Random Forest?

- Strong baseline for structured/tabular data
- Captures nonlinear relationships
- Combines many decision trees for a more robust prediction
- Provides feature-importance information

### Industry-oriented practices

- Stratified train/test split
- Missing-value imputation
- Class-balanced training
- Multiple evaluation metrics
- Feature-importance analysis
- Modular application architecture

**Important:** DiaSense is an educational ML project and is not a medical device or diagnostic system.
""")
