"""
Fungsi pembantu untuk memuat data dan file HTML.
"""

import streamlit as st
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@st.cache_data
def load_csv(filename):
    """Memuat file CSV dari folder data/processed. Mengembalikan None jika file tidak ada."""
    path = ROOT / "data" / "processed" / filename
    if not path.exists():
        # Fallback to root just in case
        path = ROOT / filename
        if not path.exists():
            return None
    return pd.read_csv(path)


@st.cache_data
def load_html(filename):
    """Membaca file HTML dari folder models. Mengembalikan None jika file tidak ada."""
    path = ROOT / "models" / filename
    if not path.exists():
        # Fallback to root just in case
        path = ROOT / filename
        if not path.exists():
            return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
