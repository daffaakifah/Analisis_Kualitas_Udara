import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
def load_data():
    data = pd.read_csv('main-data.csv')
    return data

data = load_data()

st.sidebar.header("Pilihan Visualisasi")
visualization_option = st.sidebar.selectbox(
    "Pilih Visualisasi",
    [
        "Tren Polutan per Tahun",
        "Distribusi Polutan per Stasiun",
        "Korelasi Antar Polutan",
        "Total dan Rata-rata Polutan"
    ]
)

# Main dashboard
st.title("Analisis Kualitas Udara di Beijing Tahun 2013-2017")
st.write("""
    **Pertanyaan Bisnis:**
    1. Bagaimana tren rata-rata tahunan dari berbagai polutan (PM2.5, PM10, SO2, NO2, CO, O3) serta polutan apa yang paling tinggi secara keseluruhan dan persebaran di masing-masing stasiun?
    2. Bagaimana hubungan antar polutan serta pengaruh suhu, curah hujan, kecepatan angin, dan tekanan udara?
""")

data['date'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
if visualization_option == "Tren Polutan per Tahun":
    st.header("Tren Rata-rata Tahunan dari Berbagai Polutan")
    
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

elif visualization_option == "Korelasi Antar Polutan":
    st.header("Korelasi Antar Polutan dan Variabel Meteorologi")
    
    # Correlation matrix
    correlation_matrix_all = data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'RAIN', 'WSPM']].corr()
    
    # Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix_all, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)
    plt.title("Matriks Korelasi: Polutan dan Variabel Meteorologi")
    st.pyplot(plt)

    # Scatter plots
    st.subheader("Scatter Plot Hubungan Antar Variabel")
    
    scatter_option = st.selectbox(
        "Pilih Scatter Plot",
        ["PM2.5 vs PM10", "TEMP vs PRES", "NO2 vs CO"]
    )
    
    if scatter_option == "PM2.5 vs PM10":
        plt.figure(figsize=(8, 6))
        plt.scatter(data['PM2.5'], data['PM10'])
        plt.title('Scatter Plot PM2.5 vs PM10')
        plt.xlabel('PM2.5')
        plt.ylabel('PM10')
        plt.grid(True)
        st.pyplot(plt)
    
    elif scatter_option == "TEMP vs PRES":
        plt.figure(figsize=(8, 6))
        plt.scatter(data['TEMP'], data['PRES'])
        plt.title('Scatter Plot TEMP vs PRES')
        plt.xlabel('TEMP')
        plt.ylabel('PRES')
        plt.grid(True)
        st.pyplot(plt)
    
    elif scatter_option == "NO2 vs CO":
        plt.figure(figsize=(8, 6))
        plt.scatter(data['NO2'], data['CO'])
        plt.title('Scatter Plot NO2 vs CO')
        plt.xlabel('NO2')
        plt.ylabel('CO')
        plt.grid(True)
        st.pyplot(plt)

