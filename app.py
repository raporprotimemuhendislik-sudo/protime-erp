import streamlit as st
import sqlite3
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="PROTIME ERP", layout="wide")

# Veritabanı kurulumu
def get_db():
    db = sqlite3.connect("protime_yeni_sistem.db", check_same_thread=False)
    return db

conn = get_db()
conn.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
conn.execute("CREATE TABLE IF NOT EXISTS isler (id INTEGER PRIMARY KEY, tanim TEXT, durum INTEGER)") # 0:Bekleyen, 1:Yapılacak
conn.commit()
conn.close()

# PDF temizleme
def temizle(t):
    return str(t).replace('İ','I').replace('ı','i').replace('Ş','S').replace('ş','s').replace('Ç','C').replace('ç','c').replace('Ğ','G').replace('ğ','g').replace('Ü','U').replace('ü','u').replace('Ö','O').replace('ö','o')

# Yan Menü: İş Takibi
with st.sidebar:
    st.subheader("📌 BEKLEYEN İŞLER")
    yeni = st.text_input("Yeni iş girin")
    if st.button("Ekle") and yeni:
        c = get_db(); c.execute("INSERT INTO isler (tanim, durum) VALUES (?, 0)", (yeni,)); c.commit(); c.close(); st.rerun()
    
    c = get_db()
    for row in c.execute("SELECT id, tanim FROM isler WHERE durum=0").fetchall():
        col1, col2 = st.columns([3,1])
        col1.write(row[1])
        if col2.button("✅", key=f"b_{row[0]}"): c.execute("UPDATE isler SET durum=1 WHERE id=?", (row[0],)); c.commit(); st.rerun()
    
    st.write("---")
    st.subheader("📋 YAPILACAK İŞLER")
    for row in c.execute("SELECT id, tanim FROM isler WHERE durum=1").fetchall():
        col1, col2 = st.columns([3,1])
        col1.write(row[1])
        if col2.button("❌", key=f"y_{row[0]}"): c.execute("DELETE FROM isler WHERE id=?", (row[0],)); c.commit(); st.rerun()
    c.close()

# Ana Sayfa
tab1, tab2 = st.tabs(["☀️ GES (USD)", "⚡ ELEKTRİK (TL)"])
modul = "GES" if tab1 else "ELEKTRIK"

with tab1 if modul == "GES" else tab2:
    st.header(f"{modul} Kataloğu")
    c = get_db()
    # Ekleme formu
    with st.form("ekle"):
        m, u, f = st.text_input("Marka"), st.text_input("Ürün"), st.number_input("Fiyat")
        if st.form_submit_button("Ürün Kaydet"): c.execute("INSERT INTO urunler (modul, marka, urun_adi, fiyat) VALUES (?,?,?,?)", (modul, m, u, f)); c.commit(); st.rerun()
    
    # Katalog
    for r in c.execute("SELECT id, marka, urun_adi, fiyat FROM urunler WHERE modul=?", (modul,)).fetchall():
        st.write(f"{r[1]} - {r[2]} : {r[3]}")
    c.close()
