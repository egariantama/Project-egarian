import streamlit as st
from datetime import datetime
import time

st.set_page_config(
    page_title="Jam Digital",
    layout="centered"
)

st.markdown(
    """
    <style>
    .clock {
        font-size: 90px;
        font-weight: bold;
        text-align: center;
        color: #00FFC6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

placeholder = st.empty()

while True:
    now = datetime.now().strftime("%H:%M:%S")
    placeholder.markdown(f"<div class='clock'>{now}</div>", unsafe_allow_html=True)
    time.sleep(1)
