import streamlit as st
import pandas as pd
import os
import requests
from streamlit_lottie import st_lottie

# ===============================
# 1. CONFIG & MODERN UI (CSS)
# ===============================
st.set_page_config(page_title="AKA-LABBROWS", layout="wide", page_icon="🔬")

# Fungsi Animasi Lottie
def load_lottieurl(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# CSS ORNAMEN: Background 4 Warna & Sidebar Kaca
st.markdown("""
    <style>
    /* 1. Background Gradien 4 Warna Bergerak */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #f1c40f);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Sidebar Glassmorphism (Efek Kaca) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    [data-testid="stSidebar"] * { color: white !important; }

    /* 3. Card/Kontainer Efek Kaca */
    .st-emotion-cache-1kyx9g7 {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
    }

    /* 4. Teks Putih Agar Kontras */
    h1, h2, h3, p, label, .stMarkdown { color: white !important; }
    
    /* 5. Tombol Hover Effect */
    .stButton>button {
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.2);
        color: white; border: 1px solid white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: white !important;
        color: #e73c7e !important;
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)

# ===============================
# 2. DATABASE & SESSION STATE
# ===============================
if "lab_terpilih" not in st.session_state: st.session_state.lab_terpilih = None
if "login" not in st.session_state: st.session_state.login = False

DATABASE_LAB = {
    "Lab Organik": {"gedung": "Gedung D", "key": "l1"},
    "Lab Analisis": {"gedung": "Gedung D", "key": "l2"},
    "Lab Lingkungan": {"gedung": "Gedung D", "key": "l3"},
    "Lab Instrumen": {"gedung": "Gedung E", "key": "l4"},
    "Lab Mikro": {"gedung": "Gedung E", "key": "l5"}
}

def reset_lab(): st.session_state.lab_terpilih = None

# ===============================
# 3. FUNGSI HALAMAN
# ===============================

def halaman_beranda():
    lottie_lab = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_698wi08o.json")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st_lottie(lottie_lab, height=250)
    
    st.markdown("<h1 style='text-align: center;'>AKA-LABBROWS</h1>", unsafe_allow_html=True)
    st.write("---")
    st.write("### 🚀 Selamat Datang, Kelompok 4!")
    st.write("Sistem informasi jadwal praktikum Politeknik AKA Bogor dengan penyimpanan Cloud.")
    st.video("https://youtu.be/F-j-BGyRNKo")
    
    if 'first_load' not in st.session_state:
        st.balloons()
        st.toast("Website Berhasil Dimuat!", icon="✅")
        st.session_state.first_load = True

def halaman_upload():
    st.title("📂 Cloud Storage")
    folder = "upload_jadwal"
    if not os.path.exists(folder): os.makedirs(folder)

    if not st.session_state.login:
        with st.container():
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            if st.button("Login Dosen"):
                if u == "Andi" and p == "12345678":
                    st.session_state.login = True
                    st.rerun()
    else:
        st.success("Mode Edit Aktif")
        file = st.file_uploader("Upload Jadwal", type=["pdf", "xlsx"])
        if file:
            with open(os.path.join(folder, file.name), "wb") as f:
                f.write(file.getbuffer())
            st.success("File Tersimpan!")
        if st.button("Logout"):
            st.session_state.login = False
            st.rerun()
    
    st.write("### 📑 Daftar File Cloud")
    for f_name in os.listdir(folder):
        with st.container():
            c1, c2 = st.columns([4, 1])
            c1.write(f"📄 {f_name}")
            with open(os.path.join(folder, f_name), "rb") as f:
                c2.download_button("Buka", f, file_name=f_name, key=f_name)

# ===============================
# 4. SIDEBAR & NAVIGATION
# ===============================
with st.sidebar:
    st.title("🔬 NAVIGASI")
    menu = st.radio("Menu Utama", ["Beranda", "Gedung D", "Gedung E", "Upload Jadwal"], on_change=reset_lab)
    st.write("---")
    st.caption("v2.0 - Modern Glassmorphism")

if menu == "Beranda":
    halaman_beranda()
elif menu == "Upload Jadwal":
    halaman_upload()
else:
    st.header(f"🏢 {menu}")
    labs = {k: v for k, v in DATABASE_LAB.items() if v["gedung"] == menu}
    for name, info in labs.items():
        if st.button(f"Lihat Detail {name}", key=info["key"]):
            st.info(f"Menampilkan data untuk {name}...")
