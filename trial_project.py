import streamlit as st
import pandas as pd
from pathlib import Path
import html
import re
from urllib.parse import urlencode

# ============================================================
# BANCASSPOCKET - MOBILE INSURANCE PARTNER DIRECTORY
# ============================================================

st.set_page_config(
    page_title="BancassPocket",
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


/* ============================================================
   BANCASSPOCKET - PRECISION MOBILE FILTERS V2
   Full-width, equal segments, no native radio dots, smooth blue.
   ============================================================ */

/* The Streamlit radio wrapper must use the complete content width. */
div[data-testid="stRadio"],
div[data-testid="stRadio"] > div,
div[data-testid="stRadio"] > div > div {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}

/* Remove Streamlit's native radio indicator completely.
   Keep the input in the DOM so :has(input:checked) still works. */
div[data-testid="stRadio"] [role="radiogroup"] input {
    position: absolute !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    margin: 0 !important;
    pointer-events: none !important;
}

div[data-testid="stRadio"] [role="radiogroup"] [data-baseweb="radio"],
div[data-testid="stRadio"] [role="radiogroup"] [data-baseweb="radio"] > div:first-child,
div[data-testid="stRadio"] [role="radiogroup"] svg {
    display: none !important;
}

/* Equal-width segmented shell */
div[data-testid="stRadio"] [role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    height: 58px !important;
    padding: 0 !important;
    margin: 0 !important;
    gap: 0 !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    border: 1.5px solid #D7E3F3 !important;
    border-radius: 20px !important;
    background: #FFFFFF !important;
    box-shadow: 0 7px 22px rgba(37,99,235,.08) !important;
}

/* Each segment occupies exactly 1/3 */
div[data-testid="stRadio"] [role="radiogroup"] > label {
    flex: 1 1 33.333% !important;
    width: 33.333% !important;
    max-width: 33.333% !important;
    min-width: 0 !important;
    height: 100% !important;
    min-height: 58px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    box-sizing: border-box !important;
    padding: 0 4px !important;
    margin: 0 !important;
    border: 0 !important;
    border-right: 1px solid #D7E3F3 !important;
    border-radius: 0 !important;
    background: #FFFFFF !important;
    cursor: pointer !important;
    transition: background .20s ease, box-shadow .20s ease, transform .12s ease !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:last-child {
    border-right: 0 !important;
}

/* Text only */
div[data-testid="stRadio"] [role="radiogroup"] > label p,
div[data-testid="stRadio"] [role="radiogroup"] > label span {
    margin: 0 !important;
    padding: 0 !important;
    color: #4A6280 !important;
    -webkit-text-fill-color: #4A6280 !important;
    font-size: 17px !important;
    line-height: 1.15 !important;
    font-weight: 600 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    text-align: center !important;
}

/* Selected segment */
div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) {
    color: #FFFFFF !important;
    background: linear-gradient(135deg, #1456C8 0%, #2563EB 55%, #3B82F6 100%) !important;
    border-color: #2563EB !important;
    box-shadow: 0 5px 15px rgba(37,99,235,.20) !important;
    position: relative !important;
    z-index: 2 !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) p,
div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked) span {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* Soft hover, no black/red */
div[data-testid="stRadio"] [role="radiogroup"] > label:hover {
    background: #F1F6FF !important;
}

div[data-testid="stRadio"] [role="radiogroup"] > label:has(input:checked):hover {
    background: linear-gradient(135deg, #1456C8, #3B82F6) !important;
}

/* No red focus outline */
div[data-testid="stRadio"] [role="radiogroup"] > label:focus-within {
    outline: none !important;
    box-shadow: none !important;
}

/* Category and PKS spacing */
div[data-testid="stRadio"] {
    margin-bottom: 10px !important;
}

@media (max-width: 600px) {
    .block-container {
        padding-left: 16px !important;
        padding-right: 16px !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] {
        height: 56px !important;
        min-height: 56px !important;
        border-radius: 18px !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] > label {
        min-height: 56px !important;
        padding: 0 2px !important;
    }

    div[data-testid="stRadio"] [role="radiogroup"] > label p,
    div[data-testid="stRadio"] [role="radiogroup"] > label span {
        font-size: 15px !important;
        font-weight: 650 !important;
    }

    /* Slightly tighter spacing between category and PKS rows */
    div[data-testid="stRadio"] + div[data-testid="stRadio"] {
        margin-top: 8px !important;
    }
}




/* ============================================================
   BANCASSPOCKET - SIMPLE MOBILE FILTER BUTTONS
   Layout intentionally follows the user's sketch:
   Row 1 = All / Umum / Jiwa
   Row 2 = PKS Rekanan / PKS Bancass
   Each item is an independent rounded button.
   ============================================================ */

.bp-filter-row {
    width: 100% !important;
    max-width: 100% !important;
}

/* Streamlit columns used only by the two filter rows */
.bp-filter-row ~ div[data-testid="stHorizontalBlock"],
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]),
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}

/* Every filter column must be allowed to shrink */
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]) > div[data-testid="column"],
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) > div[data-testid="column"] {
    min-width: 0 !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}

/* Filter buttons */
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]) button,
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) button {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    height: 58px !important;
    min-height: 58px !important;
    padding: 0 10px !important;
    margin: 0 !important;
    border-radius: 18px !important;
    border: 1px solid #D7E3F3 !important;
    background: #FFFFFF !important;
    color: #4D6584 !important;
    -webkit-text-fill-color: #4D6584 !important;
    box-shadow: 0 5px 16px rgba(37,99,235,.07) !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    line-height: 1.1 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    transition:
        background .20s ease,
        color .20s ease,
        transform .15s ease,
        box-shadow .20s ease !important;
}

/* Active = smooth blue */
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]) button[kind="primary"],
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) button[kind="primary"] {
    background: linear-gradient(135deg, #1554C5 0%, #2563EB 55%, #3B82F6 100%) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border-color: #2563EB !important;
    box-shadow: 0 8px 20px rgba(37,99,235,.20) !important;
}

/* Hover / click */
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]) button[kind="secondary"]:hover,
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) button[kind="secondary"]:hover {
    background: #F4F8FF !important;
    color: #2563EB !important;
    -webkit-text-fill-color: #2563EB !important;
    border-color: #BBD0F2 !important;
}

div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]) button:active,
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) button:active {
    transform: scale(.985) !important;
}

/* Space between the two rows */
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) {
    margin-top: 14px !important;
}

/* Second row: two centered buttons, like the sketch */
div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) {
    justify-content: center !important;
}

@media (max-width: 600px) {
    div[data-testid="stHorizontalBlock"]:has(button[data-testid*="category_btn"]) button,
    div[data-testid="stHorizontalBlock"]:has(button[data-testid*="pks_btn"]) button {
        height: 56px !important;
        min-height: 56px !important;
        padding: 0 7px !important;
        border-radius: 18px !important;
        font-size: 15px !important;
    }
}

