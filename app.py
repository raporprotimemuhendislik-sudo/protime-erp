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
    .kpi-card {
        background-color: white; padding: 20px; border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); border-left: 5px solid #0EA5E9;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 2. GÜVENLİ VERİTABANI BAĞLANTI HAVUZU VE KUR MOTORU
# ----------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect("protime_erp_web.db", check_same_thread=False, timeout=30)
    return conn

# 5 Dakikada bir güncellenen otomatik kur fragment'ı
@st.fragment(run_every="5m")
def kur_gostergesi_fragment():
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
        kur = float(res.json()["rates"]["TRY"])
    except Exception:
        kur = 34.50
    st.session_state.usd_kuru = kur
    st.metric(label="📊 CANLI REEL USD/TL KURU", value=f"{kur:.4f} TL")
    st.info(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")

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
            ("GES", "SOLINVED", "3.6KW 24V MPPT AKILLI İNVERTER", 206.28, 237.23),
            ("GES", "SOLINVED", "5 KW 24V MPPT AKILLI İNVERTER", 284.87, 327.60),
            ("GES", "DEYE", "DEYE 5 KW STRING ON-GRID", 515.71, 593.06),
            ("GES", "DEYE", "DEYE 12KW TRİFAZE LV HİBRİT", 2357.52, 2711.15),
            ("GES", "SOLINVED", "12V 100Ah JEL AKÜ", 126.97, 146.01),
            ("GES", "SOLINVED", "25.6 V 100Ah EFES LİTYUM AKÜ", 491.15, 564.82),
            ("ELEKTRIK", "SIEMENS", "5SL6110-7RC 1X10A C TİPİ 6KA OTOMATİK SİGORTA", 3.20, 3.68),
            ("ELEKTRIK", "SIEMENS", "5SL6116-7RC 1X16A C TİPİ 6KA OTOMATİK SİGORTA", 3.25, 3.74),
            ("ELEKTRIK", "SIEMENS", "5SL6125-7RC 1X25A C TİPİ 6KA OTOMATİK SİGORTA", 3.40, 3.91),
            ("ELEKTRIK", "SIEMENS", "5SL6325-7RC 3X25A C TİPİ 6KA OTOMATİK SİGORTA", 12.50, 14.37),
            ("ELEKTRIK", "SIEMENS", "5SL6340-7RC 3X40A C TİPİ 6KA OTOMATİK SİGORTA", 14.10, 16.22),
            ("ELEKTRIK", "SCHNEIDER", "A9R21440 4X40A 30mA KAÇAK AKIM KORUMA RÖLESİ", 35.40, 40.71),
            ("ELEKTRIK", "SCHNEIDER", "A9R21463 4X63A 30mA KAÇAK AKIM KORUMA RÖLESİ", 42.15, 48.47),
            ("ELEKTRIK", "SIEMENS", "3RT2026-1AP00 3 KUTUP 25A 11KW KONTAKTÖR 220V", 18.50, 21.28),
            ("ELEKTRIK", "ENTES", "RG-3 12C REAKTİF GÜÇ KONTROL RÖLESİ", 85.00, 97.75)
        ]
        cursor.executemany("INSERT INTO urunler (modul, marka, urun_adi, nakit_usd, kdv_usd) VALUES (?, ?, ?, ?, ?)", varsayilan_katalog)
        conn.commit()
    conn.close()

veritabanı_hazırla()

# Kur başlangıç değeri
if "usd_kuru" not in st.session_state:
    st.session_state.usd_kuru = 34.50
if "paket" not in st.session_state:
    st.session_state.paket = []

# ----------------------------------------------------
# 3. YAN NAVİGASYON PANELİ
# ----------------------------------------------------
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    st.caption("v3.0 Web Enterprise Workstation")
    st.write("---")
    
    modul = st.radio("⚡ DEPARTMAN SEÇİMİ", ["☀️ GÜNEŞ ENERJİ SİSTEMLERİ (GES)", "⚡ ELEKTRİK TAAHHÜT"], index=0)
    aktif_modul = "GES" if "GES" in modul else "ELEKTRIK"
    
    st.write("---")
    # Kur fragment çağrısı
    kur_gostergesi_fragment()
    
    st.write("---")
    st.caption("💼 Yönetici: Orhan AKBAYIR\n\n🚀 CEO: Haydar Efe CEYLAN\n\n🎨 Tasarım: Mehmet Efe TUNCER")

