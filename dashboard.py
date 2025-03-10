# -*- coding: utf-8 -*-
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Judul 
st.title("Proyek Analisis Data: Air Quality Dataset")
st.write("**Nama:** Daffa Akifah Balqis")
st.write("**Email:** daffaakifahbalqis@gmail.com")
st.write("**ID Dicoding:** daffabalqis")

# Membaca data
def load_data():
    data = pd.read_csv('main-data.csv')
    return data

data = load_data()

# Dashboard
def main():
    # Menampilkan data
    st.header("Data Kualitas Udara")
    st.sidebar.header("Pilihan Visualisasi")
visualization_option = st.sidebar.selectbox(
    "Pilih Visualisasi",
    ["Tren Polutan per Tahun", "Distribusi Polutan per Stasiun", "Analisis Lanjutan"]
)

# Main content
st.title("Analisis Kualitas Udara di Beijing")
st.write("""
    **Pertanyaan Bisnis:**
    1. Bagaimana tren rata-rata tahunan dari berbagai polutan (PM2.5, PM10, SO2, NO2, CO, O3) serta polutan apa yang paling tinggi secara keseluruhan dan persebaran di masing-masing stasiun?
    2. Bagaimana hubungan antar polutan serta pengaruh suhu, curah hujan, kecepatan angin, dan tekanan udara?
""")

if visualization_option == "Tren Polutan per Tahun":
    st.header("Tren Rata-rata Tahunan dari Berbagai Polutan")
    
    # Calculate annual means
    annual_pollutant_means = data.groupby(data['date'].dt.year)[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()
    
    # Plot
    plt.figure(figsize=(14, 8))
    for pollutant in annual_pollutant_means.columns:
        plt.plot(annual_pollutant_means.index, annual_pollutant_means[pollutant], label=pollutant, marker='o')
    
    plt.title('Tren Rata-rata Tahunan dari Berbagai Polutan')
    plt.xlabel('Tahun')
    plt.ylabel('Rata-rata Konsentrasi')
    plt.legend()
    plt.grid(True)
    st.pyplot(plt)

elif visualization_option == "Distribusi Polutan per Stasiun":
    st.header("Distribusi Polutan per Stasiun")
    
    polutan = st.selectbox("Pilih Polutan", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    
    # Calculate mean pollutant per station
    mean_pollutant = data.groupby('station')[polutan].mean().reset_index()
    
    # Plot
    plt.figure(figsize=(14, 8))
    sns.barplot(x='station', y=polutan, data=mean_pollutant, hue='station', palette='viridis')
    plt.title(f'Rata-rata Kadar {polutan} di Berbagai Stasiun')
    plt.xlabel('Stasiun')
    plt.ylabel(f'Rata-rata Kadar {polutan}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

elif visualization_option == "Analisis Lanjutan":
    st.header("Analisis Lanjutan: Kategorisasi Kadar CO")
    
    # Function to categorize CO levels
    def kategorikan_co(co_value):
        if co_value < 70:
            return "Aman"
        elif 70 <= co_value < 150:
            return "Tinggi"
        elif co_value >= 150:
            return "Sangat tinggi"
        else:
            return "Tidak Diketahui"
    
    # Apply categorization
    data['Kategori_CO'] = data['CO'].apply(kategorikan_co)
    
    # Summary table
    ringkasan_kategori_co = data.groupby('station')['Kategori_CO'].value_counts().unstack(fill_value=0)
    
    st.write("Tabel Ringkasan Kategori CO per Stasiun:")
    st.write(ringkasan_kategori_co)
    
    # Plot
    plt.figure(figsize=(14, 8))
    ringkasan_kategori_co.plot(kind='bar', stacked=True)
    plt.title('Distribusi Kategori CO per Stasiun')
    plt.xlabel('Stasiun')
    plt.ylabel('Jumlah')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(plt)

# Additional information
st.sidebar.header("Informasi Tambahan")
st.sidebar.write("""
    - **Dataset:** [Air Quality Dataset](https://github.com/daffaakifah/Analisis_Kualitas_Udara)
    - **Sumber Data:** [PRSA Data](https://archive.ics.uci.edu/ml/datasets/Beijing+PM2.5+Data)
    - **Dibuat oleh:** Daffa Akifah Balqis
""")
    
    # Kesimpulan
    st.header("Kesimpulan")
    st.write("""
    - Kadar gas yang memiliki rata-rata tertinggi adalah gas CO.
    - Kecepatan angin dan curah hujan mempengaruhi kadar CO. Apabila kecepatan angin dan curah hujan tinggi, maka dapat mengurangi konsentrasi kadar CO.
    - Stasiun kerap kali memiliki kadar CO yang sangat tinggi yang dapat berbahaya bagi kesehatan, diperlukan tindakan lebih lanjut untuk menangani kadar konsentrasi CO yang tinggi.
    """)

if __name__ == "__main__":
    main()
