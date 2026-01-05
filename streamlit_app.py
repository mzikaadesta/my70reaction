import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw

# =========================
# LOAD DATABASE
# =========================
@st.cache_data
def load_database():
    return pd.read_csv("database_senyawa.csv")

df = load_database()

st.title("🧪 Sistem Informasi Senyawa Kimia")

# =========================
# INPUT
# =========================
nama = st.text_input("Masukkan nama senyawa")
konsentrasi = st.number_input("Masukkan konsentrasi (%)", min_value=0.0, max_value=100.0)

# =========================
# PROCESS
# =========================
if st.button("Proses"):
    data = df[df["Nama_Senyawa"].str.lower() == nama.lower()]

    if data.empty:
        st.error("Senyawa tidak ditemukan dalam database.")
    else:
        row = data.iloc[0]

        # =========================
        # STRUKTUR KIMIA
        # =========================
        st.subheader("Struktur Kimia")
        mol = Chem.MolFromSmiles(str(row["SMILES"]))
        if mol:
            st.image(Draw.MolToImage(mol, size=(300, 300)))
        else:
            st.warning("Struktur tidak dapat divisualisasikan.")

        # =========================
        # KARAKTERISASI
        # =========================
        st.subheader("Karakterisasi Senyawa")
        st.write(f"**BM:** {row['BM']} g/mol")
        st.write(f"**Titik didih:** {row['Titik_Didih']} °C")
        st.write(f"**Kelarutan:** {row['Kelarutan']}")

        # =========================
        # MSDS
        # =========================
        st.subheader("MSDS (Ringkas)")
        st.write(f"**Bahaya:** {row['Bahaya_MSDS']}")
        st.write(f"**APD yang disarankan:** {row['APD']}")

        # =========================
        # STATUS KONSENTRASI
        # =========================
        status = "Tidak terklasifikasi"

        if row["Encer_Min"] <= konsentrasi <= row["Encer_Max"]:
            status = "ENCER"
        elif row["Sedang_Min"] <= konsentrasi <= row["Sedang_Max"]:
            status = "SEDANG"
        elif row["Pekat_Min"] <= konsentrasi <= row["Pekat_Max"]:
            status = "PEKAT"

        st.subheader("Status Konsentrasi")
        st.success(f"{konsentrasi}% → **{status}**")
