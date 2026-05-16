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
# CUSTOM CSS (TEMA CERAH)
# =========================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.stMetric {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
}

h1, h2, h3 {
    color: #1f4e79;
}

.sidebar .sidebar-content {
    background-color: #ffffff;
}
</style>
""", unsafe_allow_html=True)

# =========================
# JUDUL
# =========================
st.title("📈 Dashboard Simulasi Ekonomi Nikel")
st.markdown("""
Dashboard ini mensimulasikan dampak struktur pasar terhadap eksploitasi sumber daya nikel 
dengan mempertimbangkan harga, tingkat diskonto, dan green taxes.
""")

# =========================
# SIDEBAR INPUT
# =========================
st.sidebar.header("⚙️ Pengaturan Simulasi")

market = st.sidebar.selectbox(
    "Pilih Struktur Pasar",
    ["Persaingan Sempurna", "Monopoli", "Oligopoli"]
)

price = st.sidebar.slider(
    "Harga Nikel",
    50, 500, 200
)

discount = st.sidebar.slider(
    "Tingkat Diskonto (%)",
    1, 20, 5
)

green_tax = st.sidebar.slider(
    "Green Taxes (%)",
    0, 50, 10
)

initial_stock = st.sidebar.number_input(
    "Stok Cadangan Awal",
    min_value=1000,
    value=10000
)

years = st.sidebar.slider(
    "Periode Simulasi (Tahun)",
    5, 50, 20
)

# =========================
# LOGIKA PASAR
# =========================
base_production = 500

if market == "Persaingan Sempurna":
    production_factor = 1.3
elif market == "Monopoli":
    production_factor = 0.8
else:
    production_factor = 1.0

# Pengaruh variabel ekonomi
production = (
    base_production *
    production_factor *
    (price / 200) *
    (1 - green_tax / 100) *
    (1 - discount / 100)
)

# =========================
# SIMULASI DATA
# =========================
year_list = []
stock_list = []
production_list = []

stock = initial_stock

for year in range(1, years + 1):
    stock -= production

    if stock < 0:
        stock = 0

    year_list.append(year)
    stock_list.append(stock)
    production_list.append(production)

    if stock <= 0:
        break

df = pd.DataFrame({
    "Tahun": year_list,
    "Stok": stock_list,
    "Produksi": production_list
})

# =========================
# METRICS
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "⛏️ Volume Produksi",
        f"{production:,.0f} ton/tahun"
    )

with col2:
    st.metric(
        "📦 Sisa Stok",
        f"{stock:,.0f} ton"
    )

with col3:
    st.metric(
        "⏳ Estimasi Waktu Habis",
        f"{len(df)} tahun"
    )

# =========================
# GRAFIK PRODUKSI
# =========================
st.subheader("📊 Grafik Volume Produksi")

fig_prod = px.area(
    df,
    x="Tahun",
    y="Produksi",
    title="Volume Produksi Nikel"
)

st.plotly_chart(fig_prod, use_container_width=True)

# =========================
# GRAFIK STOK
# =========================
st.subheader("📉 Grafik Sisa Cadangan")

fig_stock = px.line(
    df,
    x="Tahun",
    y="Stok",
    title="Perubahan Stok Cadangan"
)

st.plotly_chart(fig_stock, use_container_width=True)

# =========================
# ANALISIS OTOMATIS
# =========================
st.subheader("🧠 Analisis Ekonomi")

analysis = ""

if market == "Persaingan Sempurna":
    analysis += """
    Pada struktur pasar persaingan sempurna, perusahaan cenderung meningkatkan produksi 
    karena tekanan kompetisi tinggi. Produksi menjadi lebih responsif terhadap perubahan harga.
    """

elif market == "Monopoli":
    analysis += """
    Dalam pasar monopoli, perusahaan lebih mengontrol produksi sehingga eksploitasi 
    sumber daya cenderung lebih lambat dibanding pasar kompetitif.
    """

else:
    analysis += """
    Pada pasar oligopoli, produksi dipengaruhi interaksi antar perusahaan besar sehingga 
    tingkat ekstraksi berada di antara monopoli dan persaingan sempurna.
    """

if green_tax > 20:
    analysis += """
    
    Green taxes yang tinggi menekan aktivitas produksi dan memperpanjang umur cadangan sumber daya.
    """

if price > 300:
    analysis += """
    
    Harga nikel yang tinggi meningkatkan insentif ekstraksi sehingga produksi meningkat signifikan.
    """

if discount > 10:
    analysis += """
    
    Tingkat diskonto yang tinggi mendorong eksploitasi sumber daya dalam jangka pendek.
    """

st.info(analysis)

# =========================
# TABEL DATA
# =========================
st.subheader("📋 Data Simulasi")

st.dataframe(df, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Dashboard Simulasi Ekonomi Nikel - Streamlit Project")
```
