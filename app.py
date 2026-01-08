import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="말씀 한 스푼", layout="centered")

# 2. Sidebar Settings
st.sidebar.title("⚙️ 설정")
font_size = st.sidebar.slider("글자 크기 조절", 18, 40, 22, 2, key="font_slider")

# 3. Custom CSS for Fixed Header, Vertical Watermark, and Button Fix
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&family=Nanum+Myeongjo:wght@700;900&display=swap');
    
    /* HIDE DEFAULT UI */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    [data-testid="stHeader"] {{ background: rgba(0,0,0,0) !important; }}

    /* FIXED TOP TITLE bar */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background-color: #F4ECD8;
        text-align: center;
        padding: 15px 0;
        font-size: 26px;
        font-weight: bold;
        color: #8B7355;
        border-bottom: 1px solid #D1C7B1;
        z-index: 999;
        font-family: 'Nanum Myeongjo', serif;
    }}

    /* VERTICAL WATERMARK - Large on the right side */
    .vertical-watermark {{
        position: fixed;
        right: 30px;
        top: 100px;
        height: 80%;
        writing-mode: vertical-rl;
        text-orientation: upright;
        font-size: 70px;
        font-family: 'Nanum Myeongjo', serif;
        font-weight: 900;
        color: #1A1A1A;
        opacity: 0.04; /* Very faint */
        z-index: -1;
        letter-spacing: 25px;
    }}

    /* SIDEBAR TOGGLE BUTTON - Removing the 'keyboard_double_arrow' text */
    [data-testid="stSidebarCollapsedControl"] {{
        background-color: #E8DFCA !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        top: 12px !important;
        left: 12px !important;
        z-index: 1000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    /* Hide the broken text inside the button */
    [data-testid="stSidebarCollapsedControl"] span {{
        display: none !important;
    }}
    /* Add a clean brown arrow icon using CSS */
    [data-testid="stSidebarCollapsedControl"]::after {{
        content: "▶";
        color: #8B7355;
        font-size: 18px;
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
        padding: 40px 0 80px 0;
        text-align: center;
        font-size: 18px;
        color: #555555;
        border-top: 1px solid #D1C7B1;
        line-height: 2.0 !important;
    }}
    
    .main-content-padding {{ padding-top: 80px; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Elements (Header & Watermark)
st.markdown('<div class="fixed-header">말씀 한 스푼</div>', unsafe_allow_html=True)
st.markdown('<div class="vertical-watermark">말씀 한 스푼</div>', unsafe_allow_html=True)

# 5. Visitor Logger
if 'visited' not in st.session_state:
    with open("visitor_log.txt", "a", encoding='utf-8') as f:
        f.write(f"Visit at: {datetime.now()}\n")
    st.session_state.visited = True

# 6. Load Data
@st.cache_data
def load_data():
    file_name = 'devotionalsabsolute.csv' # Using the corrected spelling
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"파일을 찾을 수 없습니다: {file_name}")
        return None

df = load_data()

if df is not None:
    st.markdown('<div class="main-content-padding"></div>', unsafe_allow_html=True)
    
    date_list = df['Date'].unique().tolist()
    
    # Corrected Session State Logic
    if 'current_date' not in st.session_state:
        st.session_state.current_date = date_list[0]

    st.sidebar.divider()
    st.sidebar.title("📖 목차")
    
    def on_change():
        st.session_state.current_date = st.session_state.date_selector

    st.sidebar.selectbox(
        "날짜 선택:", 
        date_list, 
        index=date_list.index(st.session_state.current_date),
        key="date_selector", 
        on_change=on_change
    )

    row = df[df['Date'] == st.session_state.current_date].iloc[0]

    # --- Display ---
    st.title(f"📅 {row['Date']}")
    st.markdown("### 📖 성경구절")
    st.info(row['Verse'])
    st.markdown("### 🖋️ 말씀 한 스푼")
    st.write(row['Devotional'])
    st.markdown("### 🙏 함께하는 기도")
    st.markdown(f'<div class="prayer-box">{row["Prayer"]}</div>', unsafe_allow_html=True)
    
    # 7. Perfected Footer
    st.markdown("""
        <div class="custom-footer">
            한국중앙교회<br>
            하 나 인 출판
        </div>
    """, unsafe_allow_html=True)
