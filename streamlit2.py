import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Load data
monthly_orders = pd.read_csv('monthly_orders.csv')
monthly_delivery_duration = pd.read_csv('monthly_delivery_duration.csv')
merged1_df = pd.read_csv('merged1.csv')
merged3_df = pd.read_csv('merged3.csv')

# Konversi kolom 'year_month2' ke datetime untuk keperluan filtering
monthly_delivery_duration['year_month2'] = pd.to_datetime(monthly_delivery_duration['year_month2'])

# tangga minimum dan maksimum
min_date = monthly_delivery_duration['year_month2'].min()
max_date = monthly_delivery_duration['year_month2'].max()

# Membuat sidebar untuk input rentang waktu
with st.sidebar:
    # Input rentang waktu
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan rentang waktu yang dipilih
filtered_data = monthly_delivery_duration[(monthly_delivery_duration['year_month2'] >= pd.to_datetime(start_date)) & 
                                          (monthly_delivery_duration['year_month2'] <= pd.to_datetime(end_date))]

# Mengatur title
st.title('E-commerce Data Analysis')

# Visualisasi untuk pertanyaan 3
st.subheader('Hubungan antara Waktu Pengiriman dengan Skor Review')
st.metric(label="Nilai Korelasi", value='-0.33367')
st.caption('Nilai tersebut membuktikan bahwa tidak adanya korelasi yang kuat antara waktu pengiriman dan skor review')
sns.scatterplot(x='delivery_time_days', y='review_score', data=merged1_df)
plt.title('Hubungan antara Waktu Pengiriman dan Skor Review')
plt.xlabel('Waktu Pengiriman (hari)')
plt.ylabel('Skor Review')
st.pyplot(plt)

# Visualisasi untuk pertanyaan 2
st.subheader('Tren Rata-rata Durasi Pengiriman per Bulan')

# Menapilkan dataframe
st.dataframe(filtered_data)

# Membuat line plot
plt.figure(figsize=(12, 6))
sns.lineplot(data=filtered_data, x='year_month2', y='delivery_duration', marker="o")

plt.title('Tren Rata-rata Durasi Pengiriman per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Rata-rata Durasi Pengiriman (hari)')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)

# Visualisasi untuk pertanyaan 1
st.subheader('Tren Jumlah Pesanan per Bulan')
st.dataframe(monthly_orders)
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_orders, x='year_month', y='order_count', marker='o')
plt.title('Tren Jumlah Pesanan per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pesanan')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt)


# Visualisasi untuk pertanyaan 4
st.subheader('Identifikasi Kategori Produk dengan Waktu Pengiriman')
st.metric(label="Rata-Rata Waktu Pengiriman", value='12 hari')
plt.figure(figsize=(12, 8))
avg_delivery_time = merged3_df.groupby('product_category_name')['delivery_time_days2'].mean().sort_values()
sns.barplot(x=avg_delivery_time.index, y=avg_delivery_time.values)
plt.xticks(rotation=90)
plt.title('Rata-Rata Waktu Pengiriman per Kategori Produk')
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-Rata Waktu Pengiriman (hari)')
st.pyplot(plt)

st.caption('Berikut adalah daftar top 10 kategori produk dengan rata-rata waktu pengiriman terlama')
top10_avg_delivery_time = avg_delivery_time.tail(10)

# Visualisasi
plt.figure(figsize=(12, 8))
sns.barplot(x=top10_avg_delivery_time.index, y=top10_avg_delivery_time.values)
plt.xticks(rotation=90)
plt.title('Top 10 Kategori Produk dengan Rata-Rata Waktu Pengiriman Terlama')
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-Rata Waktu Pengiriman (hari)')
st.pyplot(plt)

# Visualisasi terpendek
top10_avg_delivery_time_shortest = avg_delivery_time.head(10)
y_max = 20
# Visualisasi
plt.figure(figsize=(12, 8))
sns.barplot(x=top10_avg_delivery_time_shortest.index, y=top10_avg_delivery_time_shortest.values)
plt.ylim(0, y_max)
plt.xticks(rotation=90)
plt.title('Top 10 Kategori Produk dengan Rata-Rata Waktu Pengiriman Terpendek')
plt.xlabel('Kategori Produk')
plt.ylabel('Rata-Rata Waktu Pengiriman (hari)')
st.pyplot(plt)
