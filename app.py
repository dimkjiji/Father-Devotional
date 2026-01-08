import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="말씀 한 스푼", layout="centered")

# 2. Sidebar Settings
st.sidebar.title("⚙️ 설정")
font_size = st.sidebar.slider("글자 크기 조절", 18, 40, 22, 2, key="font_slider")

# 3. Enhanced Styling: Sepia, Watermark, and Clean UI
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    
    /* HIDE STREAMLIT UI ELEMENTS */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}

    /* Force Locked Sepia Theme */
    .stApp, [data-testid="stAppViewContainer"], .main {{
        background-color: #F4ECD8 !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #E8DFCA !important;
    }}

    /* Global Text Styling */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span, label, li {{
        font-family: 'Nanum Gothic', sans-serif !important;
        color: #1A1A1A !important;
        line-height: 1.8 !important;
    }}

    .stMarkdown p, .stInfo, .prayer-box {{
        font-size: {font_size}px !important;
    }}

    h1, h2, h3 {{
        font-size: {font_size + 8}px !important;
        font-weight: 700 !important;
    }}

    /* WATERMARK STYLE */
    .watermark {{
        position: fixed;
        bottom: 100px;
        right: 20px;
        opacity: 0.1;
        font-size: 50px;
        font-weight: bold;
        color: #1A1A1A;
        z-index: -1;
        pointer-events: none;
        user-select: none;
    }}

    /* FOOTER STYLE */
    .custom-footer {{
        margin-top: 50px;
        text-align: center;
        font-size: 16px;
        color: #555555;
        border-top: 1px solid #D1C7B1;
        padding-top: 20px;
    }}

    /* UI Components */
    .stInfo {{
        background-color: #E8E2D2 !important;
        border: 1px solid #D1C7B1 !important;
        color: #1A1A1A !important;
    }}

    .prayer-box {{
        background-color: #EFE6CF !important;
        border-left: 6px solid #A68B67 !important;
        padding: 20px !important;
        border-radius: 5px !important;
        font-style: italic !important;
        color: #1A1A1A !important;
        margin-bottom: 20px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Watermark and Visitor Logger
st.markdown('<div class="watermark">말씀 한 스푼</div>', unsafe_allow_html=True)

if 'visited' not in st.session_state:
    with open("visitor_log.txt", "a", encoding='utf-8') as f:
        f.write(f"Visit at: {datetime.now()}\n")
    st.session_state.visited = True

# 5. Load Data (Updated to dovotionalsabsolute.csv)
@st.cache_data
def load_data():
    file_name = 'dovotionalsabsolute.csv'
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        st.error(f"파일을 찾을 수 없습니다: {file_name}")
        return None

df = load_data()

if df is not None:
    # --- Navigation ---
    date_list = df['Date'].unique().tolist()
    if 'current_date' not in st.session_state:
        st.session_state.current_date = date_list[0]

    st.sidebar.divider()
    st.sidebar.title("📖 목차")
    
    def on_change():
        st.session_state.current_date = st.session_state.date_selector

    selected_date = st.sidebar.selectbox(
        "날짜 선택:", 
        date_list, 
        index=date_list.index(st.session_state.current_date),
        key="date_selector", 
        on_change=on_change
    )

    row = df[df['Date'] == st.session_state.current_date].iloc[0]

    # --- Main Display Content ---
    st.title(f"📅 {row['Date']}")
    
    st.markdown("### 📖 성경구절")
    st.info(row['Verse'])
    
    st.markdown("### 🖋️ 말씀 한 스푼")
    st.write(row['Devotional'])
    
    st.markdown("### 🙏 함께하는 기도")
    st.markdown(f'<div class="prayer-box">{row["Prayer"]}</div>', unsafe_allow_html=True)
    
    # 6. Final Footer Section
    st.markdown("""
        <div class="custom-footer">
            한국중앙교회<br>
            하 나 인 출판
        </div>
    """, unsafe_allow_html=True)
