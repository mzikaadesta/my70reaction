import streamlit as st
import pandas as pd
import datetime
import os

# ===============================
# 1. CONFIG & UI CUSTOMIZATION (ORANGE THEME)
# ===============================
st.set_page_config(page_title="AKA-LABBROWS", layout="wide", page_icon="🔬")

# Menyisipkan CSS untuk background Oranye dan styling teks
st.markdown("""
    <style>
    /* Mengubah background area utama menjadi Oranye */
    .stApp {
        background: linear-gradient(to right, #FF8C00, #FFA500);
    }

    /* Mengubah semua teks utama menjadi Putih agar kontras */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: white !important;
    }

    /* Styling khusus Sidebar agar tetap bersih */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] p {
        color: #333333 !important;
    }

    /* Mempercantik tombol */
    .stButton>button {
        border-radius: 20px;
        border: none;
        background-color: #ffffff;
        color: #FF8C00;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Session State
if "lab_terpilih" not in st.session_state:
    st.session_state.lab_terpilih = None
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.nama = ""

def reset_lab():
    st.session_state.lab_terpilih = None

# ===============================
# 2. DATABASE
# ===============================
AKSES_DOSEN = {
    "Andi": "12345678",
    "Dr. Budi Santoso": "1976543210",
    "Dr. Siti Aminah": "1965432109"
}

DATABASE_LAB = {
    "Lab Organik": {
        "gedung": "Gedung D", "key": "lab_org",
        "jadwal": {"senin": {"07.00": "1A", "10.00": "1B"}},
        "regulasi": ["1. Dresscode lab lengkap", "2. Dilarang makan/minum"],
        "dosen": [{"nama": "ayung, M.Si", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab Analisis": {
        "gedung": "Gedung D", "key": "lab_ana",
        "jadwal": {"selasa": {"07.00": "2E"}},
        "regulasi": ["1. Kebersihan alat utama", "2. Cek sebelum digunakan"],
        "dosen": [{"nama": "Pak Joko", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab mikro": {
        "gedung": "Gedung E", "key": "lab_mikro",
        "jadwal": {"jumat": {"07.00": "1B"}},
        "regulasi": ["1. Sterilisasi alat", "2. Jas lab bersih"],
        "dosen": [{"nama": "Bu CC", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    }
}

# ===============================
# 3. FUNGSI FITUR
# ===============================

def halaman_detail_lab(nama_lab):
    data = DATABASE_LAB[nama_lab]
    st.button("⬅ Kembali", on_click=reset_lab)
    st.title(f"🔬 {nama_lab}")
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.subheader("📜 Regulasi")
        for r in data["regulasi"]: st.write(r)
        st.link_button("📑 Form Peminjaman", data["link_form"], use_container_width=True)
    with col2:
        st.subheader("👨‍🔬 Penanggung Jawab")
        for d in data["dosen"]:
            st.info(f"**{d['nama']}**\n\n📞 {d['telp']}")

def tampilkan_gedung(nama_gedung):
    st.header(f"🏢 {nama_gedung}")
    st.image(f"https://via.placeholder.com/800x300.png?text=AREA+{nama_gedung.replace(' ', '+')}")
    st.write("### Pilih Laboratorium:")
    lab_di_gedung = {k: v for k, v in DATABASE_LAB.items() if v["gedung"] == nama_gedung}
    if lab_di_gedung:
        cols = st.columns(len(lab_di_gedung))
        for i, (nama_lab, info) in enumerate(lab_di_gedung.items()):
            with cols[i]:
                if st.button(f"Info {nama_lab}", key=info["key"]):
                    st.session_state.lab_terpilih = nama_lab
                    st.rerun()

def halaman_upload():
    st.title("🔐 Akses Dosen: Update Jadwal")
    # OTOMATISASI FOLDER
    UPLOAD_FOLDER = "upload_jadwal"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    if not st.session_state.login:
        nama = st.text_input("Nama Dosen")
        nip = st.text_input("NIP Dosen", type="password")
        if st.button("Login"):
            if nama in AKSES_DOSEN and nip == AKSES_DOSEN[nama]:
                st.session_state.login = True
                st.session_state.nama = nama
                st.rerun()
            else: st.error("Akses Ditolak!")
    else:
        st.success(f"Selamat Datang, {st.session_state.nama}")
        file = st.file_uploader("Upload Jadwal (PDF/Excel)", type=["pdf", "xlsx", "docx"])
        if file:
            with open(os.path.join(UPLOAD_FOLDER, file.name), "wb") as f:
                f.write(file.getbuffer())
            st.success(f"File {file.name} berhasil disimpan!")
        if st.button("Logout"):
            st.session_state.login = False
            st.rerun()

# ===============================
# 4. ROUTING UTAMA
# ===============================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4320/4320337.png", width=80)
    st.title("LAB-INFO")
    menu = st.radio("Menu", ["Beranda", "Jadwal Lab", "Gedung D", "Gedung E", "Gedung F", "Gedung G", "Upload Jadwal"])

if st.session_state.lab_terpilih:
    halaman_detail_lab(st.session_state.lab_terpilih)
else:
    if menu == "Beranda":
        st.title("Welcome To, AKA-LABBROWS")
        st.write("---")
        st.write("Aplikasi Informasi Laboratorium Politeknik AKA Bogor - Kelompok 4")
        st.video("https://youtu.be/F-j-BGyRNKo")
        st.balloons()
    elif menu == "Jadwal Lab":
        st.header("📅 Cek Jadwal")
        # (Tambahkan fungsi lihat_jadwal di sini)
    elif menu == "Upload Jadwal":
        halaman_upload()
    else:
        tampilkan_gedung(menu)