elif visualization_option == "Total dan Rata-rata Polutan":
    st.header("Total dan Rata-rata Polutan Berdasarkan Tahun dan Stasiun")
    
    polutan = st.selectbox("Pilih Polutan", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    
    # Calculate total and mean pollutant per year and station
    total_pollutant = data.groupby(['year', 'station'])[polutan].sum().reset_index()
    mean_pollutant = data.groupby(['year', 'station'])[polutan].mean().reset_index()
    
    # Plot total polutan
    st.subheader(f"Total {polutan} per Tahun dan Stasiun")
    plt.figure(figsize=(14, 8))
    sns.barplot(x='year', y=polutan, hue='station', data=total_pollutant, palette='bright')
    plt.title(f'Total {polutan} per Tahun dan Stasiun')
    plt.xlabel('Tahun')
    plt.ylabel(f'Total {polutan}')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    st.pyplot(plt)
    
    # Plot mean polutan
    st.subheader(f"Rata-rata {polutan} per Tahun dan Stasiun")
    plt.figure(figsize=(14, 8))
    sns.barplot(x='year', y=polutan, hue='station', data=mean_pollutant, palette='bright')
    plt.title(f'Rata-rata {polutan} per Tahun dan Stasiun')
    plt.xlabel('Tahun')
    plt.ylabel(f'Rata-rata {polutan}')
    plt.legend(title='Stasiun', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    st.pyplot(plt)

# Kesimpulan dan Saran
st.header("Kesimpulan dan Saran")
st.write("""
    ### **Kesimpulan:**
    1. **Tren Polutan**:
       - Polutan dengan rata-rata tertinggi adalah **CO (Karbon Monoksida)**, terutama di stasiun **Wanshouxigong**.
       - Kadar **PM2.5** dan **PM10** cenderung tinggi di stasiun **Dongsi** dan **Gucheng**.
       - Kadar **O3 (Ozon)** tertinggi ditemukan di stasiun **Dingling**, yang mungkin dipengaruhi oleh faktor cuaca dan lokasi geografis.

    2. **Hubungan Antar Polutan**:
       - Terdapat korelasi positif yang kuat antara **PM2.5** dan **PM10**, menunjukkan bahwa sumber polusi partikel berasal dari sumber yang sama.
       - **NO2** dan **CO** memiliki korelasi positif, yang mengindikasikan bahwa keduanya berasal dari emisi kendaraan bermotor.
       - **Temperatur (TEMP)** dan **Tekanan Udara (PRES)** memiliki korelasi negatif, yang berarti peningkatan suhu cenderung menurunkan tekanan udara.

    ### **Insight/Wawasan:**
    - Polusi udara di Beijing dipengaruhi oleh berbagai faktor, termasuk emisi kendaraan bermotor, industri, dan kondisi meteorologi seperti suhu, curah hujan, dan kecepatan angin.
    - Stasiun yang terletak di pusat kota (seperti **Dongsi** dan **Wanshouxigong**) cenderung memiliki kadar polutan yang lebih tinggi dibandingkan stasiun di pinggiran kota (seperti **Dingling**).

    ### **Saran untuk Menanggulangi Polutan:**
    1. **Pengurangan Emisi Kendaraan**:
       - Meningkatkan penggunaan transportasi umum yang ramah lingkungan.
       - Menerapkan kebijakan pembatasan kendaraan pribadi di area dengan tingkat polusi tinggi.

    2. **Peningkatan Kualitas Industri**:
       - Menerapkan teknologi ramah lingkungan di industri untuk mengurangi emisi polutan seperti **SO2** dan **NO2**.
       - Memantau dan menegakkan regulasi emisi industri secara ketat.

    3. **Penghijauan dan Ruang Terbuka Hijau**:
       - Menambah area hijau di pusat kota untuk menyerap polutan seperti **PM2.5** dan **PM10**.
       - Menanam pohon yang dapat menyerap polutan udara.

    4. **Peningkatan Kesadaran Masyarakat**:
       - Mengedukasi masyarakat tentang bahaya polusi udara dan langkah-langkah pencegahan.
       - Mendorong penggunaan masker saat tingkat polusi tinggi.

    5. **Pemantauan dan Sistem Peringatan Dini**:
       - Memperkuat sistem pemantauan kualitas udara secara real-time.
       - Memberikan peringatan dini kepada masyarakat saat tingkat polusi mencapai level berbahaya.

    Catatan:
    Pada tahun 2017 data sampai pada bulan februari
""")

# Additional information
st.sidebar.header("Informasi Tambahan")
st.sidebar.write("""
    - **Dataset:** [Air Quality Dataset](https://github.com/daffaakifah/Analisis_Kualitas_Udara)
    - **Dibuat oleh:** Daffa Akifah Balqis
    - **Email:** daffaakifahbalqis01@gmail.com
    - **Dicoding Username:** daffabalqis
""")
