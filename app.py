import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ====================================
# CONFIG
# ====================================

st.set_page_config(
    page_title="Ekonomi SDA - Nikel",
    layout="wide"
)

# ====================================
# TITLE
# ====================================

st.title("⛏️ Analisis Ekonomi SDA: Nikel")
st.markdown("""
Dashboard simulasi ekonomi sumber daya alam dan lingkungan  
untuk menganalisis harga dan stok nikel menggunakan pendekatan Hotelling Rule.
""")

# ====================================
# SIDEBAR
# ====================================

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

# ====================================
# DATA
# ====================================

data = pd.read_csv("data_nikel.csv")

# ====================================
# METRICS
# ====================================

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

# ====================================
# TABEL DATA
# ====================================

st.subheader("📊 Data Historis Nikel")

st.dataframe(
    data,
    use_container_width=True
)

# ====================================
# GRAFIK HISTORIS
# ====================================

st.subheader("📈 Grafik Harga Historis")

fig1, ax1 = plt.subplots(figsize=(10,5))

ax1.plot(
    data["Tahun"],
    data["Harga_Nikel"],
    linewidth=3
)

ax1.set_xlabel("Tahun")
ax1.set_ylabel("Harga Nikel")

st.pyplot(fig1)

# ====================================
# SIMULASI HOTELLING
# ====================================

st.subheader("📉 Simulasi Hotelling Rule")

tahun = np.arange(0, 15)

harga_simulasi = (
    harga_awal * np.exp(diskonto * tahun)
) + muc_awal + pajak_karbon

fig2, ax2 = plt.subplots(figsize=(10,5))

ax2.plot(
    tahun,
    harga_simulasi,
    linewidth=3
)

ax2.set_xlabel("Tahun")
ax2.set_ylabel("Prediksi Harga")

st.pyplot(fig2)

# ====================================
# ANALISIS
# ====================================

st.subheader("📌 Analisis")

st.write(f"""
Dengan harga awal sebesar ${harga_awal},
tingkat diskonto {diskonto:.2f},
MUC awal {muc_awal},
dan pajak karbon ${pajak_karbon},
maka harga nikel diproyeksikan meningkat
seiring waktu sesuai teori Hotelling Rule.
""")

# ====================================
# KESIMPULAN
# ====================================

st.subheader("📖 Kesimpulan")

st.success("""
Semakin tinggi tingkat diskonto dan pajak karbon,
maka harga sumber daya nikel di masa depan
akan meningkat lebih cepat.
""")
