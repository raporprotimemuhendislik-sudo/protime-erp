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
conn.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
conn.execute("CREATE TABLE IF NOT EXISTS yapılacaklar (id INTEGER PRIMARY KEY AUTOINCREMENT, is_tanimi TEXT)")
conn.commit(); conn.close()

# --- PDF OLUŞTURMA (Türkçe Karakter Destekli) ---
def pdf_olustur(paket, toplam, baslik, birim, kur=None):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # Başlık Türkçe karakter sorunu olmaması için İngilizce karakterlerle yazıldı
    elements = [Paragraph("PROTIME FIYAT LISTESI", styles['Title'])]
    
    data = [["Marka", "Urun", "Fiyat"]]
    for item in paket:
        # Ürün isimlerindeki karakterleri temizleyerek ekliyoruz
        marka = item['marka'].replace('İ', 'I').replace('ı', 'i').replace('Ş', 'S').replace('ş', 's').replace('Ç', 'C').replace('ç', 'c').replace('Ğ', 'G').replace('ğ', 'g').replace('Ü', 'U').replace('ü', 'u').replace('Ö', 'O').replace('ö', 'o')
        urun = item['urun'].replace('İ', 'I').replace('ı', 'i').replace('Ş', 'S').replace('ş', 's').replace('Ç', 'C').replace('ç', 'c').replace('Ğ', 'G').replace('ğ', 'g').replace('Ü', 'U').replace('ü', 'u').replace('Ö', 'O').replace('ö', 'o')
        data.append([marka, urun, f"{item['fiyat']:.2f} {birim}"])
    
    data.append(["", "TOPLAM", f"{toplam:,.2f} {birim}"])
    if kur: 
        data.append(["", "TOPLAM TL", f"{(toplam*kur):,.2f} TL"])
    
    table = Table(data, colWidths=[150, 200, 100])
    table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black), 
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey)
    ]))
    elements.append(table)
    doc.build(elements)
    return buffer

# --- OTURUM ---
if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 34.50
if "paket_GES" not in st.session_state: st.session_state.paket_GES = []
if "paket_ELEKTRIK" not in st.session_state: st.session_state.paket_ELEKTRIK = []

# --- YAN MENÜ (YAPILACAKLAR & DEPARTMAN) ---
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=2)
        st.session_state.usd_kuru = float(res.json()["rates"]["TRY"])
    except: st.session_state.usd_kuru = 34.50
    st.metric("📊 CANLI USD/TL", f"{st.session_state.usd_kuru:.4f}")
    
    secim = st.radio("DEPARTMAN", ["☀️ GES (USD)", "⚡ ELEKTRİK (TL)"])
    aktif_modul = "GES" if "GES" in secim else "ELEKTRIK"
    aktif_paket = st.session_state.paket_GES if aktif_modul == "GES" else st.session_state.paket_ELEKTRIK
    
    st.write("---")
    st.subheader("📌 YAPILACAK İŞLER")
    yeni_is = st.text_input("Yeni iş ekle...")
    if st.button("İşi Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi) VALUES (?)", (yeni_is,))
        conn.commit(); conn.close(); st.rerun()
    
    conn = get_db_connection()
    for row in conn.execute("SELECT id, is_tanimi FROM yapılacaklar").fetchall():
        c1, c2 = st.columns([4, 1])
        c1.write(f"- {row[1]}")
        if c2.button("❌", key=f"is_{row[0]}"):
            conn.execute("DELETE FROM yapılacaklar WHERE id=?", (row[0],)); conn.commit(); st.rerun()
    conn.close()

# --- ANA İÇERİK ---
st.title(f"{aktif_modul} İSTASYONU")
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📦 Katalog")
    # Arama çubuğu
    arama_terimi = st.text_input("🔍 Ürün veya marka ara...", key="arama_input")
    
    with st.container(height=350): 
        conn = get_db_connection()
        # Sorguyu arama terimine göre güncelledik
        sorgu = "SELECT id, marka, urun_adi, fiyat FROM urunler WHERE modul=? AND (marka LIKE ? OR urun_adi LIKE ?)"
        arama_filtresi = f"%{arama_terimi}%"
        
        for r in conn.execute(sorgu, (aktif_modul, arama_filtresi, arama_filtresi)).fetchall():
            cols = st.columns([3, 2, 1, 1])
            cols[0].write(f"{r[1]} - {r[2]}")
            cols[1].write(f"{r[3]} {'$' if aktif_modul=='GES' else 'TL'}")
            if cols[2].button("🗑️", key=f"del_{r[0]}"):
                conn.execute("DELETE FROM urunler WHERE id=?", (r[0],)); conn.commit(); st.rerun()
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

# --- HAKEDİŞ ---
st.subheader(f"📊 {aktif_modul} Hakediş Paketi")
if aktif_paket:
    toplam = sum(i["fiyat"] for i in aktif_paket)
    birim = "$" if aktif_modul == "GES" else "TL"
    
    # Paketi göster
    for i, item in enumerate(aktif_paket):
        st.write(f"✅ {item['marka']} | {item['urun']} | {item['fiyat']} {birim}")
    
    if aktif_modul == "GES":
        st.info(f"💰 TOPLAM: ${toplam:,.2f} | ₺{(toplam * st.session_state.usd_kuru):,.2f} TL")
    else:
        st.info(f"💰 TOPLAM: {toplam:,.2f} TL")
        
    kur_param = st.session_state.usd_kuru if aktif_modul == "GES" else None
    pdf_buf = pdf_olustur(aktif_paket, toplam, f"{aktif_modul} Hakediş", birim, kur_param)
    st.download_button("📄 PDF İNDİR", pdf_buf, "hakedis.pdf", "application/pdf")
    if st.button("Listeyi Temizle"):
        if aktif_modul == "GES": st.session_state.paket_GES = []
        else: st.session_state.paket_ELEKTRIK = []
        st.rerun()
