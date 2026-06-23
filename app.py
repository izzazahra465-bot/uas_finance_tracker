import streamlit as st
import pandas as pd
import os

# 1. Konfigurasi Tampilan Halaman Web
st.set_page_config(page_title="Finance Tracker UAS", layout="centered")
st.title("💰 Personal Finance Tracker")
st.write("Aplikasi sederhana untuk mencatat dan menganalisis pengeluaran bulanan.")

# 2. Setup Database Sederhana menggunakan file CSV
DATA_FILE = "data_keuangan.csv"
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Tanggal", "Kategori", "Keterangan", "Nominal"])
    df.to_csv(DATA_FILE, index=False)

# Membaca data terbaru dari file CSV
df_current = pd.read_csv(DATA_FILE)

# 3. Form Input Data Pengeluaran
st.subheader("✍️ Catat Pengeluaran Baru")
with st.form(key="finance_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        tanggal = st.date_input("Tanggal")
        kategori = st.selectbox("Kategori", ["Makanan & Minuman", "Transportasi", "Kost/Tempat Tinggal", "Hiburan", "Kuliah/Edukasi", "Lainnya"])
    with col2:
        keterangan = st.text_input("Keterangan/Detail")
        nominal = st.number_input("Nominal (Rp)", min_value=0, step=1000)
    
    submit_button = st.form_submit_button(label="Simpan Data")

# Logika ketika tombol simpan diklik
if submit_button:
    new_data = pd.DataFrame([[tanggal, kategori, keterangan, nominal]], columns=["Tanggal", "Kategori", "Keterangan", "Nominal"])
    df_updated = pd.concat([df_current, new_data], ignore_index=True)
    df_updated.to_csv(DATA_FILE, index=False)
    st.success("Data berhasil disimpan!")
    st.rerun()

# 4. Tampilan Dashboard Grafik & Tabel Riwayat
st.subheader("📊 Dashboard & Riwayat")

if not df_current.empty:
    # Menghitung total semua pengeluaran
    total_pengeluaran = df_current["Nominal"].sum()
    st.metric(label="Total Pengeluaran Kamu", value=f"Rp {total_pengeluaran:,.0f}")
    
    # Grafik Pengeluaran per Kategori
    st.write("**Persentase Pengeluaran per Kategori:**")
    kategori_chart = df_current.groupby("Kategori")["Nominal"].sum()
    st.bar_chart(kategori_chart)
    
    # Menampilkan Tabel Data
    st.write("**Tabel Riwayat Transaksi:**")
    st.dataframe(df_current, use_container_width=True)
else:
    st.info("Belum ada data keuangan yang dicatat. Silakan isi form di atas!")