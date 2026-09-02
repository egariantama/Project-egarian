import streamlit as st
import pandas as pd

# Konfigurasi Halaman & Meta Mobile Viewport
st.set_page_config(
    page_title="Direktori Rekanan Asuransi",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Kustomisasi CSS untuk Desain Mewah & Mobile-First Experience
st.markdown("""
    <style>
    /* Styling Dasar & Background */
    .main {
        background-color: #0F172A;
        color: #F8FAFC;
    }
    
    /* Custom Header/Banner */
    .lux-header {
        background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
    }
    .lux-header h1 {
        color: #F8FAFC;
        font-size: 22px;
        font-weight: 700;
        margin-bottom: 6px;
        letter-spacing: 0.5px;
    }
    .lux-header p {
        color: #94A3B8;
        font-size: 13px;
        margin: 0;
    }

    /* Badge Kualifikasi Header */
    .qual-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
    }
    .badge-a { background: rgba(59, 130, 246, 0.2); color: #60A5FA; border: 1px solid #3B82F6; }
    .badge-b { background: rgba(245, 158, 11, 0.2); color: #FBBF24; border: 1px solid #F59E0B; }
    .badge-c { background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #10B981; }

    /* Card Rekanan Asuransi */
    .lux-card {
        background: #1E293B;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    }
    .card-a { border-left: 4px solid #3B82F6; }
    .card-b { border-left: 4px solid #F59E0B; }
    .card-c { border-left: 4px solid #10B981; }

    .lux-title {
        color: #38BDF8;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 8px;
        line-height: 1.4;
    }
    .lux-info {
        font-size: 13px;
        color: #CBD5E1;
        margin-bottom: 6px;
        line-height: 1.5;
    }
    .lux-label {
        color: #94A3B8;
        font-weight: 600;
    }

    /* Badges untuk PIC & Kontak */
    .pic-tag {
        display: inline-block;
        background: #0F172A;
        border: 1px solid #475569;
        color: #E2E8F0;
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 12px;
        margin-right: 4px;
        margin-top: 4px;
    }
    .phone-tag {
        display: inline-block;
        background: rgba(59, 130, 246, 0.15);
        color: #60A5FA;
        border-radius: 6px;
        padding: 4px 8px;
        font-size: 12px;
        font-weight: 600;
        margin-right: 6px;
        margin-top: 6px;
        text-decoration: none;
    }

    /* Custom Filter Buttons Styling */
    div.stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 42px;
        font-weight: 600;
        font-size: 12px;
    }

    /* Sembunyikan elemen bawaan Streamlit yang mengganggu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Data Rekanan Berdasarkan Lampiran Dokumen
@st.cache_data
def get_insurance_data():
    return [
        # Gambar 1 - Kualifikasi A
        {"kualifikasi": "A", "no": 1, "nama": "PT ASURANSI ASTRA BUANA", "alamat": "Grha Asuransi Astra, Jalan TB Simatupang Kavling 15, Lebak Bulus, Cilandak, Jakarta 12440", "pic": "Ary Adrian, Reva Gauzi, Budi Santoso", "hp": "0811934001, 081366641206, 081383531133", "telp": "021-75900800"},
        {"kualifikasi": "A", "no": 2, "nama": "PT ASURANSI BINA DANA ARTA TBK", "alamat": "Plaza Asia 27th Floor Jl. Jend. Sudirman Kav.59 Jakarta 12190", "pic": "Eko Setiawan", "hp": "082298261222", "telp": "021-51401688"},
        {"kualifikasi": "A", "no": 3, "nama": "PT ASURANSI CENTRAL ASIA", "alamat": "Wisma Asia Lt. 10, Kav. 12-15 Jl. Letjen S. Parman Kav. 79 Jakarta 11420", "pic": "Tita Kania, Windiarto Husodo", "hp": "0818747518, 08129380502", "telp": "021-56998288 / 021-56998222"},
        {"kualifikasi": "A", "no": 4, "nama": "PT ASURANSI JASARAHARJA PUTERA", "alamat": "Wisma Raharja, JL.TB.Simatupang kav.1, Cilandak Timur, Jakarta Selatan 12560", "pic": "Nauva Marin, Yafizam Lanry Bahran, Muchammad Syafrudin", "hp": "08129550286, 085266708294, 085921517235", "telp": "021-78844444"},
        {"kualifikasi": "A", "no": 5, "nama": "PT ASURANSI MULTI ARTHA GUNA TBK", "alamat": "The City Center Batavia Tower One Lt.17 Jl. KH. Mas Mansyur Kav.126 Jakarta Pusat 10220", "pic": "Prakash Rajamanickam", "hp": "08118628541", "telp": "021-2700590"},
        {"kualifikasi": "A", "no": 6, "nama": "PT ASURANSI SINAR MAS", "alamat": "Plasa Simas Jl. Fachrudin No.18, Jakarta Pusat 10250", "pic": "Cynthia Agustina", "hp": "082211808880", "telp": "021-3902141"},
        {"kualifikasi": "A", "no": 7, "nama": "PT ASURANSI TRI PAKARTA", "alamat": "Jl. Falatehan I No.17-19, Kebayoran Baru, Kota Adm. Jakarta Selatan, DKI Jakarta 12160", "pic": "Ardana Reswari", "hp": "082225901212", "telp": "021-39502300"},
        {"kualifikasi": "A", "no": 8, "nama": "PT ASURANSI TUGU PRATAMA INDONESIA TBK", "alamat": "Wisma Tugu I, Jl. H.R. Rasuna Said, Kav C 8-9 Jakarta 12920", "pic": "Murdianto Musafa, Rully Hendra Wijaya", "hp": "081213352323, 081288687800", "telp": "021-52961777"},
        {"kualifikasi": "A", "no": 9, "nama": "PT ASURANSI WAHANA TATA", "alamat": "Gd. Asuransi Wahana Tata Jl. HR Rasuna Said Kav. C4 Jakarta Selatan 12920", "pic": "Yayuk Rahayu", "hp": "08129278769", "telp": "021-5203145"},
        {"kualifikasi": "A", "no": 10, "nama": "PT BRI ASURANSI INDONESIA (dh. PT ASURANSI BRINGIN SEJAHTERA ARTAMAKMUR)", "alamat": "Graha BRI Insurance Jl. Mampang Prapatan Raya No. 18 Jakarta Selatan - 12790", "pic": "Adit Sulistiyo Pratama, Fadjar Indra, Slamet Pambudi, Abdul Syakur", "hp": "087681511471, 08111122424, 081213033323, 081315529293", "telp": "021-79170477 / 021-79170478"},
        {"kualifikasi": "A", "no": 11, "nama": "PT LIPPO GENERAL INSURANCE TBK", "alamat": "Karawaci Office Park Blok I No.30-35 Karawaci, Tangerang 15139", "pic": "Leviano Winoto", "hp": "08179971972", "telp": "021-55790672"},
        {"kualifikasi": "A", "no": 12, "nama": "PT ZURICH ASURANSI INDONESIA TBK (D/H PT ASURANSI ADIRA DINAMIKA TBK)", "alamat": "Graha Zurich, Jl. MT. Haryono Kav. 42 Jakarta Selatan 12770", "pic": "Rudy Paulus", "hp": "081299886728", "telp": "021-29667373"},
        
        # Gambar 2 - Kualifikasi B
        {"kualifikasi": "B", "no": 1, "nama": "PT ASURANSI BINAGRIYA UPAKARA", "alamat": "Jl. Kesehatan No. 56-58 Tanah Abang, Jakarta 10160", "pic": "Arief H. Rachman, Gunadi", "hp": "0818485966, 08978781247", "telp": "021-34830348"},
        {"kualifikasi": "B", "no": 2, "nama": "PT ASURANSI BUANA INDEPENDENT", "alamat": "Jl. Pintu Besar Selatan No. 74D, 76, 78, Jakarta Barat 11110", "pic": "Esther Kurniawan", "hp": "08121107557", "telp": "021-6266286"},
        {"kualifikasi": "B", "no": 3, "nama": "PT ASURANSI CAKRAWALA PROTEKSI INDONESIA", "alamat": "CITRA Tower - Tower Utara Lantai 9, Jalan Benyamin Suaeb Kav A6, Kemayoran, Jakarta Pusat 10630", "pic": "Elisa Wisdiana, Putri Amalia", "hp": "08129367858, 085659038624", "telp": "021-30051888"},
        {"kualifikasi": "B", "no": 4, "nama": "PT ASURANSI DAYIN MITRA TBK", "alamat": "Wisma Hayam Wuruk 7th Floor Jl. Hayam Wuruk No.8 Jakarta 10120", "pic": "Ariaji Wiyoso, Mustafa Samil", "hp": "081540888890, 081310821823", "telp": "021-5708989"},
        {"kualifikasi": "B", "no": 5, "nama": "PT ASURANSI JASA INDONESIA", "alamat": "Graha Jasindo Jl. Menteng Raya No. 21, Jakarta Pusat, 10340", "pic": "Hardyan, Henri Pratama", "hp": "082112733555, 085211118895", "telp": "021-7987908"},
        {"kualifikasi": "B", "no": 6, "nama": "PT ASURANSI JASA TANIA TBK", "alamat": "Gedung Agro Plaza Lt. 9 Jl. HR. Rasuna Said Kav. X2 No.1 Jakarta 12950", "pic": "Hasbi Ashsiddiqi, Amalia Lutvita Nisa", "hp": "081296490762, 082330669897", "telp": "021-3101850"},
        {"kualifikasi": "B", "no": 7, "nama": "PT ASURANSI KREDIT INDONESIA", "alamat": "Jalan Angkasa Blok B-9 Kavling Nomor 8, Kota Baru Bandar Kemayoran, Jakarta Pusat 10610", "pic": "Yudho Pamungkas, Tara A. Napitupulu", "hp": "08159946192, 082136822933", "telp": "021-6546471"},
        {"kualifikasi": "B", "no": 8, "nama": "PT ASURANSI MITRA PELINDUNG MUSTIKA", "alamat": "AKR Tower Level 22, Jl.Panjang No.5 RT.11/RW.10, Kebon Jeruk, Jakarta Barat 11530", "pic": "Julian Fernando Hutabarat", "hp": "08111904611", "telp": "021-1500676"},
        {"kualifikasi": "B", "no": 9, "nama": "PT ASURANSI MSIG INDONESIA", "alamat": "Gedung Summitmas II lantai 15 Jalan Jendral Sudirman Kav. 61-62 Jakarta 12190", "pic": "Mohamad Riskan, Herbert Torrey Sibarani", "hp": "081617140523, 081212849990", "telp": "021-252 3110"},
        {"kualifikasi": "B", "no": 10, "nama": "PT ASURANSI RAKSA PRATIKARA", "alamat": "Jl. Abdul Muis No. 40 Wisma BSG Lt. 3 Jakarta Pusat 10160", "pic": "Agata Febrina, Rahmadila Alif Madia Putri", "hp": "081283644836, 08224137178", "telp": "021-3859007"},
        {"kualifikasi": "B", "no": 11, "nama": "PT ASURANSI RAMAYANA TBK", "alamat": "Jl. Kebon Sirih No.49 Jakarta 10340", "pic": "Suwedi", "hp": "08117887789", "telp": "021-31937148"},
        {"kualifikasi": "B", "no": 12, "nama": "PT ASURANSI UMUM MEGA", "alamat": "Menara Bank Mega, Lantai 18 Jl. Kapten Tendean, Kav. 12-14A Mampang Prapatan, Jakarta Selatan 12790", "pic": "Erico Harpend, Cicilia Shantara", "hp": "08111800583, 085163135454", "telp": "021-79175588"},
        {"kualifikasi": "B", "no": 13, "nama": "PT ASURANSI TOKIO MARINE INDONESIA", "alamat": "Sentral Senayan II Lt. 3, Jl. Asia Afrika No. 8 10270", "pic": "Faerus Stefhani", "hp": "082189291991", "telp": "021-5724007"},
        {"kualifikasi": "B", "no": 14, "nama": "PT ASURANSI TOTAL BERSAMA", "alamat": "Citra Tower Lt. 27, Jl. Benyamin Sueb Kav. A6, Kemayoran, Jakarta 10630", "pic": "Wawan Supriyanto", "hp": "082135303532", "telp": "021-22607272"},
        {"kualifikasi": "B", "no": 15, "nama": "PT CHINA TAIPING INSURANCE INDONESIA", "alamat": "Wisma Argo Manunggal Lt. 19, Jl. Jend. Gatot Subroto Kav. 22, Jakarta Selatan, 12930", "pic": "Chatarina Ike Kusuma", "hp": "082311495266", "telp": "021-2522422"},
        {"kualifikasi": "B", "no": 16, "nama": "PT CHUBB GENERAL INSURANCE INDONESIA", "alamat": "Gedung Bursa Efek Indonesia Tower II, Lantai 10, Suite 1001 Jl. Jend. Sudirman kav 52-53 Senayan, Jakarta 10190", "pic": "Wiwit Audiyanto, Rama Hifni", "hp": "082112267890, 08118703637, 08119318289", "telp": "021-29498500"},
        {"kualifikasi": "B", "no": 17, "nama": "PT GREAT EASTERN GENERAL INSURANCE INDONESIA", "alamat": "MidPlaza 2, 23rd Floor Jalan Jendral Sudirman Kav.10-11 Jakarta 10220", "pic": "Muchammad Wijaya, Alvid Alim, Muhammad Aditama", "hp": "081219620152, 082111287012, 082111020392", "telp": "021-5723737"},

        # Gambar 3 - Kualifikasi C
        {"kualifikasi": "C", "no": 1, "nama": "PT ARTHAGRAHA GENERAL INSURANCE", "alamat": "Kawasan Niaga Terpadu Sudirman (SCBD) Gedung Artha Graha Lt. 3, Jl. Jend. Sudirman Kav, 52 - 53 Jakarta 12190", "pic": "Jane Angela, Kezia Aprianto", "hp": "081398880561, 085175480920", "telp": "021-5152808"},
        {"kualifikasi": "C", "no": 2, "nama": "PT ASURANSI ARTARINDO", "alamat": "Head Office - Gedung Hermina Tower Lt. 12 Tower A JL. HBR Motik Blok B-10 Kav. 4, Gunung Sahari Selatan, Kemayoran. Jakarta Pusat 10610", "pic": "Ronald Rinaldy R.", "hp": "08561372344", "telp": "021-39710999"},
        {"kualifikasi": "C", "no": 3, "nama": "PT ASURANSI HARTA AMAN PRATAMA TBK", "alamat": "Wisma 46, Kota BNI, Jl. Jend Sudirman kav. 1, Jakarta 12920", "pic": "Henry Harwanto, Susanto, Iwan Aryanto", "hp": "0811363456, 08562053021", "telp": "021-63864420 / 021-6348760"},
        {"kualifikasi": "C", "no": 4, "nama": "PT ASURANSI CANDI UTAMA", "alamat": "AXA Tower Kuningan City Lantai 32 Suite 1, Jl. Prof. DR. Satrio No Kav.18, Jakarta 12940", "pic": "Bulan Purnamasari", "hp": "082260906019", "telp": "021-30051888"},
        {"kualifikasi": "C", "no": 5, "nama": "PT ASURANSI STACO MANDIRI", "alamat": "Jl. Kebon Kacang Raya No. 25 Jakarta Pusat 10240", "pic": "Linda Susanti", "hp": "08119278886", "telp": "021-23595999"},
        {"kualifikasi": "C", "no": 6, "nama": "PT ASURANSI PERISAI LISTRIK NASIONAL (dh. PT ASURANSI TUGU KRESNA PRATAMA)", "alamat": "JL. Raya Pasar Minggu No. 5 Pancoran, Jakarta Selatan 12780", "pic": "Dwi Astuti Eloran, Novi Yeniarti", "hp": "08118689960, 081212267676", "telp": "021-7995888"},
        {"kualifikasi": "C", "no": 7, "nama": "PT AVRIST GENERAL INSURANCE", "alamat": "Gedung Bank Panin Senayan Lt. 8, Jl. Jend. Sudirman Kav. 1, Jakarta 10270", "pic": "Rico Saputra", "hp": "082153203332", "telp": "021-5740381"},
        {"kualifikasi": "C", "no": 8, "nama": "PT AXA INSURANCE INDONESIA (dh. PT MANDIRI AXA GENERAL INSURANCE)", "alamat": "AXA Tower Lt. 16, Jl. Prof. Dr. Satrio Kav. 18, Kuningan City, Jakarta 12940", "pic": "I Dewa Putu Sidan Bayupati", "hp": "0811384109", "telp": "021-30057633"},
        {"kualifikasi": "C", "no": 9, "nama": "PT CITRA INTERNATIONAL UNDERWRITERS", "alamat": "Menara Standard Chartered 33rd Floor, Jl. Prof. Dr. Satrio No. 164 Jakarta 12930", "pic": "Harsa", "hp": "02811867140", "telp": "021-29927999 / 021-29927998"},
        {"kualifikasi": "C", "no": 10, "nama": "PT MERITZ KORINDO INSURANCE", "alamat": "Wisma Korindo, Jl. M.T. Haryono Kav. 62, Jakarta Selatan 12780", "pic": "Achmad Buchori, Zakiatul Muna", "hp": "0818217689, 082112894450", "telp": "021-7975959"},
        {"kualifikasi": "C", "no": 11, "nama": "PT MNC ASURANSI INDONESIA", "alamat": "MNC Financial Center Lt. 11, Jl. Kebon Sirih no. 21 - 27 Jakarta Pusat 10340", "pic": "Adrianus Eko Febriyansyah", "hp": "081808703366, 085692289674", "telp": "021-29701234"}
    ]

data = get_insurance_data()

# --- HEADER LUXURY ---
st.markdown("""
    <div class="lux-header">
        <h1>🛡️ DIREKTORI ASURANSI</h1>
        <p>Klasifikasi Rekanan Perkreditan Perbankan</p>
    </div>
""", unsafe_allow_html=True)

# --- BUTTONS KHUSUS KUALIFIKASI (NAVIGATION BAR) ---
if 'selected_qual' not in st.session_state:
    st.session_state.selected_qual = 'Semua'

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Semua", type="primary" if st.session_state.selected_qual == 'Semua' else "secondary"):
        st.session_state.selected_qual = 'Semua'
        st.rerun()

with col2:
    if st.button("Kual A", type="primary" if st.session_state.selected_qual == 'A' else "secondary"):
        st.session_state.selected_qual = 'A'
        st.rerun()

with col3:
    if st.button("Kual B", type="primary" if st.session_state.selected_qual == 'B' else "secondary"):
        st.session_state.selected_qual = 'B'
        st.rerun()

with col4:
    if st.button("Kual C", type="primary" if st.session_state.selected_qual == 'C' else "secondary"):
        st.session_state.selected_qual = 'C'
        st.rerun()

st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

# Input Pencarian
search_query = st.text_input("🔍 Cari PT Asuransi / PIC / Alamat:", placeholder="Ketik kata kunci...").strip()

# Logika Filter
filtered_data = data

if st.session_state.selected_qual != 'Semua':
    filtered_data = [item for item in filtered_data if item['kualifikasi'] == st.session_state.selected_qual]

if search_query:
    filtered_data = [
        item for item in filtered_data 
        if search_query.lower() in item["nama"].lower() 
        or search_query.lower() in item["alamat"].lower()
        or search_query.lower() in item["pic"].lower()
    ]

# Jumlah Data Terfilter
label_qual = f"KUALIFIKASI {st.session_state.selected_qual}" if st.session_state.selected_qual != "Semua" else "SEMUA KUALIFIKASI"
st.markdown(f"<p style='color: #64748B; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; margin-top: 10px;'>MENAMPILKAN {len(filtered_data)} REKANAN ({label_qual})</p>", unsafe_allow_html=True)

# Loop Render Card
for item in filtered_data:
    pics = [p.strip() for p in item["pic"].split(",")]
    pic_badges = "".join([f'<span class="pic-tag">👤 {p}</span>' for p in pics])
    
    qual = item['kualifikasi']
    card_class = f"card-{qual.lower()}"
    badge_class = f"badge-{qual.lower()}"
    
    st.markdown(f"""
        <div class="lux-card {card_class}">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span class="qual-badge {badge_class}">Kualifikasi {qual} #{item['no']}</span>
            </div>
            <div class="lux-title">{item['nama']}</div>
            <div class="lux-info">
                <span class="lux-label">📍 Alamat:</span><br>{item['alamat']}
            </div>
            <div class="lux-info" style="margin-top: 8px;">
                <span class="lux-label">Person in Charge (PIC):</span><br>
                {pic_badges}
            </div>
            <div style="margin-top: 10px;">
                <a class="phone-tag" href="tel:{item['telp']}">📞 Telp: {item['telp']}</a>
                <span class="phone-tag" style="background: rgba(16, 185, 129, 0.15); color: #34D399;">📱 HP: {item['hp']}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
