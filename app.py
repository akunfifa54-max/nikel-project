import streamlit as st
import numpy as np
import pandas as pd

# --- 1. CONFIG HALAMAN ---
st.set_page_config(
    page_title="PBL 3 - Ekonomi SDA & Lingkungan",
    page_icon="📊",
    layout="wide"
)

# --- 2. CUSTOM CSS (Titik Dua Sejajar & Header Rapi) ---
st.markdown("""
    <style>
    .main-title { font-size: 32px !important; font-weight: 800; color: #1E3A8A; margin-bottom: 0px; }
    .sub-title { font-size: 18px !important; color: #6B7280; margin-top: 0px; font-weight: 500; }
    .info-box { background-color: #F8FAFC; padding: 20px; border-left: 6px solid #1E3A8A; border-radius: 8px; }
    .info-table { width: 100%; border-collapse: collapse; }
    .info-table td { padding: 5px; font-size: 15px; color: #374151; vertical-align: top; border: none !important; }
    .label-cell { font-weight: 700; width: 140px; text-transform: uppercase; }
    .sep-cell { width: 20px; text-align: center; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. HEADER SECTION (Logo & Identitas) ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.write("##")
    # Link Logo Universitas Islam Bandung (Pasti Muncul)
    st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=140)

with col_text:
    st.markdown('<p class="main-title">Analisis Ekonomi Sumber Daya Nikel</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Program Studi Ekonomi Pembangunan - UNISBA</p>', unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class="info-box">
        <table class="info-table">
            <tr><td class="label-cell">KELOMPOK</td><td class="sep-cell">:</td><td>2</td></tr>
            <tr>
                <td class="label-cell">ANGGOTA</td><td class="sep-cell">:</td>
                <td>1. Radea Rahman Dwiyana (10090224001)<br>
                    2. Bunga Wiati Manaki (10090224026)<br>
                    3. Shidqi Alhamdani Mieftah (10090224032)</td>
            </tr>
            <tr><td class="label-cell">DOSEN</td><td class="sep-cell">:</td><td>Yuhka Sundaya, S.E., M.Si.</td></tr>
            <tr><td class="label-cell">MATA KULIAH</td><td class="sep-cell">:</td><td>Ekonomi SDA dan Lingkungan</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- 4. DATA HISTORIS (Bagian 1) ---
st.subheader("1. Data Historis Produksi & Harga")
try:
    # Membaca file yang diupload (Sheet 1 untuk historis)
    df_h = pd.read_csv('Nikel - Tahap 3.xlsx - Sheet1.csv')
    st.dataframe(df_h, use_container_width=True)
except:
    st.warning("File 'Nikel - Tahap 3.xlsx - Sheet1.csv' tidak ditemukan.")

# --- 5. SIDEBAR (Parameter Sesuai Data Terbaru) ---
with st.sidebar:
    st.header("⚙️ Parameter Ekonomi")
    # Default values diambil dari file Sheet 3 Anda
    a_val = st.number_input("Intersep (a)", value=1090000000.0)
    b_val = st.number_input("Slope (b)", value=1231475.0, format="%.0f")
    mc_val = st.number_input("Marginal Cost (MC)", value=143804.57)
    r_val = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    muc_0 = st.number_input("MUC Awal (λ0)", value=15163.0)
    st.info("Total Cadangan: 20,000 unit")

# --- 6. LOGIKA SIMULASI (Presisi Sheet 3) ---
def jalankan_simulasi(struktur):
    stok_awal = 20000.0
    # Penyesuaian slope untuk berbagai struktur pasar
    if struktur == "Monopoli": s_eff = b_val * 2
    elif struktur == "Oligopoli": s_eff = b_val * 1.5
    else: s_eff = b_val
    
    hasil = []
    stok_sisa = stok_awal
    
    for t in range(1, 12): # Simulasi 11 Tahun
        muc_t = muc_0 * np.exp(r_val * (t-1))
        # Rumus: q = (a - MC - MUC) / slope
        q_t = (a_val - mc_val - muc_t) / s_eff
        q_t = max(0, q_t)
        
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        
        if produksi > 0.01:
            hasil.append({
                "Tahun": t,
                "MUC (Rent)": muc_t,
                "Produksi": produksi,
                "Sisa Stok": stok_sisa
            })
    return pd.DataFrame(hasil)

# --- 7. OUTPUT SIMULASI & GRAFIK (Bagian 2) ---
st.subheader("2. Simulasi Alokasi Intertemporal")
tab1, tab2, tab3 = st.tabs(["🏛️ Persaingan Sempurna", "🏢 Monopoli", "🏪 Oligopoli"])

for t, label in zip([tab1, tab2, tab3], ["Persaingan", "Monopoli", "Oligopoli"]):
    with t:
        df_sim = jalankan_simulasi(label)
        if not df_sim.empty:
            col_left, col_right = st.columns([1, 1])
            with col_left:
                st.write(f"**Tabel Simulasi {label}**")
                st.table(df_sim.style.format({
                    "MUC (Rent)": "{:,.2f}", 
                    "Produksi": "{:,.2f}", 
                    "Sisa Stok": "{:,.2f}"
                }))
            with col_right:
                st.write(f"**Kurva Produksi & MUC {label}**")
                # Grafik Garis (Kurva)
                st.line_chart(df_sim.set_index("Tahun")[["Produksi", "MUC (Rent)"]])
        else:
            st.error("Tidak ada data untuk simulasi ini.")

st.divider()
st.subheader("3. Analisis Ekonomi")
st.info(f"Berdasarkan **Aturan Hotelling**, tingkat ekstraksi menurun seiring waktu karena nilai kelangkaan (MUC) meningkat sebesar {r_val*100:.0f}% per tahun.")
