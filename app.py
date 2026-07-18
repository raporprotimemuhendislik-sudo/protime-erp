import streamlit as st
import requests
import sqlite3
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="PROTIME ERP", layout="wide")

# --- VERİTABANI ---
def get_db_connection():
    return sqlite3.connect("protime_erp.db", check_same_thread=False)

conn = get_db_connection()
conn.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
conn.execute("CREATE TABLE IF NOT EXISTS yapılacaklar (id INTEGER PRIMARY KEY AUTOINCREMENT, is_tanimi TEXT)")
conn.commit(); conn.close()

# --- PDF OLUŞTURMA ---
def pdf_olustur(paket, toplam, baslik, birim):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph(baslik, styles['Title'])]
    data = [["Marka", "Ürün", "Fiyat"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"{item['fiyat']:.2f} {birim}"])
    data.append(["", "TOPLAM", f"{toplam:,.2f} {birim}"])
    table = Table(data, colWidths=[150, 200, 100])
    table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)]))
    elements.append(table)
    doc.build(elements)
    return buffer

# --- SESSION ---
if "paket_GES" not in st.session_state: st.session_state.paket_GES = []
if "paket_ELEKTRIK" not in st.session_state: st.session_state.paket_ELEKTRIK = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    secim = st.radio("DEPARTMAN", ["☀️ GES", "⚡ ELEKTRİK"])
    aktif_modul = "GES" if "GES" in secim else "ELEKTRIK"
    aktif_paket = st.session_state.paket_GES if aktif_modul == "GES" else st.session_state.paket_ELEKTRIK
    
    st.write("---")
    st.subheader("📌 YAPILACAK İŞLER")
    yeni_is = st.text_input("Yeni iş ekle...")
    if st.button("Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi) VALUES (?)", (yeni_is,))
        conn.commit(); conn.close()
        st.rerun()
    
    conn = get_db_connection()
    for row in conn.execute("SELECT id, is_tanimi FROM yapılacaklar").fetchall():
        c1, c2 = st.columns([4, 1])
        c1.write(f"- {row[1]}")
        if c2.button("❌", key=f"is_{row[0]}"):
            conn.execute("DELETE FROM yapılacaklar WHERE id=?", (row[0],))
            conn.commit(); conn.close(); st.rerun()
    conn.close()

# --- ANA EKRAN ---
st.title(f"{aktif_modul} İSTASYONU")
c1, c2 = st.columns([2, 1])

with c1:
    conn = get_db_connection()
    for r in conn.execute("SELECT id, marka, urun_adi, fiyat FROM urunler WHERE modul=?", (aktif_modul,)).fetchall():
        cols = st.columns([3, 2, 1])
        cols[0].write(f"{r[1]} - {r[2]} ({r[3]})")
        if cols[1].button("➕", key=f"add_{r[0]}"):
            aktif_paket.append({"marka": r[1], "urun": r[2], "fiyat": r[3]})
            st.rerun()
    conn.close()

with c2:
    with st.form("yeni_form", clear_on_submit=True):
        m = st.text_input("Marka"); t = st.text_input("Ürün"); f = st.number_input("Fiyat")
        if st.form_submit_button("Kaydet"):
            conn = get_db_connection()
            conn.execute("INSERT INTO urunler (modul, marka, urun_adi, fiyat) VALUES (?,?,?,?)", (aktif_modul, m, t, f))
            conn.commit(); conn.close(); st.rerun()

# --- HAKEDİŞ ---
if aktif_paket:
    toplam = sum(i["fiyat"] for i in aktif_paket)
    st.info(f"TOPLAM: {toplam:,.2f}")
    pdf_buf = pdf_olustur(aktif_paket, toplam, f"{aktif_modul} Hakediş", "Birim")
    st.download_button("📄 PDF İNDİR", pdf_buf, "hakedis.pdf", "application/pdf")
    if st.button("Listeyi Temizle"):
        if aktif_modul == "GES": st.session_state.paket_GES = []
        else: st.session_state.paket_ELEKTRIK = []
        st.rerun()
