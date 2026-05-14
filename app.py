import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="Ekonomi SDA - Nikel",
    layout="wide"
)

# ==================================================
# LOAD DATA
# ==================================================

data = pd.read_csv("data_nikel.csv")

# ==================================================
# TITLE
# ==================================================

st.title("⛏️ Dashboard Ekonomi SDA Nikel")

st.markdown("""
Analisis ekonomi sumber daya alam dan lingkungan
menggunakan pendekatan Hotelling Rule
untuk melihat dinamika harga, produksi,
dan kelangkaan sumber daya nikel.
""")

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.header("⚙️ Kontrol Simulasi")

harga_awal = st.sidebar.slider(
    "Harga Nikel Awal (Rp)",
    100000,
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
    "MUC Awal",
    10000,
    100000,
    20000
)

cadangan_awal = st.sidebar.slider(
    "Cadangan Awal",
    10000,
    50000,
    20000
)

# ==================================================
# METRIC CARDS
# ==================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Harga 2023",
        f"Rp {data['Harga_Nikel'].iloc[-1]:,.0f}"
    )

with col2:
    st.metric(
        "Produksi 2023",
        f"{data['Produksi_ton'].iloc[-1]:,.0f}"
    )

with col3:
    st.metric(
        "MC 2023",
        f"Rp {data['MC'].iloc[-1]:,.0f}"
    )

with col4:
    st.metric(
        "Diskonto",
        f"{diskonto:.2f}"
    )

# ==================================================
# TABEL DATA
# ==================================================

st.subheader("📊 Tabel Data Historis Nikel")

st.dataframe(
    data,
    use_container_width=True
)

# ==================================================
# GRAFIK HARGA
# ==================================================

colA, colB = st.columns(2)

with colA:

    st.subheader("📈 Harga Nikel")

    fig1, ax1 = plt.subplots(figsize=(7,4))

    ax1.plot(
        data["Tahun"],
        data["Harga_Nikel"],
        marker='o',
        linewidth=3
    )

    ax1.set_xlabel("Tahun")
    ax1.set_ylabel("Harga")

    st.pyplot(fig1)

with colB:

    st.subheader("📉 Produksi Nikel")

    fig2, ax2 = plt.subplots(figsize=(7,4))

    ax2.plot(
        data["Tahun"],
        data["Produksi_ton"],
        marker='o',
        linewidth=3
    )

    ax2.set_xlabel("Tahun")
    ax2.set_ylabel("Produksi")

    st.pyplot(fig2)

# ==================================================
# HOTELLING RULE
# ==================================================

st.subheader("📌 Simulasi Hotelling Rule")

tahun = np.arange(0, 15)

harga_simulasi = (
    harga_awal * np.exp(diskonto * tahun)
) + muc_awal

stock = cadangan_awal - (tahun * 900)

# ==================================================
# GRAFIK HOTELLING
# ==================================================

colC, colD = st.columns(2)

with colC:

    fig3, ax3 = plt.subplots(figsize=(7,4))

    ax3.plot(
        tahun,
        harga_simulasi,
        marker='o',
        linewidth=3
    )

    ax3.set_title("Kurva Harga Hotelling")

    ax3.set_xlabel("Tahun")
    ax3.set_ylabel("Harga")

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

    ax4.set_xlabel("Tahun")
    ax4.set_ylabel("Cadangan")

    st.pyplot(fig4)

# ==================================================
# HASIL SIMULASI
# ==================================================

st.subheader("📖 Hasil Simulasi")

hasil = pd.DataFrame({
    "Tahun": tahun,
    "Prediksi Harga": harga_simulasi,
    "Sisa Cadangan": stock
})

st.dataframe(
    hasil,
    use_container_width=True
)

# ==================================================
# ANALISIS
# ==================================================

st.subheader("✅ Analisis")

st.success(f"""
Dengan tingkat diskonto sebesar {diskonto:.2f},
harga sumber daya nikel diproyeksikan meningkat
mengikuti teori Hotelling Rule.

Semakin berkurang cadangan sumber daya,
harga nikel akan meningkat karena kelangkaan.
""")
