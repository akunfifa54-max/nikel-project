import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG HALAMAN ---
st.set_page_config(
    page_title="PBL 3 - Ekonomi SDA & Lingkungan",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM CSS (Agar Titik Dua Lurus & Header Rapi) ---
st.markdown("""
    <style>
    .main-title { font-size: 32px !important; font-weight: 800; color: #1F2937; margin-bottom: 0px; }
    .sub-title { font-size: 18px !important; color: #6B7280; margin-top: 0px; font-weight: 500; }
    .info-box { background-color: #F8FAFC; padding: 25px; border-left: 6px solid #1E3A8A; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
    
    /* Style Tabel Identitas agar Titik Dua Lurus */
    .info-table { width: 100%; border-collapse: collapse; }
    .info-table td { padding: 4px 2px; font-size: 16px; color: #374151; vertical-align: top; border: none !important; }
    .label-cell { font-weight: 700; color: #111827; width: 150px; text-transform: uppercase; letter-spacing: 0.5px; }
    .separator-cell { width: 20px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.write("##") 
    # Menggunakan URL Wikipedia resmi agar logo pasti muncul
    st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=150)

with col_text:
    st.markdown('<p class="main-title">Analisis Ekonomi Sumber Daya Nikel</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Program Studi Ekonomi Pembangunan - UNISBA</p>', unsafe_allow_html=True)
    
    # BOX IDENTITAS (Titik Dua Sudah Diluruskan)
    st.markdown(f"""
    <div class="info-box">
        <table class="info-table">
            <tr>
                <td class="label-cell">KELOMPOK</td>
                <td class="separator-cell">:</td>
                <td>2</td>
            </tr>
            <tr>
                <td class="label-cell">ANGGOTA</td>
                <td class="separator-cell">:</td>
                <td>
                    1. Radea Rahman Dwiyana (10090224001)<br>
                    2. Bunga Wiati Manaki (10090224026)<br>
                    3. Shidqi Alhamdani Mieftah (10090224032)
                </td>
            </tr>
            <tr>
                <td class="label-cell">DOSEN</td>
                <td class="separator-cell">:</td>
                <td>Yuhka Sundaya, S.E., M.Si.</td>
            </tr>
            <tr>
                <td class="label-cell">MATA KULIAH</td>
                <td class="separator-cell">:</td>
                <td>Ekonomi SDA dan Lingkungan</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- BAGIAN 1: DATA HISTORIS (DIKEMBALIKAN) ---
st.subheader("1. Data Historis Produksi & Harga")
try:
    df_historis = pd.read_csv('data_nikel.csv')
    st.dataframe(df_historis, use_container_width=True)
except:
    st.info("💡 Pastikan file 'data_nikel.csv' sudah diupload ke GitHub untuk melihat tabel ini.")

# --- SIDEBAR PARAMETER ---
with st.sidebar:
    st.header("⚙️ Kontrol Simulasi")
    a = st.number_input("Intersep Permintaan (a)", value=86500000.0, format="%.1f")
    b = st.number_input("Slope Permintaan (b)", value=0.0702729, format="%.7f")
    mc = st.number_input("Marginal Cost (MC)", value=176566741.2, format="%.1f")
    r = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    lambda_0 = st.number_input("MUC Awal (λ0)", value=15163.0)

# --- LOGIKA SIMULASI ---
def jalankan_simulasi(struktur):
    tahun_sim = np.arange(0, 11)
    stok_awal = 20000.0
    slope_eff = b * 2 if struktur == "Monopoli" else (b * 1.5 if struktur == "Oligopoli" else b)
    hasil = []
    stok_sisa = stok_awal
    for t in tahun_sim:
        muc_t = lambda_0 * np.exp(r * t)
        q_t = (a - (mc/1000000) - (muc_t/1000000)) / (slope_eff * 100) 
        q_t = max(0, q_t)
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        
        if produksi > 0.01: # Menghilangkan data 0.000
            hasil.append({
                "Tahun": t, "MUC": muc_t, "Produksi": produksi, "Sisa Stok": stok_sisa
            })
    return pd.DataFrame(hasil)

# --- BAGIAN 2: HASIL SIMULASI & GRAFIK ---
st.subheader("2. Simulasi Alokasi Intertemporal")
tab1, tab2, tab3 = st.tabs(["🏛️ Persaingan Sempurna", "🏢 Monopoli", "🏪 Oligopoli"])

for tab, label in zip([tab1, tab2, tab3], ["Persaingan", "Monopoli", "Oligopoli"]):
    with tab:
        df_res = jalankan_simulasi(label)
        
        col_tabel, col_grafik = st.columns([1, 1])
        with col_tabel:
            st.write(f"**Tabel {label}:**")
            st.table(df_res.style.format({
                "MUC": "{:,.2f}", "Produksi": "{:,.2f}", "Sisa Stok": "{:,.2f}"
            }))
        
        with col_grafik:
            st.write(f"**Grafik Produksi {label}:**")
            st.line_chart(df_res.set_index("Tahun")["Produksi"])
            st.write(f"**Grafik Kelangkaan (MUC):**")
            st.area_chart(df_res.set_index("Tahun")["MUC"])

st.divider()
st.subheader("3. Analisis Ekonomi")
st.info(f"Kenaikan MUC sebesar {r*100:.0f}% per tahun menunjukkan berlakunya Aturan Hotelling dalam alokasi nikel.")
