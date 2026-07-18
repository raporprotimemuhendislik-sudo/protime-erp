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
# 1. SAYFA VE TASARIM AYARLARI (SaaS UI/UX Mimarisi)
# ----------------------------------------------------
st.set_page_config(page_title="PROTIME ERP | Enterprise", page_icon="⚡", layout="wide")

# Kurumsal CSS Renk Paleti Entegrasyonu
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
    """Çoklu cihaz erişiminde 'database is locked' hatasını önleyen güvenli havuz bağlantısı"""
    conn = sqlite3.connect("protime_erp_web.db", check_same_thread=False, timeout=30)
    return conn

def veritabanı_hazırla():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS urunler (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            modul TEXT, 
            marka TEXT, 
            urun_adi TEXT, 
            nakit_usd REAL, 
            kdv_usd REAL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notlar (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            not_icerik TEXT, 
            tarih TEXT
        )
    """)
    conn.commit()
    
    # Boş veritabanına varsayılan master verileri tek seferlik enjekte etme
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

@st.cache_data(ttl=1800)  # Cihazların performansını yormamak için kuru 30 dakikada bir çeker
def dolar_kuru_cek():
    try:
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
        return float(res.json()["rates"]["TRY"])
    except Exception:
        return 34.50 # Bağlantı koparsa güvenli default kur

veritabanı_hazırla()
USD_KURU = dolar_kuru_cek()

# Ortak oturum hafıza kartı
if "paket" not in st.session_state:
    st.session_state.paket = []

# ----------------------------------------------------
# 3. YAN NAVİGASYON PANELİ (KULLANICI ARAYÜZÜ)
# ----------------------------------------------------
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    st.caption("v3.0 Web Enterprise Workstation")
    st.write("---")
    
    modul = st.radio("⚡ DEPARTMAN SEÇİMİ", ["☀️ GÜNEŞ ENERJİ SİSTEMLERİ (GES)", "⚡ ELEKTRİK TAAHHÜT"], index=0)
    aktif_modul = "GES" if "GES" in modul else "ELEKTRIK"
    
    st.write("---")
    st.metric(label="📊 CANLI REEL USD/TL KURU", value=f"{USD_KURU:.4f} TL")
    st.info(f"Son Güncelleme: {datetime.now().strftime('%H:%M')}")
    
    st.write("---")
    st.caption("💼 Yönetici: Orhan AKBAYIR\n\n🚀 CEO: Haydar Efe CEYLAN\n\n🎨 Tasarım: Mehmet Efe TUNCER")

# ----------------------------------------------------
# 4. MASTER KATALOG KONTROLLERİ VE FİLTRELEME
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
        # PyArrow çökme hatasını önlemek için ham tuple verisini string/sayı olarak ayrıştırıyoruz
        tablo_verisi.append({
            "Seç": False, 
            "ID": int(r[0]), 
            "Marka": str(r[1]), 
            "Ürün Açıklaması / Model Özellikleri": str(r[2]),
            "Nakit ($)": f"${r[3]:,.2f}", 
            "KDV'li ($)": f"${r[4]:,.2f}",
            "Nakit (TL)": f"{r[3]*USD_KURU:,.2f} TL", 
            "KDV'li (TL)": f"{r[4]*USD_KURU:,.2f} TL",
            "raw_nakit_usd": float(r[3]),
            "raw_kdv_usd": float(r[4])
        })
        
    if tablo_verisi:
        # Hatalardan arındırılmış veri editörü
        edited_df = st.data_editor(
            tablo_verisi, 
            column_config={"Seç": st.column_config.CheckboxColumn(required=True)},
            disabled=["ID", "Marka", "Ürün Açıklaması / Model Özellikleri", "Nakit ($)", "KDV'li ($)", "Nakit (TL)", "KDV'li (TL)", "raw_nakit_usd", "raw_kdv_usd"],
            use_container_width=True, key=f"grid_{aktif_modul}"
        )
        
        c_btn1, c_btn2 = st.columns([1, 1])
        with c_btn1:
            if st.button("📥 SEÇİLİ ÖĞELERİ PROJEYE TRANSFER ET"):
                secilenler = [x for x in edited_df if x["Seç"]]
                if secilenler:
                    for s in secilenler:
                        st.session_state.paket.append({
                            "id": s["ID"], 
                            "marka": s["Marka"], 
                            "urun_adi": s["Ürün Açıklaması / Model Özellikleri"], 
                            "n_usd": s["raw_nakit_usd"], 
                            "k_usd": s["raw_kdv_usd"]
                        })
                    st.success(f"{len(secilenler)} adet ürün proje havuzuna aktarıldı!")
                    st.rerun()
        with c_btn2:
            if st.button("🗑️ Seçili Ürünleri Katalogdan Kalıcı Sil"):
                silinecekler = [x["ID"] for x in edited_df if x["Seç"]]
                if silinecekler:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.executemany("DELETE FROM urunler WHERE id=?", [(x,) for x in silinecekler])
                    conn.commit()
                    conn.close()
                    st.warning("Seçilen ürünler ana veritabanından kaldırıldı.")
                    st.rerun()
    else:
        st.info("Bu departmana ait görüntülenecek veri bulunamadı.")

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
                st.success("Yeni ürün kartı buluta işlendi, tüm yetkili cihazlar anlık görebilir!")
                st.rerun()

st.write("---")

# ----------------------------------------------------
# 5. AKTİF PROJE HAKEDİŞ VE PDF RAPORLAMA İSTASYONU
# ----------------------------------------------------
st.subheader("📊 Aktif Proje Finansal Hakediş Detayları")

if st.session_state.paket:
    pk_df = []
    t_n_usd = 0; t_k_usd = 0
    for idx, item in enumerate(st.session_state.paket):
        n_tl = item["n_usd"] * USD_KURU
        k_tl = item["k_usd"] * USD_KURU
        t_n_usd += item["n_usd"]; t_k_usd += item["k_usd"]
        
        pk_df.append({
            "Sıra": idx + 1, "Marka": item["marka"], "Ürün Modeli": item["urun_adi"],
            "Nakit ($)": f"${item['n_usd']:,.2f}", "KDV Dahil ($)": f"${item['k_usd']:,.2f}",
            "Nakit (TL)": f"{n_tl:,.2f} TL", "KDV Dahil (TL)": f"{k_tl:,.2f} TL"
        })
        
    st.table(pk_df)
    
    # Finansal Özet Bandı
    st.markdown(f"""
        <div style="background-color:#0F172A; color:white; padding:16px; border-radius:6px; text-align:center; font-weight:bold; font-size:15px;">
        📊 PROJE HAKEDİŞ ÖZETİ &nbsp;|&nbsp; Toplam Matrah: ${t_n_usd:,.2f} ({t_n_usd*USD_KURU:,.2f} TL) &nbsp;|&nbsp; Brüt Hakediş (KDV Dahil): ${t_k_usd:,.2f} ({t_k_usd*USD_KURU:,.2f} TL)
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    c1, c2, _ = st.columns([1, 1, 2])
    with c1:
        if st.button("🗑️ Proje İstasyonunu Sıfırla"):
            st.session_state.paket = []
            st.rerun()
            
    with c2:
        try:
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
            hikaye = []
            styles = getSampleStyleSheet()
            
            title_style = ParagraphStyle('PdfBaslik', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=24, textColor=colors.HexColor('#0F172A'), spaceAfter=2)
            sub_style = ParagraphStyle('PdfAltBaslik', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#475569'), spaceAfter=12)
            th_style = ParagraphStyle('TabloBaslik', fontName='Helvetica-Bold', fontSize=9, textColor=colors.white, alignment=1)
            td_style = ParagraphStyle('TabloMetin', fontName='Helvetica', fontSize=8, textColor=colors.HexColor('#334155'))
            
            hikaye.append(Paragraph("PROTIME MUHENDISLIK", title_style))
            hikaye.append(Paragraph(f"{aktif_modul} SISTEMLERI PROJE TEKLIF FORMU", ParagraphStyle('SubT', fontName='Helvetica-Bold', fontSize=12, textColor=colors.HexColor('#0EA5E9'), spaceAfter=10)))
            hikaye.append(Paragraph(f"Teklif Tarihi: {datetime.now().strftime('%d.%m.%Y')} | Sistem Kuru: {USD_KURU:.4f} TL", sub_style))
            
            data = [[Paragraph("Marka", th_style), Paragraph("Urun Model Detayi", th_style), Paragraph("Nakit ($)", th_style), Paragraph("KDV Dahil ($)", th_style), Paragraph("KDV Dahil (TL)", th_style)]]
            for item in st.session_state.paket:
                data.append([
                    Paragraph(item["marka"], td_style), Paragraph(item["urun_adi"], td_style),
                    Paragraph(f"${item['n_usd']:,.2f}", td_style), Paragraph(f"${item['k_usd']:,.2f}", td_style),
                    Paragraph(f"{item['k_usd']*USD_KURU:,.2f} TL", td_style)
                ])
            
            t = Table(data, colWidths=[70, 220, 70, 70, 90])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0F172A')),
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')])
            ]))
            hikaye.append(t)
            doc.build(hikaye)
            
            st.download_button(
                label="📄 RESMİ TEKLİF RAPORU (PDF)",
                data=pdf_buffer.getvalue(),
                file_name=f"PROTIME_{aktif_modul}_TEKLIF.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"PDF Raporlama Hatası: {str(e)}")
else:
    st.info("Şu an proje havuzunuz boş. Üstteki master katalog tablosundan ürün seçip 'Projeye Transfer Et' komutunu çalıştırın.")

st.write("---")

# ----------------------------------------------------
# 6. ŞİRKET İÇİ ORTAK MÜHENDİSLİK AJANDASI
# ----------------------------------------------------
st.subheader("📝 Şirket İçi Ortak Mühendislik Ajandası & Notları")

c_note1, c_note2 = st.columns([3, 1])

with c_note2:
    yeni_not = st.text_area("Ajandaya Canlı Mühendislik Notu Bırakın")
    if st.button("Notu Buluta Gönder"):
        if yeni_not:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO notlar (not_icerik, tarih) VALUES (?, ?)", (yeni_not, datetime.now().strftime('%d.%m.%Y %H:%M')))
            conn.commit()
            conn.close()
            st.success("Mühendislik notu başarıyla paylaşıldı!")
            st.rerun()

with c_note1:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, tarih, not_icerik FROM notlar ORDER BY id DESC")
    notlar = cursor.fetchall()
    conn.close()
    
    if notlar:
        for n in notlar:
            st.info(f"📅 **{n[1]}** (Ref No: {n[0]}) \n\n {n[2]}")
        
        if st.button("🗑️ Tüm Ajanda Kayıtlarını Temizle"):
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notlar")
            conn.commit()
            conn.close()
            st.warning("Tüm ajanda kayıtları temizlendi.")
            st.rerun()
    else:
        st.caption("Şu an dijital ajandaya işlenmiş bir kurumsal not bulunmuyor.")
