import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PBL SDA - Nikel PT Vale Indonesia",
    layout="wide",
    page_icon="⛏️"
)

# =========================
# LOGO + HEADER
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    st.image("logo_unisba.png", width=120)

with col2:
    st.title("📊 PBL Ekonomi SDA - Industri Nikel")
    st.subheader("⛏️ PT Vale Indonesia (2014–2024 Data Real)")

st.markdown("""
**ANGGOTA KELOMPOK:**
- Radea Rahman Dwiyana (10090224001)  
- Bunga Wiati Manaki (10090224026)  
- Shidqi Alhamdani Mieftah (10090224032)  

**DOSEN PENGAMPU:**  
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
st.subheader("📈 Tren Produksi Nikel")
st.line_chart(df.set_index("Tahun")[["Produksi"]])

st.subheader("💰 Tren Harga Nikel")
st.line_chart(df.set_index("Tahun")[["Harga"]])

st.subheader("📊 Tren Marginal Cost (MC)")
st.line_chart(df.set_index("Tahun")[["MC"]])

# =========================
# ANALISIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

st.info("""
Data menunjukkan dinamika industri nikel Indonesia:

- Produksi relatif fluktuatif dengan kecenderungan menurun pada periode tertentu.
- Harga nikel meningkat signifikan hingga 2022 akibat permintaan global.
- MC (biaya marginal) terus meningkat yang menunjukkan semakin mahalnya ekstraksi sumber daya.

Kesimpulan:
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
st.caption("PT Vale Indonesia | PBL Ekonomi SDA | Universitas Islam Bandung (UNISBA)")
