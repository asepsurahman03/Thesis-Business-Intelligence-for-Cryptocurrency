"""
Script untuk mengupdate FORM PERSYARATAN SIDANG TESIS
berdasarkan data dari Tesis_Asep_Surahman_Sulaeman_2026_rapi.docx
"""

from docx import Document
from docx.shared import Pt
import copy
import os
import shutil

# =============================================
# DATA DARI TESIS_ASEP_SURAHMAN_SULAEMAN_2026_RAPI.DOCX
# =============================================
DATA = {
    "nama": "Asep Surahman Sulaeman",
    "nama_upper": "ASEP SURAHMAN SULAEMAN",
    "nim": "20250130001",
    "program_studi": "Magister Informatika",
    "judul": (
        "Kerangka Kerja Business Intelligence untuk Prediksi Cryptocurrency: "
        "Studi Komparatif LSTM, GRU, dan Ensemble Baseline Menggunakan "
        "Big Data Analytics dengan Integrasi Deep Learning"
    ),
    "tanggal": "05 Oktober 2026",
    "kota_tanggal": "Sukabumi, 05 Oktober 2026",
    "ketua_pembimbing": "Prof. Ts. Deden Witarsyah, S.T, Ph.D",
    "nidn_ketua_pembimbing": "0120240060",
    "anggota_pembimbing": "Assoc. Prof. Dr. Aswan Supriyadi Sunge, S.E., M.Kom",
    "nidn_anggota_pembimbing": "0426018003",
    "ketua_prodi": "Assoc. Prof. Dr. Adhi Kusnadi, S.T., M.Si",
    "nidn_ketua_prodi": "0303037304",
    "semester": "SEMESTER GANJIL TAHUN AKADEMIK 2025/2026",
    "tahun_akademik": "2025/2026",
}

# Path file
TESIS_DIR = r"Tesis"
FORM_IN = os.path.join(TESIS_DIR, "026 FORM PERSYARATAN SIDANG TESIS.docx")
FORM_OUT = os.path.join(TESIS_DIR, "026 FORM PERSYARATAN SIDANG TESIS.docx")

# Backup dulu
backup_path = FORM_OUT + ".bak_original"
if not os.path.exists(backup_path):
    shutil.copy2(FORM_IN, backup_path)
    print(f"Backup dibuat: {backup_path}")

doc = Document(FORM_IN)

def set_paragraph_text(para, new_text):
    """Ganti teks paragraf dengan mempertahankan format run pertama."""
    if not para.runs:
        para.add_run(new_text)
        return
    # Simpan format run pertama
    first_run = para.runs[0]
    font_name = first_run.font.name
    font_size = first_run.font.size
    bold = first_run.bold
    
    # Hapus semua run
    for run in para.runs:
        run.text = ""
    
    # Set teks di run pertama
    first_run.text = new_text
    if font_name:
        first_run.font.name = font_name
    if font_size:
        first_run.font.size = font_size
    first_run.bold = bold

def replace_in_para(para, old, new):
    """Replace teks dalam paragraf dengan mempertahankan format."""
    for run in para.runs:
        if old in run.text:
            run.text = run.text.replace(old, new)

print("\n=== MEMPROSES FORM ===")

# ============================
# HALAMAN 1: PENDAFTARAN SIDANG
# ============================
print("1. Mengisi PENDAFTARAN SIDANG...")

for i, para in enumerate(doc.paragraphs):
    txt = para.text

    # Header: Semester
    if "SEMESTER GENAP" in txt or "SEMESTER GANJIL" in txt:
        replace_in_para(para, "SEMESTER GENAP TAHUN AKADEMIK 2025/2026", "SEMESTER GANJIL TAHUN AKADEMIK 2025/2026")
        print(f"   [Para {i}] Update semester: {para.text.strip()[:80]}")

    # Program Studi header
    if txt.strip().startswith("PROGRAM STUDI S2"):
        replace_in_para(para, "PROGRAM STUDI S2 \t", f"PROGRAM STUDI S2 : {DATA['program_studi']}\t")
        print(f"   [Para {i}] Update program studi header: {para.text.strip()[:80]}")

    # Tanggal di halaman pertama
    if txt.strip() == "Sukabumi,":
        replace_in_para(para, "Sukabumi,", f"Sukabumi, {DATA['tanggal']}")
        print(f"   [Para {i}] Update tanggal halaman 1: {para.text.strip()[:80]}")

    # Nama Mahasiswa (tanda tangan)
    if txt.strip() == "Nama Mahasiswa":
        set_paragraph_text(para, DATA["nama"])
        print(f"   [Para {i}] Update nama mahasiswa: {para.text.strip()[:80]}")

