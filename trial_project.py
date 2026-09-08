import streamlit as st
import pandas as pd
from pathlib import Path
import html
import re

# ============================================================
# BANCAPOCKET - MOBILE INSURANCE PARTNER DIRECTORY
# ============================================================

st.set_page_config(
    page_title="BancaPocket",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

DATA_FILE = Path("data/Data_Asuransi.xlsx")

# ------------------------------------------------------------
# CSS
# ------------------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(37,99,235,.15), transparent 32%),
        linear-gradient(180deg, #f7faff 0%, #eef4fc 100%);
}

.block-container {
    width: 100% !important;
    max-width: 760px !important;
    box-sizing: border-box !important;
    padding: 0.75rem 12px 2rem !important;
    margin: 0 auto !important;
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }

/* Header */
.bp-header {
    position: relative;
    overflow: hidden;
    border-radius: 0 0 30px 30px;
    padding: 25px 22px 28px;
    color: white;
    background: linear-gradient(135deg, #1245a0 0%, #2563eb 55%, #3b82f6 100%);
    box-shadow: 0 12px 30px rgba(37,99,235,.20);
    margin: 0 0 18px;
}

.bp-header:after {
    content: "";
    position: absolute;
    width: 220px;
    height: 220px;
    right: -80px;
    top: -100px;
    border-radius: 50%;
    background: rgba(255,255,255,.10);
}

.bp-brand {
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -.8px;
    position: relative;
    z-index: 2;
}

.bp-subtitle {
    font-size: 15px;
    font-weight: 600;
    margin-top: 2px;
    position: relative;
    z-index: 2;
}

.bp-caption {
    font-size: 12px;
    opacity: .85;
    margin-top: 7px;
    position: relative;
    z-index: 2;
}

.bp-shield {
    position: absolute;
    right: 20px;
    top: 26px;
    width: 62px;
    height: 62px;
    border-radius: 20px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: 32px;
    background: rgba(255,255,255,.16);
    border: 1px solid rgba(255,255,255,.35);
    z-index: 2;
}

/* Search */
.search-label {
    font-size: 13px;
    font-weight: 700;
    color: #17233d;
    margin: 0 0 7px 3px;
}

div[data-testid="stTextInput"] input {
    border-radius: 15px !important;
    min-height: 48px !important;
    border: 1px solid #d9e2ef !important;
    background: #ffffff !important;
    color: #17233d !important;
    -webkit-text-fill-color: #17233d !important;
    caret-color: #2563eb !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    box-shadow: 0 5px 18px rgba(25,55,100,.06);
    outline: none !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    opacity: 1 !important;
}

div[data-testid="stTextInput"] input:focus {
    border: 1.5px solid #2563eb !important;
    box-shadow: 0 0 0 3px rgba(37,99,235,.10) !important;
    outline: none !important;
}


/* Search input */
div[data-testid="stTextInput"] input {
    color: #17233d !important;
    -webkit-text-fill-color: #17233d !important;
    caret-color: #2563eb !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    opacity: 1 !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #2563eb !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,.10) !important;
}


/* ============================================================
   CATEGORY — MOBILE SEGMENTED CONTROL
   ============================================================ */
.category-wrap {
    margin: 0 0 22px !important;
}

div[data-testid="stSegmentedControl"] {
    width: 100% !important;
    margin: 0 !important;
}

div[data-testid="stSegmentedControl"] > div {
    width: 100% !important;
}

div[data-testid="stSegmentedControl"] [role="radiogroup"] {
    width: 100% !important;
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    gap: 6px !important;
    padding: 5px !important;
    box-sizing: border-box !important;
    border: 1px solid #d7e2f0 !important;
    border-radius: 20px !important;
    background: rgba(255,255,255,.88) !important;
    box-shadow: 0 7px 20px rgba(37,72,120,.07) !important;
}

div[data-testid="stSegmentedControl"] [role="radio"] {
    min-width: 0 !important;
    min-height: 54px !important;
    width: 100% !important;
    border-radius: 15px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 6px 3px !important;
    box-sizing: border-box !important;
    color: #536987 !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    transition: all .18s ease !important;
}

div[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"] {
    color: #fff !important;
    background: linear-gradient(135deg,#1555c8,#2563eb) !important;
    box-shadow: 0 5px 15px rgba(37,99,235,.20) !important;
}

/* PKS filter sits neatly below the insurance category selector */
div[data-testid="stSegmentedControl"] + div[data-testid="stSegmentedControl"] {
    margin-top: 9px !important;
}

div[data-testid="stSegmentedControl"] + div[data-testid="stSegmentedControl"] [role="radio"] {
    min-height: 48px !important;
    font-size: 13px !important;
}

@media (max-width: 480px) {
    div[data-testid="stSegmentedControl"] + div[data-testid="stSegmentedControl"] [role="radio"] {
        min-height: 50px !important;
        font-size: 13px !important;
        border-radius: 13px !important;
    }
}

div[data-testid="stSegmentedControl"] [role="radio"]:active {
    transform: scale(.97) !important;
}

@media (max-width: 480px) {
    div[data-testid="stSegmentedControl"] [role="radiogroup"] {
        gap: 4px !important;
        padding: 4px !important;
        border-radius: 18px !important;
    }

    div[data-testid="stSegmentedControl"] [role="radio"] {
        min-height: 56px !important;
        font-size: 14px !important;
        border-radius: 14px !important;
    }
}


/* ============================================================
   BANCA POCKET — FINAL BLUE MOBILE THEME OVERRIDES
   ============================================================ */

/* Category + PKS segmented controls */
div[data-testid="stSegmentedControl"] {
    width: 100% !important;
    max-width: 100% !important;
    overflow: visible !important;
}

div[data-testid="stSegmentedControl"] [role="radiogroup"] {
    background: #ffffff !important;
    background-image: none !important;
    border: 1px solid #d7e3f3 !important;
    box-shadow: 0 8px 24px rgba(37, 99, 235, 0.08) !important;
}

div[data-testid="stSegmentedControl"] [role="radio"] {
    background: transparent !important;
    color: #48617f !important;
    border: 1px solid transparent !important;
    box-shadow: none !important;
    -webkit-text-fill-color: #48617f !important;
}

div[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"],
div[data-testid="stSegmentedControl"] [role="radio"][data-state="checked"],
div[data-testid="stSegmentedControl"] [role="radio"][aria-selected="true"] {
    background: linear-gradient(135deg, #1456c8 0%, #2f80ed 100%) !important;
    background-image: linear-gradient(135deg, #1456c8 0%, #2f80ed 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    border-color: transparent !important;
    box-shadow: 0 7px 18px rgba(37, 99, 235, 0.25) !important;
}

/* Prevent dark native focus/hover styles */
div[data-testid="stSegmentedControl"] [role="radio"]:hover {
    background: #eef5ff !important;
    color: #2563eb !important;
    -webkit-text-fill-color: #2563eb !important;
}

div[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"]:hover,
div[data-testid="stSegmentedControl"] [role="radio"][data-state="checked"]:hover,
div[data-testid="stSegmentedControl"] [role="radio"][aria-selected="true"]:hover {
    background: linear-gradient(135deg, #1456c8 0%, #2f80ed 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

/* Detail button — blue instead of black */
div[data-testid="stButton"] > button,
div[data-testid="stButton"] button {
    min-height: 48px !important;
    border-radius: 15px !important;
    border: 0 !important;
    background: linear-gradient(135deg, #1456c8 0%, #2f80ed 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 800 !important;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.18) !important;
    transition: transform .15s ease, box-shadow .15s ease !important;
}

div[data-testid="stButton"] > button:hover,
div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #124bb1 0%, #2563eb 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    box-shadow: 0 10px 24px rgba(37, 99, 235, 0.24) !important;
}

div[data-testid="stButton"] > button:active,
div[data-testid="stButton"] button:active {
    transform: scale(.985) !important;
}

/* Mobile: keep the three-item menus on one row */
@media (max-width: 600px) {
    div[data-testid="stSegmentedControl"] [role="radiogroup"] {
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        gap: 4px !important;
        padding: 4px !important;
        border-radius: 18px !important;
    }

    div[data-testid="stSegmentedControl"] [role="radio"] {
        min-height: 50px !important;
        padding: 4px 2px !important;
        font-size: 13px !important;
        border-radius: 13px !important;
    }

    div[data-testid="stButton"] > button {
        min-height: 50px !important;
        border-radius: 15px !important;
    }
}

/* ============================================================
   END FINAL BLUE MOBILE THEME
   ============================================================ */

/* ============================================================
   SECTION / TEXT — FORCE DARK TEXT
   ============================================================ */
.section-title {
    color: #17233d !important;
    font-size: 21px !important;
    line-height: 1.2 !important;
    font-weight: 800 !important;
    margin: 0 0 5px 2px !important;
}

.section-count {
    color: #647896 !important;
    font-size: 14px !important;
    line-height: 1.3 !important;
    font-weight: 500 !important;
    margin: 0 0 14px 2px !important;
}

.empty {
    color: #536987 !important;
    background: rgba(255,255,255,.88) !important;
    border: 1px solid #dce6f2 !important;
    border-radius: 18px !important;
    padding: 28px 16px !important;
    text-align: center !important;
}

/* Streamlit markdown/text below the search must remain visible on light UI */
.stMarkdown, .stMarkdown p, .stMarkdown div {
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* Company card */
.company-card {
    background: rgba(255,255,255,.96);
    border: 1px solid #e1e9f3;
    border-radius: 21px;
    padding: 16px;
    margin: 10px 0;
    box-shadow: 0 8px 24px rgba(36,65,105,.07);
}

.company-head {
    display:flex;
    align-items:center;
    gap:13px;
    margin-bottom:14px;
}

.company-logo {
    width:58px;
    height:58px;
    flex:0 0 58px;
    border-radius:17px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:21px;
    font-weight:800;
    background:linear-gradient(135deg,#2563eb,#60a5fa);
    box-shadow: inset 0 1px 0 rgba(255,255,255,.4);
}

.company-name {
    color:#17233d;
    font-size:16px;
    line-height:1.25;
    font-weight:800;
}

.company-type {
    color:#71829d;
    font-size:12px;
    margin-top:4px;
}

.arrow {
    margin-left:auto;
    font-size:24px;
    color:#526783;
}

.metrics {
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:7px;
}

.metric {
    background:#f7faff;
    border:1px solid #e6edf6;
    border-radius:12px;
    padding:9px 8px;
}

.metric-label {
    color:#71829d;
    font-size:10px;
    margin-bottom:4px;
}

.metric-value {
    color:#17233d;
    font-size:13px;
    font-weight:800;
}

.status-row {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:8px;
    margin-top:9px;
}

.status {
    border-radius:11px;
    padding:8px 6px;
    text-align:center;
    font-size:10px;
    font-weight:700;
}

.status.yes {
    background:#e4f8ef;
    color:#079455;
}

.status.no {
    background:#ffebeb;
    color:#e23838;
}

/* Detail */
.detail-card {
    background:white;
    border:1px solid #dfe8f3;
    border-radius:22px;
    padding:18px;
    margin-top:14px;
    box-shadow:0 10px 28px rgba(36,65,105,.08);
}

.detail-title {
    font-size:18px;
    font-weight:800;
    color:#17233d;
}

.detail-sub {
    font-size:12px;
    color:#71829d;
    margin-top:3px;
    margin-bottom:14px;
}

.detail-grid {
    display:grid;
    grid-template-columns:1fr 1fr;
    gap:9px;
}

.detail-metric {
    border:1px solid #e2eaf4;
    border-radius:14px;
    padding:11px;
}

.detail-metric .label {
    color:#71829d;
    font-size:10px;
}

.detail-metric .value {
    color:#17233d;
    font-size:15px;
    font-weight:800;
    margin-top:3px;
}

.empty {
    text-align:center;
    padding:35px 15px;
    background:white;
    border:1px dashed #cbd7e7;
    border-radius:20px;
    color:#71829d;
}

/* Bottom navigation */
.bottom-nav {
    position:fixed;
    z-index:999;
    left:50%;
    transform:translateX(-50%);
    bottom:10px;
    width:min(720px, calc(100% - 22px));
    background:rgba(255,255,255,.94);
    backdrop-filter:blur(16px);
    border:1px solid #dce6f1;
    border-radius:22px;
    box-shadow:0 10px 35px rgba(20,45,85,.14);
    display:grid;
    grid-template-columns:repeat(4,1fr);
    padding:8px 5px;
}

.nav-item {
    text-align:center;
    color:#71829d;
    font-size:10px;
    font-weight:600;
    padding:6px 2px;
}

.nav-icon {
    font-size:20px;
    line-height:1.1;
    margin-bottom:3px;
}

.nav-active {
    color:#2563eb;
}

/* Desktop still looks like phone/tablet */
@media (min-width: 900px) {
    .block-container { max-width: 780px !important; }
}

/* Mobile */
@media (max-width: 480px) {
    .bp-header { padding: 22px 18px 24px; border-radius: 0 0 26px 26px; }
    .bp-brand { font-size:24px; }
    .section-title { font-size:21px !important; color:#17233d !important; }
    .metrics { gap:5px; }
    .metric-value { font-size:12px; }
    .company-card { padding:13px; }
    .company-logo { width:52px; height:52px; flex-basis:52px; }
}


/* ============================================================
   BANCA POCKET - FORCE BLUE PRIMARY COLOR
   Overrides Streamlit's red/pink primary theme.
   ============================================================ */
:root,
html,
body,
.stApp,
[data-testid="stAppViewContainer"] {
    --primary-color: #2563EB !important;
    --primary-color-light: #60A5FA !important;
    --primary-color-dark: #1456C8 !important;
    --st-primary-color: #2563EB !important;
    --st-primary-color-light: #60A5FA !important;
    --st-primary-color-dark: #1456C8 !important;
}

/* Current Streamlit segmented control + BaseWeb variants */
div[data-testid="stSegmentedControl"] button,
div[data-testid="stSegmentedControl"] [role="radio"],
div[data-testid="stSegmentedControl"] [data-baseweb="button"] {
    color: #48617F !important;
    -webkit-text-fill-color: #48617F !important;
    background: #FFFFFF !important;
    background-image: none !important;
    border-color: #D7E3F3 !important;
}

/* Selected item: BLUE */
div[data-testid="stSegmentedControl"] button[aria-pressed="true"],
div[data-testid="stSegmentedControl"] button[data-selected="true"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"],
div[data-testid="stSegmentedControl"] [role="radio"][aria-selected="true"],
div[data-testid="stSegmentedControl"] [role="radio"][data-state="checked"],
div[data-testid="stSegmentedControl"] [data-selected="true"],
div[data-testid="stSegmentedControl"] [data-state="checked"],
div[data-testid="stSegmentedControl"] [data-highlighted="true"] {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: linear-gradient(135deg, #1456C8 0%, #2563EB 55%, #3B82F6 100%) !important;
    background-image: linear-gradient(135deg, #1456C8 0%, #2563EB 55%, #3B82F6 100%) !important;
    border-color: #2563EB !important;
    box-shadow: 0 6px 18px rgba(37,99,235,.25) !important;
}

/* Fallback if the app runs an older Streamlit radio */
div[data-testid="stRadio"] label:has(input:checked) {
    color: #FFFFFF !important;
    background: linear-gradient(135deg, #1456C8, #3B82F6) !important;
    border-color: #2563EB !important;
}

/* Focus/hover must stay blue, never red */
div[data-testid="stSegmentedControl"] button:focus,
div[data-testid="stSegmentedControl"] button:focus-visible,
div[data-testid="stSegmentedControl"] [role="radio"]:focus,
div[data-testid="stSegmentedControl"] [role="radio"]:focus-visible {
    outline: none !important;
    border-color: #2563EB !important;
    box-shadow: 0 0 0 2px rgba(37,99,235,.18) !important;
}

div[data-testid="stSegmentedControl"] button:hover,
div[data-testid="stSegmentedControl"] [role="radio"]:hover {
    color: #2563EB !important;
    -webkit-text-fill-color: #2563EB !important;
    background: #EEF5FF !important;
}

div[data-testid="stSegmentedControl"] button[aria-pressed="true"]:hover,
div[data-testid="stSegmentedControl"] [role="radio"][aria-checked="true"]:hover,
div[data-testid="stSegmentedControl"] [data-selected="true"]:hover {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    background: linear-gradient(135deg, #1456C8, #3B82F6) !important;
}

/* Primary Streamlit buttons */
button[kind="primary"],
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1456C8, #3B82F6) !important;
    color: #FFFFFF !important;
    border-color: #2563EB !important;
}



/* ============================================================
   BANCA POCKET - FINAL MOBILE FILTER UI
   Native radio version: no BaseWeb black/red segmented control.
   ============================================================ */

/* Hide native radio circles */
div[data-testid="stRadio"] > label {
    display: none !important;
}

div[data-testid="stRadio"] [role="radiogroup"] {
    width: 100% !important;
    display: flex !important;
    flex-direction: row !important;
    align-items: stretch !important;
    gap: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    background: #FFFFFF !important;
    border: 1px solid #D7E3F3 !important;
    border-radius: 18px !important;
    overflow: hidden !important;
    box-shadow: 0 8px 22px rgba(37, 99, 235, .08) !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    background: #FFFFFF !important;
    border: 0 !important;
    border-right: 1px solid #D7E3F3 !important;
    border-radius: 0 !important;
    cursor: pointer !important;
    transition: all .18s ease !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:last-child {
    border-right: 0 !important;
}

/* Text wrapper */
div[data-testid="stRadio"] [role="radiogroup"] > label > div:last-child,
div[data-testid="stRadio"] [role="radiogroup"] > label p,
div[data-testid="stRadio"] [role="radiogroup"] > label span {
    color: #48617F !important;
    -webkit-text-fill-color: #48617F !important;
    font-weight: 700 !important;
}

/* Hide radio input/circle */
div[data-testid="stRadio"] [role="radiogroup"] input {
    position: absolute !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Selected label = blue */
div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(135deg, #1456C8 0%, #2563EB 55%, #3B82F6 100%) !important;
    border-color: #2563EB !important;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,.10),
                0 6px 18px rgba(37,99,235,.20) !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) > div:last-child,
div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p,
div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Hover */
div[data-testid="stRadio"] [role="radiogroup"] > label:hover {
    background: #EEF5FF !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked):hover {
    background: linear-gradient(135deg, #1456C8, #3B82F6) !important;
}

/* Category selector */
div[data-testid="stRadio"]:has(input[value="▦  All"]) [role="radiogroup"] {
    min-height: 58px !important;
}

/* PKS selector directly below category */
div[data-testid="stRadio"] + div[data-testid="stRadio"] {
    margin-top: 10px !important;
}

/* Mobile */
@media (max-width: 600px) {
    div[data-testid="stRadio"] [role="radiogroup"] {
        min-height: 54px !important;
        border-radius: 17px !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] > label {
        min-height: 54px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        padding: 0 3px !important;
        overflow: hidden !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] > label p,
    div[data-testid="stRadio"] [role="radiogroup"] > label span {
        font-size: 14px !important;
        white-space: nowrap !important;
        margin: 0 !important;
    }
}

</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def normalize_column(name):
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def find_column(df, aliases):
    normalized = {normalize_column(c): c for c in df.columns}

    # exact normalized match
    for alias in aliases:
        key = normalize_column(alias)
        if key in normalized:
            return normalized[key]

    # partial match
    for alias in aliases:
        key = normalize_column(alias)
        for norm, original in normalized.items():
            if key in norm or norm in key:
                return original

    return None


def format_number(value):
    if pd.isna(value):
        return "-"
    try:
        value = float(value)
        if value.is_integer():
            return f"{value:,.0f}".replace(",", ".")
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except Exception:
        return str(value)


def clean_yes_no(value):
    if pd.isna(value):
        return "No"
    text = str(value).strip().lower()
    if text in ["yes", "y", "ya", "1", "true", "ada", "aktif"]:
        return "Yes"
    return "No"


def company_initial(name):
    words = re.findall(r"[A-Za-z0-9]+", str(name))
    if not words:
        return "A"
    if len(words) >= 2:
        return (words[0][0] + words[1][0]).upper()
    return words[0][:2].upper()


@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        return None, f"File {DATA_FILE.as_posix()} belum ditemukan."

    try:
        # Default: first sheet
        df = pd.read_excel(DATA_FILE)
        df = df.dropna(how="all").copy()
        return df, None
    except Exception as e:
        return None, f"Gagal membaca Excel: {e}"


def prepare_data(df):
    mapping = {
        "name": find_column(df, [
            "Nama Asuransi", "Nama Asuradur", "Asuransi",
            "Asuradur", "Nama Perusahaan"
        ]),
        "type": find_column(df, [
            "Jenis Asuransi", "Jenis", "Kategori",
            "Tipe Asuransi", "Type"
        ]),
        "investment": find_column(df, [
            "Investasi", "Investasi (Rp Miliar)", "Investments"
        ]),
        "assets": find_column(df, [
            "Aset", "Aset (Rp Miliar)", "Assets"
        ]),
        "equity": find_column(df, [
            "Ekuitas", "Ekuitas (Rp Miliar)", "Equity"
        ]),
        "premium": find_column(df, [
            "Pendapatan Jasa Asuransi",
            "Pendapatan Jasa Asuransi (Rp Miliar)",
            "Pendapatan Asuransi"
        ]),
        "profit": find_column(df, [
            "Laba (Rugi)", "Laba Rugi",
            "Laba (Rugi) (Rp Miliar)", "Profit"
        ]),
        "credit": find_column(df, [
            "PKS Rekanan Perkreditan",
            "PKS Kredit", "PKS Rekanan Kredit"
        ]),
        "banca": find_column(df, [
            "PKS Bancassurance", "PKS Banca", "Bancassurance"
        ]),
    }

    out = pd.DataFrame()

    if mapping["name"]:
        out["Nama Asuransi"] = df[mapping["name"]].astype(str).str.strip()
    else:
        # fallback: first column
        out["Nama Asuransi"] = df.iloc[:, 0].astype(str).str.strip()

    if mapping["type"]:
        out["Jenis Asuransi"] = df[mapping["type"]].fillna("").astype(str).str.strip()
    else:
        out["Jenis Asuransi"] = "Asuransi Umum"

    for key, label in [
        ("investment", "Investasi"),
        ("assets", "Aset"),
        ("equity", "Ekuitas"),
        ("premium", "Pendapatan Jasa Asuransi"),
        ("profit", "Laba (Rugi)"),
    ]:
        if mapping[key]:
            out[label] = pd.to_numeric(
                df[mapping[key]].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False),
                errors="coerce"
            )
        else:
            out[label] = pd.NA

    for key, label in [
        ("credit", "PKS Rekanan Perkreditan"),
        ("banca", "PKS Bancassurance"),
    ]:
        if mapping[key]:
            out[label] = df[mapping[key]].apply(clean_yes_no)
        else:
            out[label] = "No"

    out = out[out["Nama Asuransi"].str.lower().ne("nan")]
    out = out[out["Nama Asuransi"].str.strip().ne("")]
    out = out.drop_duplicates(subset=["Nama Asuransi"], keep="first").reset_index(drop=True)

    return out, mapping


def infer_type(value):
    text = str(value).lower()
    if "jiwa" in text or "life" in text:
        return "Asuransi Jiwa"
    return "Asuransi Umum"


# ------------------------------------------------------------
# Load data
# ------------------------------------------------------------
df_raw, error = load_data()

if error:
    st.markdown(
        f'<div style="padding:18px;border-radius:16px;background:#ffe8ec;color:#d92d45;font-weight:700;">'
        f'⚠️ {html.escape(error)}<br><span style="font-size:12px;font-weight:500;">'
        f'Upload file Excel ke folder <b>data</b> dengan nama <b>Data_Asuransi.xlsx</b>.</span></div>',
        unsafe_allow_html=True
    )
    st.stop()

df, column_mapping = prepare_data(df_raw)

# ------------------------------------------------------------
# Header
# ------------------------------------------------------------
st.markdown("""
<div class="bp-header">
    <div class="bp-brand">BancaPocket</div>
    <div class="bp-subtitle">Daftar Perusahaan Asuransi</div>
    <div class="bp-caption">Informasi Mitra Asuransi dalam Genggaman Anda</div>
    <div class="bp-shield">🛡️</div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Category state
# ------------------------------------------------------------
if "category" not in st.session_state:
    st.session_state.category = "All Asuransi"

# Responsive segmented selector — no st.columns, so it will not stack or overflow on phones.
category_options = ["▦  All", "🏢  Umum", "♥  Jiwa"]
category_index = {"All Asuransi": 0, "Asuransi Umum": 1, "Asuransi Jiwa": 2}.get(
    st.session_state.category, 0
)

category_choice = st.radio(
    "Kategori Asuransi",
    category_options,
    index=category_index,
    horizontal=True,
    label_visibility="collapsed",
    key="category_selector",
)

category_map = {
    "▦  All": "All Asuransi",
    "🏢  Umum": "Asuransi Umum",
    "♥  Jiwa": "Asuransi Jiwa",
}
new_category = category_map.get(category_choice, st.session_state.category)
if new_category != st.session_state.category:
    st.session_state.category = new_category
    st.session_state.selected_company = None
    st.rerun()

# ------------------------------------------------------------
# PKS FILTER
# ------------------------------------------------------------
if "pks_filter" not in st.session_state:
    st.session_state.pks_filter = "Semua"

pks_options = ["Semua", "PKS Kredit", "PKS Banca"]
pks_index = {
    "Semua": 0,
    "PKS Kredit": 1,
    "PKS Banca": 2,
}.get(st.session_state.pks_filter, 0)

pks_choice = st.radio(
    "Filter PKS",
    pks_options,
    index=pks_index,
    horizontal=True,
    label_visibility="collapsed",
    key="pks_selector",
)

if pks_choice and pks_choice != st.session_state.pks_filter:
    st.session_state.pks_filter = pks_choice
    st.session_state.selected_company = None
    st.rerun()

# ------------------------------------------------------------
# Search
# ------------------------------------------------------------
st.markdown('<div class="search-label">Cari Asuradur</div>', unsafe_allow_html=True)
search = st.text_input(
    "search",
    placeholder="🔎  Cari nama asuransi...",
    label_visibility="collapsed"
)

category = st.session_state.category

# All Asuransi = tampilkan semua perusahaan.
# Jika memilih kategori tertentu, filter berdasarkan Jenis Asuransi.
if category == "All Asuransi":
    filtered = df.copy()
elif column_mapping["type"]:
    filtered = df[df["Jenis Asuransi"].apply(infer_type).eq(category)].copy()
else:
    # Jika Excel belum memiliki kolom Jenis Asuransi,
    # data tetap ditampilkan saat kategori dipilih.
    filtered = df.copy()

# Filter status PKS. Filter ini dapat dipakai bersamaan dengan
# kategori Asuransi Umum / Jiwa dan pencarian nama.
pks_filter = st.session_state.pks_filter

if pks_filter == "PKS Kredit":
    filtered = filtered[
        filtered["PKS Rekanan Perkreditan"]
        .apply(clean_yes_no)
        .eq("Yes")
    ].copy()
elif pks_filter == "PKS Banca":
    filtered = filtered[
        filtered["PKS Bancassurance"]
        .apply(clean_yes_no)
        .eq("Yes")
    ].copy()

if search.strip():
    filtered = filtered[
        filtered["Nama Asuransi"].str.contains(
            search.strip(), case=False, na=False
        )
    ].copy()

# ------------------------------------------------------------
# Section
# ------------------------------------------------------------
count_label = "Semua Asuransi" if category == "All Asuransi" else category
pks_label = "" if pks_filter == "Semua" else f" • {pks_filter}"

st.markdown(
    f'<div class="section-title">Asuradur Partner</div>'
    f'<div class="section-count">Total {len(filtered)} {count_label}{pks_label}</div>',
    unsafe_allow_html=True
)

# ------------------------------------------------------------
# Cards
# ------------------------------------------------------------
if "selected_company" not in st.session_state:
    st.session_state.selected_company = None

if filtered.empty:
    st.markdown(
        '<div class="empty">🔎<br><br><b>Asuradur tidak ditemukan</b><br>'
        'Coba gunakan kata kunci lain.</div>',
        unsafe_allow_html=True
    )
else:
    for idx, row in filtered.iterrows():
        name = str(row["Nama Asuransi"])
        initials = company_initial(name)
        selected = st.session_state.selected_company == name

        credit = clean_yes_no(row["PKS Rekanan Perkreditan"])
        banca = clean_yes_no(row["PKS Bancassurance"])

        # IMPORTANT:
        # This HTML is intentionally built as one continuous string.
        # It avoids Streamlit Markdown interpreting indented HTML
        # as a code block.
        card_html = (
            '<div class="company-card">'
            '<div class="company-head">'
            f'<div class="company-logo">{html.escape(initials)}</div>'
            '<div style="min-width:0;">'
            f'<div class="company-name">{html.escape(name)}</div>'
            f'<div class="company-type">{html.escape(str(row["Jenis Asuransi"]) if category == "All Asuransi" else category)}</div>'
            '</div>'
            '<div class="arrow">›</div>'
            '</div>'
            '<div class="metrics">'
            '<div class="metric">'
            '<div class="metric-label">Investasi</div>'
            f'<div class="metric-value">{format_number(row["Investasi"])}</div>'
            '</div>'
            '<div class="metric">'
            '<div class="metric-label">Aset</div>'
            f'<div class="metric-value">{format_number(row["Aset"])}</div>'
            '</div>'
            '<div class="metric">'
            '<div class="metric-label">Ekuitas</div>'
            f'<div class="metric-value">{format_number(row["Ekuitas"])}</div>'
            '</div>'
            '</div>'
            '<div class="status-row">'
            f'<div class="status {"yes" if credit == "Yes" else "no"}">'
            f'PKS Kredit<br>{credit}'
            '</div>'
            f'<div class="status {"yes" if banca == "Yes" else "no"}">'
            f'PKS Banca<br>{banca}'
            '</div>'
            '</div>'
            '</div>'
        )

        st.markdown(card_html, unsafe_allow_html=True)

        if st.button(
            "Lihat Detail" if not selected else "Tutup Detail",
            key=f"detail_{idx}_{re.sub(r'[^a-zA-Z0-9]', '_', name)}",
            use_container_width=True
        ):
            st.session_state.selected_company = None if selected else name
            st.rerun()

        if selected:
            st.markdown(
                '<div class="detail-card">'
                f'<div class="detail-title">{html.escape(name)}</div>'
                f'<div class="detail-sub">{html.escape(str(row["Jenis Asuransi"]) if category == "All Asuransi" else category)}</div>'
                '<div class="detail-grid">'
                '<div class="detail-metric">'
                '<div class="label">Investasi</div>'
                f'<div class="value">{format_number(row["Investasi"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Aset</div>'
                f'<div class="value">{format_number(row["Aset"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Ekuitas</div>'
                f'<div class="value">{format_number(row["Ekuitas"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Pendapatan Jasa Asuransi</div>'
                f'<div class="value">{format_number(row["Pendapatan Jasa Asuransi"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">Laba (Rugi)</div>'
                f'<div class="value">{format_number(row["Laba (Rugi)"])} <small>Rp Miliar</small></div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">PKS Rekanan Perkreditan</div>'
                f'<div class="value">{credit}</div>'
                '</div>'
                '<div class="detail-metric">'
                '<div class="label">PKS Bancassurance</div>'
                f'<div class="value">{banca}</div>'
                '</div>'
                '</div>'
                '</div>',
                unsafe_allow_html=True
            )
