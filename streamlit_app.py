import streamlit as st
import pandas as pd
import os

# ===============================
# 1. CONFIG & UI CUSTOMIZATION
# ===============================
st.set_page_config(page_title="AKA-LABBROWS", layout="wide", page_icon="🔬")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #FF8C00 0%, #FF4500 100%);
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: white !important;
    }
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.95);
    }
    [data-testid="stSidebar"] .stRadio label, [data-testid="stSidebar"] h1 {
        color: #2c3e50 !important;
    }
    .st-emotion-cache-1kyx9g7 {
        background-color: rgba(255, 255, 255, 0.15);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# Inisialisasi Session State
if "login" not in st.session_state:
    st.session_state.login = False
    st.session_state.nama = ""

# ===============================
# 2. DATABASE SEDERHANA
# ===============================
AKSES_DOSEN = {"Andi": "12345678", "Admin": "aka123"}

# ===============================
# 3. FUNGSI LOGIKA CLOUD STORAGE
# ===============================

def halaman_upload_dan_akses():
    st.title("📂 Cloud Storage Laboratorium")
    
    # Membuat folder di server Cloud jika belum ada
    UPLOAD_FOLDER = "upload_jadwal"
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    # BAGIAN 1: UPLOAD (Hanya untuk Dosen)
    st.write("### 📤 Upload Jadwal Baru")
    if not st.session_state.login:
        with st.expander("Klik untuk Login Dosen/Admin"):
            user = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.button("Login"):
                if user in AKSES_DOSEN and pw == AKSES_DOSEN[user]:
                    st.session_state.login = True
                    st.session_state.nama = user
                    st.rerun()
                else:
                    st.error("Akun tidak ditemukan")
    else:
        st.info(f"Login sebagai: {st.session_state.nama}")
        uploaded_file = st.file_uploader("Pilih File", type=["pdf", "xlsx", "docx", "png", "jpg"])
        
        if uploaded_file:
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File {uploaded_file.name} berhasil disimpan di Cloud!")
        
        if st.button("Logout"):
            st.session_state.login = False
            st.rerun()

    st.divider()

    # BAGIAN 2: AKSES & BUKA FILE (Untuk Semua User)
    st.write("### 📜 Daftar Jadwal di Cloud")
    
    list_files = os.listdir(UPLOAD_FOLDER)
    
    if len(list_files) > 0:
        for file_name in list_files:
            file_path = os.path.join(UPLOAD_FOLDER, file_name)
            
            # Membuat baris untuk setiap file
            col_name, col_btn = st.columns([3, 1])
            with col_name:
                st.write(f"📄 {file_name}")
            with col_btn:
                # Tombol Download agar file bisa dibuka/diunduh
                with open(file_path, "rb") as f:
                    st.download_button(
                        label="Buka/Unduh",
                        data=f,
                        file_name=file_name,
                        mime="application/octet-stream",
                        key=file_name # Key unik untuk setiap tombol
                    )
    else:
        st.warning("Belum ada file yang di-upload ke Cloud.")

# ===============================
# 4. SIDEBAR & ROUTING
# ===============================
with st.sidebar:
    st.title("🔬 AKA-LAB")
    menu = st.radio("Navigasi", ["Beranda", "Akses Cloud Jadwal"])

if menu == "Beranda":
    st.title("🌟 Welcome To, AKA-LABBROWS")
    st.write("Aplikasi Manajemen Lab Politeknik AKA Bogor")
    st.video("https://youtu.be/F-j-BGyRNKo")
    st.balloons()

elif menu == "Akses Cloud Jadwal":
    halaman_upload_dan_akses()
