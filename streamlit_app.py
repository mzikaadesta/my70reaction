import streamlit as st
import pandas as pd
import datetime

# ===============================
# 1. CONFIG & INITIAL STATE
# ===============================
# Catatan: st.set_page_config harus menjadi perintah pertama
st.set_page_config(page_title="AKA-LABBROWS", layout="wide", page_icon="🔬")

# Tambahkan storage sementara untuk simulasi database kirim dokumen
if "db_peminjaman" not in st.session_state:
    st.session_state.db_peminjaman = []

if "lab_terpilih" not in st.session_state:
    st.session_state.lab_terpilih = None

# CSS (Tetap sama seperti punyamu)
st.markdown("""
    <style>
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
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { border-radius: 20px; background: rgba(255, 255, 255, 0.2); color: white; border: 1px solid white; transition: 0.3s; }
    .stButton>button:hover { background: white !important; color: #e73c7e !important; transform: scale(1.05); }
    </style>
    """, unsafe_allow_html=True)

def reset_lab():
    st.session_state.lab_terpilih = None

# ===============================
# 2. DATABASE LAB (Data Tetap)
# ===============================
DATABASE_LAB = {
    "Lab Organik": {"gedung": "Gedung D", "key": "l_org", "jadwal": {"senin": {"07.00": "1A"}}, "regulasi": ["1. Dresscode lengkap"], "dosen": "Ayung, M.Si", "form": "https://drive.google.com/..."},
    "Lab Analisis": {"gedung": "Gedung D", "key": "l_ana", "jadwal": {"selasa": {"07.00": "2E"}}, "regulasi": ["1. Prosedur ketat"], "dosen": "Pak Joko", "form": "https://drive.google.com/..."},
    # ... (Tambahkan lab lainnya di sini)
}

# ===============================
# 3. FUNGSI HALAMAN (Baru: Form Pengiriman)
# ===============================
def halaman_detail_lab(nama_lab):
    data = DATABASE_LAB[nama_lab]
    st.button("⬅ Kembali", on_click=reset_lab)
    st.title(f"🔬 {nama_lab}")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📜 Regulasi & Form")
        for r in data["regulasi"]: st.write(r)
        st.link_button("📂 Download Formulir GDrive", data["form"])
    
    with col2:
        st.subheader("📤 Kirim Notifikasi Peminjaman")
        with st.form("form_kirim"):
            nama = st.text_input("Nama Lengkap")
            nim = st.text_input("NIM")
            tgl = st.date_input("Rencana Pinjam")
            pesan = st.text_area("Pesan untuk Laboran")
            submit = st.form_submit_button("Kirim ke Laboran")
            
            if submit:
                # Simulasi pengiriman data ke database admin
                st.session_state.db_peminjaman.append({
                    "nama": nama, "nim": nim, "lab": nama_lab, "tgl": str(tgl), "pesan": pesan, "status": "Pending"
                })
                st.success("✅ Notifikasi terkirim! Silakan serahkan formulir fisik ke dosen.")

def halaman_admin():
    st.title("👨‍💼 Dashboard Laboran (Admin)")
    st.write("Daftar mahasiswa yang berencana meminjam lab:")
    if not st.session_state.db_peminjaman:
        st.info("Belum ada data peminjaman masuk.")
    else:
        df = pd.DataFrame(st.session_state.db_peminjaman)
        st.table(df)
        if st.button("Hapus Semua Riwayat"):
            st.session_state.db_peminjaman = []
            st.rerun()

def tampilkan_gedung(nama_gedung):
    st.header(f"🏢 {nama_gedung}")
    lab_di_gedung = {k: v for k, v in DATABASE_LAB.items() if v["gedung"] == nama_gedung}
    cols = st.columns(len(lab_di_gedung))
    for i, (nama_lab, info) in enumerate(lab_di_gedung.items()):
        with cols[i]:
            if st.button(f"Pilih {nama_lab}", key=info["key"]):
                st.session_state.lab_terpilih = nama_lab
                st.rerun()

# ===============================
# 4. SIDEBAR & ROUTING
# ===============================
with st.sidebar:
    st.title("🔬 Lab-Info")
    menu = st.radio("Menu", ["Beranda", "Jadwal Lab", "Gedung D", "Gedung E", "Dashboard Admin"], on_change=reset_lab)

if st.session_state.lab_terpilih:
    halaman_detail_lab(st.session_state.lab_terpilih)
else:
    if menu == "Beranda":
        st.title("Welcome to AKA-LABBROWS")
        st.video("https://youtu.be/F-j-BGyRNKo")
        st.balloons()
    elif menu == "Dashboard Admin":
        halaman_admin()
    elif menu == "Jadwal Lab":
        st.write("Pilih lab di sidebar untuk melihat jadwal.")
    else:
        tampilkan_gedung(menu)