# ============================
# HALAMAN 2: LEMBAR PERSYARATAN SIDANG
# ============================
print("\n2. Mengisi LEMBAR PERSYARATAN SIDANG...")

for i, para in enumerate(doc.paragraphs):
    txt = para.text.strip()

    # Nama :
    if txt == "Nama\t:":
        replace_in_para(para, "Nama\t:", f"Nama\t: {DATA['nama']}")
        print(f"   [Para {i}] Nama: {para.text.strip()[:80]}")

    # NIM :
    if txt == "NIM\t:":
        replace_in_para(para, "NIM\t:", f"NIM\t: {DATA['nim']}")
        print(f"   [Para {i}] NIM: {para.text.strip()[:80]}")

    # Program Studi :
    if txt == "Program Studi :":
        replace_in_para(para, "Program Studi :", f"Program Studi : {DATA['program_studi']}")
        print(f"   [Para {i}] Program Studi: {para.text.strip()[:80]}")

    # Sukabumi, (di halaman persyaratan)
    if "Sukabumi, \u0081" in txt or txt == "Sukabumi, \x81" or "Sukabumi, \u0081" in para.text:
        replace_in_para(para, "Sukabumi, \u0081", f"Sukabumi, {DATA['tanggal']}")
        print(f"   [Para {i}] Tanggal persyaratan: {para.text.strip()[:80]}")

    # Nama mahasiswa di bawah tanda tangan
    if txt == "Staff Admin Akademik\tNama Mahasiswa":
        replace_in_para(para, "Nama Mahasiswa", DATA["nama"])
        print(f"   [Para {i}] TTD nama: {para.text.strip()[:80]}")

    # Garis (titik-titik nama)
    if txt == "\u0081.\t\u0081":
        replace_in_para(para, "\u0081.\t\u0081", f"(Admin)\t{DATA['nama']}")
        print(f"   [Para {i}] Garis nama: {para.text.strip()[:80]}")

# ============================
# HALAMAN 3: LEMBAR PERSETUJUAN PELAKSANAAN SIDANG
# ============================
print("\n3. Mengisi LEMBAR PERSETUJUAN PELAKSANAAN SIDANG...")

