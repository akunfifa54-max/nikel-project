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

st.pyplot(fig)