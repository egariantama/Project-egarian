import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(page_title="COVID-19 Dashboard Indonesia", layout="wide")
st.title("📊 COVID-19 Dashboard - Indonesia")
st.markdown("Data dari Our World In Data (diproses sebelumnya di notebook)")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("indo_covid_cleaned.csv", parse_dates=["date"])

df = load_data()

# Sidebar - Tampilan keren
with st.sidebar:
    st.markdown("## 🦠 COVID-19 Dashboard")
    st.image("https://th.bing.com/th/id/OIP.2uvMD54NDV2owYM5xpCV6gHaFq?w=224&h=180&c=7&r=0&o=7&dpr=1.1&pid=1.7&rm=3", width=100)
    st.markdown("Pantau perkembangan COVID-19 di Indonesia secara visual dan interaktif.")
    st.markdown("---")

    st.markdown("### 📅 Filter Tanggal")
    start_date = st.date_input("🗓️ Tanggal Mulai", df['date'].min())
    end_date = st.date_input("🗓️ Tanggal Akhir", df['date'].max())

    st.markdown("---")
    total_days = (df['date'].max() - df['date'].min()).days
    st.markdown(f"📌 **Rentang Waktu Data:** `{df['date'].min().date()}` → `{df['date'].max().date()}`")
    st.markdown(f"⏱️ **Total Hari Terdata:** `{total_days}` hari")
    st.markdown("---")
    st.caption("📊 Data dari Our World In Data")

# Filter berdasarkan tanggal
mask = (df['date'] >= pd.to_datetime(start_date)) & (df['date'] <= pd.to_datetime(end_date))
filtered_df = df.loc[mask]

# Statistik Umum
st.subheader("📈 Statistik Umum")
col1, col2, col3, col4 = st.columns(4)
total_cases = filtered_df["new_cases"].sum()
total_deaths = filtered_df["new_deaths"].sum()
cfr = total_deaths / total_cases
col1.metric("Total Kasus", f"{int(filtered_df['total_cases'].max()):,}")
col2.metric("Total Kematian", f"{int(filtered_df['total_deaths'].max()):,}")
col3.metric("Total Vaksinasi", f"{int(filtered_df['total_vaccinations'].max()):,}")
col4.metric("Case Fatality Rate (CFR)", f"{cfr:.2%}")

# Grafik Kasus Harian (dengan 2 y-axis)
st.subheader("📉 Grafik Kasus Harian")
fig, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="date", y="new_cases", label="Kasus Baru", ax=ax1, color='tab:blue')
ax1.set_ylabel("Kasus Baru", color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax2 = ax1.twinx()
sns.lineplot(data=filtered_df, x="date", y="new_deaths", label="Kematian Baru", ax=ax2, color='tab:orange')
ax2.set_ylabel("Kematian Baru", color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')
fig.suptitle("Perkembangan Kasus dan Kematian Harian")
fig.tight_layout()
st.pyplot(fig)

# Grafik Vaksinasi
st.subheader("💉 Perkembangan Vaksinasi")
fig2, ax2 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="date", y="people_vaccinated", label="Divaksinasi", ax=ax2)
sns.lineplot(data=filtered_df, x="date", y="people_fully_vaccinated", label="Vaksin Lengkap", ax=ax2)
ax2.set_ylabel("Jumlah")
ax2.set_title("Vaksinasi COVID-19")
ax2.legend()
st.pyplot(fig2)

# Grafik 7-Hari Rata-rata
st.subheader("📊 Rata-rata 7 Hari Kasus dan Kematian")
filtered_df["new_cases_ma7"] = filtered_df["new_cases"].rolling(window=7).mean()
filtered_df["new_deaths_ma7"] = filtered_df["new_deaths"].rolling(window=7).mean()

fig, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=filtered_df, x="date", y="new_cases_ma7", label="Kasus Baru (7-day MA)", ax=ax1, color='blue')
ax2 = ax1.twinx()
sns.lineplot(data=filtered_df, x="date", y="new_deaths_ma7", label="Kematian Baru (7-day MA)", ax=ax2, color='red')
ax1.set_ylabel("Kasus Baru (Rata-rata)")
ax2.set_ylabel("Kematian Baru (Rata-rata)")
plt.title("Perkembangan COVID-19 (7 Hari Rata-Rata)")
fig.tight_layout()
st.pyplot(fig)

# Grafik per Bulan
st.subheader("📅 Kasus dan Kematian per Bulan")
filtered_df["month"] = filtered_df["date"].dt.to_period("M")
monthly = filtered_df.groupby("month")[["new_cases", "new_deaths"]].sum().reset_index()
monthly["month"] = monthly["month"].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x="month", y="new_cases", label="Kasus Baru", ax=ax)
sns.lineplot(data=monthly, x="month", y="new_deaths", label="Kematian Baru", ax=ax)
plt.xticks(rotation=45)
plt.title("Jumlah Kasus & Kematian per Bulan")
plt.tight_layout()
st.pyplot(fig)

# Puncak kasus dan kematian
st.subheader("📌 Puncak Kasus dan Kematian")
peak_case = filtered_df.loc[filtered_df["new_cases"].idxmax()]
peak_death = filtered_df.loc[filtered_df["new_deaths"].idxmax()]
st.markdown(f"📌 **Puncak Kasus Baru:** {peak_case['date'].date()} dengan {peak_case['new_cases']:,} kasus")
st.markdown(f"📌 **Puncak Kematian Baru:** {peak_death['date'].date()} dengan {peak_death['new_deaths']:,} kematian")

# Tabel data terbaru
with st.expander("📋 Data Terbaru"):
    st.dataframe(filtered_df[['date', 'new_cases', 'new_deaths', 'people_vaccinated', 'people_fully_vaccinated']].tail(20))
