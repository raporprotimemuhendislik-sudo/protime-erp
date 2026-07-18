import streamlit as st
import requests
from datetime import datetime
import sqlite3
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ----------------------------------------------------
# 1. SAYFA VE TASARIM AYARLARI
# ----------------------------------------------------
st.set_page_config(page_title="PROTIME ERP | Enterprise", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button { background-color: #0F172A; color: white; border-radius: 6px; width: 100%; }
    .stMetric { background-color: #ffffff; padding: 10px; border-radius: 10px; border: 1px solid #e0e0e0; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. VERİTABANI VE KUR MOTORU (FRAGMENT)
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
    saat = datetime.now().strftime('%H:%M:%S')
    
    st.metric(label="📊 CANLI REEL USD/TL KURU", value=f"{kur:.4f} TL")
    st.caption(f"Güncelleme: {saat} | Sistem Saati: {saat}")

def veritabanı_hazırla():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, nakit_usd REAL, kdv_usd REAL)")
    c.execute("CREATE TABLE IF NOT EXISTS notlar (id INTEGER PRIMARY KEY AUTOINCREMENT, not_icerik TEXT, tarih TEXT)")
    conn.commit()
    conn.close()

veritabanı_hazırla()

if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 34.50
if "paket" not in st.session_state: st.session_state.paket = []

# ----------------------------------------------------
# 3. YAN NAVİGASYON VE ARAYÜZ
# ----------------------------------------------------
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    modul = st.radio("⚡ DEPARTMAN SEÇİMİ", ["☀️ GÜNEŞ ENERJİ SİSTEMLERİ (GES)", "⚡ ELEKTRİK TAAHHÜT"])
    aktif_modul = "GES" if "GES" in modul else "ELEKTRIK"
    st.write("---")
    kur_gostergesi_fragment()

st.title(f"PROTIME ERP // {aktif_modul} İSTASYONU")

# ----------------------------------------------------
# 4. KATALOG VE İŞLEMLER
# ----------------------------------------------------
col1, col2 = st.columns([2, 1])

with col1:
    conn = get_db_connection()
    rows = conn.execute("SELECT id, marka, urun_adi, nakit_usd, kdv_usd FROM urunler WHERE modul=?", (aktif_modul,)).fetchall()
    conn.close()
    
    data = [{"Seç": False, "ID": r[0], "Marka": r[1], "Ürün": r[2], "Nakit ($)": r[3], "KDV'li ($)": r[4]} for r in rows]
    edited = st.data_editor(data, use_container_width=True)
    
    if st.button("📥 SEÇİLİLERİ PROJEYE EKLE"):
        for x in edited:
            if x["Seç"]:
                st.session_state.paket.append({"marka": x["Marka"], "urun": x["Ürün"], "n_usd": x["Nakit ($)"], "k_usd": x["KDV'li ($)"]})
        st.rerun()

# ----------------------------------------------------
# 5. FİNANSAL HAKEDİŞ
# ----------------------------------------------------
st.subheader("📊 Aktif Proje Finansal Hakediş")
if st.session_state.paket:
    t_n, t_k = 0, 0
    for item in st.session_state.paket:
        t_n += item["n_usd"]
        t_k += item["k_usd"]
        st.write(f"✅ **{item['marka']}** - {item['urun']} | **{item['n_usd']*st.session_state.usd_kuru:,.2f} TL**")
    
    st.info(f"💰 Toplam Matrah: ${t_n:,.2f} // Güncel Kur ile: {(t_n*st.session_state.usd_kuru):,.2f} TL")
    
    if st.button("🗑️ Proje Havuzunu Sıfırla"):
        st.session_state.paket = []
        st.rerun()
else:
    st.write("Proje havuzunda henüz ürün bulunmuyor.")

# ----------------------------------------------------
# 6. AJANDA
# ----------------------------------------------------
st.subheader("📝 Mühendislik Ajandası")
yeni_not = st.text_input("Not ekle:")
if st.button("Notu Kaydet"):
    conn = get_db_connection()
    conn.execute("INSERT INTO notlar (not_icerik, tarih) VALUES (?, ?)", (yeni_not, datetime.now().strftime('%d.%m.%Y')))
    conn.commit()
    conn.close()
    st.rerun()
