import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(
    page_title="Asuradur Risk Heatmap",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================
# CONFIG
# =========================
THRESHOLD_2026 = 250_000   # Rp juta = Rp250 miliar
THRESHOLD_2028 = 500_000   # Rp juta = Rp500 miliar

SHEETS = {
    "Asuransi Umum": "Asuransi Umum",
    "Asuransi Jiwa": "Asuransi Jiwa",
    "Umum – PKS Bancass": "Umum PKS Bancass",
    "Life – PKS Bancass": "Life PKS Bancass",
}

# =========================
# STYLE – MOBILE LOOK
# =========================
st.markdown("""
<style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}

    .block-container {
        max-width: 1250px;
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
        padding-bottom: 4rem;
    }

    .hero {
        padding: 1.15rem 1.25rem;
        border-radius: 22px;
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 55%, #334155 100%);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 10px 28px rgba(15,23,42,.16);
    }
    .hero-title {
        font-size: 1.65rem;
        font-weight: 800;
        margin: 0;
        letter-spacing: -.03em;
    }
    .hero-subtitle {
        margin-top: .35rem;
        font-size: .88rem;
        color: #cbd5e1;
    }

    .kpi {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 1rem;
        box-shadow: 0 5px 18px rgba(15,23,42,.06);
        min-height: 105px;
    }
    .kpi-label {
        color: #64748b;
        font-size: .76rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: .04em;
    }
    .kpi-value {
        color: #0f172a;
        font-size: 1.65rem;
        font-weight: 800;
        margin-top: .2rem;
    }
    .kpi-note {
        color: #94a3b8;
        font-size: .72rem;
        margin-top: .15rem;
    }

    .risk-card {
        border-radius: 16px;
        padding: .8rem 1rem;
        margin: .35rem 0;
        border: 1px solid #e2e8f0;
        background: #fff;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #0f172a;
        margin: 1.2rem 0 .65rem;
    }

    .legend {
        display:flex;
        flex-wrap:wrap;
        gap:.45rem;
        margin:.3rem 0 .7rem;
    }
    .pill {
        border-radius:999px;
        padding:.32rem .65rem;
        font-size:.72rem;
        font-weight:700;
        border:1px solid #e2e8f0;
        background:#f8fafc;
    }

    .small-muted {
        color:#64748b;
        font-size:.78rem;
    }

    @media (max-width: 700px) {
        .block-container {
            padding: .65rem .55rem 3rem;
        }
        .hero-title { font-size: 1.35rem; }
        .kpi-value { font-size: 1.35rem; }
        div[data-testid="stHorizontalBlock"] {
            gap: .45rem;
        }
        .section-title { margin-top: .9rem; }
    }
</style>
""", unsafe_allow_html=True)

# =========================
# HELPERS
# =========================
def rupiah_miliar(x):
    if pd.isna(x):
        return "-"
    return f"Rp {x/1000:,.1f} M"

def rupiah_triliun(x):
    if pd.isna(x):
        return "-"
    return f"Rp {x/1_000_000:,.2f} T"

def yes(v):
    return str(v).strip().lower() in {"yes", "ya", "true", "1"}

def clean_main_sheet(raw):
    # File sumber memiliki 3 baris header/metadata sebelum header sebenarnya.
    df = pd.read_excel(raw, header=2)

    # Hapus kolom kosong total
    df = df.dropna(axis=1, how="all").copy()

    # Normalisasi nama kolom
    df.columns = [str(c).strip() for c in df.columns]

    if "Asuradur" not in df.columns:
        return pd.DataFrame()

    # Baris yang bukan perusahaan: header kategori dan baris nomor kolom.
    df["Asuradur"] = df["Asuradur"].astype("string").str.strip()
    df["No"] = pd.to_numeric(df["No"], errors="coerce")

    # Perusahaan harus punya nama dan nilai Modal Sendiri numerik.
    df["Modal Sendiri"] = pd.to_numeric(df["Modal Sendiri"], errors="coerce")
    df = df[df["Asuradur"].notna() & df["Modal Sendiri"].notna()].copy()

    # Pastikan angka numerik
    for c in ["Investasi", "Aset", "Pendapatan Jasa Asuransi",
              "Laba (Rugi) Setelah Pajak", "Ekuitas"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # Risk capital classification
    df["Status 2026"] = np.where(
        df["Modal Sendiri"] >= THRESHOLD_2026, "MEMENUHI", "AT RISK"
    )
    df["Status 2028"] = np.where(
        df["Modal Sendiri"] >= THRESHOLD_2028, "MEMENUHI", "AT RISK"
    )

    def capital_risk(row):
        cap = row["Modal Sendiri"]
        if cap < THRESHOLD_2026:
            return "CRITICAL"
        elif cap < THRESHOLD_2028:
            return "WATCHLIST"
        return "LOW RISK"

    df["Capital Risk"] = df.apply(capital_risk, axis=1)

    # Gap to thresholds
    df["Gap 2026 (Rp juta)"] = (THRESHOLD_2026 - df["Modal Sendiri"]).clip(lower=0)
    df["Gap 2028 (Rp juta)"] = (THRESHOLD_2028 - df["Modal Sendiri"]).clip(lower=0)

    # Combined flag hanya untuk screening, bukan pengganti assessment risiko resmi.
    extra = []
    for _, r in df.iterrows():
        flags = []
        if r["Capital Risk"] == "CRITICAL":
            flags.append("Modal < 250 M")
        elif r["Capital Risk"] == "WATCHLIST":
            flags.append("Modal < 500 M")
        if "Market At Risk" in df.columns and yes(r["Market At Risk"]):
            flags.append("Market At Risk")
        if "Bank At Risk" in df.columns and yes(r["Bank At Risk"]):
            flags.append("Bank At Risk")
        extra.append(flags)
    df["Risk Flags"] = extra

    return df.reset_index(drop=True)

def clean_pks_sheet(raw):
    df = pd.read_excel(raw)
    df.columns = [str(c).strip() for c in df.columns]
    if "Asuradur" not in df.columns:
        return pd.DataFrame()

    df["Asuradur"] = df["Asuradur"].astype("string").str.strip()
    df["Modal Sendiri"] = pd.to_numeric(df.get("Modal Sendiri"), errors="coerce")
    df = df[df["Asuradur"].notna() & df["Modal Sendiri"].notna()].copy()

    df["Status 2026"] = np.where(df["Modal Sendiri"] >= THRESHOLD_2026, "MEMENUHI", "AT RISK")
    df["Status 2028"] = np.where(df["Modal Sendiri"] >= THRESHOLD_2028, "MEMENUHI", "AT RISK")
    df["Capital Risk"] = np.select(
        [
            df["Modal Sendiri"] < THRESHOLD_2026,
            df["Modal Sendiri"] < THRESHOLD_2028,
        ],
        ["CRITICAL", "WATCHLIST"],
        default="LOW RISK",
    )
    return df.reset_index(drop=True)

def prepare_all(uploaded_file):
    result = {}
    for key, sheet in SHEETS.items():
        try:
            if sheet in ["Asuransi Umum", "Asuransi Jiwa"]:
                result[key] = clean_main_sheet(uploaded_file)
            else:
                result[key] = clean_pks_sheet(uploaded_file)
        except Exception as e:
            result[key] = pd.DataFrame()
    return result

# =========================
# DATA SOURCE
# =========================
st.markdown("""
<div class="hero">
    <div class="hero-title">🛡️ Asuradur Risk Heatmap</div>
    <div class="hero-subtitle">
        Mapping kecukupan modal asuradur terhadap minimum Rp250 miliar
        per Desember 2026 dan Rp500 miliar per Desember 2028.
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Filter & Data")
    uploaded = st.file_uploader(
        "Upload Excel sumber",
        type=["xlsx", "xls"],
        help="Upload file universe asuradur dengan struktur sheet yang sama."
    )
    st.caption("Jika tidak upload, aplikasi menggunakan file sumber yang diletakkan di folder aplikasi.")

# Local fallback
if uploaded is None:
    local_candidates = [
        "2026 - Universe Asuradur At Risk 1.xlsx",
        "Universe Asuradur At Risk 1.xlsx",
    ]
    local_file = next((f for f in local_candidates if __import__("os").path.exists(f)), None)
    if local_file:
        source = local_file
    else:
        st.info("Silakan upload file Excel pada sidebar.")
        st.stop()
else:
    source = uploaded

data = prepare_all(source)

# =========================
# GLOBAL FILTERS
# =========================
available_types = [k for k,v in data.items() if not v.empty]
if not available_types:
    st.error("Tidak ada data perusahaan yang berhasil dibaca dari file.")
    st.stop()

c1, c2, c3 = st.columns([1.1, 1.1, 1.6])
with c1:
    selected_type = st.selectbox("Jenis", available_types)
with c2:
    risk_filter = st.selectbox(
        "Capital Risk",
        ["Semua", "CRITICAL", "WATCHLIST", "LOW RISK"]
    )
with c3:
    search = st.text_input("🔎 Cari asuradur", placeholder="Nama perusahaan...")

df = data[selected_type].copy()

if risk_filter != "Semua":
    df = df[df["Capital Risk"] == risk_filter]

if search:
    df = df[df["Asuradur"].str.contains(search, case=False, na=False)]

# =========================
# KPI
# =========================
total = len(df)
critical = int((df["Capital Risk"] == "CRITICAL").sum())
watch = int((df["Capital Risk"] == "WATCHLIST").sum())
low = int((df["Capital Risk"] == "LOW RISK").sum())
avg_cap = df["Modal Sendiri"].mean() if total else np.nan

k1, k2, k3, k4 = st.columns(4)
k1.markdown(f"""<div class="kpi"><div class="kpi-label">Asuradur</div>
<div class="kpi-value">{total}</div><div class="kpi-note">hasil filter</div></div>""", unsafe_allow_html=True)
k2.markdown(f"""<div class="kpi"><div class="kpi-label">Critical</div>
<div class="kpi-value">{critical}</div><div class="kpi-note">modal &lt; Rp250 M</div></div>""", unsafe_allow_html=True)
k3.markdown(f"""<div class="kpi"><div class="kpi-label">Watchlist</div>
<div class="kpi-value">{watch}</div><div class="kpi-note">Rp250–&lt;500 M</div></div>""", unsafe_allow_html=True)
k4.markdown(f"""<div class="kpi"><div class="kpi-label">Avg. Modal</div>
<div class="kpi-value">{rupiah_miliar(avg_cap)}</div><div class="kpi-note">Rp juta pada sumber</div></div>""", unsafe_allow_html=True)

# =========================
# RISK LEGEND
# =========================
st.markdown('<div class="section-title">🎯 Risk Mapping</div>', unsafe_allow_html=True)
st.markdown("""
<div class="legend">
  <span class="pill">🔴 CRITICAL: Modal &lt; Rp250 M</span>
  <span class="pill">🟠 WATCHLIST: Rp250 M – &lt; Rp500 M</span>
  <span class="pill">🟢 LOW RISK: Modal ≥ Rp500 M</span>
</div>
""", unsafe_allow_html=True)

# =========================
# HEATMAP / SCATTER
# =========================
if not df.empty:
    plot_df = df.copy()
    plot_df["Modal (Rp Miliar)"] = plot_df["Modal Sendiri"] / 1000

    # Sort for stable vertical mapping
    plot_df = plot_df.sort_values("Modal Sendiri", ascending=True).reset_index(drop=True)
    plot_df["Rank"] = np.arange(1, len(plot_df) + 1)

    fig = px.scatter(
        plot_df,
        x="Modal (Rp Miliar)",
        y="Rank",
        color="Capital Risk",
        size="Modal (Rp Miliar)",
        hover_name="Asuradur",
        hover_data={
            "Modal (Rp Miliar)": ":,.1f",
            "Rank": False,
            "Capital Risk": True,
            "Status 2026": True,
            "Status 2028": True,
        },
        category_orders={
            "Capital Risk": ["CRITICAL", "WATCHLIST", "LOW RISK"]
        },
        height=max(430, min(760, 260 + len(plot_df)*7)),
    )

    # Threshold lines
    fig.add_vline(
        x=250, line_width=2, line_dash="dash",
        annotation_text="Rp250 M – batas 2026",
        annotation_position="top"
    )
    fig.add_vline(
        x=500, line_width=2, line_dash="dash",
        annotation_text="Rp500 M – batas 2028",
        annotation_position="top"
    )

    fig.update_layout(
        template="plotly_white",
        margin=dict(l=10,r=10,t=45,b=10),
        xaxis_title="Modal Sendiri (Rp Miliar)",
        yaxis_title="Urutan Asuradur berdasarkan modal",
        legend_title="Capital Risk",
        hoverlabel=dict(font_size=12),
    )
    fig.update_yaxes(showticklabels=False)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # =========================
    # RISK MATRIX
    # =========================
    st.markdown('<div class="section-title">🧭 Compliance Matrix</div>', unsafe_allow_html=True)
    matrix = pd.crosstab(df["Status 2026"], df["Status 2028"])
    matrix = matrix.reindex(
        index=["AT RISK", "MEMENUHI"],
        columns=["AT RISK", "MEMENUHI"],
        fill_value=0
    )

    fig2 = go.Figure(data=go.Heatmap(
        z=matrix.values,
        x=["2028: AT RISK", "2028: MEMENUHI"],
        y=["2026: AT RISK", "2026: MEMENUHI"],
        text=matrix.values,
        texttemplate="%{text}",
        hovertemplate="2026=%{y}<br>2028=%{x}<br>Jumlah=%{z}<extra></extra>",
        showscale=False,
    ))
    fig2.update_layout(
        height=320,
        margin=dict(l=10,r=10,t=10,b=10),
        xaxis_title="Target Desember 2028",
        yaxis_title="Target Desember 2026",
    )
    st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # =========================
    # TOP AT RISK
    # =========================
    at_risk = df[df["Capital Risk"].isin(["CRITICAL", "WATCHLIST"])].copy()
    if not at_risk.empty:
        st.markdown('<div class="section-title">🚨 Priority Watchlist</div>', unsafe_allow_html=True)

        show_cols = [
            "Asuradur", "Modal Sendiri", "Status 2026", "Status 2028",
            "Capital Risk", "Gap 2026 (Rp juta)", "Gap 2028 (Rp juta)"
        ]
        show_cols = [c for c in show_cols if c in at_risk.columns]
        display_df = at_risk[show_cols].copy()

        display_df["Modal"] = display_df["Modal Sendiri"].map(rupiah_miliar)
        display_df["Gap 2026"] = display_df["Gap 2026 (Rp juta)"].map(rupiah_miliar)
        display_df["Gap 2028"] = display_df["Gap 2028 (Rp juta)"].map(rupiah_miliar)

        display_df = display_df[
            ["Asuradur", "Modal", "Capital Risk", "Status 2026", "Status 2028",
             "Gap 2026", "Gap 2028"]
        ]
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # =========================
    # DETAIL
    # =========================
    st.markdown('<div class="section-title">📋 Detail Asuradur</div>', unsafe_allow_html=True)

    detail_cols = [
        "Asuradur", "Modal Sendiri", "Investasi", "Aset",
        "Pendapatan Jasa Asuransi", "Laba (Rugi) Setelah Pajak",
        "Predikat Infobank", "PKS Rekanan (PCP)", "Status 2026",
        "Status 2028", "Capital Risk", "Market At Risk",
        "Bank At Risk", "PKS Bancassurance (DSG)", "Keterangan"
    ]
    detail_cols = [c for c in detail_cols if c in df.columns]
    detail = df[detail_cols].copy()

    for c in ["Modal Sendiri", "Investasi", "Aset", "Pendapatan Jasa Asuransi",
              "Laba (Rugi) Setelah Pajak"]:
        if c in detail.columns:
            detail[c] = detail[c].map(rupiah_miliar)

    st.dataframe(
        detail,
        use_container_width=True,
        hide_index=True,
        height=470,
    )

    # =========================
    # DOWNLOAD
    # =========================
    export = df.copy()
    export["Modal Sendiri (Rp Miliar)"] = export["Modal Sendiri"] / 1000
    export["Gap 2026 (Rp Miliar)"] = export["Gap 2026 (Rp juta)"] / 1000
    export["Gap 2028 (Rp Miliar)"] = export["Gap 2028 (Rp juta)"] / 1000

    csv = export.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ Download hasil mapping CSV",
        data=csv,
        file_name="asuradur_risk_heatmap.csv",
        mime="text/csv",
        use_container_width=True,
    )

else:
    st.warning("Tidak ada asuradur yang sesuai filter.")

# =========================
# FOOTNOTE
# =========================
st.caption(
    "Sumber data: file Excel yang di-upload pengguna. Nilai modal pada sumber menggunakan "
    "satuan Rp juta. Klasifikasi CRITICAL/WATCHLIST/LOW RISK adalah screening berbasis "
    "threshold modal dan bukan penilaian risiko resmi/regulator."
)
