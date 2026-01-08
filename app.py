import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="말씀 한 스푼", layout="centered")

# 2. Sidebar Settings
st.sidebar.title("⚙️ 설정")
font_size = st.sidebar.slider("글자 크기 조절", 18, 40, 22, 2, key="font_slider")

# 3. Custom CSS for Header, Vertical Watermark, and Clean UI
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo&display=swap');
    
    /* HIDE DEFAULT UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; }}

    /* FIXED TOP TITLE */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #F4ECD8;
        text-align: center;
        padding: 15px 0;
        font-size: 24px;
        font-weight: bold;
        color: #8B7355;
        border-bottom: 1px solid #D1C7B1;
        z-index: 999;
        font-family: 'Nanum Myeongjo', serif;
    }}

    /* VERTICAL WATERMARK ON THE RIGHT */
    .vertical-watermark {{
        position: fixed;
        right: 5%;
        top: 15%;
        height: 70%;
        writing-mode: vertical-rl;
        text-orientation: upright;
        font-size: 60px;
        font-family: 'Nanum Myeongjo', serif;
        font-weight: 900;
        color: #1A1A1A;
        opacity: 0.04;
        z-index: -1;
        letter-spacing: 20px;
    }}

    /* SIDEBAR TOGGLE BUTTON FIX */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #E8DFCA !important;
        color: #1A1A1A !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        top: 10px !important;
        left: 10px !important;
        z-index: 1000 !important;
    }}

    /* THEME & TEXT */
    .stApp {{ background-color: #F4ECD8 !important; }}
    [data-testid="stSidebar"] {{ background-color: #E8DFCA !important; }}

    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, label {{
        font-family: 'Nanum Gothic', sans-serif !important;
        color: #1A1A1A !important;
    }}

    .stMarkdown p, .stInfo, .prayer-box {{ font-size: {font_size}px !important; line-height: 1.8; }}
    h1, h2, h3 {{ font-size: {font_size + 8}px !important; font-weight: 700; }}

    /* COMPONENTS */
    .stInfo {{ background-color: #E8E2D2 !important; border: 1px solid #D1C7B1 !important; color: #1A1A1A !important; }}
    .prayer-box {{
        background-color: #EFE6CF !important;
        border-left: 6px solid #A68B67 !important;
        padding: 20px !important;
        border-radius: 5px !important;
        font-style: italic !important;
        margin-bottom: 20px !important;
    }}

    .custom-footer {{
        margin-top: 80px;
        padding: 30px 0 60px 0;
        text-align: center;
        font-size: 18px;
        color: #555555;
        border-top: 1px solid #D1C7B1;
    }}
    
    /* PADDING FOR FIXED HEADER */
    .main-content {{ padding-top: 60px; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Elements (Header & Watermark)
st.markdown('<div class="fixed-header">말씀 한 스푼</div>', unsafe_allow_html=True)
st.markdown('<div class="vertical-watermark">말씀 한 스푼</div>', unsafe_allow_html=True)

# 5. Load Data
@st.cache_data
def load_data():
    file_name = 'dovotionalsabsolute.csv' # Kept your 'o' spelling
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"파일을 찾을 수 없습니다: {file_name}")
        return None

df = load_data()

if df is not None:
    # Adding extra space so content starts below fixed header
    st.markdown('<div class="main-content"></div>', unsafe_allow_html=True)
    
    date_list = df['Date'].unique().tolist()
    if 'current_date' not in st.session_state:
        st.session_state.current_date = date
