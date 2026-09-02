import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import io

# Config Halaman Streamlit
st.set_page_config(
    page_title="Executive Report - Universe Asuradur At Risk 2026",
    page_icon="📑",
    layout="wide"
)

# Fungsi untuk membaca dan mengolah data dari file Excel lokal
@st.cache_data
def load_and_process_data(file_path):
    # Membaca Sheet Asuransi Umum & Jiwa
    df_umum = pd.read_excel(file_path, sheet_name='Asuransi Umum', header=1)
    df_jiwa = pd.read_excel(file_path, sheet_name='Asuransi Jiwa', header=1)
    
    # Filter baris valid
    df_umum = df_umum.dropna(subset=['Asuradur']).copy()
    df_jiwa = df_jiwa.dropna(subset=['Asuradur']).copy()

    # Tambahkan Label Jenis Asuransi
    df_umum['Kategori'] = 'Asuransi Umum'
    df_jiwa['Kategori'] = 'Asuransi Jiwa'

    # Gabungkan Data
    df_all = pd.concat([df_umum, df_jiwa], ignore_index=True)

    # Clean & Convert Kolom Numerik (dalam Rp Juta)
    num_cols = ['Investasi', 'Aset', 'Modal Sendiri', 'Pendapatan Jasa Asuransi', 'Laba (Rugi) Setelah Pajak', 'Ekuitas']
    for col in num_cols:
        if col in df_all.columns:
            df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)

    return df_all

FILE_PATH = '2026 - Universe Asuradur At Risk 1.xlsx'

# Load Data
try:
    df = load_and_process_data(FILE_PATH)
except Exception as e:
    st.error(f"❌ Gagal membaca file `{FILE_PATH}`. Pastikan file tersimpan di direktori yang sama dengan `app.py`. Error: {e}")
    st.stop()

# --- SIDEBAR FILTER ---
st.sidebar.header("🎯 Filter Laporan")

kategori_selected = st.sidebar.multiselect(
    "Kategori Asuransi",
    options=df['Kategori'].unique(),
    default=df['Kategori'].unique()
)

predikat_options = [x for x in df['Predikat Infobank'].dropna().unique() if str(x).strip() != '']
predikat_selected = st.sidebar.multiselect(
    "Predikat Infobank",
    options=predikat_options,
    default=predikat_options
)

# Apply Filter
df_filtered = df[
    (df['Kategori'].isin(kategori_selected)) &
    (df['Predikat Infobank'].isin(predikat_selected))
].copy()

# --- MAIN DASHBOARD / REPORT ---
st.title("📑 Executive Report: Universe Asuradur At Risk 2026")
st.markdown("*Laporan Analisis Kinerja Keuangan & Pemetaan Risiko Portofolio Perusahaan Asuransi Rekanan*")
st.markdown("---")

# 1. SUMMARY METRICS
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.metric("Total Asuradur", f"{len(df_filtered)} Perusahaan")
with m2:
    st.metric("Total Aset", f"Rp {df_filtered['Aset'].sum() / 1e6:,.2f} T")
with m3:
    st.metric("Total Investasi", f"Rp {df_filtered['Investasi'].sum() / 1e6:,.2f} T")
with m4:
    st.metric("Total Ekuitas", f"Rp {df_filtered['Ekuitas'].sum() / 1e6:,.2f} T")
with m5:
    total_laba = df_filtered['Laba (Rugi) Setelah Pajak'].sum() / 1e3
    st.metric("Total Laba Bersih", f"Rp {total_laba:,.2f} M")

st.markdown("---")

# 2. VISUALISASI UTAMA
col_left, col_right = st.columns([6, 4])

with col_left:
    st.subheader("🏆 Top 10 Asuradur Berdasarkan Aset")
    top_10 = df_filtered.sort_values(by='Aset', ascending=False).head(10)
    fig_bar = px.bar(
        top_10,
        x='Aset',
        y='Asuradur',
        color='Kategori',
        orientation='h',
        labels={'Aset': 'Aset (Rp Juta)', 'Asuradur': ''},
        color_discrete_map={'Asuransi Umum': '#1f77b4', 'Asuransi Jiwa': '#2ca02c'}
    )
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("📊 Distribusi Predikat Infobank")
    fig_pie = px.pie(
        df_filtered,
        names='Predikat Infobank',
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("---")

# 3. ANALISIS PEMETAAN RISIKO & PERMIT KETENTUAN EKUITAS
st.subheader("⚠️ Profil & Pemetaan Risiko")
r1, r2, r3 = st.columns(3)

with r1:
    st.markdown("#### Market At Risk")
    if 'Market At Risk' in df_filtered.columns:
        df_mar = df_filtered['Market At Risk'].value_counts().reset_index()
        df_mar.columns = ['Status Market Risk', 'Jumlah']
        st.dataframe(df_mar, hide_index=True, use_container_width=True)

with r2:
    st.markdown("#### Bank At Risk")
    if 'Bank At Risk' in df_filtered.columns:
        df_bar = df_filtered['Bank At Risk'].value_counts().reset_index()
        df_bar.columns = ['Status Bank Risk', 'Jumlah']
        st.dataframe(df_bar, hide_index=True, use_container_width=True)

with r3:
    st.markdown("#### Kepatuhan Ekuitas (Min. 250 M / Des 26)")
    if 'Min. 250 M/ 31 Des-26' in df_filtered.columns:
        df_eq = df_filtered['Min. 250 M/ 31 Des-26'].value_counts().reset_index()
        df_eq.columns = ['Status Memenuhi', 'Jumlah']
        st.dataframe(df_eq, hide_index=True, use_container_width=True)

st.markdown("---")

# 4. TABEL DETIL DATA & EXPORT
st.subheader("📋 Tabel Detail Report Asuradur")

# Kolom utama yang ditampilkan
display_cols = [
    'No', 'Asuradur', 'Kategori', 'Aset', 'Investasi', 'Ekuitas', 
    'Pendapatan Jasa Asuransi', 'Laba (Rugi) Setelah Pajak', 
    'Predikat Infobank', 'Market At Risk', 'Bank At Risk'
]
available_cols = [c for c in display_cols if c in df_filtered.columns]

st.dataframe(
    df_filtered[available_cols].sort_values(by='Aset', ascending=False),
    use_container_width=True,
    hide_index=True
)

# Export Data Terfilter
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    df_filtered.to_excel(writer, sheet_name='Executive_Report', index=False)

st.download_button(
    label="📥 Download Executive Report (Excel)",
    data=buffer.getvalue(),
    file_name="Executive_Report_Asuradur_At_Risk_2026.xlsx",
    mime="application/vnd.ms-excel"
)
