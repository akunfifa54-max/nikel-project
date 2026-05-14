import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =====================================
# CONFIG
# =====================================

st.set_page_config(
    page_title="Ekonomi SDA Nikel",
    layout="wide"
)

# =====================================
# TITLE
# =====================================

st.title("⛏️ Analisis Ekonomi SDA: Nikel")

st.write("""
Dashboard analisis ekonomi sumber daya alam dan lingkungan
menggunakan data produksi, harga nikel,
dan simulasi Hotelling Rule.
""")

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("⚙️ Kontrol Simulasi")

harga_awal = st.sidebar.slider(
    "Harga Nikel Awal",
    100000,
    300000,
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
    50000,
    20000
)

# =====================================
# DATA
# =====================================

data = pd.read_csv("data_nikel.csv")

# =====================================
# METRIC
# =====================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Harga Nikel 2023",
        f"Rp {data['Harga_Nikel'].iloc[-1]:,.0f}"
    )

with col2:
    st.metric(
        "Produksi 2023",
        f"{data['Produksi_ton'].iloc[-1]:,.0f} ton"
    )

with col3:
    st.metric(
        "MC 2023",
        f"Rp {data['MC'].iloc[-1]:,.0f}"
    )

# =====================================
# TABEL
# =====================================

st.subheader("📊 Tabel Data Nikel")

st.dataframe(
    data,
    use_container_width=True
)

# =====================================
# GRAFIK HARGA
# =====================================

st.subheader("📈 Grafik Harga Nikel")

fig1, ax1 = plt.subplots(figsize=(10,5))

ax1.plot(
    data["Tahun"],
    data["Harga_Nikel"],
    marker='o',
    linewidth=3
)

ax1.set_xlabel("Tahun")
ax1.set_ylabel("Harga Nikel")

st.pyplot(fig1)

# =====================================
# GRAFIK PRODUKSI
# =====================================

st.subheader("📉 Grafik Produksi Nikel")

fig2, ax2 = plt.subplots(figsize=(10,5))

ax2.plot(
    data["Tahun"],
    data["Produksi_ton"],
    marker='o',
    linewidth=3
)

ax2.set_xlabel("Tahun")
ax2.set_ylabel("Produksi (ton)")

st.pyplot(fig2)

# =====================================
# HOTELLING
# =====================================

st.subheader("📌 Kurva Hotelling Rule")

tahun = np.arange(0, 15)

harga_simulasi = (
    harga_awal * np.exp(diskonto * tahun)
) + muc_awal

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.plot(
    tahun,
    harga_simulasi,
    marker='o',
    linewidth=3
)

ax3.set_xlabel("Tahun")
ax3.set_ylabel("Prediksi Harga")

st.pyplot(fig3)

# =====================================
# ANALISIS
# =====================================

st.subheader("📖 Analisis")

st.write("""
Grafik menunjukkan bahwa harga nikel
cenderung meningkat dalam jangka panjang,
sementara produksi mengalami fluktuasi.
Simulasi Hotelling menunjukkan bahwa
harga sumber daya akan meningkat seiring waktu
karena kelangkaan sumber daya alam.
""")
