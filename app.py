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

# ----------------------------------------------------
# 1. TASARIM VE AYARLAR
# ----------------------------------------------------
st.set_page_config(page_title="PROTIME ERP | Enterprise", page_icon="⚡", layout="wide")

# ----------------------------------------------------
# 2. VERİTABANI VE KUR MOTORU
# ----------------------------------------------------
def get_db_connection():
    return sqlite3.connect("protime_erp_web.db", check_same_thread=False, timeout=30)

@st.fragment(run_every="5m")
def kur_gostergesi_fragment():
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
        kur = float(res.json()["rates"]["TRY"])
    except:
        kur = 34.50
    st.session_state.usd_kuru = kur
    tr_saat = datetime.now(ZoneInfo("Europe/Istanbul")).strftime('%H:%M:%S')
    st.metric(label="📊 CANLI REEL USD/TL KURU", value=f"{kur:.4f} TL")
    st.caption(f"Güncelleme (TR): {tr_saat}")

# ----------------------------------------------------
# 3. PDF OLUŞTURMA FONKSİYONU
# ----------------------------------------------------
def pdf_olustur(paket, toplam_usd, toplam_tl):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    
    elements.append(Paragraph("PROTIME MÜHENDİSLİK - PROJE HAKEDİŞ RAPORU", styles['Title']))
    elements.append(Paragraph(f"Tarih: {datetime.now().strftime('%d.%m.%Y')}", styles['Normal']))
    
    data = [["Marka", "Ürün", "Fiyat ($)", "Fiyat (TL)"]]
    for item in paket:
        data.append([item['marka'], item['urun'], f"${item['n_usd']:.2f}", f"{(item['n_usd']*st.session_state.usd_kuru):,.2f} TL"])
    
    data.append(["", "TOPLAM", f"${toplam_usd:.2f}", f"{toplam_tl:,.2f} TL"])
    
    t = Table(data, colWidths=[100, 200, 80, 80])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey), ('GRID', (0,0), (-1,-1), 1, colors.black)]))
    elements.append(t)
    
    doc.build(elements)
    return buffer

# ----------------------------------------------------
# 4. YAN MENÜ
# ----------------------------------------------------
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    modul = st.radio("⚡ DEPARTMAN SEÇİMİ", ["☀️ GÜNEŞ ENERJİ SİSTEMLERİ (GES)", "⚡ ELEKTRİK TAAHHÜT"])
    aktif_modul = "GES" if "GES" in modul else "ELEKTRIK"
    st.write("---")
    kur_gostergesi_fragment()
    st.write("---")
    st.subheader("📌 YAPILACAK İŞLER")
    yeni_is = st.text_input("Yeni iş ekle...")
    if st.button("İşi Ekle") and yeni_is:
        conn = get_db_connection()
        conn.execute("INSERT INTO yapılacaklar (is_tanimi) VALUES (?)", (yeni_is,))
        conn.commit()
        conn.close()
        st.rerun()

# ----------------------------------------------------
# 5. ANA İÇERİK
# ----------------------------------------------------
st.title(f"PROTIME ERP // {aktif_modul} İSTASYONU")
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📦 Katalog Ürünleri")
    conn = get_db_connection()
    rows = conn.execute("SELECT id, marka, urun_adi, nakit_usd FROM urunler WHERE modul=?", (aktif_modul,)).fetchall()
    conn.close()
    
    data = [{"Seç": False, "ID": r[0], "Marka": r[1], "Ürün": r[2], "Fiyat ($)": r[3]} for r in rows]
    edited = st.data_editor(data, use_container_width=True)
    
    if st.button("📥 SEÇİLİLERİ PROJEYE EKLE"):
        for x in edited:
            if x["Seç"]:
                st.session_state.paket.append({"marka": x["Marka"], "urun": x["Ürün"], "n_usd": x["Fiyat ($)"]})
        st.rerun()

with col2:
    st.subheader("➕ Yeni Ürün Ekle")
    with st.form("yeni_urun_form", clear_on_submit=True):
        m_marka = st.text_input("Marka")
        m_tanim = st.text_input("Ürün Tanımı")
        m_fiyat = st.number_input("Nakit Fiyat ($)", min_value=0.0, step=1.0)
        if st.form_submit_button("Veritabanına Kaydet"):
            if m_marka and m_tanim and m_fiyat > 0:
                conn = get_db_connection()
                conn.execute("INSERT INTO urunler (modul, marka, urun_adi, nakit_usd) VALUES (?, ?, ?, ?)", (aktif_modul, m_marka, m_tanim, m_fiyat))
                conn.commit()
                conn.close()
                st.rerun()

# ----------------------------------------------------
# 6. HAKEDİŞ VE PDF
# ----------------------------------------------------
st.subheader("📊 Aktif Proje Finansal Hakediş")
if st.session_state.paket:
    t_n_usd = 0
    for item in st.session_state.paket:
        t_n_usd += item["n_usd"]
        st.write(f"✅ **{item['marka']}** | {item['urun']} | **${item['n_usd']:.2f}** -> **{(item['n_usd']*st.session_state.usd_kuru):,.2f} TL**")
    
    toplam_tl = t_n_usd * st.session_state.usd_kuru
    st.info(f"💰 TOPLAM: ${t_n_usd:,.2f} // {toplam_tl:,.2f} TL")
    
    # PDF İndirme Butonu
    pdf_buffer = pdf_olustur(st.session_state.paket, t_n_usd, toplam_tl)
    st.download_button(label="📄 PDF OLARAK İNDİR", data=pdf_buffer, file_name="hakedis_raporu.pdf", mime="application/pdf")
    
    if st.button("🗑️ Proje Havuzunu Sıfırla"):
        st.session_state.paket = []
        st.rerun()
