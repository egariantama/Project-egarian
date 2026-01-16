import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="FBI Bancassurance", layout="centered")

@st.cache_data(ttl=60)
def load_excel():
    return {
        "kpi": pd.read_excel("data_fbi.xlsx", sheet_name="kpi"),
        "amfs": pd.read_excel("data_fbi.xlsx", sheet_name="amfs"),
        "jiwa": pd.read_excel("data_fbi.xlsx", sheet_name="jiwa"),
        "kebakaran": pd.read_excel("data_fbi.xlsx", sheet_name="kebakaran"),
        "trend": pd.read_excel("data_fbi.xlsx", sheet_name="daily_trend")
    }

data = load_excel()

st.title("📊 Daily FBI Bancassurance")
st.caption(f"as {datetime.now().strftime('%d %B %Y')}")

# ================= KPI =================
cols = st.columns(len(data["kpi"]))
for col, row in zip(cols, data["kpi"].itertuples()):
    col.metric(row.metric, f"{row.value} {row.unit}")

# ================= AMFS =================
st.subheader("AMFS Snapshot")
for _, r in data["amfs"].iterrows():
    st.metric(r["metric"], f"{r['value']} {r['unit']}")

# ================= JIWA =================
st.subheader("Rabat Jiwa")
for _, r in data["jiwa"].iterrows():
    st.metric(r["metric"], f"Rp {r['value']} M")

# ================= KEBAKARAN =================
st.subheader("Rabat Kebakaran")
for _, r in data["kebakaran"].iterrows():
    st.metric(r["metric"], f"Rp {r['value']} M")

# ================= TREND =================
st.subheader("Daily Trend FBI")
fig, ax = plt.subplots()
ax.plot(data["trend"]["hk"], data["trend"]["dec25"], label="Dec '25")
ax.plot(data["trend"]["hk"], data["trend"]["jan26"], label="Jan '26")
ax.legend()
ax.grid(True)
st.pyplot(fig)
