import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="말씀 한 스푼", layout="centered")

# 2. Sidebar Settings
st.sidebar.title("⚙️ 설정")
font_size = st.sidebar.slider("글자 크기 조절", 18, 40, 22, 2, key="font_slider")

# 3. THE DEFINITIVE CSS: Restoring Sidebar Button & Fixing UI
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@700;900&display=swap');
    
    /* 1. MAKE HEADER INVISIBLE BUT FUNCTIONAL */
    [data-testid="stHeader"] {{
        background-color: rgba(0,0,0,0) !important; /* Fully transparent */
    }}
    
    /* Hide the default Streamlit menu and footer */
    #MainMenu {{ visibility: hidden !important; }}
    footer {{ visibility: hidden !important; }}

    /* 2. CUSTOM SIDEBAR TOGGLE BUTTON */
    /* We make the button container visible and style it */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #8B7355 !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        position: fixed !important;
        top: 15px !important;
        left: 15px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 10000 !important;
    }}
    
    /* Force hide the 'keyboard...' text */
    [data-testid="stSidebarCollapsedControl"] span {{
        display: none !important;
    }}

    /* Put a clean White Triangle in the button */
    [data-testid="stSidebarCollapsedControl"]::after {{
        content: "▶" !important;
        font-size: 16px !important;
        color: white !important;
        margin-left: 3px;
    }}

    /* 3. VERTICAL WATERMARK (Locked to Right) */
    .vertical-watermark {{
        position: fixed;
        right: 25px;
        top: 15%;
        height: 70%;
        writing-mode: vertical-rl;
        text-orientation: upright;
        font-size: 65px;
        font-family: 'Nanum Myeongjo', serif;
        font-weight: 900;
        color: #1A1A1A;
        opacity: 0.05 !important;
        z-index: -1;
        letter-spacing: 20px;
        pointer-events: none;
    }}

    /* 4. APP TITLE BAR */
    .app-title-bar {{
        text-align: center;
        padding: 15px;
        background-color: #E8DFCA;
        border-radius: 10px;
        margin-bottom: 35px;
        font-family: 'Nanum Myeongjo', serif;
        font-size: 28px;
        color: #8B7355;
        font-weight: bold;
    }}

    /* 5. THEME */
    .stApp {{ background-color: #F4ECD8 !important; }}
    [data-testid="stSidebar"] {{ background-color: #E8DFCA !important; }}
    
    * {{
        font-family: 'Nanum Gothic', sans-serif !important;
        color: #1A1A1A !important;
    }}

    .stMarkdown p, .stInfo, .prayer-box {{ font-size: {font_size}px !important; line-height: 1.8; }}
    h1, h2, h3 {{ font-size: {font_size + 8}px !important; font-weight: 700; }}

    .stInfo {{ background-color: #E8E2D2 !important; border: 1px solid #D1C7B1 !important; }}
    .prayer-box {{
        background-color: #EFE6CF;
        border-left: 6px solid #A68B67;
        padding: 22px;
        border-radius: 8px;
        font-style: italic;
    }}
    
    .custom-footer {{
        margin-top: 70px;
        padding: 40px 0;
        text-align: center;
        font-size: 18px;
        color: #555555;
        border-top: 1px solid #D1C7B1;
        line-height: 2.2 !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Visible Elements
st.markdown('<div class="vertical-watermark">말씀 한 스푼</div>', unsafe_allow_html=True)
st.markdown('<div class="app-title-bar">말씀 한 스푼</div>', unsafe_allow_html=True)

# 5. Load Data
@st.cache_data
def load_data():
    file_name = 'devotionalsabsolute.csv'
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"파일을 찾을 수 없습니다: {file_name}")
        return None

df = load_data()

if df is not None:
    date_list = df['Date'].unique().tolist()
    if 'current_date' not in st.session_state:
        st.session_state.current_date = date_list[0]

    st.sidebar.divider()
    st.sidebar.title("📖 목차")
    
    def on_change():
        st.session_state.current_date = st.session_state.date_selector

    st.sidebar.selectbox("날짜 선택:", date_list, 
        index=date_list.index(st.session_state.current_date),
        key="date_selector", on_change=on_change)

    row = df[df['Date'] == st.session_state.current_date].iloc[0]

    # --- Content ---
    st.title(f"📅 {row['Date']}")
    st.markdown("### 📖 성경구절")
    st.info(row['Verse'])
    st.markdown("### 🖋️ 말씀 한 스푼")
    st.write(row['Devotional'])
    st.markdown("### 🙏 함께하는 기도")
    st.markdown(f'<div class="prayer-box">{row["Prayer"]}</div>', unsafe_allow_html=True)
    
    # 6. Footer
    st.markdown("""
        <div class="custom-footer">
            한국중앙교회<br>
            하 나 인 출판
        </div>
    """, unsafe_allow_html=True)