for i, para in enumerate(doc.paragraphs):
    txt = para.text.strip()

    if txt == "Nama Mahasiswa\t:":
        replace_in_para(para, "Nama Mahasiswa\t:", f"Nama Mahasiswa\t: {DATA['nama']}")
        print(f"   [Para {i}] Nama mahasiswa: {para.text.strip()[:80]}")

    if "NIM\t:" in txt and "Program Studi" not in txt and i > 30:
        replace_in_para(para, "NIM\t:", f"NIM\t: {DATA['nim']}")
        print(f"   [Para {i}] NIM persetujuan: {para.text.strip()[:80]}")

    if txt == "Program Studi\t:":
        replace_in_para(para, "Program Studi\t:", f"Program Studi\t: {DATA['program_studi']}")
        print(f"   [Para {i}] Program Studi: {para.text.strip()[:80]}")

    if txt == "Judul Penelitian\t:":
        replace_in_para(para, "Judul Penelitian\t:", f"Judul Penelitian\t: {DATA['judul']}")
        print(f"   [Para {i}] Judul: {para.text.strip()[:80]}")

    # Nama Dosen (ketua & anggota pembimbing)
    if txt == "Nama Dosen\tNama Dosen":
        replace_in_para(para, "Nama Dosen\tNama Dosen",
                        f"{DATA['ketua_pembimbing']}\t{DATA['anggota_pembimbing']}")
        print(f"   [Para {i}] Nama dosen: {para.text.strip()[:80]}")

    # NIDN pembimbing
    if txt == "NIDN.\tNIDN.":
        replace_in_para(para, "NIDN.\tNIDN.",
                        f"NIDN. {DATA['nidn_ketua_pembimbing']}\tNIDN. {DATA['nidn_anggota_pembimbing']}")
        print(f"   [Para {i}] NIDN pembimbing: {para.text.strip()[:80]}")

    # Ketua Program Studi
    if "Ketua Program Studi" in txt and "..." in txt:
        replace_in_para(para, "Ketua Program Studi ... ", f"Ketua Program Studi Magister Informatika")
        print(f"   [Para {i}] Kaprodi label: {para.text.strip()[:80]}")

    # NIDN Kaprodi
    if txt == "NIDN :":
        replace_in_para(para, "NIDN :", f"NIDN : {DATA['nidn_ketua_prodi']}")
        print(f"   [Para {i}] NIDN kaprodi: {para.text.strip()[:80]}")

# ============================
# UPDATE TABLE 0: Form Pendaftaran
# ============================
print("\n4. Mengisi Tabel Form Pendaftaran...")

table0 = doc.tables[0]
# R0: Nama | value | NIM
# Isi kolom 1 (nilai)
def set_cell_text(cell, text):
    """Isi teks cell tabel."""
    for para in cell.paragraphs:
        for run in para.runs:
            run.text = ""
    if cell.paragraphs:
        if cell.paragraphs[0].runs:
            cell.paragraphs[0].runs[0].text = text
        else:
            cell.paragraphs[0].add_run(text)
    else:
        cell.add_paragraph(text)

# Row 0: Nama + NIM
set_cell_text(table0.rows[0].cells[1], DATA["nama"])
# NIM di kolom 2 (setelah label "NIM:")
for para in table0.rows[0].cells[2].paragraphs:
    if "NIM:" in para.text:
        replace_in_para(para, "NIM:", f"NIM: {DATA['nim']}")
        break
print(f"   Nama: {table0.rows[0].cells[1].text}")

# Row 2: Program Studi
set_cell_text(table0.rows[2].cells[1], DATA["program_studi"])
print(f"   Program Studi: {table0.rows[2].cells[1].text}")

# Row 8: Ketua Pembimbing
set_cell_text(table0.rows[8].cells[1], DATA["ketua_pembimbing"])
print(f"   Ketua Pembimbing: {table0.rows[8].cells[1].text}")

# Row 9: Anggota Pembimbing
set_cell_text(table0.rows[9].cells[1], DATA["anggota_pembimbing"])
print(f"   Anggota Pembimbing: {table0.rows[9].cells[1].text}")

# Row 10: Judul
set_cell_text(table0.rows[10].cells[1], DATA["judul"])
print(f"   Judul: {table0.rows[10].cells[1].text[:80]}")

# Simpan
doc.save(FORM_OUT)
print(f"\n✅ SELESAI! Form tersimpan di: {FORM_OUT}")
print("\nData yang diisi:")
print(f"  Nama          : {DATA['nama']}")
print(f"  NIM           : {DATA['nim']}")
print(f"  Program Studi : {DATA['program_studi']}")
print(f"  Ketua Pembimbing  : {DATA['ketua_pembimbing']} (NIDN: {DATA['nidn_ketua_pembimbing']})")
print(f"  Anggota Pembimbing: {DATA['anggota_pembimbing']} (NIDN: {DATA['nidn_anggota_pembimbing']})")
print(f"  Ketua Prodi   : {DATA['ketua_prodi']} (NIDN: {DATA['nidn_ketua_prodi']})")
print(f"  Tanggal       : {DATA['kota_tanggal']}")
print(f"  Judul         : {DATA['judul'][:80]}...")
