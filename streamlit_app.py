import streamlit as st

st.snow()
import streamlit as st
import datetime

# ===============================
# CONFIG & INITIAL STATE
# ===============================
st.set_page_config(page_title="Sistem Informasi Laboratorium", layout="wide", page_icon="🔬")

if "lab_terpilih" not in st.session_state:
    st.session_state.lab_terpilih = None

def reset_lab():
    st.session_state.lab_terpilih = None

# ===============================
# DATABASE LAB (LENGKAP DENGAN KEY UNIK)
# ===============================
DATABASE_LAB = {
    "Lab Organik": {"gedung": "Gedung B", "key": "l_org", "dosen": "Golda, M.Si", "email": "golda@univ.ac.id"},
    "Lab Analisis": {"gedung": "Gedung B", "key": "l_ana", "dosen": "Pak Joko", "email": "joko@univ.ac.id"},
    "Lab Lingkungan": {"gedung": "Gedung B", "key": "l_lin", "dosen": "Pak Purbay", "email": "purbay@univ.ac.id"},
    "Lab Instrumen": {"gedung": "Gedung E", "key": "l_ins", "dosen": "Pak DD", "email": "dd@univ.ac.id"},
    "Lab Mikro": {"gedung": "Gedung E", "key": "l_mik", "dosen": "Dosen Mikro", "email": "mikro@univ.ac.id"},
    "Lab Komputer": {"gedung": "Gedung E", "key": "l_kom", "dosen": "Dosen Komputer", "email": "komp@univ.ac.id"},
    "Lab Fisika": {"gedung": "Gedung F", "key": "l_fis", "dosen": "Pak Purbay", "email": "fisika@univ.ac.id"},
    "Lab Teknologi": {"gedung": "Gedung G", "key": "l_tek", "dosen": "Agoy, M.Si", "email": "agoy@univ.ac.id"},
}

# ===============================
# FITUR: FORM PEMINJAMAN INTERAKTIF
# ===============================
def halaman_pinjam_lab():
    st.title("📑 Form Pengajuan Peminjaman Lab")
    st.info("Gunakan formulir ini untuk mengajukan izin penggunaan alat atau ruangan laboratorium.")
    
    with st.form("main_form_pinjam"):
        col1, col2 = st.columns(2)
        
        with col1:
            nama = st.text_input("Nama Lengkap Mahasiswa")
            nim = st.text_input("NIM / ID Mahasiswa")
            lab_tujuan = st.selectbox("Pilih Laboratorium", list(DATABASE_LAB.keys()))
            
        with col2:
            # Menggunakan template datetime sesuai permintaanmu
            waktu_event = st.datetime_input(
                "Jadwalkan Waktu Penggunaan",
                datetime.datetime.now() + datetime.timedelta(days=1),
            )
            durasi = st.selectbox("Estimasi Durasi", ["1-3 Jam", "3-6 Jam", "Full Day"])

        keperluan = st.text_area("Tujuan / Keperluan Praktikum/Penelitian")
        
        # Fitur Upload File (KTM / Surat Izin)
        berkas = st.file_uploader("Upload Berkas Pendukung (Format: PDF/JPG/PNG)", type=['pdf', 'jpg', 'png'])
        
        submitted = st.form_submit_button("Kirim Pengajuan ke Laboran")
        
        if submitted:
            if nama and nim and keperluan:
                # Logika sukses
                st.success(f"Berhasil! Pengajuan {nama} telah diteruskan ke {DATABASE_LAB[lab_tujuan]['dosen']}.")
                st.balloons()
                
                # Preview Data yang dikirim
                with st.expander("Lihat Detail Resume Pengajuan"):
                    st.write(f"**Nama:** {nama}")
                    st.write(f"**Lab:** {lab_tujuan}")
                    st.write(f"**Waktu:** {waktu_event}")
                    if berkas:
                        st.write(f"**Berkas Lampiran:** {berkas.name}")
            else:
                st.error("Gagal! Mohon isi Nama, NIM, dan Keperluan terlebih dahulu.")

# ===============================
# FUNGSI TAMPILAN GEDUNG & DETAIL
# ===============================
def tampilkan_gedung(nama_gedung):
    st.header(f"🏢 {nama_gedung}")
    
    # Logika Foto Dinamis
    fotos = {
        "Gedung B": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+B",
        "Gedung E": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+E",
        "Gedung F": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+F",
        "Gedung G": "https://via.placeholder.com/800x300.png?text=VISUALISASI+GEDUNG+G"
    }
    st.image(fotos.get(nama_gedung, "https://via.placeholder.com/800x300"))
    
    st.divider()
    st.subheader("Daftar Laboratorium")
    
    lab_di_gedung = {k: v for k, v in DATABASE_LAB.items() if v["gedung"] == nama_gedung}
    cols = st.columns(len(lab_di_gedung))
    
    for i, (nama_lab, info) in enumerate(lab_di_gedung.items()):
        with cols[i]:
            if st.button(f"🔍 Info {nama_lab}", key=info["key"]):
                st.session_state.lab_terpilih = nama_lab
                st.rerun()

def halaman_detail_lab(nama_lab):
    st.button("⬅ Kembali ke Gedung", on_click=reset_lab)
    st.title(f"🔬 Detail: {nama_lab}")
    st.write(f"Selamat datang di halaman informasi khusus {nama_lab}.")
    # Di sini bisa kamu tambahkan list regulasi dan dosen seperti kode sebelumnya

# ===============================
# SIDEBAR & ROUTING
# ===============================
with st.sidebar:
    st.title("🔬 Lab-Info System")
    menu = st.radio("Navigasi Utama", ["Beranda", "Gedung B", "Gedung E", "Gedung F", "Gedung G", "Form Pinjam Lab"])

if st.session_state.lab_terpilih:
    halaman_detail_lab(st.session_state.lab_terpilih)
else:
    if menu == "Beranda":
        st.title("Sistem Informasi & Peminjaman Lab")
        st.write("Silakan pilih gedung di sidebar untuk melihat informasi lab atau klik **Form Pinjam Lab** untuk melakukan pengajuan.")
    elif menu == "Form Pinjam Lab":
        halaman_pinjam_lab()
    else:
        tampilkan_gedung(menu)
