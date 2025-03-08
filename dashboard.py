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

main_data = load_data()

# Dashboard
def main():
    # Menampilkan data
    st.header("Data Kualitas Udara")
    st.write(main_data.head())
    
    # Visualisasi Tren Polutan
    st.header("Tren Rata-rata Tahunan Polutan")
    main_data['date'] = pd.to_datetime(main_data[['year', 'month', 'day', 'hour']])
    annual_pollutant_means = main_data.groupby(main_data['date'].dt.year)[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']].mean()

    fig, ax = plt.subplots(figsize=(14, 8))
    ax.plot(annual_pollutant_means.index, annual_pollutant_means['PM2.5'], label='PM2.5', marker='o')
    ax.plot(annual_pollutant_means.index, annual_pollutant_means['PM10'], label='PM10', marker='o')
    ax.plot(annual_pollutant_means.index, annual_pollutant_means['SO2'], label='SO2', marker='o')
    ax.plot(annual_pollutant_means.index, annual_pollutant_means['NO2'], label='NO2', marker='o')
    ax.plot(annual_pollutant_means.index, annual_pollutant_means['CO'], label='CO', marker='o')
    ax.plot(annual_pollutant_means.index, annual_pollutant_means['O3'], label='O3', marker='o')
    ax.set_title('Tren Rata-rata Tahunan dari Berbagai Polutan')
    ax.set_xlabel('Tahun')
    ax.set_ylabel('Rata-rata Konsentrasi')
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
    
    # Analisis Pengaruh Faktor Lingkungan terhadap CO
    st.header("Pengaruh Faktor Lingkungan terhadap Konsentrasi CO")
    st.subheader("Hubungan Suhu dan CO")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(main_data['TEMP'], main_data['CO'], alpha=0.5)
    ax.set_title('Hubungan antara Suhu dan CO')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Konsentrasi CO')
    ax.grid(True)
    st.pyplot(fig)
    
    st.subheader("Hubungan Curah Hujan dan CO")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(main_data['RAIN'], main_data['CO'], alpha=0.5)
    ax.set_title('Hubungan antara Curah Hujan dan CO')
    ax.set_xlabel('Curah Hujan (mm)')
    ax.set_ylabel('Konsentrasi CO')
    ax.grid(True)
    st.pyplot(fig)
    
    st.subheader("Hubungan Kecepatan Angin dan CO")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(main_data['WSPM'], main_data['CO'], alpha=0.5)
    ax.set_title('Hubungan antara Kecepatan Angin dan CO')
    ax.set_xlabel('Kecepatan Angin (m/s)')
    ax.set_ylabel('Konsentrasi CO')
    ax.grid(True)
    st.pyplot(fig)
    
    st.subheader("Hubungan Tekanan Udara dan CO")
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.scatter(main_data['PRES'], main_data['CO'], alpha=0.5)
    ax.set_title('Hubungan antara Tekanan Udara dan CO')
    ax.set_xlabel('Tekanan Udara (hPa)')
    ax.set_ylabel('Konsentrasi CO')
    ax.grid(True)
    st.pyplot(fig)
    
    # Kategorisasi CO
    st.header("Kategorisasi Konsentrasi CO")
    main_data['Kategori_CO'] = main_data['CO'].apply(lambda x: "Aman" if x < 70 else ("Tinggi" if 70 <= x < 150 else "Sangat Tinggi"))
    st.write(main_data[['station', 'CO', 'Kategori_CO']].head())
    
    # Ringkasan Kategori CO per Stasiun
    st.subheader("Ringkasan Kategori Kejadian Kadar CO per Stasiun")
    ringkasan_kategori_co = main_data.groupby('station')['Kategori_CO'].value_counts().unstack(fill_value=0)
    st.write(ringkasan_kategori_co)
    
    # Kesimpulan
    st.header("Kesimpulan")
    st.write("""
    - Kadar gas yang memiliki rata-rata tertinggi adalah gas CO.
    - Kecepatan angin dan curah hujan mempengaruhi kadar CO. Apabila kecepatan angin dan curah hujan tinggi, maka dapat mengurangi konsentrasi kadar CO.
    - Stasiun kerap kali memiliki kadar CO yang sangat tinggi yang dapat berbahaya bagi kesehatan, diperlukan tindakan lebih lanjut untuk menangani kadar konsentrasi CO yang tinggi.
    """)

if __name__ == "__main__":
    main()
