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
# HEADER + LOGO
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists("logo_unisba.png"):
        st.image("logo_unisba.png", width=120)

with col2:
    st.title("📊 PBL Ekonomi Sumber Daya Alam")
    st.subheader("⛏️ PT Vale Indonesia (Data 2014–2024)")

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
# SIDEBAR (DATA SAMPING)
# =========================
st.sidebar.header("⚙️ Panel Simulasi")

market = st.sidebar.selectbox(
    "Struktur Pasar",
    ["Persaingan Sempurna", "Monopoli", "Oligopoli"]
)

price_factor = st.sidebar.slider("Faktor Harga (Simulasi)", 50, 200, 100)
cost_pressure = st.sidebar.slider("Tekanan Biaya (MC)", 50, 200, 100)
resource_efficiency = st.sidebar.slider("Efisiensi Produksi", 50, 150, 100)

st.sidebar.markdown("---")
st.sidebar.info("Data dasar: 2014–2024 (PT Vale Indonesia)")

# =========================
# DATA ASLI
# =========================
df = pd.DataFrame({
    "Tahun": [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024],
    "Produksi": [78726000,81177000,77581000,76807000,74806000,71025000,72237000,65388000,60090000,70728000,71311000],
    "Harga": [155425900,127648400,98366800,108620400,145862400,196511700,201144200,260717600,370685700,252293500,237823600],
    "MC": [15163,15940,16758,17617,18520,19470,20468,21517,22621,23780,25000]
})

# =========================
# KPI
# =========================
st.subheader("📌 Key Indicators (2024)")

col1, col2, col3 = st.columns(3)

col1.metric("⛏️ Produksi", f"{df['Produksi'].iloc[-1]:,}")
col2.metric("💰 Harga", f"{df['Harga'].iloc[-1]:,}")
col3.metric("📈 MC", f"{df['MC'].iloc[-1]:,}")

# =========================
# DATA TRANSFORM (SIDEBAR EFFECT)
# =========================
df_sim = df.copy()

df_sim["Produksi_Simulasi"] = df_sim["Produksi"] * (resource_efficiency / 100)
df_sim["Harga_Simulasi"] = df_sim["Harga"] * (price_factor / 100)
df_sim["MC_Simulasi"] = df_sim["MC"] * (cost_pressure / 100)

# =========================
# GRAFIK
# =========================
st.subheader("📈 Tren Produksi (Aktual vs Simulasi)")
st.line_chart(df_sim.set_index("Tahun")[["Produksi", "Produksi_Simulasi"]])

st.subheader("💰 Tren Harga")
st.line_chart(df_sim.set_index("Tahun")[["Harga", "Harga_Simulasi"]])

st.subheader("📊 Tren MC")
st.line_chart(df_sim.set_index("Tahun")[["MC", "MC_Simulasi"]])

# =========================
# ANALISIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

if market == "Persaingan Sempurna":
    text = "Pasar kompetitif → produksi tinggi dan sensitif terhadap efisiensi."
elif market == "Monopoli":
    text = "Monopoli → produksi lebih terkendali dan stabil."
else:
    text = "Oligopoli → produksi moderat karena interaksi beberapa perusahaan."

if price_factor > 120:
    text += " Harga tinggi meningkatkan insentif produksi."
if cost_pressure > 120:
    text += " Tekanan biaya tinggi menurunkan profitabilitas."
if resource_efficiency > 120:
    text += " Efisiensi tinggi meningkatkan output produksi."

st.info(text)

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Lengkap & Simulasi")
st.dataframe(df_sim, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("PBL SDA | PT Vale Indonesia | Universitas Islam Bandung")
