```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================
# KONFIGURASI HALAMAN
# =========================
st.set_page_config(
    page_title="Dashboard Simulasi Ekonomi Nikel",
    layout="wide",
    page_icon="📊"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
.main {
    background-color: #f4f7fb;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3 {
    color: #1d3557;
}

[data-testid="stMetric"] {
    background-color: white;
    border-radius: 15px;
    padding: 20px;
    box-shadow: 0px 3px 10px rgba(0,0,0,0.08);
    text-align: center;
}

.sidebar .sidebar-content {
    background-color: white;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.title("📈 Dashboard Simulasi Ekonomi Nikel")

st.markdown("""
Dashboard ini digunakan untuk mensimulasikan pengaruh struktur pasar terhadap eksploitasi sumber daya nikel.  
Simulasi mempertimbangkan:
- Harga Nikel
- Tingkat Diskonto
- Green Taxes
- Struktur Pasar
""")

# =========================
# SIDEBAR
# =========================
st.sidebar.header("⚙️ Pengaturan Simulasi")

market = st.sidebar.selectbox(
    "Struktur Pasar",
    [
        "Persaingan Sempurna",
        "Monopoli",
        "Oligopoli"
    ]
)

price = st.sidebar.slider(
    "Harga Nikel",
    50,
    500,
    200
)

discount = st.sidebar.slider(
    "Tingkat Diskonto (%)",
    1,
    20,
    5
)

green_tax = st.sidebar.slider(
    "Green Taxes (%)",
    0,
    50,
    10
)

initial_stock = st.sidebar.number_input(
    "Cadangan Awal",
    min_value=1000,
    max_value=1000000,
    value=10000,
    step=1000
)

years = st.sidebar.slider(
    "Periode Simulasi",
    5,
    50,
    20
)

# =========================
# LOGIKA EKONOMI
# =========================
base_production = 500

if market == "Persaingan Sempurna":
    market_factor = 1.3
elif market == "Monopoli":
    market_factor = 0.8
else:
    market_factor = 1.0

production = (
    base_production *
    market_factor *
    (price / 200) *
    (1 - green_tax / 100) *
    (1 - discount / 100)
)

# =========================
# SIMULASI DATA
# =========================
tahun = []
stok = []
produksi = []

remaining_stock = initial_stock

for year in range(1, years + 1):

    remaining_stock -= production

    if remaining_stock < 0:
        remaining_stock = 0

    tahun.append(year)
    stok.append(remaining_stock)
    produksi.append(production)

    if remaining_stock <= 0:
        break

df = pd.DataFrame({
    "Tahun": tahun,
    "Produksi": produksi,
    "Stok": stok
})

# =========================
# METRICS
# =========================
st.subheader("📌 Indikator Utama")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⛏️ Volume Produksi",
        f"{production:,.0f} ton/tahun"
    )

with col2:
    st.metric(
        "📦 Sisa Stok",
        f"{remaining_stock:,.0f} ton"
    )

with col3:
    st.metric(
        "⏳ Waktu Habis",
        f"{len(df)} tahun"
    )

# =========================
# GRAFIK PRODUKSI
# =========================
st.subheader("📊 Grafik Volume Produksi")

fig1 = px.area(
    df,
    x="Tahun",
    y="Produksi",
    title="Perkembangan Produksi Nikel"
)

st.plotly_chart(fig1, use_container_width=True)

# =========================
# GRAFIK STOK
# =========================
st.subheader("📉 Grafik Sisa Cadangan")

fig2 = px.line(
    df,
    x="Tahun",
    y="Stok",
    title="Perubahan Stok Cadangan"
)

st.plotly_chart(fig2, use_container_width=True)

# =========================
# ANALISIS OTOMATIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

analisis = ""

if market == "Persaingan Sempurna":
    analisis += """
    Pada pasar persaingan sempurna, perusahaan cenderung meningkatkan produksi karena persaingan tinggi.
    Harga memiliki pengaruh besar terhadap volume ekstraksi.
    """

elif market == "Monopoli":
    analisis += """
    Dalam struktur monopoli, produksi lebih terkendali karena pasar dikuasai satu perusahaan.
    Eksploitasi sumber daya cenderung lebih lambat.
    """

else:
    analisis += """
    Pada pasar oligopoli, produksi dipengaruhi oleh interaksi beberapa perusahaan besar.
    Tingkat produksi berada di antara monopoli dan persaingan sempurna.
    """

if green_tax >= 20:
    analisis += """

    Green taxes yang tinggi menekan produksi dan memperpanjang umur cadangan sumber daya.
    """

if price >= 300:
    analisis += """

    Harga nikel yang tinggi meningkatkan insentif ekstraksi sehingga produksi meningkat.
    """

if discount >= 10:
    analisis += """

    Tingkat diskonto yang tinggi mendorong eksploitasi sumber daya dalam jangka pendek.
    """

st.info(analisis)

# =========================
# DATAFRAME
# =========================
st.subheader("📋 Data Simulasi")

st.dataframe(
    df,
    use_container_width=True
)

# =========================
# KESIMPULAN
# =========================
st.subheader("📚 Kesimpulan")

st.success(f"""
Struktur pasar {market.lower()} menghasilkan volume produksi sekitar {production:,.0f} ton per tahun.
Dengan cadangan awal sebesar {initial_stock:,.0f} ton, sumber daya diperkirakan habis dalam {len(df)} tahun.
""")

# =========================
# FOOTER
# =========================
st.markdown("---")

st.caption("Dashboard Simulasi Ekonomi Nikel | Streamlit Project")
```
