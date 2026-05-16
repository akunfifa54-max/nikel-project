import streamlit as st
import pandas as pd
import os

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PBL SDA - PT Vale Indonesia",
    layout="wide",
    page_icon="⛏️"
)

# =========================
# LOGO (SAFE)
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists("logo_unisba.png"):
        st.image("logo_unisba.png", width=120)
    else:
        st.warning("Logo UNISBA belum diupload")

with col2:
    st.title("📊 PBL Ekonomi Sumber Daya Alam")
    st.subheader("⛏️ PT Vale Indonesia (2014–2024 Data)")

# =========================
# IDENTITAS
# =========================
st.markdown("""
### 👥 Anggota Kelompok
- Radea Rahman Dwiyana (10090224001)  
- Bunga Wiati Manaki (10090224026)  
- Shidqi Alhamdani Mieftah (10090224032)  

### 🎓 Dosen Pengampu
Yuhka Sundaya, S.E., M.Si.
""")

st.divider()

# =========================
# SIDEBAR (LENGKAP)
# =========================
st.sidebar.header("⚙️ Panel Simulasi")

market = st.sidebar.selectbox(
    "Struktur Pasar",
    ["Persaingan Sempurna", "Monopoli", "Oligopoli"]
)

price_factor = st.sidebar.slider("Faktor Harga", 50, 200, 100)
discount = st.sidebar.slider("Tingkat Diskonto (%)", 1, 20, 5)
green_tax = st.sidebar.slider("Green Tax (%)", 0, 50, 10)
efficiency = st.sidebar.slider("Efisiensi Produksi", 50, 150, 100)
cost_pressure = st.sidebar.slider("Tekanan Biaya (MC)", 50, 200, 100)

st.sidebar.markdown("---")
st.sidebar.info("Data dasar: 2014–2024 PT Vale Indonesia")

# =========================
# DATA ASLI
# =========================
df = pd.DataFrame({
    "Tahun": [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    "Produksi": [78726000,
