import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Judul
st.title("Analisis Nikel")

# Membaca data
data = pd.read_csv("data_nikel.csv")

# Menampilkan tabel
st.subheader("Data Historis Nikel")
st.dataframe(data)

# Membuat grafik
st.subheader("Grafik Harga Nikel")

fig, ax = plt.subplots()

ax.plot(data["Tahun"], data["Harga_Nikel"])

ax.set_xlabel("Tahun")
ax.set_ylabel("Harga Nikel")

st.pyplot(fig)import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Judul
st.title("Analisis Ekonomi SDA: Nikel")

st.write("""
Dashboard simulasi ekonomi sumber daya alam dan lingkungan
untuk menganalisis harga dan stok nikel.
""")

# =========================
# SIDEBAR
# =========================

st.sidebar.title("⚙️ Kontrol Simulasi")

# Input simulasi
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
    "MUC Awal (λ0) $",
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

# =========================
# DATA HISTORIS
# =========================

data = pd.read_csv("data_nikel.csv")

st.subheader("📊 Data Historis Nikel")
st.dataframe(data)

# =========================
# GRAFIK HISTORIS
# =========================

st.subheader("📈 Grafik Harga Historis")

fig1, ax1 = plt.subplots()

ax1.plot(
    data["Tahun"],
    data["Harga_Nikel"]
)

ax1.set_xlabel("Tahun")
ax1.set_ylabel("Harga Nikel")

st.pyplot(fig1)

# =========================
# SIMULASI HOTELLING
# =========================

st.subheader("📉 Simulasi Hotelling Rule")

tahun = np.arange(0, 11)

harga_simulasi = (
    harga_awal * np.exp(diskonto * tahun)
) + muc_awal + pajak_karbon

fig2, ax2 = plt.subplots()

ax2.plot(
    tahun,
    harga_simulasi
)

ax2.set_xlabel("Tahun")
ax2.set_ylabel("Prediksi Harga")

st.pyplot(fig2)

# =========================
# HASIL SIMULASI
# =========================

st.subheader("📌 Hasil Simulasi")

st.write("Harga Awal:", harga_awal)
st.write("Tingkat Diskonto:", diskonto)
st.write("MUC Awal:", muc_awal)
st.write("Pajak Karbon:", pajak_karbon)

# =========================
# KESIMPULAN
# =========================

st.subheader("📖 Kesimpulan")

st.write("""
Semakin tinggi tingkat diskonto dan pajak karbon,
maka harga sumber daya nikel di masa depan
akan meningkat lebih cepat sesuai pendekatan
Hotelling Rule dalam ekonomi sumber daya alam.
""")
