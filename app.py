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
    .info-table td { padding: 4px 8px; font-size: 16px; color: #374151; border: none !important; }
    .label-cell { font-weight: 700; color: #111827; width: 160px; text-transform: uppercase; letter-spacing: 0.5px; }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_text = st.columns([1, 5])
with col_logo:
    st.write("##") 
    try:
        st.image("Lambang-Universitas_Islam_Bandung.png", width=150)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=150)

with col_text:
    st.markdown('<p class="main-title">Analisis Intertemporal Sumber Daya Alam</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Program Studi Ekonomi Pembangunan - UNISBA</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="info-box">
        <table class="info-table" style="width:100%;">
            <tr><td class="label-cell">KELOMPOK</td><td>: 2</td></tr>
            <tr>
                <td class="label-cell" style="vertical-align: top;">ANGGOTA</td>
                <td style="padding-top: 0px;">
                    <ul style="list-style-type: none; padding: 0; margin: 0;">
                        <li>: 1. Radea Rahman Dwiyana (10090224001)</li>
                        <li>&nbsp;&nbsp; 2. Bunga Wiati Manaki (10090224026)</li>
                        <li>&nbsp;&nbsp; 3. Shidqi Alhamdani Mieftah (10090224032)</li>
                    </ul>
                </td>
            </tr>
            <tr><td class="label-cell">DOSEN</td><td>: Yuhka Sundaya, S.E., M.Si.</td></tr>
            <tr><td class="label-cell">MATA KULIAH</td><td>: Ekonomi SDA dan Lingkungan</td></tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- SIDEBAR PARAMETER ---
with st.sidebar:
    st.header("⚙️ Kontrol Simulasi")
    a = st.number_input("Intersep Permintaan (a)", value=86500000.0, format="%.1f")
    b = st.number_input("Slope Permintaan (b)", value=0.0702729, format="%.7f")
    mc = st.number_input("Marginal Cost (MC)", value=176566741.2, format="%.1f")
    r = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    stok_awal = st.number_input("Total Cadangan (S)", value=20000.0)
    lambda_0 = st.number_input("MUC Awal (λ0)", value=15163.0)

# --- LOGIKA SIMULASI ---
def jalankan_simulasi(struktur):
    tahun_sim = np.arange(0, 11)
    slope_eff = b * 2 if struktur == "Monopoli" else (b * 1.5 if struktur == "Oligopoli" else b)
    hasil = []
    stok_sisa = stok_awal
    for t in tahun_sim:
        muc_t = lambda_0 * np.exp(r * t)
        q_t = (a - (mc/1000000) - (muc_t/1000000)) / (slope_eff * 100) 
        q_t = max(0, q_t)
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        hasil.append({"Tahun": t, "MUC": muc_t, "Produksi": produksi, "Sisa_Stok": stok_sisa})
    return pd.DataFrame(hasil)

# --- TAMPILAN UTAMA ---
st.title("📊 Hasil Simulasi & Grafik")

tab1, tab2, tab3 = st.tabs(["🏛️ Persaingan Sempurna", "🏢 Monopoli", "🏪 Oligopoli"])

for tab, label in zip([tab1, tab2, tab3], ["Persaingan", "Monopoli", "Oligopoli"]):
    with tab:
        df_res = jalankan_simulasi(label)
        
        col_tab1, col_tab2 = st.columns([1, 1])
        with col_tab1:
            st.write("**Tabel Data:**")
            st.table(df_res.style.format({"MUC": "{:,.2f}", "Produksi": "{:,.2f}", "Sisa_Stok": "{:,.2f}"}))
        
        with col_tab2:
            st.write("**Grafik Produksi per Tahun:**")
            st.line_chart(df_res.set_index("Tahun")["Produksi"])
            
            st.write("**Grafik MUC (Scarcity Rent):**")
            st.area_chart(df_res.set_index("Tahun")["MUC"])

st.divider()
st.subheader("💡 Analisis Ringkas")
st.info(f"Grafik di atas menunjukkan bahwa dengan r={r*100:.0f}%, produksi cenderung menurun seiring waktu sementara MUC (biaya kelangkaan) meningkat mengikuti Aturan Hotelling.")