/* ============================================================
   END SIMPLE MOBILE FILTER BUTTONS
   ============================================================ */

/* Prevent horizontal overflow without creating an overflow/scroll container.
   `overflow-x:hidden` can break position:sticky on mobile Safari. */
html, body, .stApp, [data-testid="stAppViewContainer"] {
    max-width: 100% !important;
    overflow-x: visible !important;
}

/* Streamlit's main section is the actual scrolling viewport.
   Keep vertical scrolling here so position:sticky has a real scroll
   container on desktop and especially iOS Safari. */
section.main {
    max-width: 100% !important;
    overflow: visible !important;
}


/* ============================================================
   BANCASSPOCKET - FINAL POLISHED MOBILE LAYOUT
   Inspired by the approved mobile mockup.
   ============================================================ */

/* Keep Streamlit columns horizontal on mobile.
   This app uses horizontal blocks only for the filter controls. */
div[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    display: flex !important;
    flex-wrap: nowrap !important;
    align-items: stretch !important;
    box-sizing: border-box !important;
    gap: 10px !important;
}

div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    min-width: 0 !important;
    flex: 1 1 0 !important;
    width: auto !important;
    box-sizing: border-box !important;
}

/* Filter buttons: white by default */
div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
    width: 100% !important;
    min-width: 0 !important;
    height: 68px !important;
    min-height: 68px !important;
    padding: 6px 5px !important;
    margin: 0 !important;
    border-radius: 20px !important;
    border: 1px solid #dbe6f4 !important;
    background: rgba(255,255,255,.96) !important;
    background-image: none !important;
    color: #4e6686 !important;
    -webkit-text-fill-color: #4e6686 !important;
    font-size: 17px !important;
    font-weight: 700 !important;
    line-height: 1.15 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    box-shadow: 0 7px 22px rgba(39,78,130,.07) !important;
    transition: all .18s ease !important;
}

