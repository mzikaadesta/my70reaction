
import streamlit as st
import pandas as pd
import datetime
import os
st.set_page_config(page_title="AKA-LABBROWS", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    /* 1. Background Gradien 4 Warna Bergerak */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab, #f1c40f);
        background-size: 400% 400%;
        animation: gradient 10s ease infinite;
        color: white;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* 2. Mengubah Sidebar Jadi Transparan (Glassmorphism) */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* 3. Menyesuaikan teks di Sidebar agar putih & bersih */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* 4. Efek Kaca pada Kontainer/Card */
    .st-emotion-cache-1kyx9g7 {
        background: rgba(255, 255, 255, 0.15) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
    }

    /* 5. Mempercantik Tombol (Hover Effect) */
    .stButton>button {
        border-radius: 20px;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        border: 1px solid white;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background: white !important;
        color: #e73c7e !important;
        transform: scale(1.05);
    }

    /* Judul Utama */
    h1 {
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        font-weight: 800 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. CONFIG & INITIAL STATE 
st.set_page_config(page_title="Sistem Informasi Laboratorium", layout="wide", page_icon="🔬")

if "lab_terpilih" not in st.session_state:
    st.session_state.lab_terpilih = None

if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.nama = ""

def reset_lab():
    st.session_state.lab_terpilih = None


# DATABASE 

DATABASE_LAB = {
    "Lab Organik": {
        "gedung": "Gedung D", 
        "key": "lab_org_unique",
        "jadwal": {"senin": {"07.00": "1A", "10.00": "1B"}},
        "regulasi": ["1. Dresscode lab lengkap", "2. Dilarang makan/minum"],
        "dosen": [{"nama": "ayung, M.Si", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab Analisis": {
        "gedung": "Gedung D",
        "key": "lab_ana_unique",
        "jadwal": {"selasa": {"07.00": "2E"}},
        "regulasi": ["1. Prosedur analisis ketat", "2. Cek alat sebelum pakai"],
        "dosen": [{"nama": "Pak Joko", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab Lingkungan": {
        "gedung": "Gedung D",
        "key": "lab_ling_unique",
        "jadwal": {"rabu": {"10.00": "2E"}},
        "regulasi": ["1. Pakai masker", "2. Buang limbah sesuai aturan"],
        "dosen": [{"nama": "Pak Purbay", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab Instrumen": {
        "gedung": "Gedung E",
        "key": "lab_ins_unique",
        "jadwal": {"kamis": {"07.00": "1D"}},
        "regulasi": ["1. Izin laboran khusus", "2. Kalibrasi mandiri"],
        "dosen": [{"nama": "Pak DD", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab mikro": {
        "gedung": "Gedung E",
        "key": "lab_mikro_unique",
        "jadwal": {"jumat": {"07.00": "1B"}},
        "regulasi": ["1. Sterilisasi alat", "2. Jas lab bersih"],
        "dosen": [{"nama": "Bu CC", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab Fisika": {
        "gedung": "Gedung F",
        "key": "lab_fisika_unique",
        "jadwal": {"senin": {"14.00": "2A"}},
        "regulasi": ["1. Hati-hati arus listrik", "2. Rapikan kabel setelah pakai"],
        "dosen": [{"nama": "Mas Jaka", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    },
    "Lab Teknologi": {
        "gedung": "Gedung G",
        "key": "lab_tek_unique",
        "jadwal": {"selasa": {"14.00": "1C"}},
        "regulasi": ["1. Safety first", "2. Sepatu tertutup"],
        "dosen": [{"nama": "agoy, M.Si", "telp": "08xxx"}],
        "link_form": "https://youtu.be/opl6dScRQzQ"
    }
}


# TAMPILAN
def halaman_detail_lab(nama_lab):
    data = DATABASE_LAB[nama_lab]
    st.button("⬅ Kembali ke Menu Utama", on_click=reset_lab)
    st.title(f"🔬 {nama_lab}")
    st.divider()
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.subheader("📜 Regulasi Peminjaman")
        for r in data["regulasi"]:
            st.write(r)
        st.divider()
        st.link_button("📑 Formulir Peminjaman Eksternal", data["link_form"], type="primary", use_container_width=True)
    with col2:
        st.subheader("👨‍🔬 Dosen & Laboran")
        for d in data["dosen"]:
            with st.container(border=True):
                st.write(f"**{d['nama']}**")
                st.caption(f"📞 {d['telp']}")

def tampilkan_gedung(nama_gedung):
    st.header(f"🏢 {nama_gedung}")
   fotos = {
        "Gedung D": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+D",
        "Gedung E": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+E",
        "Gedung F": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+F",
        "Gedung G": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+G"
    }
    st.image(fotos.get(nama_gedung, "https://via.placeholder.com/800x300"), caption=f"Area {nama_gedung}")
    st.divider()
    st.write("### Pilih Laboratorium:")
    lab_di_gedung = {k: v for k, v in DATABASE_LAB.items() if v["gedung"] == nama_gedung}
    if lab_di_gedung:
        cols = st.columns(len(lab_di_gedung))
        for i, (nama_lab, info) in enumerate(lab_di_gedung.items()):
            with cols[i]:
                if st.button(f"Informasi {nama_lab}", key=info["key"]):
                    st.session_state.lab_terpilih = nama_lab
                    st.rerun()

def lihat_jadwal():
    st.header("📅 Jadwal Laboratorium")
    lab_nama = st.selectbox("Pilih Lab", list(DATABASE_LAB.keys()))
    hari = st.selectbox("Pilih Hari", ["senin", "selasa", "rabu", "kamis", "jumat"])
    jadwal_hari = DATABASE_LAB[lab_nama]["jadwal"].get(hari)
    if jadwal_hari:
        for jam, kls in jadwal_hari.items():
            st.info(f"🕒 **{jam}** — Kelas **{kls}**")
    else:
        st.warning("Tidak ada jadwal untuk hari ini.")




# sidebar 
with st.sidebar:
     st.image("url vidio", width=70)
       st.title("🔬 Lab-Info System")
    st.write("---")
    menu = st.radio(
        "Navigasi Utama", 
        ["Beranda", "Jadwal Lab", "Gedung D", "Gedung E", "Gedung F", "Gedung G"], 
        on_change=reset_lab
    )

# home
if st.session_state.lab_terpilih:
    halaman_detail_lab(st.session_state.lab_terpilih)
else:
    if menu == "Beranda":
        st.title("welcome To AKA-LABBROWS")
        st.write("**Projek Logika Dan Pemrograman Komputer - Kelompok 4**")
        st.write("Tempat khusus untuk kamu yang ingin meminjam lab di Politeknik AKA Bogor.")
        st.video("https://youtu.be/F-j-BGyRNKo")
        st.write("Politeknik AKA Bogor didirikan pada tahun 1959 dan merupakan perguruan tinggi di lingkungan Kementerian Perindustrian. Terdapat beberapa laboratorium yang terdapat di Politeknik AKA Bogor, antara lain, Gedung D (Lab Organik, Lab Analisis, Lab Lingkungan), Gedung E (Lab Instrumen, Lab Mikro), Gedung F (Lab Fisika), Gedung G (Lab Teknologi).")
        st.balloons()
    elif menu == "Jadwal Lab":
        lihat_jadwal()
    elif menu == "Penambahan Jadwal Laboratorium":
        halaman_penambahan_jadwal_lab()
    else:
        tampilkan_gedung(menu)
