import streamlit as st
import requests
import sqlite3
import io
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

st.set_page_config(page_title="PROTIME ERP", layout="wide")

# --- VERİTABANI ---
def get_db_connection():
    return sqlite3.connect("protime_yeni.db", check_same_thread=False)

conn = get_db_connection()
conn.execute("CREATE TABLE IF NOT EXISTS urunler_v3 (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
conn.execute("CREATE TABLE IF NOT EXISTS yapılacaklar (id INTEGER PRIMARY KEY AUTOINCREMENT, is_tanimi TEXT)")
conn.commit(); conn.close()

# --- PDF OLUŞTURMA (GÜVENLİ YAPI) ---
def pdf_olustur(paket, toplam, baslik, birim, kur=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=50, leftMargin=50, topMargin=50, bottomMargin=50)
    elements = []
    styles = getSampleStyleSheet()

    # Logo ekleme (Dosya varsa ekle)
    if os.path.exists("logo.png"):
        elements.append(Image("logo.png", width=120, height=40))
        elements.append(Paragraph("<br/>", styles['Normal']))
    
    # Firma Bilgileri
    firma = """
    <b>PROTIME MÜHENDİSLİK</b><br/>
    Küçük Kayaş Mah. 19 Mayıs Bulvarı 222/A Mamak, ANKARA<br/>
    Tel: 0530 135 89 86 / 0533 285 10 31<br/><br/>
    """
    elements.append(Paragraph(firma, styles['Normal']))
    
    # Başlık ve Tablo
    elements.append(Paragraph(f"<b>{baslik}</b>", styles['Title']))
    elements.append(Paragraph("<br/>", styles['Normal']))
    
    data = [["Marka", "Ürün", "Fiyat"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"{item['fiyat']:.2f} {birim}"])
    data.append(["", "TOPLAM", f"{toplam:,.2f} {birim}"])
    if kur:
        data.append(["", "TOPLAM (TL)", f"{(toplam*kur):,.2f} TL"])
    
    table = Table(data, colWidths=[100, 250, 80])
    table.setStyle(TableStyle([('GRID', (0,0), (-1,-1), 0.5, colors.black), ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)]))
    elements.append(table)
    
    doc.build(elements)
    return buffer

# --- OTURUM ---
if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 34.50
if "kur_zaman" not in st.session_state: st.session_state.kur_zaman = "N/A"
if "paket_GES" not in st.session_state: st.session_state.paket_GES = []
if "paket_ELEKTRIK" not in st.session_state: st.session_state.paket_ELEKTRIK = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("PROTIME ERP")
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=3)
        st.session_state.usd_kuru = float(res.json()["rates"]["TRY"])
        st.session_state.kur_zaman = datetime.now(ZoneInfo("Europe/Istanbul")).strftime("%H:%M:%S")
    except: st.session_state.usd_kuru = 34.50
    
    st.metric("📊 USD/TL", f"{st.session_state.usd_kuru:.4f}")
    st.caption(f"🕒 {st.session_state.kur_zaman}")
    
    secim = st.radio("DEPARTMAN", ["☀️ GES (USD)", "⚡ ELEKTRİK (TL)"])
    aktif_modul = "GES" if "GES" in secim else "ELEKTRIK"
    aktif_paket = st.session_state.paket_GES if aktif_modul == "GES" else st.session_state.paket_ELEKTRIK
    
    st.write("---")
    yeni_is = st.text_input("📌 Yeni iş ekle...")
    if st.button("Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi) VALUES (?)", (yeni_is,))
        conn.commit(); conn.close()
        st.success("İş eklendi!")
        st.rerun()

# --- ANA EKRAN ---
st.title(f"{aktif_modul} İSTASYONU")
c1, c2 = st.columns([2, 1])

with c1:
    conn = get_db_connection()
    for r in conn.execute("SELECT id, marka, urun_adi, fiyat FROM urunler_v3 WHERE modul=?", (aktif_modul,)).fetchall():
        cols = st.columns([3, 2, 1])
        cols[0].write(f"{r[1]} - {r[2]} ({r[3]}{'$' if aktif_modul=='GES' else 'TL'})")
        if cols[1].button("➕", key=f"add_{r[0]}"):
            aktif_paket.append({"marka": r[1], "urun": r[2], "fiyat": r[3]})
            st.rerun()
    conn.close()

with c2:
    with st.form("yeni", clear_on_submit=True):
        m = st.text_input("Marka"); t = st.text_input("Ürün"); f = st.number_input("Fiyat")
        if st.form_submit_button("Kaydet"):
            conn = get_db_connection()
            conn.execute("INSERT INTO urunler_v3 (modul, marka, urun_adi, fiyat) VALUES (?,?,?,?)", (aktif_modul, m, t, f))
            conn.commit(); conn.close(); st.rerun()

# --- HAKEDİŞ ---
if aktif_paket:
    toplam = sum(i["fiyat"] for i in aktif_paket)
    kur = st.session_state.usd_kuru if aktif_modul == "GES" else None
    
    st.info(f"TOPLAM: {toplam:,.2f} {'$' if aktif_modul=='GES' else 'TL'}")
    
    pdf_buf = pdf_olustur(aktif_paket, toplam, f"{aktif_modul} Hakediş", "$" if aktif_modul=='GES' else "TL", kur)
    st.download_button("📄 PDF İNDİR", pdf_buf, "fatura.pdf", "application/pdf")
