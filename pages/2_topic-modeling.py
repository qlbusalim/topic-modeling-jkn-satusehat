"""
Halaman Topic Modeling.
Menampilkan hasil LDA per aplikasi beserta visualisasi pyLDAvis.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import matplotlib.pyplot as plt
from utils.helpers import load_csv, load_html

WARNA_APP = ["#4C9A8A", "#E07B54"]
WARNA_TOPIK = "#5B86A8"

st.set_page_config(page_title="Topic Modeling", layout="wide")
st.title("Hasil Topic Modeling LDA")

topik_df = load_csv("daftar_topik_mobile_jkn_satusehat.csv")
distribusi_df = load_csv("distribusi_topik_mobile_jkn_satusehat.csv")
hasil_df = load_csv("hasil_topic_modeling_mobile_jkn_satusehat.csv")

if topik_df is None or distribusi_df is None:
    st.error(
        "File hasil topic modeling belum tersedia. "
        "Jalankan notebook terlebih dahulu."
    )
    st.stop()

apps = sorted(topik_df["source_app"].unique().tolist())
pilihan = st.sidebar.selectbox("Aplikasi", apps)


# Daftar topik
st.subheader(f"Daftar Topik - {pilihan}")

topik_app = topik_df[topik_df["source_app"] == pilihan][["topic_number", "top_words"]].copy()
topik_app.columns = ["Topik", "Kata-kata Kunci"]
st.table(topik_app.reset_index(drop=True))


# Distribusi review per topik
st.subheader("Distribusi Review per Topik")

dist_app = distribusi_df[distribusi_df["source_app"] == pilihan]

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(
    dist_app["topic_number"].astype(str),
    dist_app["jumlah_review"],
    color=WARNA_TOPIK
)
ax.set_xlabel("Topik")
ax.set_ylabel("Jumlah Review")
ax.set_title(f"Distribusi Review per Topik - {pilihan}")
plt.tight_layout()
st.pyplot(fig)
plt.close()

dist_tampil = dist_app[["topic_number", "jumlah_review", "persentase"]].copy()
dist_tampil.columns = ["Topik", "Jumlah Review", "Persentase (%)"]
dist_tampil["Persentase (%)"] = dist_tampil["Persentase (%)"].round(2)
st.dataframe(dist_tampil.reset_index(drop=True), use_container_width=True)


# Contoh review per topik
if hasil_df is not None:
    st.subheader("Contoh Review per Topik")

    hasil_app = hasil_df[hasil_df["source_app"] == pilihan]

    for topic_num in sorted(hasil_app["dominant_topic"].unique()):
        st.write(f"**Topik {topic_num}**")

        contoh = (
            hasil_app[hasil_app["dominant_topic"] == topic_num]
            .sort_values("topic_probability", ascending=False)
            [["review", "clean_review", "topic_probability"]]
            .head(3)
        )
        contoh.columns = ["Review Asli", "Setelah Preprocessing", "Probabilitas"]
        contoh["Probabilitas"] = contoh["Probabilitas"].round(4)
        st.dataframe(contoh.reset_index(drop=True), use_container_width=True)


# Visualisasi pyLDAvis
st.subheader("Visualisasi Interaktif LDA")

safe_name = pilihan.lower().replace(" ", "_")
html_content = load_html(f"lda_visualization_{safe_name}.html")

if html_content is not None:
    components.html(html_content, height=800, scrolling=True)
else:
    st.info(f"File visualisasi pyLDAvis untuk {pilihan} belum tersedia.")


# Perbandingan distribusi antar aplikasi
st.subheader("Perbandingan Distribusi Topik Antar Aplikasi")

perbandingan = distribusi_df.pivot(
    index="topic_number",
    columns="source_app",
    values="persentase"
).fillna(0)

fig, ax = plt.subplots(figsize=(8, 4))
perbandingan.plot(kind="bar", ax=ax, color=WARNA_APP)
ax.set_xlabel("Topik")
ax.set_ylabel("Persentase Review (%)")
ax.set_title("Perbandingan Persentase Dominant Topic per Aplikasi")
plt.xticks(rotation=0)
plt.legend(title="Aplikasi")
plt.tight_layout()
st.pyplot(fig)
plt.close()

st.dataframe(
    perbandingan.reset_index().rename(columns={"topic_number": "Topik"}),
    use_container_width=True
)
