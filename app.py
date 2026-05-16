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
# HEADER + LOGO SAFE
# =========================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists("logo_unisba.png"):
        st.image("logo_unisba.png", width=120)

with col2:
    st.title("📊 PBL Ekonomi Sumber Daya Alam")
    st.subheader("⛏️ PT Vale Indonesia (Data 2014–2024)")

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
# SIDEBAR (FULL CONTROL PANEL)
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
st.sidebar.info("Data: PT Vale Indonesia 2014–2024")

# =========================
# DATA (FIXED & CLEAN)
# =========================
df = pd.DataFrame({
    "Tahun": [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    "Produksi": [78726000, 81177000, 77581000, 76807000, 74806000, 71025000, 72237000, 65388000, 60090000, 70728000, 71311000],
    "Harga": [155425900, 127648400, 98366800, 108620400, 145862400, 196511700, 201144200, 260717600, 370685700, 252293500, 237823600],
    "MC": [15163, 15940, 16758, 17617, 18520, 19470, 20468, 21517, 22621, 23780, 25000]
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
# SIMULASI EFFECT (SIDEBAR IMPACT)
# =========================
df_sim = df.copy()

df_sim["Produksi_Simulasi"] = df_sim["Produksi"] * (efficiency / 100) * (1 - discount / 100)
df_sim["Harga_Simulasi"] = df_sim["Harga"] * (price_factor / 100)
df_sim["MC_Simulasi"] = df_sim["MC"] * (cost_pressure / 100)

# =========================
# GRAFIK
# =========================
st.subheader("📈 Produksi (Aktual vs Simulasi)")
st.line_chart(df_sim.set_index("Tahun")[["Produksi", "Produksi_Simulasi"]])

st.subheader("💰 Harga (Aktual vs Simulasi)")
st.line_chart(df_sim.set_index("Tahun")[["Harga", "Harga_Simulasi"]])

st.subheader("📊 MC (Aktual vs Simulasi)")
st.line_chart(df_sim.set_index("Tahun")[["MC", "MC_Simulasi"]])

# =========================
# ANALISIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

text = ""

if market == "Persaingan Sempurna":
    text = "Pasar kompetitif → produksi tinggi dan efisien."
elif market == "Monopoli":
    text = "Monopoli → produksi lebih rendah dan terkontrol."
else:
    text = "Oligopoli → produksi stabil di tingkat menengah."

if green_tax > 20:
    text += " Green tax tinggi menekan produksi."
if discount > 10:
    text += " Diskonto tinggi mempercepat eksploitasi."
if price_factor > 120:
    text += " Harga tinggi meningkatkan produksi."

st.info(text)

# =========================
# TABLE
# =========================
st.subheader("📋 Data Lengkap & Simulasi")
st.dataframe(df_sim, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("PBL SDA | PT Vale Indonesia | UNISBA")
# =========================
# KESIMPULAN
# =========================
st.subheader("📌 Kesimpulan")

st.markdown("""
Dari hasil analisis data industri nikel PT Vale Indonesia periode 2014–2024, dapat disimpulkan bahwa:

- Produksi nikel mengalami fluktuasi dengan kecenderungan penurunan pada beberapa periode, yang menunjukkan adanya tekanan pada sisi produksi dan efisiensi sumber daya.
- Harga nikel menunjukkan tren peningkatan signifikan hingga tahun 2022, yang mencerminkan meningkatnya permintaan global terhadap nikel sebagai bahan baku industri baterai dan energi.
- Biaya marginal (MC) terus meningkat dari tahun ke tahun, yang mengindikasikan bahwa biaya ekstraksi sumber daya semakin mahal akibat menurunnya kualitas atau ketersediaan cadangan.

Secara keseluruhan, industri nikel menunjukkan karakteristik sumber daya alam yang semakin langka (scarcity resource), di mana peningkatan harga tidak selalu diikuti oleh peningkatan produksi secara proporsional.

Hal ini menegaskan pentingnya pengelolaan sumber daya yang efisien, kebijakan lingkungan seperti green tax, serta strategi produksi yang mempertimbangkan keberlanjutan jangka panjang.
""")
