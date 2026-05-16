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
# LOGO SAFE LOAD (ANTI ERROR)
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists("logo_unisba.png"):
        st.image("logo_unisba.png", width=120)
    else:
        st.warning("Logo UNISBA belum diupload ke GitHub")

with col2:
    st.title("📊 PBL Ekonomi Sumber Daya Alam")
    st.subheader("⛏️ PT Vale Indonesia (2014–2024)")

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
# DATA REAL KAMU
# =========================
df = pd.DataFrame({
    "Tahun": [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    "Produksi": [78726000,81177000,77581000,76807000,74806000,71025000,72237000,65388000,60090000,70728000,71311000],
    "Harga": [155425900,127648400,98366800,108620400,145862400,196511700,201144200,260717600,370685700,252293500,237823600],
    "MC": [15163,15940,16758,17617,18520,19470,20468,21517,22621,23780,25000]
})

# =========================
# KPI (2024)
# =========================
st.subheader("📌 Key Indicators (2024)")

col1, col2, col3 = st.columns(3)

col1.metric("⛏️ Produksi", f"{df['Produksi'].iloc[-1]:,}")
col2.metric("💰 Harga", f"{df['Harga'].iloc[-1]:,}")
col3.metric("📈 MC", f"{df['MC'].iloc[-1]:,}")

# =========================
# GRAFIK
# =========================
st.subheader("📈 Tren Produksi")
st.line_chart(df.set_index("Tahun")[["Produksi"]])

st.subheader("💰 Tren Harga")
st.line_chart(df.set_index("Tahun")[["Harga"]])

st.subheader("📊 Tren MC (Marginal Cost)")
st.line_chart(df.set_index("Tahun")[["MC"]])

# =========================
# INSIGHT
# =========================
st.subheader("🧠 Analisis Ekonomi")

st.info("""
Data menunjukkan dinamika industri nikel Indonesia:

• Produksi cenderung fluktuatif namun relatif menurun pada periode tertentu  
• Harga nikel meningkat signifikan hingga 2022 karena permintaan global  
• MC terus meningkat → biaya ekstraksi semakin mahal  

KESIMPULAN:
Industri nikel menunjukkan karakteristik sumber daya alam yang semakin langka dan biaya ekstraksi meningkat dari tahun ke tahun.
""")

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Lengkap 2014–2024")
st.dataframe(df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("PBL Ekonomi SDA | PT Vale Indonesia | Universitas Islam Bandung")
