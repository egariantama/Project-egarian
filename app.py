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

offset = {"WIB": 7, "WITA": 8, "WIT": 9}[zona]

# =========================
# STYLE RESPONSIVE CORPORATE
# =========================
st.markdown(
    """
    <style>
    body {
        background-color: #0B1E3D;
    }

    /* ===== DESKTOP / TV ===== */
    .clock {
        font-size: 100px;
        font-weight: bold;
        text-align: center;
        color: #FFD200;
        margin-top: 20px;
    }
    .date {
        font-size: 36px;
        text-align: center;
        color: white;
        margin-top: -20px;
    }
    .countdown {
        font-size: 34px;
        text-align: center;
        color: #FFD200;
        margin-top: 10px;
        font-weight: bold;
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

    /* ===== MOBILE MODE ===== */
    @media only screen and (max-width: 768px) {
        .clock {
            font-size: 48px;
            margin-top: 10px;
        }
        .date {
            font-size: 18px;
            margin-top: 0;
        }
        .countdown {
            font-size: 16px;
            padding: 0 10px;
        }
        .running-text {
            font-size: 14px;
            padding: 6px;
        }
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
hari_id = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
bulan_id = [
    "Januari", "Februari", "Maret", "April",
    "Mei", "Juni", "Juli", "Agustus",
    "September", "Oktober", "November", "Desember"
]

# =========================
# INPUT RUNNING TEXT
# =========================
running_text = st.sidebar.text_input(
    "Running Text Informasi",
    "Hai... Destia Chairany. R, ayok semangat aku sayang sama kamu, kamu cantik hari ini, kamu spesial banget buat aku"
)

# =========================
# TARGET RAMADHAN
# =========================
ramadhan_date = datetime(2026, 2, 18, 0, 0, 0)

# =========================
# PLACEHOLDER
# =========================
clock_placeholder = st.empty()
date_placeholder = st.empty()
countdown_placeholder = st.empty()
running_placeholder = st.empty()

# =========================
# LOOP JAM
# =========================
while True:
    now = datetime.utcnow() + timedelta(hours=offset)

    jam = now.strftime("%H:%M:%S")
    hari = hari_id[now.weekday()]
    tanggal = now.day
    bulan = bulan_id[now.month - 1]
    tahun = now.year

    diff = ramadhan_date - now
    if diff.total_seconds() > 0:
        days = diff.days
        hours, remainder = divmod(diff.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        countdown_text = (
            f"Menuju Ramadhan 1447 H • "
            f"{days} Hari {hours} Jam {minutes} Menit {seconds} Detik"
        )
    else:
        countdown_text = "🌙 Selamat Menunaikan Ibadah Puasa Ramadhan 🌙"

    clock_placeholder.markdown(
        f"<div class='clock'>{jam} {zona}</div>",
        unsafe_allow_html=True
    )

    date_placeholder.markdown(
        f"<div class='date'>{hari}, {tanggal} {bulan} {tahun}</div>",
        unsafe_allow_html=True
    )

    countdown_placeholder.markdown(
        f"<div class='countdown'>{countdown_text}</div>",
        unsafe_allow_html=True
    )

    running_placeholder.markdown(
        f"<div class='running-text'>{running_text}</div>",
        unsafe_allow_html=True
    )

    time.sleep(1)