# ----------------------------------------------------
# 4. KATALOG VE PROJE İŞLEMLERİ (USD_KURU yerine st.session_state.usd_kuru kullanıldı)
# ----------------------------------------------------
st.title(f"PROTIME ERP // {aktif_modul} DEPARTMANI İSTASYONU")
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📦 Şiriket Ortak Master Katalog Verileri")
    arama = st.text_input("🔍 Akıllı Model veya Üretici Ara...", "")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    if arama:
        cursor.execute("SELECT id, marka, urun_adi, nakit_usd, kdv_usd FROM urunler WHERE modul=? AND (urun_adi LIKE ? OR marka LIKE ?)", (aktif_modul, f"%{arama}%", f"%{arama}%"))
    else:
        cursor.execute("SELECT id, marka, urun_adi, nakit_usd, kdv_usd FROM urunler WHERE modul=?", (aktif_modul,))
    rows = cursor.fetchall()
    conn.close()
    
    tablo_verisi = []
    for r in rows:
        tablo_verisi.append({
            "Seç": False, "ID": int(r[0]), "Marka": str(r[1]), "Ürün Açıklaması / Model Özellikleri": str(r[2]),
            "Nakit ($)": f"${r[3]:,.2f}", "KDV'li ($)": f"${r[4]:,.2f}",
            "Nakit (TL)": f"{r[3]*st.session_state.usd_kuru:,.2f} TL", "KDV'li (TL)": f"{r[4]*st.session_state.usd_kuru:,.2f} TL",
            "raw_nakit_usd": float(r[3]), "raw_kdv_usd": float(r[4])
        })
        
    if tablo_verisi:
        edited_df = st.data_editor(tablo_verisi, column_config={"Seç": st.column_config.CheckboxColumn(required=True)},
            disabled=["ID", "Marka", "Ürün Açıklaması / Model Özellikleri", "Nakit ($)", "KDV'li ($)", "Nakit (TL)", "KDV'li (TL)", "raw_nakit_usd", "raw_kdv_usd"],
            use_container_width=True, key=f"grid_{aktif_modul}")
        
        c_btn1, c_btn2 = st.columns([1, 1])
        with c_btn1:
            if st.button("📥 SEÇİLİ ÖĞELERİ PROJEYE TRANSFER ET"):
                secilenler = [x for x in edited_df if x["Seç"]]
                for s in secilenler:
                    st.session_state.paket.append({"id": s["ID"], "marka": s["Marka"], "urun_adi": s["Ürün Açıklaması / Model Özellikleri"], "n_usd": s["raw_nakit_usd"], "k_usd": s["raw_kdv_usd"]})
                st.rerun()
        with c_btn2:
            if st.button("🗑️ Seçili Ürünleri Kalıcı Sil"):
                silinecekler = [x["ID"] for x in edited_df if x["Seç"]]
                if silinecekler:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.executemany("DELETE FROM urunler WHERE id=?", [(x,) for x in silinecekler])
                    conn.commit()
                    conn.close()
                    st.rerun()

with col_right:
    st.subheader("➕ Yeni Katalog Kartı Girişi")
    with st.form("yeni_urun_form", clear_on_submit=True):
        m_marka = st.text_input("Üretici Marka Ekle")
        m_tanim = st.text_input("Model / Teknik Özellik Tanımı")
        m_fiyat = st.number_input("Birim Matrah Fiyatı (USD)", min_value=0.0, step=1.0)
        if st.form_submit_button("Canlı Veritabanına İşle"):
            if m_marka and m_tanim and m_fiyat > 0:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO urunler (modul, marka, urun_adi, nakit_usd, kdv_usd) VALUES (?, ?, ?, ?, ?)", (aktif_modul, m_marka, m_tanim, m_fiyat, m_fiyat * 1.20))
                conn.commit()
                conn.close()
                st.rerun()

# ----------------------------------------------------
# 5. AKTİF PROJE HAKEDİŞ VE PDF RAPORLAMA (Kalan kısımlar aynı)
# ----------------------------------------------------
st.subheader("📊 Aktif Proje Finansal Hakediş Detayları")
if st.session_state.paket:
    pk_df = []
    t_n_usd = 0; t_k_usd = 0
    for idx, item in enumerate(st.session_state.paket):
        n_tl = item["n_usd"] * st.session_state.usd_kuru
        k_tl = item["k_usd"] * st.session_state.usd_kuru
        t_n_usd += item["n_usd"]; t_k_usd += item["k_usd"]
        pk_df.append({"Sıra": idx+1, "Marka": item["marka"], "Ürün Modeli": item["urun_adi"], "Nakit ($)": f"${item['n_usd']:,.2f}", "KDV Dahil ($)": f"${item['k_usd']:,.2f}", "Nakit (TL)": f"{n_tl:,.2f} TL", "KDV Dahil (TL)": f"{k_tl:,.2f} TL"})
    st.table(pk_df)
    st.markdown(f'<div style="background-color:#0F172A; color:white; padding:16px; border-radius:6px; text-align:center;">📊 Toplam Matrah: ${t_n_usd:,.2f} ({t_n_usd*st.session_state.usd_kuru:,.2f} TL)</div>', unsafe_allow_html=True)
    if st.button("🗑️ Proje İstasyonunu Sıfırla"):
        st.session_state.paket = []
        st.rerun()
