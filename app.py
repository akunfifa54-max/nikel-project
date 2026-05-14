import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Analisis Intertemporal Nikel",
    layout="wide"
)

# ====================================
# CSS
# ====================================

st.markdown("""
<style>

.stApp {
    background-color: #020817;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #1e1e2f;
}

h1,h2,h3,h4 {
    color: white;
}

.metric-card {
    background-color: #17375e;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    color: white;
}

.info-box {
    background-color: #17375e;
    padding: 25px;
    border-radius: 20px;
    color: white;
    margin-bottom: 30px;
}

</style>
""", unsafe_allow_html=True)

# ====================================
# SIDEBAR
# ====================================

st.sidebar.title("⚙️ Kontrol Simulasi")

harga_awal = st.sidebar.slider(
    "Harga Nikel (P0)",
    50000,
    400000,
    150000
)

diskonto = st.sidebar.slider(
    "Tingkat Diskonto (r)",
    0.01,
    0.20,
    0.05
)

muc_awal = st.sidebar.slider(
    "MUC Awal (λ0)",
    0,
    100000,
    20000
)

pajak = st.sidebar.slider(
    "Pajak Karbon Future ($)",
    0,
    100,
    20
)

# ====================================
# DATA
# ====================================

data = pd.read_csv("data_nikel.csv")

# ====================================
# HEADER
# ====================================

st.title("Analisis Intertemporal Sumber Daya Nikel")

st.subheader("Ekonomi SDA dan Lingkungan")

# ====================================
# INFO BOX
# ====================================

st.markdown("""
<div class="info-box">

<h2>KELOMPOK : 2</h2>

<h3>ANGGOTA</h3>

<p style="font-size:20px;">
1. Radea Rahman Dwiyana (10090224001)<br><br>

2. Bunga Wiati Manaki (10090224026)<br><br>

3. Shidqi Alhamdani Mieftah (10090224032)
</p>

<hr>

<h3>DOSEN</h3>

<p style="font-size:20px;">
Yuhka Sundaya, S.E., M.Si.
</p>

<hr>

<h3>MATA KULIAH</h3>

<p style="font-size:20px;">
Ekonomi SDA dan Lingkungan
</p>

</div>
""", unsafe_allow_html=True)

# ====================================
# PARAMETER
# ====================================

st.subheader("📌 Parameter Dasar Analisis")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <h3>Harga 2024</h3>
    <h2>{data['Harga'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <h3>Produksi</h3>
    <h2>{data['Produksi'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
    <h3>MC</h3>
    <h2>{data['mc'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
    <h3>Diskonto</h3>
    <h2>{diskonto}</h2>
    </div>
    """, unsafe_allow_html=True)

# ====================================
# TABEL
# ====================================

st.subheader("📊 Data Historis Produksi & Harga")

st.dataframe(data, use_container_width=True)

# ====================================
# GRAFIK
# ====================================

col1, col2 = st.columns(2)

with col1:

    st.subheader("📈 Grafik Harga Nikel")

    fig1, ax1 = plt.subplots(figsize=(7,4))

    ax1.plot(
        data["Tahun"],
        data["Harga"],
        marker='o',
        linewidth=3
    )

    st.pyplot(fig1)

with col2:

    st.subheader("📉 Grafik Produksi Nikel")

    fig2, ax2 = plt.subplots(figsize=(7,4))

    ax2.plot(
        data["Tahun"],
        data["Produksi"],
        marker='o',
        linewidth=3
    )

    st.pyplot(fig2)

# ====================================
# SIMULASI
# ====================================

st.subheader("📌 Simulasi Hotelling Rule")

tahun = np.arange(2014, 2025)

harga = (
    harga_awal *
    np.exp(
        diskonto * np.arange(len(tahun))
    )
) + muc_awal + pajak

stock = np.linspace(20000, 10000, len(tahun))

# ====================================
# KURVA
# ====================================

col3, col4 = st.columns(2)

with col3:

    st.subheader("📈 Kurva Harga Hotelling")

    fig3, ax3 = plt.subplots(figsize=(7,4))

    ax3.plot(
        tahun,
        harga,
        marker='o',
        linewidth=3
    )

    st.pyplot(fig3)

with col4:

    st.subheader("📉 Kurva Sisa Cadangan")

    fig4, ax4 = plt.subplots(figsize=(7,4))

    ax4.plot(
        tahun,
        stock,
        marker='o',
        linewidth=3
    )

    st.pyplot(fig4)

# ====================================
# HASIL SIMULASI
# ====================================

st.subheader("📖 Hasil Simulasi")

hasil = pd.DataFrame({
    "Tahun": tahun,
    "Prediksi Harga": harga,
    "Sisa Stock": stock
})

st.dataframe(hasil, use_container_width=True)
