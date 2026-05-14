import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ======================================
# PAGE CONFIG
# ======================================

st.set_page_config(
    page_title="Ekonomi SDA - Nikel",
    layout="wide"
)

# ======================================
# JUDUL
# ======================================

st.title("⛏️ Analisis Ekonomi SDA: Nikel")

st.write("""
Dashboard analisis ekonomi sumber daya alam dan lingkungan
untuk melihat perkembangan harga dan stok nikel
menggunakan pendekatan Hotelling Rule.
""")

# ======================================
# SIDEBAR
# ======================================

st.sidebar.title("⚙️ Kontrol Simulasi")

harga_awal = st.sidebar.slider(
    "Harga Nikel Awal ($)",
    40.0,
    150.0,
    80.0
)

diskonto = st.sidebar.slider(
    "Tingkat Diskonto (r)",
    0.01,
    0.20,
    0.05
)

muc_awal = st.sidebar.slider(
    "MUC Awal (λ0)",
    0.0,
    100.0,
    20.0
)

pajak_karbon = st.sidebar.slider(
    "Pajak Karbon Future ($)",
    0.0,
    200.0,
    50.0
)

# ======================================
# DATA
# ======================================

data = pd.read_csv("data_nikel.csv")

# ======================================
# METRIC
# ======================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Harga Terakhir",
        f"${data['Harga_Nikel'].iloc[-1]}"
    )

with col2:
    st.metric(
        "Stock Terakhir",
        f"{data['Stock_Nikel'].iloc[-1]}"
    )

with col3:
    st.metric(
        "Diskonto",
        f"{diskonto:.2f}"
    )

# ======================================
# TABEL DATA
# ======================================

st.subheader("📊 Tabel Data Historis Nikel")

st.dataframe(
    data,
    use_container_width=True
)

# ======================================
# GRAFIK HARGA
# ======================================

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

# ======================================
# GRAFIK STOCK
# ======================================

st.subheader("📉 Grafik Stock Nikel")

fig2, ax2 = plt.subplots(figsize=(10,5))

ax2.plot(
    data["Tahun"],
    data["Stock_Nikel"],
    marker='o',
    linewidth=3
)

ax2.set_xlabel("Tahun")
ax2.set_ylabel("Stock Nikel")

st.pyplot(fig2)

# ======================================
# KURVA HOTELLING
# ======================================

st.subheader("📌 Kurva Hotelling Rule")

tahun_simulasi = np.arange(0, 15)

harga_simulasi = (
    harga_awal * np.exp(diskonto * tahun_simulasi)
) + muc_awal + pajak_karbon

fig3, ax3 = plt.subplots(figsize=(10,5))

ax3.plot(
    tahun_simulasi,
    harga_simulasi,
    marker='o',
    linewidth=3
)

ax3.set_xlabel("Tahun")
ax3.set_ylabel("Prediksi Harga Nikel")

st.pyplot(fig3)

# ======================================
# ANALISIS
# ======================================

st.subheader("📖 Analisis")

st.write(f"""
Dengan harga awal sebesar ${harga_awal},
tingkat diskonto {diskonto:.2f},
MUC awal sebesar {muc_awal},
dan pajak karbon sebesar ${pajak_karbon},
maka harga nikel diproyeksikan meningkat
seiring waktu mengikuti teori Hotelling Rule.
""")

# ======================================
# KESIMPULAN
# ======================================

st.subheader("✅ Kesimpulan")

st.success("""
Semakin tinggi tingkat diskonto dan pajak karbon,
maka harga sumber daya nikel di masa depan
akan meningkat lebih cepat.
""")
