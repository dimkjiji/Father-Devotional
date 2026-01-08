import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. Page Configuration
st.set_page_config(page_title="아버지의 말씀", layout="centered")

# 2. Sidebar Settings
st.sidebar.title("⚙️ 설정")
font_size = st.sidebar.slider("글자 크기 조절", 18, 40, 22, 2, key="font_slider")

# 3. Clean Sepia Styling with Hidden Menus
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

    .stMarkdown p, .stInfo, .prayer-box, .stTextArea textarea {{
        font-size: {font_size}px !important;
    }}

    h1, h2, h3 {{
        font-size: {font_size + 8}px !important;
        font-weight: 700 !important;
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

    .stTextArea textarea {{
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Visitor Logger
if 'visited' not in st.session_state:
    with open("visitor_log.txt", "a", encoding='utf-8') as f:
        f.write(f"Visit at: {datetime.now()}\n")
    st.session_state.visited = True

# 5. Load Data
@st.cache_data
def load_data():
    file_name = 'devotional_clean.csv'
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

    selected_date = st.sidebar.selectbox("날짜 선택:", date_list, 
        index=date_list.index(st.session_state.current_date),
        key="date_selector", on_change=on_change)

    row = df[df['Date'] == st.session_state.current_date].iloc[0]

    # --- Main Display ---
    st.title(f"📅 {row['Date']}")
    st.markdown("### 📖 성경구절")
    st.info(row['Verse'])
    st.markdown("### 🖋️ 말씀 한 스푼")
    st.write(row['Devotional'])
    st.markdown("### 🙏 함께하는 기도")
    st.markdown(f'<div class="prayer-box">{row["Prayer"]}</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("📝 나의 묵상")
    user_note = st.text_area("주님이 주신 생각들...", key=f"text_{st.session_state.current_date}", height=150)
    
    if st.button("묵상 저장하기"):
        with open("reflections.txt", "a", encoding='utf-8') as f:
            f.write(f"\n[{st.session_state.current_date}]\n{user_note}\n{'-'*20}")
        st.toast("묵상이 저장되었습니다!")
