import streamlit as st

st.set_page_config(
    page_title="Konsultasi Keuangan",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Aplikasi Konsultasi Keuangan")
st.write("Masukkan data keuangan Anda untuk mendapatkan analisis sederhana.")

# Input
pendapatan = st.number_input(
    "Pendapatan Bulanan (Rp)",
    min_value=0.0,
    step=100000.0
)

pengeluaran = st.number_input(
    "Pengeluaran Bulanan (Rp)",
    min_value=0.0,
    step=100000.0
)

if st.button("Analisa Keuangan"):

    sisa_dana = pendapatan - pengeluaran

    if pendapatan > 0:
        rasio_tabungan = (sisa_dana / pendapatan) * 100
    else:
        rasio_tabungan = 0

    st.subheader("📊 Hasil Analisa")

    st.metric(
        label="Sisa Dana",
        value=f"Rp {sisa_dana:,.0f}"
    )

    st.metric(
        label="Persentase Sisa Dana",
        value=f"{rasio_tabungan:.1f}%"
    )

    st.markdown("---")

    if sisa_dana < 0:
        st.error(
            "Pengeluaran Anda melebihi pendapatan. "
            "Prioritaskan pengurangan pengeluaran tidak penting."
        )

    elif rasio_tabungan < 10:
        st.warning(
            "Kondisi cukup ketat. Disarankan menabung minimal 10%-20% dari pendapatan."
        )

    elif rasio_tabungan < 30:
        st.success(
            "Keuangan Anda cukup sehat. Mulailah membangun dana darurat dan investasi."
        )

    else:
        st.success(
            "Kondisi keuangan sangat baik. "
            "Pertimbangkan investasi jangka panjang dan diversifikasi aset."
        )

    # Financial Health Score
    score = min(max(rasio_tabungan * 2.5, 0), 100)

    st.markdown("---")
    st.subheader("🏆 Financial Health Score")

    st.progress(int(score))
    st.write(f"Skor Keuangan: **{score:.0f}/100**")

    if score < 40:
        kategori = "Perlu Perbaikan"
    elif score < 70:
        kategori = "Cukup Baik"
    else:
        kategori = "Sangat Sehat"

    st.write(f"Kategori: **{kategori}**")

    # Rekomendasi
    st.markdown("---")
    st.subheader("💡 Rekomendasi")

    dana_darurat = pengeluaran * 6

    st.write(
        f"Target Dana Darurat: **Rp {dana_darurat:,.0f}** "
        "(6 bulan pengeluaran)"
    )

    investasi = pendapatan * 0.2

    st.write(
        f"Rekomendasi Investasi Bulanan: "
        f"**Rp {investasi:,.0f}** (20% pendapatan)"
    )

st.markdown("---")
st.caption("Versi 1.0 - Konsultasi Keuangan Sederhana")
