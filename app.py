import streamlit as st
import pandas as pd

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="PBL Ekonomi SDA - Nikel",
    layout="wide",
    page_icon="⛏️"
)

# =========================
# CSS CLEAN MODERN
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}

.block-container {
    padding: 2rem 2.5rem;
}

h1, h2, h3 {
    color: #0b3d91;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 16px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📊 PBL Ekonomi SDA - Simulasi Nikel")
st.subheader("⛏️ PT Vale Indonesia")

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
# SIDEBAR INPUT
# =========================
st.sidebar.header("⚙️ Parameter Simulasi")

market = st.sidebar.selectbox(
    "Struktur Pasar",
    ["Persaingan Sempurna", "Monopoli", "Oligopoli"]
)

price = st.sidebar.slider("Harga Nikel", 50, 500, 200)
discount = st.sidebar.slider("Tingkat Diskonto (%)", 1, 20, 5)
green_tax = st.sidebar.slider("Green Tax (%)", 0, 50, 10)
stock0 = st.sidebar.number_input("Stok Awal (ton)", 1000, 100000, 10000)

st.sidebar.info("Periode tetap: 2014 - 2024")

# =========================
# TIME RANGE
# =========================
years = list(range(2014, 2025))

# =========================
# MARKET STRUCTURE MODEL
# =========================
if market == "Persaingan Sempurna":
    market_factor = 1.3
elif market == "Monopoli":
    market_factor = 0.8
else:
    market_factor = 1.0

base_production = 500 * market_factor * (price/200) * (1 - green_tax/100) * (1 - discount/100)

# =========================
# SIMULASI DINAMIS (REALISTIS)
# =========================
stock = stock0
data = []

for y in years:

    # efek kelangkaan (semakin sedikit stok → produksi turun)
    scarcity = stock / stock0

    production = base_production * (0.4 + scarcity)

    stock -= production
    if stock < 0:
        stock = 0

    data.append([y, production, stock])

    if stock == 0:
        break

df = pd.DataFrame(data, columns=["Tahun", "Produksi", "Stok"])

# =========================
# KPI DASHBOARD
# =========================
st.subheader("📌 Indikator Utama")

col1, col2, col3 = st.columns(3)

col1.metric("⛏️ Produksi/Tahun", f"{df['Produksi'].iloc[-1]:,.0f} ton")
col2.metric("📦 Sisa Stok", f"{df['Stok'].iloc[-1]:,.0f} ton")
col3.metric("📅 Tahun Efektif", f"{len(df)} tahun")

# =========================
# GRAFIK (STYLE PBL)
# =========================
st.subheader("📈 Tren Produksi & Stok")

col4, col5 = st.columns(2)

with col4:
    st.line_chart(df.set_index("Tahun")[["Stok"]])
    st.caption("📉 Penurunan stok nikel (2014–2024)")

with col5:
    st.area_chart(df.set_index("Tahun")[["Produksi"]])
    st.caption("📊 Dinamika produksi nikel")

# =========================
# ANALISIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

text = ""

if market == "Persaingan Sempurna":
    text += "Pasar kompetitif mendorong produksi lebih tinggi."
elif market == "Monopoli":
    text += "Monopoli menekan produksi sehingga eksploitasi lebih lambat."
else:
    text += "Oligopoli menghasilkan produksi moderat."

if green_tax > 20:
    text += " Green tax tinggi menurunkan aktivitas ekstraksi."
if discount > 10:
    text += " Diskonto tinggi mempercepat eksploitasi sumber daya."
if price > 300:
    text += " Harga tinggi meningkatkan insentif produksi."

st.info(text)

# =========================
# DATA TABLE
# =========================
st.subheader("📋 Data Simulasi (2014–2024)")
st.dataframe(df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("PT Vale Indonesia | PBL Ekonomi Sumber Daya Alam")
