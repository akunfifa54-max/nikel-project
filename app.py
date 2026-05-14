import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =========================================
# CONFIG
# =========================================

st.set_page_config(
    page_title="Analisis Intertemporal Nikel",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.stApp {
    background-color: #020817;
    color: white;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #1e1e2f;
}

.block-container {
    padding-top: 2rem;
}

.metric-card {
    background-color: #1e3a5f;
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
}

</style>
""", unsafe_allow_html=True)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.image(
    "https://upload.wikimedia.org/wikipedia/id/thumb/5/55/Logo_Unisba.svg/1200px-Logo_Unisba.svg.png",
    width=120
)

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
    "Pajak Karbon Future",
    0,
    100,
    20
)

# =========================================
# DATA
# =========================================

data = pd.read_csv("data_nikel.csv")

# =========================================
# HEADER
# =========================================

col1, col2 = st.columns([1,5])

with col1:
    st.image(
        "https://upload.wikimedia.org/wikipedia/id/thumb/5/55/Logo_Unisba.svg/1200px-Logo_Unisba.svg.png",
        width=150
    )

with col2:
    st.title("Analisis Intertemporal Sumber Daya Nikel")
    st.subheader("Ekonomi Sumber Daya Alam dan Lingkungan")

# =========================================
# INFO BOX
# =========================================

st.markdown("""
<div class="info-box">

### ANGGOTA KELOMPOK

1. Nama Anggota 1  
2. Nama Anggota 2  
3. Nama Anggota 3  

### DOSEN PENGAMPU

Nama Dosen

</div>
""", unsafe_allow_html=True)

# =========================================
# PARAMETER
# =========================================

st.subheader("📌 Parameter Dasar Analisis")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f"""
    <div class="metric-card">
    <h3>Harga 2023</h3>
    <h2>Rp {data['Harga_Nikel'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
    <h3>Produksi</h3>
    <h2>{data['Produksi_ton'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
    <h3>MC</h3>
    <h2>{data['MC'].iloc[-1]:,.0f}</h2>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
    <h3>Diskonto</h3>
    <h2>{diskonto}</h2>
    </div>
    """, unsafe_allow_html=True)

# =========================================
# TABEL
# =========================================

st.subheader("📊 Tabel Data Nikel")

st.dataframe(data, use_container_width=True)

# =========================================
# GRAFIK
# =========================================

colA, colB = st.columns(2)

with colA:

    st.subheader("📈 Grafik Harga Nikel")

    fig1, ax1 = plt.subplots(figsize=(7,4))

    ax1.plot(
        data["Tahun"],
        data["Harga_Nikel"],
        marker='o',
        linewidth=3
    )

    ax1.set_facecolor("#0f172a")

    st.pyplot(fig1)

with colB:

    st.subheader("📉 Grafik Produksi")

    fig2, ax2 = plt.subplots(figsize=(7,4))

    ax2.plot(
        data["Tahun"],
        data["Produksi_ton"],
        marker='o',
        linewidth=3
    )

    ax2.set_facecolor("#0f172a")

    st.pyplot(fig2)

# =========================================
# HOTELLING
# =========================================

st.subheader("📌 Simulasi Hotelling Rule")

tahun = np.arange(0, 15)

harga = (
    harga_awal * np.exp(diskonto * tahun)
) + muc_awal + pajak

stock = 20000 - (tahun * 900)

colC, colD = st.columns(2)

with colC:

    fig3, ax3 = plt.subplots(figsize=(7,4))

    ax3.plot(
        tahun,
        harga,
        marker='o',
        linewidth=3
    )

    ax3.set_title("Kurva Harga Hotelling")

    st.pyplot(fig3)

with colD:

    fig4, ax4 = plt.subplots(figsize=(7,4))

    ax4.plot(
        tahun,
        stock,
        marker='o',
        linewidth=3
    )

    ax4.set_title("Kurva Sisa Cadangan")

    st.pyplot(fig4)

# =========================================
# HASIL
# =========================================

st.subheader("📖 Hasil Simulasi")

hasil = pd.DataFrame({
    "Tahun": tahun,
    "Prediksi Harga": harga,
    "Sisa Stock": stock
})

st.dataframe(hasil, use_container_width=True)
