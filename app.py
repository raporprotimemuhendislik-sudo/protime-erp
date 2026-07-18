import streamlit as st
import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import sqlite3
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="PROTIME ERP", layout="wide")

# --- VERİTABANI VE PDF ---
def get_db_connection():
    return sqlite3.connect("protime_erp_web.db", check_same_thread=False)

def pdf_olustur(paket, toplam_usd, toplam_tl):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = [Paragraph("HAKEDIS RAPORU", getSampleStyleSheet()['Title'])]
    data = [["Marka", "Ürün", "Fiyat ($)", "Fiyat (TL)"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"${item['n_usd']}", f"{(item['n_usd']*st.session_state.usd_kuru):,.2f} TL"])
    elements.append(Table(data, colWidths=[100, 200, 80, 80]))
    doc.build(elements)
    return buffer

# --- SESSION BAŞLATMA ---
if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 34.50
if "paket" not in st.session_state: st.session_state.paket = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("PROTIME")
    aktif_modul = "GES" if "GES" in st.radio("DEPARTMAN", ["☀️ GES", "⚡ ELEKTRİK"]) else "ELEKTRIK"
    st.write("---")
    st.subheader("📌 YAPILACAKLAR")
    yeni_is = st.text_input("Yeni iş...")
    if st.button("İş Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi) VALUES (?)", (yeni_is,))
        conn.commit(); conn.close(); st.rerun()
    
    conn = get_db_connection()
    for row in conn.execute("SELECT id, is_tanimi FROM yapılacaklar").fetchall():
        c1, c2 = st.columns([4, 1])
        c1.write(f"- {row[1]}")
        if c2.button("❌", key=f"is_{row[0]}"):
            conn.execute("DELETE FROM yapılacaklar WHERE id=?", (row[0],))
            conn.commit(); conn.close(); st.rerun()
    conn.close()

# --- ANA İÇERİK ---
st.title(f"{aktif_modul} İSTASYONU")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📦 Katalog (Küçük Liste)")
    conn = get_db_connection()
    for r in conn.execute("SELECT id, marka, urun_adi, nakit_usd FROM urunler WHERE modul=?", (aktif_modul,)).fetchall():
        cols = st.columns([3, 2, 1, 1])
        cols[0].caption(f"{r[1]} - {r[2]}")
        cols[1].caption(f"${r[3]}")
        if cols[2].button("🗑️", key=f"del_{r[0]}"):
            conn.execute("DELETE FROM urunler WHERE id=?", (r[0],)); conn.commit(); st.rerun()
        if cols[3].button("➕", key=f"add_{r[0]}"):
            st.session_state.paket.append({"marka": r[1], "urun": r[2], "n_usd": r[3]})
            st.rerun()
    conn.close()

with c2:
    st.subheader("➕ Ürün Ekle")
    with st.form("yeni", clear_on_submit=True):
        m = st.text_input("Marka"); t = st.text_input("Tanım"); f = st.number_input("Fiyat ($)")
        if st.form_submit_button("Kaydet"):
            conn = get_db_connection()
            conn.execute("INSERT INTO urunler (modul, marka, urun_adi, nakit_usd) VALUES (?,?,?,?)", (aktif_modul, m, t, f))
            conn.commit(); conn.close(); st.rerun()

# --- HAKEDİŞ ---
if st.session_state.paket:
    st.subheader("📊 Finansal Hakediş")
    toplam = sum(i["n_usd"] for i in st.session_state.paket)
    for i, item in enumerate(st.session_state.paket):
        st.write(f"✅ {item['marka']} | {item['urun']} | ${item['n_usd']}")
    st.info(f"💰 Toplam: ${toplam:,.2f} / {(toplam*st.session_state.usd_kuru):,.2f} TL")
    if st.button("📄 PDF İndir"):
        st.download_button("İndir", pdf_olustur(st.session_state.paket, toplam, toplam*st.session_state.usd_kuru), "rapor.pdf")
