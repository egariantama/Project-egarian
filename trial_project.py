import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Setup Halaman Streamlit
st.set_page_config(
    page_title="Dashboard Universe Asuradur At Risk",
    page_icon="📊",
    layout="wide"
)

# Fungsi membaca dan mengolah data Excel
@st.cache_data
def load_data(file_path):
    # Membaca sheet Asuransi Umum & Jiwa
    df_umum = pd.read_excel(file_path, sheet_name='Asuransi Umum', header=1)
    df_jiwa = pd.read_excel(file_path, sheet_name='Asuransi Jiwa', header=1)
    
    # Menghapus baris kosong / footer yang tidak valid
    df_umum = df_umum.dropna(subset=['Asuradur']).copy()
    df_jiwa = df_jiwa.dropna(subset=['Asuradur']).copy()

    # Tambahkan penanda jenis asuransi
    df_umum['Jenis'] = 'Asuransi Umum'
    df_jiwa['Jenis'] = 'Asuransi Jiwa'

    # Konversi kolom numerik
    num_cols = ['Investasi', 'Aset', 'Modal Sendiri', 'Pendapatan Jasa Asuransi', 'Laba (Rugi) Setelah Pajak', 'Ekuitas']
    for col in num_cols:
        if col in df_umum.columns:
            df_umum[col] = pd.to_numeric(df_umum[col], errors='coerce').fillna(0)
        if col in df_jiwa.columns:
            df_jiwa[col] = pd.to_numeric(df_jiwa[col], errors='coerce').fillna(0)

    return df_umum, df_jiwa

# File Path
FILE_PATH = '2026 - Universe Asuradur At Risk 1.xlsx'

try:
    df_umum, df_jiwa = load_data(FILE_PATH)
    df_all = pd.concat([df_umum, df_jiwa], ignore_index=True)
except Exception as e:
    st.error(f"Gagal memuat file Excel. Pastikan file '{FILE_PATH}' berada di direktori yang sama. Error: {e}")
    st.stop()

# --- SIDEBAR: FILTER ---
st.sidebar.title("🔍 Filter Data")
selected_jenis = st.sidebar.multiselect(
    "Pilih Kategori Asuransi:",
    options=['Asuransi Umum', 'Asuransi Jiwa'],
    default=['Asuransi Umum', 'Asuransi Jiwa']
)

selected_predikat = st.sidebar.multiselect(
    "Predikat Infobank:",
    options=df_all['Predikat Infobank'].dropna().unique(),
    default=df_all['Predikat Infobank'].dropna().unique()
)

# Apply Filter
df_filtered = df_all[
    (df_all['Jenis'].isin(selected_jenis)) & 
    (df_all['Predikat Infobank'].isin(selected_predikat))
]

# --- MAIN PAGE: HEADER ---
st.title("📊 Executive Report: Universe Asuradur At Risk")
st.markdown("Dashboard analisis kinerjadan pemetaan risiko portofolio perusahaan asuransi rekanan.")
st.markdown("---")

# --- METRIC CARDS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Perusahaan", len(df_filtered))
with col2:
    total_aset = df_filtered['Aset'].sum() / 1e6
    st.metric("Total Aset", f"Rp {total_aset:,.2f} T")
with col3:
    total_investasi = df_filtered['Investasi'].sum() / 1e6
    st.metric("Total Investasi", f"Rp {total_investasi:,.2f} T")
with col4:
    total_laba = df_filtered['Laba (Rugi) Setelah Pajak'].sum() / 1e6
    st.metric("Total Laba (Rugi)", f"Rp {total_laba:,.2f} T")

st.markdown("---")

# --- TABEL LAYOUT ANALISIS ---
tab1, tab2, tab3 = st.tabs(["📈 Analisis Keuangan", "⚠️ Pemetaan Risiko", "📋 Raw Data"])

with tab1:
    st.subheader("Top 10 Perusahaan Asuransi Berdasarkan Aset")
    top_aset = df_filtered.sort_values(by='Aset', ascending=False).head(10)
    fig_aset = px.bar(
        top_aset, 
        x='Aset', 
        y='Asuradur', 
        color='Jenis',
        orientation='h',
        title="10 Perusahaan dengan Aset Terbesar (Dalam Juta Rp)",
        text_auto='.2s'
    )
    fig_aset.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_aset, use_container_width=True)

    col_chart1, col_chart2 = st.columns(2)
    with col_chart1:
        st.subheader("Distribus Predikat Infobank")
        fig_predikat = px.pie(
            df_filtered, 
            names='Predikat Infobank', 
            hole=0.4,
            title="Sebaran Predikat Perusahaan"
        )
        st.plotly_chart(fig_predikat, use_container_width=True)

    with col_chart2:
        st.subheader("Aset vs Pendapatan Jasa Asuransi")
        fig_scatter = px.scatter(
            df_filtered, 
            x='Aset', 
            y='Pendapatan Jasa Asuransi',
            color='Jenis',
            hover_name='Asuradur',
            size='Modal Sendiri',
            title="Korelasi Aset dan Pendapatan Jasa Asuransi"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

with tab2:
    st.subheader("Profil & Pemetaan Risiko Perusahaan")
    col_risk1, col_risk2 = st.columns(2)
    
    with col_risk1:
        if 'Market At Risk' in df_filtered.columns:
            st.markdown("**Market At Risk**")
            market_risk_counts = df_filtered['Market At Risk'].value_counts().reset_index()
            market_risk_counts.columns = ['Status', 'Jumlah']
            st.dataframe(market_risk_counts, use_container_width=True)

    with col_risk2:
        if 'Bank At Risk' in df_filtered.columns:
            st.markdown("**Bank At Risk**")
            bank_risk_counts = df_filtered['Bank At Risk'].value_counts().reset_index()
            bank_risk_counts.columns = ['Status', 'Jumlah']
            st.dataframe(bank_risk_counts, use_container_width=True)

with tab3:
    st.subheader("Data Lengkap Perusahaan")
    st.dataframe(df_filtered, use_container_width=True)
    
    # Download Button
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        df_filtered.to_excel(writer, sheet_name='Filtered_Data', index=False)
    
    st.download_button(
        label="📥 Download Data Terfilter (Excel)",
        data=buffer.getvalue(),
        file_name="Report_Universe_Asuradur_Filtered.xlsx",
        mime="application/vnd.ms-excel"
    )
