import streamlit as st
import pandas as pd

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Simulasi Ekonomi Nikel",
    layout="wide",
    page_icon="⛏️"
)

# =========================
# CSS CERAH
# =========================
st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}

.block-container {
    padding: 2rem;
}

h1, h2, h3 {
    color: #1f4e79;
}

[data-testid="stMetric"] {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}
</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================
st.title("📊 Dashboard Simulasi Ekonomi Nikel")
st.write("Simulasi: Persaingan Sempurna, Monopoli, Oligopoli")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Parameter")

market = st.sidebar.selectbox(
    "Struktur Pasar",
    ["Persaingan Sempurna", "Monopoli", "Oligopoli"]
)

price = st.sidebar.slider("Harga Nikel", 50, 500, 200)
discount = st.sidebar.slider("Diskonto (%)", 1, 20, 5)
green_tax = st.sidebar.slider("Green Tax (%)", 0, 50, 10)

stock0 = st.sidebar.number_input("Stok Awal", 1000, 100000, 10000)
years = st.sidebar.slider("Tahun Simulasi", 5, 50, 20)

# =========================
# MODEL PASAR
# =========================
if market == "Persaingan Sempurna":
    factor = 1.3
elif market == "Monopoli":
    factor = 0.8
else:
    factor = 1.0

production = 500 * factor * (price/200) * (1 - green_tax/100) * (1 - discount/100)

# =========================
# SIMULASI
# =========================
stock = stock0
data = []

for t in range(1, years + 1):
    stock -= production
    if stock < 0:
        stock = 0

    data.append([t, production, stock])

    if stock == 0:
        break

df = pd.DataFrame(data, columns=["Tahun", "Produksi", "Stok"])

# =========================
# METRIC
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("⛏️ Produksi/Tahun", f"{production:,.0f}")
col2.metric("📦 Sisa Stok", f"{stock:,.0f}")
col3.metric("⏳ Waktu Habis", f"{len(df)} tahun")

# =========================
# GRAFIK (STREAMLIT NATIF)
# =========================
st.subheader("📉 Grafik Stok")
st.line_chart(df.set_index("Tahun")["Stok"])

st.subheader("📊 Grafik Produksi")
st.area_chart(df.set_index("Tahun")["Produksi"])

# =========================
# ANALISIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

text = ""

if market == "Persaingan Sempurna":
    text = "Persaingan tinggi → produksi lebih agresif dan cepat mengurangi stok."
elif market == "Monopoli":
    text = "Monopoli → produksi lebih terkontrol sehingga stok lebih awet."
else:
    text = "Oligopoli → produksi berada di tingkat moderat karena ada beberapa pemain besar."

if green_tax > 20:
    text += " Green tax tinggi menekan produksi."
if discount > 10:
    text += " Diskonto tinggi mempercepat eksploitasi."
if price > 300:
    text += " Harga tinggi meningkatkan produksi."

st.info(text)

# =========================
# DATA
# =========================
st.subheader("📋 Data Simulasi")
st.dataframe(df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Dashboard Simulasi Ekonomi Nikel")
