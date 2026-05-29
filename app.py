"""
Halaman utama aplikasi Streamlit.
Menampilkan ringkasan proyek dan gambaran umum data.
"""

import streamlit as st
from utils.helpers import load_csv

st.set_page_config(
    page_title="Topic Modeling - Mobile JKN & SATUSEHAT",
    layout="wide",
)

st.title("Topic Modeling Ulasan Play Store")
st.caption("Analisis ulasan aplikasi Mobile JKN dan SATUSEHAT dari Google Play Store")

st.write(
    "Proyek ini menganalisis topik-topik utama yang dibahas pengguna "
    "dalam ulasan aplikasi Mobile JKN dan SATUSEHAT di Google Play Store "
    "menggunakan metode Latent Dirichlet Allocation (LDA)."
)

df = load_csv("review_mobile_jkn_satusehat_clean.csv")

if df is None:
    st.error(
        "File data belum tersedia. "
        "Jalankan notebook terlebih dahulu untuk menghasilkan data."
    )
    st.stop()

# Ringkasan jumlah data
st.subheader("Ringkasan Data")

apps = df["source_app"].unique()
cols = st.columns(len(apps) + 1)
cols[0].metric("Total Review", f"{len(df):,}")

for i, app_name in enumerate(apps):
    n = len(df[df["source_app"] == app_name])
    cols[i + 1].metric(app_name, f"{n:,}")

# Tahapan analisis
st.subheader("Tahapan Analisis")
st.write(
    "1. Pengumpulan data ulasan dari Google Play Store "
    "menggunakan google-play-scraper\n"
    "2. Text preprocessing: case folding, pembersihan karakter, "
    "stopword removal, stemming Sastrawi\n"
    "3. Exploratory Data Analysis: distribusi rating, "
    "wordcloud, frekuensi kata\n"
    "4. Topic modeling menggunakan LDA dengan 4 topik per aplikasi"
)

# Contoh data
st.subheader("Contoh Data")

contoh = (
    df[["source_app", "review", "clean_review", "rating"]]
    .groupby("source_app", group_keys=False)
    .head(3)
    .reset_index(drop=True)
)
st.dataframe(contoh, use_container_width=True)

st.caption("Proyek Mata Kuliah Analisis Data Tak Terstruktur, Semester 6")
