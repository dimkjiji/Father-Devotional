import streamlit as st
import pandas as pd
import os

# 1. Page Configuration
st.set_page_config(page_title="아버지의 말씀", layout="centered")

# 2. Sidebar Settings
st.sidebar.title("⚙️ 설정")
font_size = st.sidebar.slider(
    "글자 크기 조절", 
    min_value=18, 
    max_value=36, 
    value=22, 
    step=2, 
    key="font_slider" 
)

# 3. Enhanced Styling (Custom Prayer Box)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700&display=swap');
    
    .stApp {{
        font-family: 'Nanum Gothic', -apple-system, sans-serif !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: #1E1E1E !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #262626 !important;
    }}

    /* The main text style */
    .stMarkdown p, .stInfo, .prayer-box {{
        font-size: {font_size}px !important;
        line-height: 1.8;
    }}

    h1, h2, h3 {{
        font-size: {font_size + 8}px !important;
    }}

    /* CUSTOM PRAYER BOX STYLE (Replacing the bright green) */
    .prayer-box {{
        background-color: #2D2D2D; /* Slightly lighter than background */
        border-left: 5px solid #8B7355; /* Muted gold/brown accent */
        padding: 20px;
        border-radius: 5px;
        color: #DCDCDC; /* Soft white text */
        font-style: italic;
    }}
    </style>
    """, unsafe_allow_html=True)

# 4. Load Data
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
    # --- Navigation Logic ---
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

    # --- MAIN DISPLAY ---
    st.title(f"📅 {row['Date']}")
    
    st.markdown("### 📖 성경구절")
    st.info(row['Verse'])
    
    st.markdown("### 🖋️ 말씀 한 스푼")
    st.write(row['Devotional'])
    
    # --- UPDATED PRAYER SECTION ---
    st.markdown("### 🙏 함께하는 기도")
    st.markdown(f'<div class="prayer-box">{row["Prayer"]}</div>', unsafe_allow_html=True)

    st.divider()

    # --- JOURNAL SECTION ---
    st.subheader("📝 나의 묵상")
    user_note = st.text_area(
        "주님이 주신 생각들...", 
        key=f"text_{st.session_state.current_date}",
        height=150
    )
    
    if st.button("묵상 저장하기"):
        with open("reflections.txt", "a", encoding='utf-8') as f:
            f.write(f"\n[{st.session_state.current_date}]\n{user_note}\n{'-'*20}")
        st.toast("묵상이 저장되었습니다!")