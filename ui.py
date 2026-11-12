
import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: Inter, sans-serif; }
    .stApp {
      background: radial-gradient(circle at 85% 5%, rgba(65,190,140,.12), transparent 30%),
                  radial-gradient(circle at 10% 90%, rgba(64,130,220,.10), transparent 28%), #071218;
    }
    .block-container { max-width:1180px; padding-top:2rem; }
    .hero {
      min-height:420px; border-radius:30px; overflow:hidden; display:flex; align-items:center;
      background:linear-gradient(100deg,rgba(5,13,18,.98),rgba(5,13,18,.72)),
      url('https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1800&q=85') center/cover;
      border:1px solid rgba(255,255,255,.08); box-shadow:0 25px 80px rgba(0,0,0,.28);
    }
    .hero-content { padding:55px; max-width:650px; }
    .hero h1 { font-size:4.2rem; margin:.3rem 0; letter-spacing:-.06em; }
    .hero p { color:#a9bac1; font-size:1.1rem; line-height:1.6; }
    .badge { display:inline-block; padding:7px 12px; border-radius:999px; color:#69e2a1; background:rgba(57,217,138,.10); border:1px solid rgba(57,217,138,.25); font-size:.78rem; font-weight:700; }
    .card { background:rgba(15,34,42,.72); border:1px solid rgba(255,255,255,.07); border-radius:20px; padding:20px; }
    .muted { color:#8ea6ae; }
    .result { border-radius:22px; padding:26px; border:1px solid rgba(57,217,138,.30); background:rgba(57,217,138,.07); }
    </style>
    """, unsafe_allow_html=True)
