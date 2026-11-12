
import streamlit as st
import plotly.express as px
from src.model import FEATURES

st.title("💡 Key Insights")
st.caption("Only the insights useful for understanding the dataset and model.")

df=st.session_state["df"]; m=st.session_state["model_bundle"]
a,b,c=st.columns(3)
a.metric("Records",f"{len(df):,}")
b.metric("Positive class",f"{df.outcome.mean()*100:.1f}%")
c.metric("Top model feature",m["importance"].iloc[0]["Feature"].replace("_"," ").title())

fig=px.histogram(df,x="glucose",color=df["outcome"].map({0:"Lower risk class",1:"Higher risk class"}),nbins=25,title="Glucose distribution by target class")
fig.update_layout(template="plotly_dark",legend_title="")
st.plotly_chart(fig,use_container_width=True)

st.markdown("### What the model learns")
for _,r in m["importance"].head(5).iterrows():
    st.write(f"**{r['Feature'].replace('_',' ').title()}** — relative importance {r['Importance']:.3f}")
