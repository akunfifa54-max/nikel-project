import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG HALAMAN ---
st.set_page_config(
    page_title="PBL 3 - Ekonomi SDA & Lingkungan",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    .main-title { font-size: 32px !important; font-weight: 800; color: #1F2937; margin-bottom: 0px; }
    .sub-title { font-size: 18px !important; color: #6B7280; margin-top: 0px; font-weight: 500; }
    .info-box { background-color: #F8FAFC; padding: 25px; border-left: 6px solid #1E3A8A; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    .info-table { width: 100%; border-collapse: collapse; }
    .info-table td { padding: 4px 2px; font-size: 16px; color: #374151; vertical-align: top; border: none !important; }
    .label-cell { font-weight: 700; color: #111827; width: 150px; text-transform: uppercase; letter-spacing: 0.5px; }
    .separator-cell { width: 20px; font-weight: 700; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=140)

with col_text:
    st.markdown('<p class="main-title">Analisis Ekonomi Sumber Daya Nikel</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Program Studi Ekonomi Pembangunan - UNISBA</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <table class="info-table">
            <tr><td class="label-cell">KELOMPOK</td><td class="separator-cell">:</td><td>2</td></tr>
            <tr>
                <td class="label-cell">ANGGOTA</td><td class="separator-cell">:</td>
                <td>
                    1. Radea Rahman Dwiyana (10090224001)<br>
                    2. Bunga Wiati Manaki (10090224026)<br>
                    3. Shidqi Alhamdani Mieftah (10090224032)
                </td>
            </tr>
            <tr><td class="label-cell">DOSEN</td><td class="separator-cell">:</td><td>Yuhka Sundaya, S.E., M.Si.</td></tr>
            <tr><td class="label-cell">MATA KULIAH</td><td class="separator-cell">:</td><td>Ekonomi SDA dan Lingkungan</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- DATA HISTORIS (Sheet 1) ---
try:
    df_historis = pd.read_csv('Nikel - Tahap 3.xlsx - Sheet1.csv')
    st.subheader("1. Data Historis Produksi & Harga")
    st.dataframe(df_historis, use_container_width=True)
except:
    pass

# --- SIDEBAR (Mengambil Default dari Sheet 3) ---
with st.sidebar:
    st.header("⚙️ Kontrol Simulasi")
    a = st.number_input("Intersep Permintaan (a)", value=1090000000.0)
    b = st.number_input("Slope Permintaan (b)", value=1231475.0) # Nilai absolut dari data
    mc = st.number_input("Marginal Cost (MC)", value=143804.57)
    r = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    lambda_0 = st.number_input("MUC Awal (λ0)", value=15163.0)

# --- LOGIKA SIMULASI ---
def hitung_simulasi(struktur):
    tahun = np.arange(1, 12) # Simulasi 11 tahun
    stok_sisa = 20000.0
    slope_eff = b * 2 if struktur == "Monopoli" else (b * 1.5 if struktur == "Oligopoli" else b)
    data = []
    
    for t in tahun:
        muc = lambda_0 * np.exp(r * (t-1))
        # Rumus Q = (a - MC - MUC) / b
        q = (a - mc - muc) / slope_eff
        q = max(0, q)
        prod = min(q, stok_sisa)
        stok_sisa -= prod
        
        if prod > 0:
            data.append({
                "Tahun": int(t), 
                "MUC": muc, 
                "Produksi": prod, 
                "Sisa Stok": stok_sisa
            })
    return pd.DataFrame(data)

# --- VISUALISASI ---
st.subheader("2. Simulasi Alokasi Intertemporal")
t1, t2, t3 = st.tabs(["🏛️ Persaingan Sempurna", "🏢 Monopoli", "🏪 Oligopoli"])

for t, label in zip([t1, t2, t3], ["Persaingan", "Monopoli", "Oligopoli"]):
    with t:
        df = hitung_simulasi(label)
        if not df.empty:
            c1, c2 = st.columns([1, 1])
            with c1:
                st.write(f"**Tabel {label}**")
                st.table(df.style.format({"MUC": "{:,.2f}", "Produksi": "{:,.2f}", "Sisa Stok": "{:,.2f}"}))
            with c2:
                st.write("**Kurva Produksi & Kelangkaan**")
                # Grafik garis untuk Produksi dan MUC
                st.line_chart(df.set_index("Tahun")[["Produksi", "MUC"]])
        else:
            st.warning("Data tidak tersedia untuk parameter ini.")

st.divider()
st.info(f"**Analisis Ekonomi:** Berdasarkan data Sheet 3, dengan cadangan 20.000 ton dan tingkat diskonto {r*100:.0f}%, "
         "ekstraksi akan mengikuti pola penurunan produksi seiring meningkatnya biaya kelangkaan (MUC) sesuai Aturan Hotelling.")
