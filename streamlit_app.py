import streamlit as st
import pandas as pd

st.title("Jadwal Laboratorium")

# =========================
# Data jadwal tiap lab
# =========================
jadwal_lab = {
    "Lab Kimia": pd.DataFrame({
        "Hari": ["Senin", "Rabu", "Jumat"],
        "Waktu": ["08.00–10.00", "13.00–15.00", "09.00–11.00"],
        "Nama Kegiatan": ["Praktikum Dasar", "Penelitian", "Praktikum Lanjut"]
    }),

    "Lab Fisika": pd.DataFrame({
        "Hari": ["Selasa", "Kamis"],
        "Waktu": ["08.00–10.00", "13.00–15.00"],
        "Nama Kegiatan": ["Eksperimen Mekanika", "Eksperimen Listrik"]
    }),

    "Lab Biologi": pd.DataFrame({
        "Hari": ["Senin", "Kamis"],
        "Waktu": ["10.00–12.00", "08.00–10.00"],
        "Nama Kegiatan": ["Praktikum Mikrobiologi", "Kultur Sel"]
    })
}

# =========================
# Pilih laboratorium
# =========================
lab_dipilih = st.selectbox(
    "Pilih Laboratorium",
    options=list(jadwal_lab.keys())
)

# =========================
# Tampilkan jadwal
# =========================
st.subheader(f"Jadwal {lab_dipilih}")
st.dataframe(
    jadwal_lab[lab_dipilih],
    use_container_width=True
)
