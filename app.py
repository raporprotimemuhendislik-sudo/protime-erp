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
    conn = sqlite3.connect("protime_erp_final.db", check_same_thread=False)
    # Tablo adını değiştirdik (yapılacaklar -> yapılacaklar_v2)
    conn.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
    conn.execute("CREATE TABLE IF NOT EXISTS yapılacaklar_v2 (id INTEGER PRIMARY KEY AUTOINCREMENT, is_tanimi TEXT, durum INTEGER DEFAULT 0)")
    return conn

# --- PDF OLUŞTURMA ---
def pdf_olustur(paket, toplam, birim, kur=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = [Paragraph("PROTIME FIYAT LISTESI", styles['Title'])]
    
    data = [["Marka", "Urun", "Fiyat"]]
    for item in paket:
        m = item['marka'].replace('İ', 'I').replace('ı', 'i').replace('Ş', 'S').replace('ş', 's').replace('Ç', 'C').replace('ç', 'c').replace('Ğ', 'G').replace('ğ', 'g').replace('Ü', 'U').replace('ü', 'u').replace('Ö', 'O').replace('ö', 'o')
        u = item['urun'].replace('İ', 'I').replace('ı', 'i').replace('Ş', 'S').replace('ş', 's').replace('Ç', 'C').replace('ç', 'c').replace('Ğ', 'G').replace('ğ', 'g').replace('Ü', 'U').replace('ü', 'u').replace('Ö', 'O').replace('ö', 'o')
        data.append([m, u, f"{item['fiyat']:.2f} {birim}"])
    
    data.append(["", "TOPLAM", f"{toplam:,.2f} {birim}"])
    if kur: data.append(["", "TOPLAM TL", f"{(toplam*kur):,.2f} TL"])
    
    table = Table(data, colWidths=[150, 200, 100])
    table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)]))
    elements.append(table)
    doc.build(elements)
    return buffer

# --- OTURUM ---
if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 34.50
if "paket_GES" not in st.session_state: st.session_state.paket_GES = []
if "paket_ELEKTRIK" not in st.session_state: st.session_state.paket_ELEKTRIK = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    
    # 1. BEKLEYEN İŞLER
    st.subheader("⏳ BEKLEYEN İŞLER")
    yeni_is = st.text_input("Yeni iş ekle...")
    if st.button("Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar_v2 (is_tanimi, durum) VALUES (?, 0)", (yeni_is,))
        conn.commit(); conn.close(); st.rerun()
    
    conn = get_db_connection()
    bekleyenler = conn.execute("SELECT id, is_tanimi FROM yapılacaklar_v2 WHERE durum=0").fetchall()
    for row in bekleyenler:
        c1, c2 = st.columns([4, 1])
        c1.write(f"• {row[1]}")
        if c2.button("✅", key=f"bekleyen_{row[0]}"):
            conn.execute("UPDATE yapılacaklar_v2 SET durum=1 WHERE id=?", (row[0],)); conn.commit(); st.rerun()

    # 2. YAPILACAK İŞLER
    st.write("---")
    st.subheader("📋 YAPILACAK İŞLER")
    yapilacaklar = conn.execute("SELECT id, is_tanimi FROM yapılacaklar_v2 WHERE durum=1").fetchall()
    for row in yapilacaklar:
        c1, c2 = st.columns([4, 1])
        c1.write(f"✓ {row[1]}")
        if c2.button("🗑️", key=f"sil_{row[0]}"):
            conn.execute("DELETE FROM yapılacaklar_v2 WHERE id=?", (row[0],)); conn.commit(); st.rerun()
    conn.close()

# --- ANA İÇERİK ---
aktif_modul = "GES" if "GES" in st.radio("DEPARTMAN", ["☀️ GES (USD)", "⚡ ELEKTRİK (TL)"]) else "ELEKTRIK"
aktif_paket = st.session_state.paket_GES if aktif_modul == "GES" else st.session_state.paket_ELEKTRIK

st.title(f"{aktif_modul} İSTASYONU")
arama = st.text_input("🔍 Ürün veya marka ara...")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📦 Katalog")
    with st.container(height=400):
        conn = get_db_connection()
        sorgu = "SELECT id, marka, urun_adi, fiyat FROM urunler WHERE modul=? AND (marka LIKE ? OR urun_adi LIKE ?)"
        for r in conn.execute(sorgu, (aktif_modul, f"%{arama}%", f"%{arama}%")).fetchall():
            cols = st.columns([3, 2, 1, 1])
            cols[0].write(f"{r[1]} - {r[2]}")
            cols[1].write(f"{r[3]} {'$' if aktif_modul=='GES' else 'TL'}")
            if cols[3].button("➕", key=f"add_{r[0]}"):
                aktif_paket.append({"marka": r[1], "urun": r[2], "fiyat": r[3]})
                st.rerun()
        conn.close()

with c2:
    st.subheader("➕ Yeni Ürün")
    with st.form("yeni", clear_on_submit=True):
        m = st.text_input("Marka"); t = st.text_input("Ürün"); f = st.number_input("Fiyat")
        if st.form_submit_button("Kaydet"):
            conn = get_db_connection()
            conn.execute("INSERT INTO urunler (modul, marka, urun_adi, fiyat) VALUES (?,?,?,?)", (aktif_modul, m, t, f))
            conn.commit(); conn.close(); st.rerun()
