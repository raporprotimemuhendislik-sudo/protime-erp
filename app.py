import streamlit as st
import requests
from datetime import datetime
import sqlite3
import io

# PDF Raporlama Bileşenleri
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ----------------------------------------------------
# 1. SAYFA VE TASARIM AYARLARI
# ----------------------------------------------------
st.set_page_config(page_title="PROTIME ERP | Enterprise", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F8FAFC; }
    .stButton>button {
        background-color: #0F172A; color: white; border-radius: 6px;
        border: none; padding: 0.5rem 1rem; font-weight: 600; width: 100%;
    }
    .stButton>button:hover { background-color: #1E293B; color: #0EA5E9; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: bold; color: #0F172A; }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. VERİTABANI VE KUR MOTORU
# ----------------------------------------------------
def get_db_connection():
    return sqlite3.connect("protime_erp_web.db", check_same_thread=False, timeout=30)

def veritabanı_hazırla():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, nakit_usd REAL, kdv_usd REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS notlar (id INTEGER PRIMARY KEY AUTOINCREMENT, not_icerik TEXT, tarih TEXT)")
    conn.commit()
    
    cursor.execute("SELECT COUNT(*) FROM urunler")
    if cursor.fetchone()[0] == 0:
        varsayilan_katalog = [
            ("GES", "SOLINVED", "1.2 KW MPPT AKILLI İNVERTER", 132.61, 152.50),
            ("GES", "DEYE", "DEYE 5 KW STRING ON-GRID", 515.71, 593.06),
            ("ELEKTRIK", "SIEMENS", "5SL6110-7RC 1X10A C TİPİ 6KA OTOMATİK SİGORTA", 3.20, 3.68),
            ("ELEKTRIK", "SCHNEIDER", "A9R21440 4X40A 30mA KAÇAK AKIM KORUMA RÖLESİ", 35.40, 40.71)
        ]
        cursor.executemany("INSERT INTO urunler (modul, marka, urun_adi, nakit_usd, kdv_usd) VALUES (?, ?, ?, ?, ?)", varsayilan_katalog)
        conn.commit()
    conn.close()

# 5 Dakikada bir güncellenen otomatik kur fragment'ı
@st.fragment(run_every="5m")
def kur_gostergesi_fragment():
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
        kur = float(res.json()["rates"]["TRY"])
    except:
        kur = 34.50
    st.session_state.usd_kuru = kur
    st.metric(label="📊 CANLI REEL USD/TL KURU", value=f"{kur:.4f} TL")
    st.caption(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")

veritabanı_hazırla()
if "usd_kuru" not in st.session_state:
    st.session_state.usd_kuru = 34.50
if "paket" not in st.session_state:
    st.session_state.paket = []

# ----------------------------------------------------
# 3. YAN NAVİGASYON PANELİ
# ----------------------------------------------------
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    st.write("---")
    modul = st.radio("⚡ DEPARTMAN SEÇİMİ", ["☀️ GÜNEŞ ENERJİ SİSTEMLERİ (GES)", "⚡ ELEKTRİK TAAHHÜT"], index=0)
    aktif_modul = "GES" if "GES" in modul else "ELEKTRIK"
    st.write("---")
    kur_gostergesi_fragment() # Kur burada otomatik güncellenir

# ----------------------------------------------------
# 4. KATALOG VE İŞLEMLER
# ----------------------------------------------------
st.title(f"PROTIME ERP // {aktif_modul} İSTASYONU")
col_left, col_right = st.columns([2, 1])

with col_left:
    arama = st.text_input("🔍 Ara...", "")
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT id, marka, urun_adi, nakit_usd, kdv_usd FROM urunler WHERE modul=?" + (" AND (urun_adi LIKE ? OR marka LIKE ?)" if arama else "")
    params = (aktif_modul,) + ((f"%{arama}%", f"%{arama}%") if arama else ())
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    tablo_verisi = [{
        "Seç": False, "ID": int(r[0]), "Marka": str(r[1]), "Ürün": str(r[2]),
        "Nakit ($)": f"${r[3]:,.2f}", "Nakit (TL)": f"{r[3]*st.session_state.usd_kuru:,.2f} TL",
        "raw_n": float(r[3]), "raw_k": float(r[4])
    } for r in rows]
    
    edited_df = st.data_editor(tablo_verisi, use_container_width=True, disabled=["ID", "Marka", "Ürün", "Nakit ($)", "Nakit (TL)"])

    if st.button("📥 SEÇİLİLERİ TRANSFER ET"):
        for s in edited_df:
            if s["Seç"]:
                st.session_state.paket.append({"marka": s["Marka"], "urun_adi": s["Ürün"], "n_usd": s["raw_n"], "k_usd": s["raw_k"]})
        st.rerun()

# ----------------------------------------------------
# 5. FİNANSAL HAKEDİŞ
# ----------------------------------------------------
st.subheader("📊 Aktif Proje Finansal Hakediş")
if st.session_state.paket:
    for item in st.session_state.paket:
        st.write(f"**{item['marka']}** - {item['urun_adi']} | {item['n_usd']*st.session_state.usd_kuru:,.2f} TL")
    if st.button("🗑️ Sıfırla"):
        st.session_state.paket = []
        st.rerun()
