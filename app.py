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

st.set_page_config(page_title="PROTIME ERP | Enterprise", page_icon="⚡", layout="wide")

# ----------------------------------------------------
# PDF VE VERİTABANI AYARLARI
# ----------------------------------------------------
def get_db_connection():
    return sqlite3.connect("protime_erp_web.db", check_same_thread=False, timeout=30)

def pdf_olustur(paket, toplam_usd, toplam_tl):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    elements.append(Paragraph("PROTIME MÜHENDİSLİK - HAKEDİŞ RAPORU", styles['Title']))
    data = [["Marka", "Ürün", "Fiyat ($)", "Fiyat (TL)"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"${item['n_usd']:.2f}", f"{(item['n_usd']*st.session_state.usd_kuru):,.2f} TL"])
    data.append(["", "TOPLAM", f"${toplam_usd:.2f}", f"{toplam_tl:,.2f} TL"])
    t = Table(data, colWidths=[100, 200, 80, 80])
    t.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 1, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.grey)]))
    elements.append(t)
    doc.build(elements)
    return buffer

@st.fragment(run_every="5m")
def kur_gostergesi_fragment():
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
        st.session_state.usd_kuru = float(res.json()["rates"]["TRY"])
    except:
        st.session_state.usd_kuru = 34.50
    st.metric("📊 CANLI REEL USD/TL KURU", f"{st.session_state.usd_kuru:.4f} TL")

# Başlatıcılar
if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 34.50
if "paket" not in st.session_state: st.session_state.paket = []

# ----------------------------------------------------
# YAN MENÜ
# ----------------------------------------------------
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    aktif_modul = "GES" if "GES" in st.radio("⚡ DEPARTMAN", ["☀️ GES", "⚡ ELEKTRİK TAAHHÜT"]) else "ELEKTRIK"
    kur_gostergesi_fragment()
    st.write("---")
    
    st.subheader("📌 YAPILACAKLAR")
    yeni_is = st.text_input("Yeni iş...")
    if st.button("İş Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi) VALUES (?)", (yeni_is,))
        conn.commit(); conn.close(); st.rerun()
    
    conn = get_db_connection()
    isler = conn.execute("SELECT id, is_tanimi FROM yapılacaklar").fetchall()
    conn.close()
    if isler:
        st.error(f"⚠️ {len(isler)} Bekleyen İş!")
        for i in isler:
            col_i1, col_i2 = st.columns([4, 1])
            col_i1.write(f"- {i[1]}")
            if col_i2.button("❌", key=f"is_{i[0]}"):
                conn = get_db_connection()
                conn.execute("DELETE FROM yapılacaklar WHERE id=?", (i[0],))
                conn.commit(); conn.close(); st.rerun()

# ----------------------------------------------------
# ANA İÇERİK
# ----------------------------------------------------
st.title(f"PROTIME ERP // {aktif_modul} İSTASYONU")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📦 Katalog")
    conn = get_db_connection()
    rows = conn.execute("SELECT id, marka, urun_adi, nakit_usd FROM urunler WHERE modul=?", (aktif_modul,)).fetchall()
    conn.close()
    for r in rows:
        c1, c2, c3, c4 = st.columns([2, 2, 1, 1])
        c1.write(r[1]); c2.write(r[2]); c3.write(f"${r[3]}")
        if c4.button("🗑️", key=f"del_{r[0]}"):
            conn = get_db_connection()
            conn.execute("DELETE FROM urunler WHERE id=?", (r[0],))
            conn.commit(); conn.close(); st.rerun()
        if st.button("Ekle", key=f"add_{r[0]}"):
            st.session_state.paket.append({"marka": r[1], "urun": r[2], "n_usd": r[3]})
            st.rerun()

with col2:
    st.subheader("➕ Yeni Ürün Ekle")
    with st.form("yeni", clear_on_submit=True):
        m, t, f = st.text_input("Marka"), st.text_input("Tanım"), st.number_input("USD Fiyat")
        if st.form_submit_button("Kaydet"):
            conn = get_db_connection()
            conn.execute("INSERT INTO urunler (modul, marka, urun_adi, nakit_usd) VALUES (?,?,?,?)", (aktif_modul, m, t, f))
            conn.commit(); conn.close(); st.rerun()

# HAKEDİŞ
st.subheader("📊 Finansal Hakediş")
if "paket" in st.session_state and st.session_state.paket:
    t_n = 0
    for i, item in enumerate(st.session_state.paket):
        t_n += item["n_usd"]
        st.write(f"✅ {item['marka']} - {item['urun']} | **${item['n_usd']}** (~{(item['n_usd']*st.session_state.usd_kuru):,.2f} TL)")
    
    tl_toplam = t_n * st.session_state.usd_kuru
    st.info(f"💰 TOPLAM: ${t_n:,.2f} | {tl_toplam:,.2f} TL")
    
    c_pdf, c_del = st.columns(2)
    pdf_buffer = pdf_olustur(st.session_state.paket, t_n, tl_toplam)
    c_pdf.download_button("📄 PDF İndir", pdf_buffer, "rapor.pdf", "application/pdf")
    if c_del.button("🗑️ Listeyi Temizle"):
        st.session_state.paket = []
        st.rerun()
