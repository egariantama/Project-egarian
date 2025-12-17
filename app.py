import streamlit as st
from datetime import datetime, timedelta
import time

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Jam Digital Cabang",
    layout="wide"
)

# =========================
# PILIH ZONA WAKTU
# =========================
zona = st.sidebar.selectbox(
    "Pilih Zona Waktu",
    ["WIB", "WITA", "WIT"]
)

offset = {
    "WIB": 7,
    "WITA": 8,
    "WIT": 9
}[zona]

# =========================
# STYLE CORPORATE MANDIRI
# =========================
st.markdown(
    """
    <style>
    body {
        background-color: #0B1E3D;
    }
    .clock {
        font-size: 100px;
        font-weight: bold;
        text-align: center;
        color: #FFD200;
        margin-top: 30px;
    }
    .date {
        font-size: 36px;
        text-align: center;
        color: white;
        margin-top: -20px;
    }
    .running-text {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #FFD200;
        color: #0B1E3D;
        font-size: 28px;
        font-weight: bold;
        padding: 10px;
        animation: marquee 15s linear infinite;
        white-space: nowrap;
        overflow: hidden;
    }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# NAMA HARI & BULAN (ID)
# =========================
hari_id = [
    "Senin", "Selasa", "Rabu",
    "Kamis", "Jumat", "Sabtu", "Minggu"
]

bulan_id = [
    "Januari", "Februari", "Maret", "April",
    "Mei", "Juni", "Juli", "Agustus",
    "September", "Oktober", "November", "Desember"
]

# =========================
# INPUT RUNNING TEXT
# =========================
running_text = st.sidebar.text_input(
    "Running Text Informasi Cabang",
    "Selamat Datang di Bank Mandiri | Layanan Buka Rekening Cepat | Prioritas Kepuasan Nasabah"
)

# =========================
# PLACEHOLDER
# =========================
clock_placeholder = st.empty()
date_placeholder = st.empty()
running_placeholder = st.empty()

# =========================
# LOOP JAM
# =========================
while True:
    now_utc = datetime.utcnow()
    now = now_utc + timedelta(hours=offset)

    jam = now.strftime("%H:%M:%S")
    hari = hari_id[now.weekday()]
    tanggal = now.day
    bulan = bulan_id[now.month - 1]
    tahun = now.year

    clock_placeholder.markdown(
        f"<div class='clock'>{jam} {zona}</div>",
        unsafe_allow_html=True
    )

    date_placeholder.markdown(
        f"<div class='date'>{hari}, {tanggal} {bulan} {tahun}</div>",
        unsafe_allow_html=True
    )

    running_placeholder.markdown(
        f"<div class='running-text'>{running_text}</div>",
        unsafe_allow_html=True
    )

    time.sleep(1)
