
import streamlit as st

st.markdown("""
<div class="hero">
  <div class="hero-content">
    <div class="badge">AI-POWERED DIABETES RISK SCREENING</div>
    <h1>DiaSense</h1>
    <p>Know your estimated diabetes risk using a few simple health details and a Random Forest machine-learning model.</p>
  </div>
</div>
""", unsafe_allow_html=True)

st.write("")

a, b, c = st.columns(3)
items = [
    (a, "🩺", "Simple", "Only a few health details are needed."),
    (b, "🌲", "AI Powered", "Random Forest for tabular risk classification."),
    (c, "📊", "Transparent", "Model performance and key insights are available.")
]
for col, icon, title, text in items:
    with col:
        st.markdown(
            f'<div class="card"><h3>{icon} {title}</h3><p class="muted">{text}</p></div>',
            unsafe_allow_html=True
        )

st.write("")
if st.button("🩺 Check Your Risk →", use_container_width=True):
    st.switch_page("pages/predict.py")

st.caption("DiaSense is an educational decision-support prototype, not a medical diagnostic tool.")
