import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

st.set_page_config(page_title="BancaPocket", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"]{font-family:Inter,sans-serif}
.stApp{background:linear-gradient(180deg,#F3F7FF,#F8FAFD)}
#MainMenu,header,footer{visibility:hidden}
.block-container{max-width:620px;padding:14px 12px 90px}
div[data-testid="stTextInput"] label,div[data-testid="stRadio"] label{display:none}
div[data-testid="stTextInput"] input{border:1px solid #D8E2F0;border-radius:15px;min-height:45px}
div[data-testid="stRadio"]>div{background:#EAF0F8;border-radius:15px;padding:4px}
div[data-testid="stRadio"] label{font-size:12px;font-weight:700;border-radius:11px;padding:8px}
.hero{background:linear-gradient(135deg,#0D47A1,#1769E8 58%,#4FA3FF);border-radius:27px;padding:24px 20px;color:white;box-shadow:0 15px 35px #2563eb33;margin-bottom:14px;position:relative;overflow:hidden}
.hero-title{font-size:28px;font-weight:800}.hero-sub{font-size:16px;font-weight:700;margin-top:5px}.hero-desc{font-size:11px;opacity:.88;margin-top:8px}.hero-icon{position:absolute;right:22px;bottom:18px;font-size:52px}
.section{font-size:17px;font-weight:800;color:#102A52;margin:18px 0 9px}
.card{background:#fff;border:1px solid #E0E8F3;border-radius:20px;padding:14px;margin:9px 0;box-shadow:0 7px 22px #0f172a0d}
.logo{width:50px;height:50px;border-radius:15px;background:#F7FAFE;border:1px solid #E3EBF5;display:flex;align-items:center;justify-content:center;font-size:24px}
.name{font-size:14px;font-weight:800;color:#102A52;line-height:1.25}.type{font-size:10px;color:#71819A;margin-top:3px}
.label{font-size:9px;color:#71819A}.value{font-size:13px;font-weight:800;color:#173968;margin-top:2px}
.badge{padding:7px 8px;border-radius:10px;text-align:center;font-size:9px;font-weight:800}.yes{background:#E3F8EE;color:#11945C}.no{background:#FFE7E7;color:#D92D20}
.detail{background:#fff;border:1px solid #E0E8F3;border-radius:22px;padding:17px;box-shadow:0 8px 26px #0f172a0d}
.metric{background:#F8FAFD;border:1px solid #E6EDF6;border-radius:14px;padding:11px;margin-top:8px}
.metric-label{font-size:9px;color:#71819A}.metric-value{font-size:16px;font-weight:800;color:#173968;margin-top:3px}
div.stButton>button{border-radius:13px;border:1px solid #D8E2F0;background:#fff;font-weight:700;min-height:40px}
</style>
""", unsafe_allow_html=True)

DEMO = pd.DataFrame([
["PT Asuransi Jasa Indonesia (Jasindo)","Asuransi Umum",12450,28731,8912,16420,2318,"Yes","Yes","🟦"],
["PT Asuransi Kredit Indonesia (Askrindo)","Asuransi Umum",8321,21115,6784,14250,1987,"Yes","No","🔵"],
["PT Asuransi Umum BRI (BRI Insurance)","Asuransi Umum",6712,18229,5331,11620,1650,"Yes","Yes","🔷"],
["PT Asuransi Sinar Mas","Asuransi Umum",5821,16447,4993,10340,1422,"No","Yes","🔴"],
["PT Asuransi Allianz Utama Indonesia","Asuransi Umum",7104,20339,6120,12910,1820,"Yes","No","🔵"],
["PT Asuransi Jiwa IFG","Asuransi Jiwa",15231,32118,10442,12441,2318,"Yes","Yes","🔴"],
["PT Asuransi Jiwa Manulife Indonesia","Asuransi Jiwa",28114,55219,18772,12441,2318,"Yes","No","🟢"],
],columns=["Nama Asuransi","Jenis Asuransi","Investasi","Aset","Ekuitas","Pendapatan Jasa Asuransi","Laba (Rugi)","PKS Rekanan Perkreditan","PKS Bancassurance","Logo"])

FILE=Path("data/Data Asuransi.xlsx")
if FILE.exists():
    try:
        df=pd.read_excel(FILE)
        df.columns=[str(c).strip() for c in df.columns]
        aliases={"Asuradur":"Nama Asuransi","Jenis":"Jenis Asuransi",
                 "Investasi (Rp Miliar)":"Investasi","Aset (Rp Miliar)":"Aset",
                 "Ekuitas (Rp Miliar)":"Ekuitas",
                 "Pendapatan Jasa Asuransi (Rp Miliar)":"Pendapatan Jasa Asuransi",
                 "Laba (Rugi) (Rp Miliar)":"Laba (Rugi)",
                 "PKS Kredit":"PKS Rekanan Perkreditan"}
        df=df.rename(columns=aliases)
        for c in DEMO.columns:
            if c not in df.columns: df[c]=0 if c in ["Investasi","Aset","Ekuitas","Pendapatan Jasa Asuransi","Laba (Rugi)"] else ""
        for c in ["Investasi","Aset","Ekuitas","Pendapatan Jasa Asuransi","Laba (Rugi)"]:
            df[c]=pd.to_numeric(df[c],errors="coerce").fillna(0)
        if "Logo" not in df.columns: df["Logo"]="🏢"
    except Exception:
        df=DEMO.copy()
else:
    df=DEMO.copy()

def fmt(x):
    return f"{float(x):,.0f}".replace(",",".")

def badge(label,val):
    ok=str(val).strip().lower() in ["yes","ya","y","true"]
    return f"<div><div class='label'>{label}</div><div class='badge {'yes' if ok else 'no'}'>{'Yes' if ok else 'No'}</div></div>"

if "page" not in st.session_state: st.session_state.page="home"
if "selected" not in st.session_state: st.session_state.selected=None

st.markdown("""
<div class="hero">
<div class="hero-title">BancaPocket</div>
<div class="hero-sub">Daftar Perusahaan Asuransi</div>
<div class="hero-desc">Informasi Mitra Asuransi dalam Genggaman Anda</div>
<div class="hero-icon">🛡️</div>
</div>
""",unsafe_allow_html=True)

if st.session_state.page=="detail":
    r=df[df["Nama Asuransi"]==st.session_state.selected]
    if r.empty:
        st.session_state.page="home"; st.rerun()
    r=r.iloc[0]
    if st.button("← Kembali",use_container_width=True):
        st.session_state.page="home"; st.session_state.selected=None; st.rerun()
    st.markdown('<div class="section">Profil Perusahaan</div>',unsafe_allow_html=True)
    st.markdown(f"""<div class="detail"><div style="display:flex;gap:12px;align-items:center">
    <div class="logo">{r["Logo"]}</div><div><div class="name" style="font-size:20px">{r["Nama Asuransi"]}</div>
    <div class="type">{r["Jenis Asuransi"]}</div></div></div></div>""",unsafe_allow_html=True)
    st.markdown('<div class="section">Informasi Keuangan</div>',unsafe_allow_html=True)
    pairs=[("Investasi",r["Investasi"]),("Aset",r["Aset"]),("Ekuitas",r["Ekuitas"]),
           ("Pendapatan Jasa Asuransi",r["Pendapatan Jasa Asuransi"]),("Laba (Rugi)",r["Laba (Rugi)"])]
    for i in range(0,len(pairs),2):
        cols=st.columns(2)
        for j,(label,val) in enumerate(pairs[i:i+2]):
            with cols[j]:
                st.markdown(f'<div class="metric"><div class="metric-label">{label}</div><div class="metric-value">Rp {fmt(val)} Miliar</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section">Status Kerja Sama</div>',unsafe_allow_html=True)
    a,b=st.columns(2)
    with a: st.markdown(f'<div class="metric">{badge("PKS Rekanan Perkreditan",r["PKS Rekanan Perkreditan"])}</div>',unsafe_allow_html=True)
    with b: st.markdown(f'<div class="metric">{badge("PKS Bancassurance",r["PKS Bancassurance"])}</div>',unsafe_allow_html=True)
    st.markdown('<div class="section">Perbandingan Keuangan</div>',unsafe_allow_html=True)
    vals=[r["Investasi"],r["Aset"],r["Ekuitas"],r["Pendapatan Jasa Asuransi"],r["Laba (Rugi)"]]
    fig=go.Figure(go.Bar(x=["Investasi","Aset","Ekuitas","Pendapatan","Laba/Rugi"],y=vals,marker_color="#2563EB"))
    fig.update_layout(height=290,margin=dict(l=5,r=5,t=10,b=5),paper_bgcolor="white",plot_bgcolor="white",xaxis=dict(showgrid=False),yaxis=dict(gridcolor="#EEF2F7",title="Rp Miliar"))
    st.plotly_chart(fig,use_container_width=True)
else:
    cat=st.radio("Kategori",["🏢 Asuransi Umum","❤️ Asuransi Jiwa"],horizontal=True,label_visibility="collapsed")
    typ="Asuransi Umum" if "Umum" in cat else "Asuransi Jiwa"
    search=st.text_input("Cari",placeholder="🔎  Cari nama asuransi...",label_visibility="collapsed")
    result=df[df["Jenis Asuransi"].astype(str).str.contains(typ,case=False,na=False)].copy()
    if search: result=result[result["Nama Asuransi"].astype(str).str.contains(search,case=False,na=False)]
    result=result.sort_values("Nama Asuransi")
    st.markdown(f'<div style="font-size:13px;font-weight:700;color:#415675;margin:10px 2px">Total {len(result)} {typ}</div>',unsafe_allow_html=True)
    for _,r in result.iterrows():
        st.markdown(f"""<div class="card"><div style="display:flex;gap:11px;align-items:flex-start">
        <div class="logo">{r["Logo"]}</div><div style="flex:1"><div class="name">{r["Nama Asuransi"]}</div><div class="type">{r["Jenis Asuransi"]}</div></div><div style="font-size:23px;color:#52709A">›</div></div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1.05fr 1.05fr;gap:6px;margin-top:7px">
        <div><div class="label">Investasi</div><div class="value">{fmt(r["Investasi"])}</div></div>
        <div><div class="label">Aset</div><div class="value">{fmt(r["Aset"])}</div></div>
        <div><div class="label">Ekuitas</div><div class="value">{fmt(r["Ekuitas"])}</div></div>
        {badge("PKS Kredit",r["PKS Rekanan Perkreditan"])}
        {badge("PKS Banca",r["PKS Bancassurance"])}</div></div>""",unsafe_allow_html=True)
        if st.button(f"Lihat Detail • {r['Nama Asuransi']}",key=f"open_{r['Nama Asuransi']}",use_container_width=True):
            st.session_state.selected=r["Nama Asuransi"]; st.session_state.page="detail"; st.rerun()
    if result.empty: st.info("Perusahaan tidak ditemukan.")

st.markdown("<div style='height:20px'></div>",unsafe_allow_html=True)
n1,n2,n3,n4=st.columns(4)
with n1:
    if st.button("⌂\nBeranda",use_container_width=True):
        st.session_state.page="home"; st.rerun()
with n2:
    if st.button("🏢\nAsuransi",use_container_width=True):
        st.session_state.page="home"; st.rerun()
with n3:
    if st.button("▥\nReport",use_container_width=True): st.info("Report akan dikembangkan pada tahap berikutnya.")
with n4:
    if st.button("ⓘ\nInfo",use_container_width=True): st.info("BancaPocket — Insurance Partner Directory.")
