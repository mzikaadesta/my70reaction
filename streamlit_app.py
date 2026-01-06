import streamlit as st
import time

# ===============================
# 1. SIDEBAR GLASSMORPHISM (CSS)
# ===============================
st.markdown("""
    <style>
    /* Mengubah Sidebar menjadi efek kaca transparan */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(15px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    /* Mengatur warna teks di sidebar agar tetap kontras */
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Opsional: Membuat background utama gradien agar efek kaca terlihat */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    </style>
    """, unsafe_allow_html=True)

# ===============================
# 2. FUNGSI EFEK TYPEWRITER
# ===============================
def typewriter(text, speed=50):
    """
    Fungsi untuk menampilkan teks dengan efek mengetik.
    Speed: milidetik per karakter.
    """
    container = st.empty()
    displayed_text = ""
    for char in text:
        displayed_text += char
        # Menggunakan HTML untuk styling teks typewriter
        container.markdown(f"<h1 style='text-align: center; color: white;'>{displayed_text}</h1>", unsafe_allow_html=True)
        time.sleep(speed / 1000)

# ===============================
# 3. IMPLEMENTASI PADA HALAMAN
# ===============================

# Navigasi Sidebar (Glassmorphism sudah aktif via CSS di atas)
with st.sidebar:
    st.title("🔬 LAB-INFO")
    st.write("Menu Navigasi")
    st.radio("Pilih Halaman", ["Beranda", "Jadwal", "Kontak"])

# Menjalankan Efek Typewriter di Beranda
typewriter("Selamat Datang di AKA-LABBROWS")

st.write("---")
st.markdown("""
    <div style='background: rgba(255,255,255,0.1); padding: 20px; border-radius: 15px; border: 1px solid rgba(255,255,255,0.2);'>
        <p style='text-align: center; color: white;'>
            Sistem Informasi Laboratorium Modern Politeknik AKA Bogor.
        </p>
    </div>
""", unsafe_allow_html=True)
