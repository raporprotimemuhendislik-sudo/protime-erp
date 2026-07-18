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
    return sqlite3.connect("protime_erp_final.db", check_same_thread=False)

conn = get_db_connection()
# 'durum' sütunu eklendi: 0 = Bekleyen, 1 = Kabul Edilen (Yapılacak)
conn.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
conn.execute("CREATE TABLE IF NOT EXISTS yapılacaklar (id INTEGER PRIMARY KEY AUTOINCREMENT, is_tanimi TEXT, durum INTEGER DEFAULT 0)")
conn.commit(); conn.close()

# --- PDF OLUŞTURMA (Aynı kalıyor) ---
def pdf_olustur(paket, toplam, birim, kur=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph("PROTIME FIYAT LISTESI", styles['Title'])]
    data = [["Marka", "Urun", "Fiyat"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"{item['fiyat']:.2f} {birim}"])
    data.append(["", "TOPLAM", f"{toplam:,.2f} {birim}"])
    if kur: data.append(["", "TOPLAM TL", f"{(toplam*kur):,.2f} TL"])
    table = Table(data, colWidths=[150, 200, 100])
    table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)]))
    elements.append(table)
    doc.build(elements)
    return buffer

# --- YAN MENÜ ---
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    
    st.subheader("📌 BEKLEYEN İŞLER")
    yeni_is = st.text_input("Yeni iş girin...", key="yeni_is")
    if st.button("Bekleyenlere Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi, durum) VALUES (?, 0)", (yeni_is,))
        conn.commit(); conn.close(); st.rerun()
    
    conn = get_db_connection()
    bekleyenler = conn.execute("SELECT id, is_tanimi FROM yapılacaklar WHERE durum=0").fetchall()
    for row in bekleyenler:
        c1, c2 = st.columns([4, 1])
        c1.write(f"⏳ {row[1]}")
        if c2.button("✅ Kabul Et", key=f"kabul_{row[0]}"):
            conn.execute("UPDATE yapılacaklar SET durum=1 WHERE id=?", (row[0],)); conn.commit(); st.rerun()
    
    st.write("---")
    st.subheader("📋 YAPILACAK İŞLER")
    yapilacaklar = conn.execute("SELECT id, is_tanimi FROM yapılacaklar WHERE durum=1").fetchall()
    for row in yapilacaklar:
        c1, c2 = st.columns([4, 1])
        c1.write(f"✅ {row[1]}")
        if c2.button("❌", key=f"sil_{row[0]}"):
            conn.execute("DELETE FROM yapılacaklar WHERE id=?", (row[0],)); conn.commit(); st.rerun()
    conn.close()

# --- ANA İÇERİK ---
# ... (Ürün Katalog ve Hakediş kısımları aynı kalıyor) ...