/* Active filter = smooth BancassPocket blue */
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    width: 100% !important;
    min-width: 0 !important;
    height: 68px !important;
    min-height: 68px !important;
    padding: 6px 5px !important;
    margin: 0 !important;
    border-radius: 20px !important;
    border: 1px solid #2563eb !important;
    background: linear-gradient(135deg,#1554c5 0%,#2563eb 55%,#3b82f6 100%) !important;
    background-image: linear-gradient(135deg,#1554c5 0%,#2563eb 55%,#3b82f6 100%) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    line-height: 1.15 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    box-shadow: 0 10px 25px rgba(37,99,235,.18) !important;
    transition: all .18s ease !important;
}

div[data-testid="stHorizontalBlock"] button[kind="secondary"]:hover {
    background: #f5f9ff !important;
    color: #2563eb !important;
    -webkit-text-fill-color: #2563eb !important;
    border-color: #bfd3f0 !important;
}

div[data-testid="stHorizontalBlock"] button:active {
    transform: scale(.985) !important;
}

/* Make the PKS row narrower and centered */
div[data-testid="stHorizontalBlock"]:has(button[key*="pks_btn"]) {
    max-width: 76% !important;
    margin-left: auto !important;
    margin-right: auto !important;
}

/* Category / cooperation section headings */
.filter-section-title {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    margin: 7px 0 10px;
}

.filter-section-title .main {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #17233d;
    font-size: 17px;
    font-weight: 800;
}

.filter-section-title .main:before {
    content: "";
    display: inline-block;
    width: 5px;
    height: 25px;
    border-radius: 99px;
    background: linear-gradient(180deg,#2563eb,#60a5fa);
}

.filter-section-title .hint {
    color: #7184a0;
    font-size: 12px;
    font-weight: 500;
    text-align: right;
}

.search-label {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    color: #17233d !important;
    font-size: 17px !important;
    font-weight: 800 !important;
    margin: 22px 0 9px 3px !important;
}

.search-label:before {
    content: "⌕";
    color: #2563eb;
    font-size: 27px;
    line-height: 1;
    font-weight: 500;
}

/* Search field closer to the mockup */
div[data-testid="stTextInput"] input {
    min-height: 54px !important;
    border-radius: 18px !important;
    padding: 0 16px !important;
    font-size: 16px !important;
    border: 1px solid #d5e1f0 !important;
    box-shadow: 0 7px 20px rgba(39,78,130,.07) !important;
}

/* More breathing room between filters and results */
.section-title {
    margin-top: 28px !important;
    font-size: 27px !important;
    line-height: 1.1 !important;
    font-weight: 800 !important;
    color: #17233d !important;
}

.section-count {
    font-size: 16px !important;
    color: #6c809e !important;
    margin-top: 6px !important;
    margin-bottom: 18px !important;
}

/* Mobile card polish */
.company-card {
    border-radius: 24px !important;
    padding: 15px !important;
    margin: 12px 0 !important;
    box-shadow: 0 10px 28px rgba(39,78,130,.08) !important;
}

.company-name {
    font-size: 16px !important;
}

.metric {
    border-radius: 14px !important;
    padding: 11px 9px !important;
}

.status {
    border-radius: 14px !important;
    padding: 10px 6px !important;
}

/* Prevent horizontal overflow on all screen sizes */
html, body, #root, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
.block-container {
    max-width: 100% !important;
    overflow-x: hidden !important;
}

@media (max-width: 600px) {
    .block-container {
        padding: 18px 18px 36px !important;
    }

    .bp-header {
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 28px 18px 30px !important;
        border-radius: 0 0 28px 28px !important;
    }

    .bp-brand {
        font-size: 28px !important;
    }

    .bp-subtitle {
        font-size: 17px !important;
        margin-top: 5px !important;
    }

    .bp-caption {
        font-size: 13px !important;
        line-height: 1.4 !important;
        max-width: 82% !important;
    }

    .bp-shield {
        right: 16px !important;
        top: 25px !important;
        width: 70px !important;
        height: 70px !important;
        border-radius: 22px !important;
    }

    div[data-testid="stHorizontalBlock"] {
        gap: 8px !important;
    }

    div[data-testid="stHorizontalBlock"] button[kind="secondary"],
    div[data-testid="stHorizontalBlock"] button[kind="primary"] {
        height: 62px !important;
        min-height: 62px !important;
        font-size: 15px !important;
        border-radius: 18px !important;
    }

    div[data-testid="stHorizontalBlock"]:has(button[key*="pks_btn"]) {
        max-width: 82% !important;
    }

    .filter-section-title {
        margin-top: 18px !important;
    }

    .filter-section-title .main {
        font-size: 16px !important;
    }

    .filter-section-title .hint {
        font-size: 11px !important;
    }

    .section-title {
        font-size: 25px !important;
    }

    .company-card {
        padding: 14px !important;
    }

    .company-logo {
        width: 56px !important;
        height: 56px !important;
        flex-basis: 56px !important;
    }

    .metrics {
        gap: 7px !important;
    }

    .metric-value {
        font-size: 13px !important;
    }
}


/* ============================================================
   FINAL FILTER CARDS — MOBILE MOCKUP MATCH
   Keyed containers make the two rows independently controllable.
   ============================================================ */

/* Kill the older segmented/radio styling if remnants exist. */
.st-key-category_filters,
.st-key-pks_filters {
    width: 100% !important;
    max-width: 100% !important;
    overflow: visible !important;
}

.st-key-category_filters div[data-testid="stHorizontalBlock"],
.st-key-pks_filters div[data-testid="stHorizontalBlock"] {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    display: grid !important;
    gap: 12px !important;
    align-items: stretch !important;
    box-sizing: border-box !important;
}

.st-key-category_filters div[data-testid="stHorizontalBlock"] {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}

.st-key-pks_filters div[data-testid="stHorizontalBlock"] {
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
}

.st-key-category_filters div[data-testid="column"],
.st-key-pks_filters div[data-testid="column"] {
    width: auto !important;
    max-width: none !important;
    min-width: 0 !important;
    flex: none !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: visible !important;
}

.st-key-category_filters .stButton,
.st-key-pks_filters .stButton {
    width: 100% !important;
    margin: 0 !important;
}

.st-key-category_filters button,
.st-key-pks_filters button {
    position: relative !important;
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    height: 112px !important;
    min-height: 112px !important;
    box-sizing: border-box !important;
    padding: 16px 8px !important;
    border-radius: 22px !important;
    border: 1px solid #dbe6f4 !important;
    background: rgba(255,255,255,.98) !important;
    background-image: none !important;
    color: #17233d !important;
    -webkit-text-fill-color: #17233d !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    box-shadow: 0 8px 22px rgba(37,78,130,.08) !important;
    transition: transform .16s ease, box-shadow .18s ease, background .18s ease !important;
}

/* Category cards */
.st-key-category_filters button::before {
    display: block !important;
    margin-bottom: 6px !important;
    font-size: 27px !important;
    line-height: 1 !important;
    font-weight: 700 !important;
    color: #526b8d !important;
    -webkit-text-fill-color: #526b8d !important;
}

.st-key-category_filters div[data-testid="column"]:nth-child(1) button::before {
    content: "▦" !important;
}
.st-key-category_filters div[data-testid="column"]:nth-child(2) button::before {
    content: "▥" !important;
}
.st-key-category_filters div[data-testid="column"]:nth-child(3) button::before {
    content: "♥" !important;
}

.st-key-category_filters button::after {
    display: block !important;
    margin-top: 5px !important;
    font-size: 12px !important;
    line-height: 1.15 !important;
    font-weight: 500 !important;
    color: #7286a3 !important;
    -webkit-text-fill-color: #7286a3 !important;
}

.st-key-category_filters div[data-testid="column"]:nth-child(1) button::after {
    content: "Semua Asuransi" !important;
}
.st-key-category_filters div[data-testid="column"]:nth-child(2) button::after {
    content: "Asuransi Umum" !important;
}
.st-key-category_filters div[data-testid="column"]:nth-child(3) button::after {
    content: "Asuransi Jiwa" !important;
}

/* PKS cards — same shape/proportion as Category cards */
.st-key-pks_filters button {
    height: 112px !important;
    min-height: 112px !important;
    text-align: center !important;
    padding: 16px 8px !important;
}

.st-key-pks_filters button::before {
    position: static !important;
    display: block !important;
    margin-bottom: 6px !important;
    transform: none !important;
    font-size: 27px !important;
    line-height: 1 !important;
    color: #607796 !important;
    -webkit-text-fill-color: #607796 !important;
}

.st-key-pks_filters div[data-testid="column"]:nth-child(1) button::before {
    content: "↺" !important;
}
.st-key-pks_filters div[data-testid="column"]:nth-child(2) button::before {
    content: "▤" !important;
}
.st-key-pks_filters div[data-testid="column"]:nth-child(3) button::before {
    content: "♢" !important;
}

.st-key-pks_filters button::after {
    display: block !important;
    margin-top: 6px !important;
    font-size: 12px !important;
    line-height: 1.15 !important;
    font-weight: 500 !important;
    color: #7286a3 !important;
    -webkit-text-fill-color: #7286a3 !important;
}

.st-key-pks_filters div[data-testid="column"]:nth-child(1) button::after {
    content: "Tampilkan Semua" !important;
}
.st-key-pks_filters div[data-testid="column"]:nth-child(2) button::after {
    content: "Kerja Sama Kredit" !important;
}
.st-key-pks_filters div[data-testid="column"]:nth-child(3) button::after {
    content: "Bancassurance" !important;
}

/* Active card */
.st-key-category_filters button[kind="primary"],
.st-key-pks_filters button[kind="primary"] {
    background: linear-gradient(135deg,#1554c5 0%,#2563eb 55%,#3b82f6 100%) !important;
    background-image: linear-gradient(135deg,#1554c5 0%,#2563eb 55%,#3b82f6 100%) !important;
    border-color: #2563eb !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    box-shadow: 0 10px 26px rgba(37,99,235,.22) !important;
}

.st-key-category_filters button[kind="primary"]::before,
.st-key-category_filters button[kind="primary"]::after,
.st-key-pks_filters button[kind="primary"]::before,
.st-key-pks_filters button[kind="primary"]::after {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.st-key-category_filters button:hover,
.st-key-pks_filters button:hover {
    transform: translateY(-1px) !important;
}

.st-key-category_filters button:active,
.st-key-pks_filters button:active {
    transform: scale(.985) !important;
}

/* Desktop/tablet: keep the same clean proportions but use a wider content area. */
@media (min-width: 601px) {
    .st-key-category_filters button {
        height: 118px !important;
        min-height: 118px !important;
    }
    .st-key-pks_filters button {
        height: 118px !important;
        min-height: 118px !important;
    }
}

/* iPhone / narrow screens */
@media (max-width: 600px) {
    .st-key-category_filters div[data-testid="stHorizontalBlock"],
    .st-key-pks_filters div[data-testid="stHorizontalBlock"] {
        gap: 9px !important;
    }

    .st-key-category_filters button {
        height: 108px !important;
        min-height: 108px !important;
        border-radius: 20px !important;
        padding: 13px 4px !important;
        font-size: 18px !important;
    }

    .st-key-category_filters button::before {
        font-size: 25px !important;
    }

    .st-key-category_filters button::after {
        font-size: 10.5px !important;
    }

    .st-key-pks_filters button {
        height: 108px !important;
        min-height: 108px !important;
        border-radius: 20px !important;
        padding: 13px 4px !important;
        font-size: 18px !important;
    }

    .st-key-pks_filters button::before {
        font-size: 25px !important;
        margin-bottom: 6px !important;
    }

    .st-key-pks_filters button::after {
        font-size: 10px !important;
    }

    /* Remove excessive vertical whitespace from Streamlit's button wrappers. */
    .st-key-category_filters [data-testid="stButton"],
    .st-key-pks_filters [data-testid="stButton"] {
        margin-bottom: 0 !important;
    }
}

/* ============================================================
   BANCASSPOCKET - FREEZE TOP FILTER BAR
   ============================================================ */

/* No Streamlit ancestor is allowed to clip the sticky element. */
html, body, .stApp,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
section.main,
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlock"] {
    overflow-x: visible !important;
    overflow-y: visible !important;
}

/* Actual Streamlit keyed container used by the two filter rows. */
.st-key-sticky_filters {
    position: -webkit-sticky !important;
    position: sticky !important;
    top: 0 !important;
    z-index: 999999 !important;
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
    align-self: stretch !important;

    margin: 0 0 18px 0 !important;
    padding: 10px 0 14px 0 !important;

    background: rgba(239,245,253,.98) !important;
    -webkit-backdrop-filter: blur(18px) saturate(150%) !important;
    backdrop-filter: blur(18px) saturate(150%) !important;

    border-bottom: 1px solid rgba(205,220,239,.95) !important;
    box-shadow: 0 8px 24px rgba(37,78,130,.12) !important;
}

/* Make sure Streamlit's generated children do not create another scroll context. */
.st-key-sticky_filters,
.st-key-sticky_filters > div,
.st-key-sticky_filters [data-testid="stVerticalBlock"],
.st-key-sticky_filters [data-testid="stVerticalBlockBorderWrapper"] {
    overflow: visible !important;
}

/* Keep the filter controls compact while frozen. */
.st-key-sticky_filters .filter-section-title {
    margin-top: 4px !important;
    margin-bottom: 7px !important;
}

.st-key-sticky_filters .filter-section-title .main {
    font-size: 15px !important;
}

.st-key-sticky_filters .filter-section-title .hint {
    font-size: 11px !important;
}

.st-key-sticky_filters .st-key-category_filters button {
    height: 70px !important;
    min-height: 70px !important;
    border-radius: 16px !important;
}

.st-key-sticky_filters .st-key-category_filters button::after {
    display: none !important;
}

.st-key-sticky_filters .st-key-pks_filters button {
    height: 64px !important;
    min-height: 64px !important;
    border-radius: 16px !important;
    font-size: 14px !important;
}

.st-key-sticky_filters .st-key-pks_filters button::before,
.st-key-sticky_filters .st-key-pks_filters button::after {
    display: none !important;
}

@media (max-width: 600px) {
    .st-key-sticky_filters {
        top: 0 !important;
        width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 7px 0 10px 0 !important;
        border-radius: 0 0 18px 18px !important;
    }

    .st-key-sticky_filters .filter-section-title {
        margin-top: 2px !important;
        margin-bottom: 5px !important;
    }

    .st-key-sticky_filters .filter-section-title .main {
        font-size: 14px !important;
    }

    .st-key-sticky_filters .filter-section-title .hint {
        font-size: 10px !important;
    }

    .st-key-sticky_filters .st-key-category_filters button {
        height: 66px !important;
        min-height: 66px !important;
        border-radius: 15px !important;
        font-size: 15px !important;
        padding: 7px 3px !important;
    }

    .st-key-sticky_filters .st-key-category_filters button::before {
        font-size: 19px !important;
        margin-bottom: 2px !important;
    }

    .st-key-sticky_filters .st-key-pks_filters button {
        height: 58px !important;
        min-height: 58px !important;
        border-radius: 15px !important;
        font-size: 13px !important;
    }
}


/* ============================================================
   BANCAPOCKET - MOBILE NAVIGATION
   Menu hanya di bagian bawah layar.
   ============================================================ */
.st-key-top_nav { display:none !important; }

/* Dashboard */
.dashboard-wrap { margin-top: 2px; }
.dashboard-section { margin: 18px 0 9px; }
.dashboard-section-title {
    font-size: 18px;
    line-height: 1.2;
    font-weight: 800;
    color: #17233d;
    letter-spacing: -.3px;
}
.dashboard-section-sub {
    font-size: 11px;
    color: #8190a8;
    margin-top: 4px;
}

.kpi-hero {
    background: linear-gradient(135deg,#1245a0 0%,#2563eb 62%,#3b82f6 100%);
    color: #fff;
    border-radius: 22px;
    padding: 18px 18px 17px;
    box-shadow: 0 12px 28px rgba(37,99,235,.18);
    position: relative;
    overflow: hidden;
}
.kpi-hero:after {
    content:"";
    position:absolute;
    width:150px;height:150px;
    right:-65px;top:-72px;
    border-radius:50%;
    background:rgba(255,255,255,.10);
}
.kpi-hero .eyebrow { font-size:11px; font-weight:600; opacity:.86; }
.kpi-hero .big { font-size:32px; font-weight:800; letter-spacing:-1px; margin-top:2px; position:relative; z-index:1; }
.kpi-hero .caption { font-size:10px; opacity:.82; margin-top:2px; position:relative; z-index:1; }

.dash-grid-2 { display:grid; grid-template-columns:1fr 1fr; gap:9px; }
.dash-card {
    background:#fff;
    border:1px solid #dce7f4;
    border-radius:19px;
    padding:14px 14px 13px;
    box-shadow:0 7px 20px rgba(20,45,85,.06);
}
.dash-card .label { font-size:10px; color:#7a8ba5; font-weight:600; }
.dash-card .value { font-size:22px; line-height:1.05; color:#17233d; font-weight:800; margin-top:4px; }
.dash-card .sub { font-size:10px; color:#91a0b6; margin-top:4px; }

.dash-stat-row {
    display:flex; align-items:center; justify-content:space-between;
    gap:10px; padding:10px 0; border-bottom:1px solid #edf2f8;
}
.dash-stat-row:last-child { border-bottom:0; padding-bottom:0; }
.dash-stat-name { font-size:11px; color:#50617b; font-weight:600; }
.dash-stat-value { font-size:13px; color:#17233d; font-weight:800; white-space:nowrap; }
.bar-track { height:7px; background:#edf3fa; border-radius:99px; overflow:hidden; margin-top:5px; }
.bar-fill { height:100%; background:linear-gradient(90deg,#2563eb,#60a5fa); border-radius:99px; }

.financial-card {
    background:#fff;
    border:1px solid #dce7f4;
    border-radius:21px;
    padding:15px;
    box-shadow:0 7px 20px rgba(20,45,85,.06);
}
.financial-note {
    display:inline-flex; align-items:center; gap:6px;
    padding:6px 9px; border-radius:10px;
    background:#eef5ff; color:#2563eb;
    font-size:9px; font-weight:700;
    margin:6px 0 8px;
}
.financial-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
.fin-item { background:#f7faff; border-radius:15px; padding:11px 10px; border:1px solid #edf2f8; }
.fin-item.full { grid-column:1 / -1; }
.fin-item .label { font-size:9px; color:#7b8ca6; font-weight:600; }
.fin-item .value { font-size:16px; color:#17233d; font-weight:800; margin-top:3px; letter-spacing:-.2px; }
.fin-item .unit { font-size:9px; color:#95a3b8; font-weight:500; }

.donut-card {
    background:#fff; border:1px solid #dce7f4; border-radius:21px;
    padding:15px; box-shadow:0 7px 20px rgba(20,45,85,.06);
}
.donut-layout { display:flex; align-items:center; gap:15px; }
.donut {
    width:112px; height:112px; border-radius:50%; flex:0 0 112px;
    background:conic-gradient(#2563eb 0 var(--rekanan-pct), #d8e2ef var(--rekanan-pct) var(--no-pks-end), #8fb1f5 var(--no-pks-end) 100%);
    display:grid; place-items:center;
}
.donut:after { content:""; width:76px; height:76px; border-radius:50%; background:#fff; grid-area:1/1; }
.donut-center { grid-area:1/1; z-index:1; text-align:center; }
.donut-center .num { font-size:20px; font-weight:800; color:#17233d; }
.donut-center .txt { font-size:8px; color:#8795aa; }
.legend { flex:1; }
.legend-row { display:flex; align-items:center; justify-content:space-between; margin:7px 0; gap:8px; }
.legend-left { display:flex; align-items:center; gap:7px; font-size:10px; color:#5f708a; font-weight:600; }
.legend-dot { width:8px; height:8px; border-radius:50%; background:#2563eb; flex:0 0 8px; }
.legend-dot.muted { background:#d8e2ef; }
.legend-dot.banca-dot { background:#8fb1f5; }
.legend-value { font-size:11px; font-weight:800; color:#17233d; }

.st-key-bottom_nav {
    position: fixed !important;
    z-index: 9999 !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
    bottom: 10px !important;
    width: min(720px, calc(100% - 24px)) !important;
    max-width: min(720px, calc(100% - 24px)) !important;
    box-sizing: border-box !important;
    background: rgba(255,255,255,.985) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border: 1px solid #d7e3f2 !important;
    border-radius: 22px !important;
    box-shadow: 0 12px 34px rgba(20,45,85,.16) !important;
    padding: 8px !important;
}

/* ============================================================
   BOTTOM NAV — TRUE EDGE-TO-EDGE 3 EQUAL COLUMNS
   The previous layout left an unused strip on the right on iPhone.
   Force the actual Streamlit horizontal block and every wrapper to
   occupy the full navigation width, then divide it into 3 equal cells.
   ============================================================ */
.st-key-bottom_nav > div,
.st-key-bottom_nav > div > div,
.st-key-bottom_nav div[data-testid="stVerticalBlock"],
.st-key-bottom_nav div[data-testid="stVerticalBlockBorderWrapper"] {
    width: 100% !important;
    max-width: none !important;
    min-width: 0 !important;
    box-sizing: border-box !important;
}

.st-key-bottom_nav div[data-testid="stHorizontalBlock"] {
    display: grid !important;
    grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
    width: 100% !important;
    max-width: none !important;
    min-width: 0 !important;
    gap: 8px !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
    overflow: visible !important;
}

.st-key-bottom_nav div[data-testid="column"] {
    width: auto !important;
    min-width: 0 !important;
    max-width: 100% !important;
    flex: none !important;
    padding: 0 !important;
    margin: 0 !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
}

/* Never allow a trailing Streamlit layout/spacer cell to create a blank
   area after the third navigation item. The bottom navigation has exactly
   three real buttons. */
.st-key-bottom_nav div[data-testid="column"]:nth-child(n+4) {
    display: none !important;
}

.st-key-bottom_nav div[data-testid="column"] > div,
.st-key-bottom_nav div[data-testid="column"] > div > div {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}

.st-key-bottom_nav div[data-testid="stButton"],
.st-key-bottom_nav div[data-testid="stButton"] > div {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    box-sizing: border-box !important;
}

.st-key-bottom_nav div[data-testid="stButton"] > button,
.st-key-bottom_nav div[data-testid="stButton"] button {
    width: 100% !important;
    min-width: 100% !important;
    max-width: none !important;
}

.st-key-bottom_nav button {
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    height: 56px !important;
    min-height: 56px !important;
    max-height: 56px !important;
    min-width: 0 !important;
    padding: 7px 6px !important;
    margin: 0 !important;
    border-radius: 17px !important;
    font-size: 11.5px !important;
    font-weight: 700 !important;
    line-height: 1.05 !important;
    letter-spacing: 0 !important;
    box-sizing: border-box !important;
    border: 1px solid #d6e2f0 !important;
    box-shadow: none !important;
    white-space: nowrap !important;
    overflow: hidden !important;
}

.st-key-bottom_nav button p {
    display: block !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    text-align: center !important;
}

.st-key-bottom_nav button[kind="primary"] {
    color: #fff !important;
    background: linear-gradient(135deg,#1557c7 0%,#2563eb 58%,#3b82f6 100%) !important;
    border-color: #2563eb !important;
    box-shadow: 0 7px 18px rgba(37,99,235,.22) !important;
}

.st-key-bottom_nav button[kind="secondary"] {
    color: #526783 !important;
    background: #edf3fa !important;
    border-color: #d6e2f0 !important;
}

.st-key-bottom_nav button[kind="secondary"]:hover {
    background: #e6eef8 !important;
    border-color: #cbd9ea !important;
}

@media (max-width: 480px) {
    .st-key-bottom_nav {
        left: 50% !important;
        right: auto !important;
        bottom: 8px !important;
        width: calc(100vw - 24px) !important;
        max-width: calc(100vw - 24px) !important;
        padding: 6px !important;
        border-radius: 21px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
    }

    /* On narrow screens use the viewport as the single source of truth.
       This eliminates Streamlit's hidden inner max-width that caused the
       blank strip after Fee Based Income. */
    .st-key-bottom_nav > div,
    .st-key-bottom_nav > div > div,
    .st-key-bottom_nav div[data-testid="stVerticalBlock"],
    .st-key-bottom_nav div[data-testid="stVerticalBlockBorderWrapper"],
    .st-key-bottom_nav div[data-testid="stHorizontalBlock"] {
        width: 100% !important;
        max-width: none !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }

    .st-key-bottom_nav div[data-testid="stHorizontalBlock"] {
        /* Break out of Streamlit's narrower inner content width.
           The navigation container itself is the reference width. */
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        width: calc(100vw - 36px) !important;
        max-width: calc(100vw - 36px) !important;
        min-width: 0 !important;
        gap: 6px !important;
        margin-left: calc((100% - (100vw - 36px)) / 2) !important;
        margin-right: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
        box-sizing: border-box !important;
    }

    .st-key-bottom_nav div[data-testid="column"] {
        min-width: 0 !important;
        width: auto !important;
        max-width: 100% !important;
        overflow: hidden !important;
    }

    /* Mobile: exactly 3 visible cells, each with identical width. */
    .st-key-bottom_nav div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr)) !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 6px !important;
    }

    .st-key-bottom_nav div[data-testid="column"]:nth-child(n+4) {
        display: none !important;
    }
    .st-key-bottom_nav div[data-testid="column"]:nth-child(-n+3) {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        flex: none !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    .st-key-bottom_nav button {
        height: 53px !important;
        min-height: 53px !important;
        max-height: 53px !important;
        padding: 6px 2px !important;
        border-radius: 16px !important;
        font-size: 10px !important;
        line-height: 1.05 !important;
    }

    .st-key-bottom_nav button p {
        font-size: 10px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: clip !important;
        width: 100% !important;
    }
}

/* Keep content clear of the fixed bottom navigation. */
.block-container { padding-bottom: 6rem !important; }

@media (max-width: 480px) {
    .dash-grid-2 { gap:7px; }
    .dash-card { padding:12px; }
    .dash-card .value { font-size:19px; }
    .financial-grid { gap:7px; }
    .fin-item .value { font-size:14px; }
    .donut { width:96px; height:96px; flex-basis:96px; }
    .donut:after { width:65px; height:65px; }
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


def parse_excel_number(value):
    """
    Membaca angka dari Excel tanpa merusak nilai desimal.

    Excel/Pandas biasanya sudah membaca nilai seperti 6913,412
    sebagai float 6913.412. Nilai numerik seperti itu TIDAK boleh
    diproses lagi dengan menghapus titik, karena titik tersebut adalah
    pemisah desimal Python, bukan pemisah ribuan.
    """
    if pd.isna(value):
        return pd.NA

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)

    text = str(value).strip()
    if not text:
        return pd.NA

    try:
        # Format Indonesia dengan koma sebagai desimal: 6913,412
        if "," in text:
            return float(text.replace(".", "").replace(",", "."))

        # String angka biasa dari Excel/Pandas: 6913.412
        return float(text)
    except (ValueError, TypeError):
        return pd.NA


def format_number(value):
    """
    Tampilkan angka dalam format Indonesia tanpa angka desimal.

    Contoh:
      6913.412   -> 6.913
      18184.582  -> 18.184
      5770.571   -> 5.770

    Angka di belakang koma dipotong (bukan dibulatkan).
    """
    if pd.isna(value):
        return "—"

    try:
        number = float(value)
        return f"{int(number):,}".replace(",", ".")
    except (ValueError, TypeError):
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
            "PKS Rekanan", "PKS Rekanan Kredit"
        ]),
        "banca": find_column(df, [
            "PKS Bancassurance", "PKS Bancass", "Bancassurance"
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
            out[label] = df[mapping[key]].apply(parse_excel_number)
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
    <div class="bp-subtitle">Partner Asuransi, Lebih Dekat</div>
    <div class="bp-caption">Informasi Rekanan Asuransi dalam Genggaman Anda</div>
    <div class="bp-shield">🛡️</div>
</div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# APP NAVIGATION STATE — hanya Dashboard & Kerja Sama
# Navigasi ditampilkan hanya pada bottom navigation.
# ------------------------------------------------------------
if "active_menu" not in st.session_state:
    st.session_state.active_menu = "Dashboard"

# Custom bottom navigation uses a URL query parameter instead of
# Streamlit's st.columns(), removing internal column-width side effects.
_ALLOWED_MENUS = {"Dashboard", "Kerja Sama", "Fee Based Income"}
_menu_from_url = st.query_params.get("menu")
if _menu_from_url in _ALLOWED_MENUS:
    st.session_state.active_menu = _menu_from_url

def set_active_menu(value):
    st.session_state.active_menu = value
    # Detail perusahaan tidak dibawa ketika berpindah menu.
    st.session_state.selected_company = None

# ------------------------------------------------------------
# DASHBOARD
# ------------------------------------------------------------
if st.session_state.active_menu == "Dashboard":
    total = len(df)
    umum = int(df["Jenis Asuransi"].apply(infer_type).eq("Asuransi Umum").sum())
    jiwa = int(df["Jenis Asuransi"].apply(infer_type).eq("Asuransi Jiwa").sum())
    rekanan = int(df["PKS Rekanan Perkreditan"].apply(clean_yes_no).eq("Yes").sum())
    bancass = int(df["PKS Bancassurance"].apply(clean_yes_no).eq("Yes").sum())
    no_pks = int(
        (
            df["PKS Rekanan Perkreditan"].apply(clean_yes_no).eq("No")
            & df["PKS Bancassurance"].apply(clean_yes_no).eq("No")
        ).sum()
    )

    def pct(value, base=total):
        if not base:
            return 0.0
        return value / base * 100

    # FINANCIAL SUMMARY — KHUSUS PKS REKANAN
    rekanan_df = df[df["PKS Rekanan Perkreditan"].apply(clean_yes_no).eq("Yes")].copy()

    def financial_total(column):
        if column not in rekanan_df.columns:
            return pd.NA
        series = pd.to_numeric(rekanan_df[column], errors="coerce")
        if series.notna().any():
            return series.sum()
        return pd.NA

    fin_investasi = financial_total("Investasi")
    fin_aset = financial_total("Aset")
    fin_ekuitas = financial_total("Ekuitas")
    fin_pendapatan = financial_total("Pendapatan Jasa Asuransi")
    fin_laba = financial_total("Laba (Rugi)")

    st.markdown('<div class="dashboard-wrap">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="kpi-hero">'
        f'<div class="eyebrow">TOTAL ASURADUR</div>'
        f'<div class="big">{total:,}'.replace(',', '.') + '</div>'
        f'<div class="caption">Seluruh perusahaan asuransi dalam database BancaPocket</div>'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-section">'
        '<div class="dashboard-section-title">Komposisi Asuradur</div>'
        '<div class="dashboard-section-sub">Distribusi berdasarkan jenis perusahaan</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dash-grid-2">'
        '<div class="dash-card">'
        '<div class="label">ASURANSI UMUM</div>'
        f'<div class="value">{umum:,}'.replace(',', '.') + '</div>'
        f'<div class="sub">{pct(umum):.1f}% dari total</div>'
        '<div class="bar-track"><div class="bar-fill" style="width:' + f'{pct(umum):.1f}' + '%"></div></div>'
        '</div>'
        '<div class="dash-card">'
        '<div class="label">ASURANSI JIWA</div>'
        f'<div class="value">{jiwa:,}'.replace(',', '.') + '</div>'
        f'<div class="sub">{pct(jiwa):.1f}% dari total</div>'
        '<div class="bar-track"><div class="bar-fill" style="width:' + f'{pct(jiwa):.1f}' + '%"></div></div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-section">'
        '<div class="dashboard-section-title">Status Kerja Sama</div>'
        '<div class="dashboard-section-sub">Ringkasan status PKS pada seluruh asuradur</div>'
        '</div>',
        unsafe_allow_html=True
    )

    # Donut 3 warna. Karena status PKS dapat overlap (satu asuradur
    # dapat memiliki PKS Rekanan dan PKS Bancass sekaligus), segmen
    # donut dinormalisasi dari total ketiga hitungan. Angka asli dan
    # persentase terhadap total asuradur tetap ditampilkan di legend.
    donut_total = rekanan + no_pks + bancass
    if donut_total > 0:
        donut_rekanan_pct = rekanan / donut_total * 100
        donut_no_pks_end = donut_rekanan_pct + (no_pks / donut_total * 100)
    else:
        donut_rekanan_pct = 0
        donut_no_pks_end = 0

    st.markdown(
        '<div class="donut-card">'
        '<div class="donut-layout">'
        f'<div class="donut" style="--rekanan-pct:{donut_rekanan_pct:.2f}%;--no-pks-end:{donut_no_pks_end:.2f}%">'
        '<div class="donut-center"></div></div>'
        '<div class="legend">'
        '<div class="legend-row"><div class="legend-left"><span class="legend-dot"></span>PKS Rekanan</div>'
        f'<div class="legend-value">{rekanan:,}'.replace(',', '.') + f' &nbsp;({pct(rekanan):.1f}%)</div></div>'
        '<div class="legend-row"><div class="legend-left"><span class="legend-dot muted"></span>Tidak Ada PKS</div>'
        f'<div class="legend-value">{no_pks:,}'.replace(',', '.') + f' &nbsp;({pct(no_pks):.1f}%)</div></div>'
        '<div class="legend-row"><div class="legend-left"><span class="legend-dot banca-dot"></span>PKS Bancass</div>'
        f'<div class="legend-value">{bancass:,}'.replace(',', '.') + f' &nbsp;({pct(bancass):.1f}%)</div></div>'
        '</div></div></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-section">'
        '<div class="dashboard-section-title">Cakupan Kerja Sama</div>'
        '<div class="dashboard-section-sub">Jumlah asuradur berdasarkan jenis PKS</div>'
        '</div>',
        unsafe_allow_html=True
    )

    max_pks = max(rekanan, bancass, 1)
    st.markdown(
        '<div class="dash-card">'
        '<div class="dash-stat-row"><div style="flex:1">'
        '<div class="dash-stat-name">PKS Rekanan</div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{rekanan/max_pks*100:.1f}%"></div></div>'
        f'</div><div class="dash-stat-value">{rekanan:,}'.replace(',', '.') + '</div></div>'
        '<div class="dash-stat-row"><div style="flex:1">'
        '<div class="dash-stat-name">PKS Bancass</div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{bancass/max_pks*100:.1f}%"></div></div>'
        f'</div><div class="dash-stat-value">{bancass:,}'.replace(',', '.') + '</div></div>'
        '<div class="dash-stat-row"><div style="flex:1">'
        '<div class="dash-stat-name">Tidak Ada PKS</div>'
        f'<div class="bar-track"><div class="bar-fill" style="width:{no_pks/max(total,1)*100:.1f}%"></div></div>'
        f'</div><div class="dash-stat-value">{no_pks:,}'.replace(',', '.') + '</div></div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="dashboard-section">'
        '<div class="dashboard-section-title">Ringkasan Data Keuangan</div>'
        '<div class="dashboard-section-sub">Kinerja agregat asuradur yang memiliki PKS Rekanan</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="financial-card">'
        f'<div class="financial-note">✓ {rekanan:,}'.replace(',', '.') + ' Asuradur Rekanan</div>'
        '<div class="financial-grid">'
        '<div class="fin-item"><div class="label">INVESTASI</div>'
        f'<div class="value">{format_number(fin_investasi)} <span class="unit">Rp Miliar</span></div></div>'
        '<div class="fin-item"><div class="label">ASET</div>'
        f'<div class="value">{format_number(fin_aset)} <span class="unit">Rp Miliar</span></div></div>'
        '<div class="fin-item"><div class="label">EKUITAS</div>'
        f'<div class="value">{format_number(fin_ekuitas)} <span class="unit">Rp Miliar</span></div></div>'
        '<div class="fin-item"><div class="label">PENDAPATAN JASA ASURANSI</div>'
        f'<div class="value">{format_number(fin_pendapatan)} <span class="unit">Rp Miliar</span></div></div>'
        '<div class="fin-item full"><div class="label">LABA (RUGI)</div>'
        f'<div class="value">{format_number(fin_laba)} <span class="unit">Rp Miliar</span></div></div>'
        '</div></div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.active_menu == "Kerja Sama":
    # ------------------------------------------------------------
    # MOBILE FILTERS — STICKY / FREEZE TOP
    # ------------------------------------------------------------
    # Native Streamlit buttons are used intentionally. Clicking a filter
    # performs only the normal Streamlit rerun; it does not open a new tab.

    if "category" not in st.session_state:
        st.session_state.category = "All Asuransi"
    if "pks_filter" not in st.session_state or st.session_state.pks_filter not in {
        "Lepas Filter", "PKS Rekanan", "PKS Bancass"
    }:
        st.session_state.pks_filter = "Lepas Filter"

    category_items = [
        ("▦  All", "All Asuransi"),
        ("🏢  Umum", "Asuransi Umum"),
        ("♥  Jiwa", "Asuransi Jiwa"),
    ]

    def set_category(value):
        st.session_state.category = value

    def set_pks(value):
        st.session_state.pks_filter = value

    # Everything below is placed inside one Streamlit container so the
    # category + PKS controls can freeze together while the user scrolls.
    with st.container(key="sticky_filters"):

        # ------------------------------------------------------------
        # Row 1 — All / Umum / Jiwa
        # ------------------------------------------------------------
        st.markdown(
            '<div class="filter-section-title">'
            '<div class="main">Kategori Asuransi</div>'
            '<div class="hint"><span style="padding-right:18px;">Pilih jenis asuransi</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(key="category_filters"):
            cat_cols = st.columns(3, gap="small")
            for i, (label, value) in enumerate(category_items):
                with cat_cols[i]:
                    # Short label; CSS supplies the icon/subtitle for the card UI.
                    short_label = ["All", "Umum", "Jiwa"][i]
                    st.button(
                        short_label,
                        key=f"category_btn_{i}",
                        use_container_width=True,
                        type="primary" if st.session_state.category == value else "secondary",
                        on_click=set_category,
                        args=(value,),
                    )

        # ------------------------------------------------------------
        # Row 2 — Lepas Filter / PKS Rekanan / PKS Bancass
        # ------------------------------------------------------------
        st.markdown(
            '<div class="filter-section-title">'
            '<div class="main">Jenis Kerja Sama</div>'
            '<div class="hint"><span style="padding-right:18px;">Pilih atau lepas filter PKS</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

        with st.container(key="pks_filters"):
            # "Lepas Filter" hanya menghapus filter PKS. Filter kategori
            # (All / Umum / Jiwa) dan pencarian nama tetap dipertahankan.
            pks_items = ["Lepas Filter", "PKS Rekanan", "PKS Bancass"]
            pks_cols = st.columns(3, gap="small")
            for i, value in enumerate(pks_items):
                with pks_cols[i]:
                    st.button(
                        value,
                        key=f"pks_btn_{i}",
                        use_container_width=True,
                        type="primary" if st.session_state.pks_filter == value else "secondary",
                        on_click=set_pks,
                        args=(value,),
                    )

    # ------------------------------------------------------------
    # ------------------------------------------------------------
    # Search
    # ------------------------------------------------------------
    st.markdown('<div class="search-label">Cari Asuradur</div>', unsafe_allow_html=True)
    search = st.text_input(
        "search",
        placeholder="Cari nama asuransi...",
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

    if pks_filter == "PKS Rekanan":
        filtered = filtered[
            filtered["PKS Rekanan Perkreditan"]
            .apply(clean_yes_no)
            .eq("Yes")
        ].copy()
    elif pks_filter == "PKS Bancass":
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
    pks_label = "" if pks_filter == "Lepas Filter" else f" • {pks_filter}"

    st.markdown(
        f'<div class="section-title">Daftar Asuradur</div>'
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
                f'PKS Rekanan<br>{credit}'
                '</div>'
                f'<div class="status {"yes" if banca == "Yes" else "no"}">'
                f'PKS Bancass<br>{banca}'
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


# ------------------------------------------------------------
# FEE BASED INCOME — TAHAP PENGEMBANGAN
# ------------------------------------------------------------
elif st.session_state.active_menu == "Fee Based Income":
    st.markdown(
        '<div class="dashboard-wrap">'
        '<div class="dashboard-section">'
        '<div class="dashboard-section-title">Fee Based Income</div>'
        '<div class="dashboard-section-sub">Modul sedang dalam tahap pengembangan</div>'
        '</div>'
        '<div class="financial-card" style="text-align:center;padding:32px 18px;">'
        '<div style="font-size:42px;">💰</div>'
        '<div style="font-size:16px;font-weight:800;color:#17233d;margin-top:10px;">Fee Based Income</div>'
        '<div style="font-size:11px;color:#8190a8;margin-top:6px;">Fitur monitoring dan analisis pendapatan berbasis fee akan dikembangkan pada tahap berikutnya.</div>'
        '</div></div>',
        unsafe_allow_html=True
    )

# ------------------------------------------------------------
# BOTTOM NAVIGATION — Dashboard, Kerja Sama, Fee Based Income
# ------------------------------------------------------------
# ------------------------------------------------------------
# CUSTOM BOTTOM NAVIGATION — EXACT 3-SHAPE GRID
# ------------------------------------------------------------
_nav_active = st.session_state.active_menu

st.markdown(
    f"""
    <div class="bp-bottom-nav">
        <a class="bp-nav-item {'active' if _nav_active == 'Dashboard' else ''}"
           href="?menu=Dashboard" aria-label="Dashboard">
            <span class="bp-nav-icon">▦</span>
            <span class="bp-nav-label">Dashboard</span>
        </a>
        <a class="bp-nav-item {'active' if _nav_active == 'Kerja Sama' else ''}"
           href="?menu=Kerja%20Sama" aria-label="Kerja Sama">
            <span class="bp-nav-icon">▤</span>
            <span class="bp-nav-label">Kerja Sama</span>
        </a>
        <a class="bp-nav-item {'active' if _nav_active == 'Fee Based Income' else ''}"
           href="?menu=Fee%20Based%20Income" aria-label="Fee Based Income">
            <span class="bp-nav-icon">💰</span>
            <span class="bp-nav-label">Fee Based Income</span>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    /* Custom navigation: exactly three real grid items. */
    .bp-bottom-nav {
        position: fixed;
        z-index: 99999;
        left: 50%;
        bottom: 10px;
        transform: translateX(-50%);
        width: min(720px, calc(100vw - 24px));
        height: 76px;
        padding: 8px;
        box-sizing: border-box;
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 8px;
        border: 1px solid #d7e3f2;
        border-radius: 24px;
        background: rgba(255,255,255,.97);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        box-shadow: 0 12px 34px rgba(20,45,85,.16);
        overflow: hidden;
    }

    .bp-nav-item {
        width: 100%;
        min-width: 0;
        height: 100%;
        box-sizing: border-box;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 7px;
        padding: 0 6px;
        margin: 0;
        border: 1px solid #d6e2f0;
        border-radius: 18px;
        background: #edf3fa;
        color: #526783;
        text-decoration: none !important;
        font-family: 'Inter', sans-serif;
        font-size: 12px;
        font-weight: 600;
        line-height: 1;
        white-space: nowrap;
        overflow: hidden;
    }

    .bp-nav-item.active {
        color: #fff;
        background: linear-gradient(135deg,#1557c7 0%,#2563eb 58%,#3b82f6 100%);
        border-color: #2563eb;
        box-shadow: 0 7px 18px rgba(37,99,235,.22);
    }

    .bp-nav-item:hover,
    .bp-nav-item:focus,
    .bp-nav-item:active {
        text-decoration: none !important;
    }

    .bp-nav-icon {
        flex: 0 0 auto;
        font-size: 17px;
        line-height: 1;
    }

    .bp-nav-label {
        min-width: 0;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }

    @media (max-width: 480px) {
        .bp-bottom-nav {
            left: 12px;
            right: 12px;
            transform: none;
            width: auto;
            max-width: none;
            height: 74px;
            bottom: 8px;
            padding: 6px;
            gap: 6px;
            border-radius: 22px;
        }

        .bp-nav-item {
            border-radius: 17px;
            gap: 5px;
            padding: 0 4px;
            font-size: 10.5px;
        }

        .bp-nav-icon {
            font-size: 15px;
        }
    }

    .block-container {
        padding-bottom: 6rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

