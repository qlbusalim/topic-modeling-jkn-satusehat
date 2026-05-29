"""
Halaman Exploratory Data Analysis.
Menampilkan distribusi rating, wordcloud, dan analisis frekuensi kata.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from utils.helpers import load_csv

WARNA_APP = ["#4C9A8A", "#E07B54"]
WARNA_UTAMA = "#4C9A8A"
WARNA_HIST = "#7FB5AC"
WARNA_BIGRAM = "#5B86A8"

st.set_page_config(page_title="EDA", layout="wide")
st.title("Exploratory Data Analysis")

df = load_csv("review_mobile_jkn_satusehat_clean.csv")

if df is None:
    st.error("File data belum tersedia. Jalankan notebook terlebih dahulu.")
    st.stop()

apps = sorted(df["source_app"].unique().tolist())
pilihan = st.sidebar.selectbox("Aplikasi", ["Semua"] + apps)

if pilihan != "Semua":
    data = df[df["source_app"] == pilihan].copy()
else:
    data = df.copy()

st.write(f"Menampilkan {len(data):,} review.")


# Distribusi Rating
st.subheader("Distribusi Rating")

if pilihan == "Semua":
    tabel_rating = pd.crosstab(df["rating"], df["source_app"])
    fig, ax = plt.subplots(figsize=(8, 4))
    tabel_rating.plot(kind="bar", ax=ax, color=WARNA_APP)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Review")
    ax.set_title("Distribusi Rating per Aplikasi")
    plt.xticks(rotation=0)
    plt.legend(title="Aplikasi")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
else:
    fig, ax = plt.subplots(figsize=(8, 4))
    rating_counts = data["rating"].value_counts().sort_index()
    ax.bar(rating_counts.index.astype(str), rating_counts.values, color=WARNA_UTAMA)
    ax.set_xlabel("Rating")
    ax.set_ylabel("Jumlah Review")
    ax.set_title(f"Distribusi Rating - {pilihan}")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# Distribusi Panjang Review
st.subheader("Distribusi Panjang Review (Setelah Preprocessing)")

fig, ax = plt.subplots(figsize=(8, 4))

if pilihan == "Semua":
    for i, app_name in enumerate(apps):
        subset = df[df["source_app"] == app_name]
        ax.hist(
            subset["word_count_clean"], bins=30, alpha=0.6,
            label=app_name, color=WARNA_APP[i % len(WARNA_APP)],
            edgecolor="white"
        )
    ax.legend()
else:
    ax.hist(data["word_count_clean"], bins=30, color=WARNA_HIST, edgecolor="white")

ax.set_xlabel("Jumlah Kata")
ax.set_ylabel("Frekuensi")
ax.set_title("Distribusi Panjang Review Setelah Preprocessing")
plt.tight_layout()
st.pyplot(fig)
plt.close()


# Wordcloud
st.subheader("Word Cloud")

if pilihan == "Semua":
    col1, col2 = st.columns(2)

    for col, app_name in zip([col1, col2], apps):
        subset = df[df["source_app"] == app_name]
        teks = " ".join(subset["clean_review"].dropna())

        if teks.strip():
            wc = WordCloud(
                width=800, height=400,
                background_color="white",
                colormap="GnBu",
                collocations=False
            ).generate(teks)

            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            ax.set_title(app_name)
            plt.tight_layout()
            col.pyplot(fig)
            plt.close()
else:
    teks = " ".join(data["clean_review"].dropna())

    if teks.strip():
        wc = WordCloud(
            width=800, height=400,
            background_color="white",
            colormap="GnBu",
            collocations=False
        ).generate(teks)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(f"Word Cloud - {pilihan}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()


# Top Words
st.subheader("20 Kata Paling Sering Muncul")

top_words_df = load_csv("top_words_mobile_jkn_satusehat.csv")

if top_words_df is not None:
    if pilihan == "Semua":
        col1, col2 = st.columns(2)

        for col, app_name in zip([col1, col2], apps):
            tw = top_words_df[top_words_df["source_app"] == app_name].head(20)
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.barh(tw["kata"], tw["frekuensi"], color=WARNA_UTAMA)
            ax.invert_yaxis()
            ax.set_xlabel("Frekuensi")
            ax.set_title(app_name)
            plt.tight_layout()
            col.pyplot(fig)
            plt.close()
    else:
        tw = top_words_df[top_words_df["source_app"] == pilihan].head(20)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(tw["kata"], tw["frekuensi"], color=WARNA_UTAMA)
        ax.invert_yaxis()
        ax.set_xlabel("Frekuensi")
        ax.set_title(f"Top 20 Kata - {pilihan}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
else:
    st.info("File top_words belum tersedia.")


# Bigrams
st.subheader("20 Bigram Paling Sering Muncul")

bigram_df = load_csv("bigram_mobile_jkn_satusehat.csv")

if bigram_df is not None:
    if pilihan == "Semua":
        col1, col2 = st.columns(2)

        for col, app_name in zip([col1, col2], apps):
            bg = bigram_df[bigram_df["source_app"] == app_name].head(20)
            fig, ax = plt.subplots(figsize=(6, 5))
            ax.barh(bg["ngram"], bg["frekuensi"], color=WARNA_BIGRAM)
            ax.invert_yaxis()
            ax.set_xlabel("Frekuensi")
            ax.set_title(app_name)
            plt.tight_layout()
            col.pyplot(fig)
            plt.close()
    else:
        bg = bigram_df[bigram_df["source_app"] == pilihan].head(20)
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.barh(bg["ngram"], bg["frekuensi"], color=WARNA_BIGRAM)
        ax.invert_yaxis()
        ax.set_xlabel("Frekuensi")
        ax.set_title(f"Top 20 Bigram - {pilihan}")
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()
else:
    st.info("File bigram belum tersedia.")
