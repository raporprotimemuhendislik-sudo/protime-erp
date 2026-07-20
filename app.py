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
    conn.execute("CREATE TABLE IF NOT EXISTS urunler (id INTEGER PRIMARY KEY AUTOINCREMENT, modul TEXT, marka TEXT, urun_adi TEXT, fiyat REAL)")
    conn.execute("CREATE TABLE IF NOT EXISTS yapılacaklar_v2 (id INTEGER PRIMARY KEY AUTOINCREMENT, is_tanimi TEXT, durum INTEGER DEFAULT 0)")
    return conn

# --- BAŞLANGIÇ VERİLERİNİ YÜKLEME (GES VE ELEKTRİK KATALOĞU) ---
def katalog_urunlerini_ekle():
    conn = get_db_connection()
    
    # GES Ürünleri Kontrolü ve Yüklemesi
    sayi_ges = conn.execute("SELECT COUNT(*) FROM urunler WHERE modul='GES'").fetchone()[0]
    if sayi_ges == 0:
        ges_urunleri = [
            ("GES", "SOLINVED", "1.2 KW MPPT AKILLI İNVERTER", 132.61),
            ("GES", "SOLINVED", "3.6KW 24V MPPT AKILLI İNVERTER", 206.28),
            ("GES", "SOLINVED", "5 KW 24V MPPT AKILLI İNVERTER", 284.87),
            ("GES", "SOLINVED", "6.5 KW 48V MPPT AKILLI İNVERTER", 304.51),
            ("GES", "SOLINVED", "8.2 KW MPPT AKILLI İNVERTER", 491.15),
            ("GES", "SOLINVED", "12 KW MPPT AKILLI İNVERTER", 589.38),
            ("GES", "SOLINVED", "ASPENDOS SERİSİ ALL IN ONE BATERY MODULE (5kWh)", 933.19),
            ("GES", "SOLINVED", "ASPENDOS SERİSİ ALL IN ONE INVERTER MODULE (6KW-49V)", 392.92),
            ("GES", "NEXDOUN", "4 KW 24V MPPT AKILLI İNVERTER", 249.48),
            ("GES", "NEXDOUN", "6 KW 48V MPPT AKILLI İNVERTER", 374.22),
            ("GES", "MERSON", "12 KW 48V MPPT AKILLI İNVERTER", 727.65),
            ("GES", "VIGOR", "12V 100AH JEL AKÜ", 129.41),
            ("GES", "SOLINVED", "12V 100Ah JEL AKÜ", 126.97),
            ("GES", "SOLINVED", "12V 150Ah JEL AKÜ", 190.45),
            ("GES", "SOLINVED", "12V 200Ah JEL AKÜ", 253.94),
            ("GES", "SOLINVED", "12.8 V 100Ah LITYUM AKÜ", 270.13),
            ("GES", "SOLINVED", "25.6 V 100Ah EFES LİTYUM AKÜ", 491.15),
            ("GES", "SOLINVED", "25.6 V 200Ah EFES LİTYUM AKÜ", 834.96),
            ("GES", "SOLINVED", "51,2 V 100Ah KAPADOKYA LİTYUM AKÜ", 884.07),
            ("GES", "SOLINVED", "51.2V 100AH LİTYUMBAKÜ KABLOSU", 29.47),
            ("GES", "SOLINVED", "51.2V 314AH HİTİT SERİSİ LİTYUM AKÜ", 2259.29),
            ("GES", "SOLINVED", "102,4 V 100Ah Lithium Duvar Tipi - Serilenebilir", 1964.60),
            ("GES", "SOLINVED", "XH CONTROL BOX", 884.07),
            ("GES", "MEXSUN", "12.8V 200AH LITYUM AKU", 554.40),
            ("GES", "MEXSUN", "12.8V 300AH LİTYUM AKÜ", 658.35),
            ("GES", "SOLINVED", "CM04 4G KAMERA", 62.70),
            ("GES", "SOLINVED", "CM22 WİFİ KAMERA", 70.54),
            ("GES", "SOLINVED", "22 kW RADIUS MODEL AC CHARGER", 401.28),
            ("GES", "SOLINVED", "3 HP 1.5kW 150-440v 1x220", 142.43),
            ("GES", "SOLINVED", "3 HP 2.2KW 150-440V 1X220", 225.93),
            ("GES", "SOLINVED", "5.5HP 4KW 150-440V 1X220", 250.49),
            ("GES", "SOLINVED", "3 HP 2.2KW 150-440V 3X220", 132.61),
            ("GES", "SOLINVED", "5.5 HP 4KW 3X220", 196.46),
            ("GES", "SOLINVED", "2 HP 1.5kW 250-900V", 145.87),
            ("GES", "SOLINVED", "3 HP 2.2kW 250-900V", 152.26),
            ("GES", "SOLINVED", "5.5 HP 4kW 250-900V", 176.81),
            ("GES", "SOLINVED", "7.5 HP 5.5kW 250-900V", 235.75),
            ("GES", "SOLINVED", "10 HP 7.5kW 250-900V", 255.40),
            ("GES", "SOLINVED", "15 HP 11kW 250-900V", 333.98),
            ("GES", "SOLINVED", "20 HP 15kW 250-900V", 373.27),
            ("GES", "SOLINVED", "25 HP 18.5kW 250-900V", 471.50),
            ("GES", "SOLINVED", "30 HP 22kW 250-900V", 540.27),
            ("GES", "SOLINVED", "40 HP 30kW 250-900V", 736.73),
            ("GES", "SOLINVED", "50 HP 37kW 250-900V", 884.07),
            ("GES", "SOLINVED", "60 HP 45kW 250-900V", 1080.53),
            ("GES", "SOLINVED", "70 HP 55kW 250-900V", 1276.99),
            ("GES", "SOLINVED", "90 HP 75kW 250-900V", 1473.45),
            ("GES", "SOLINVED", "110 HP 90kW 250-900V", 1915.49),
            ("GES", "SOLINVED", "150 HP 110kw 250-900V", 1964.60),
            ("GES", "SOLINVED", "160 HP 132kW 250-900V", 3045.13),
            ("GES", "SOLINVED", "200 HP 160kW 250-900V", 3830.97),
            ("GES", "SOLINVED", "225 HP 185kW 250-900V", 4469.47),
            ("GES", "SOLINVED", "250 HP 200kW 250-900V", 4665.93),
            ("GES", "SOLINVED", "48V 750W 3.8TON 95M (2X550W)", 176.81),
            ("GES", "SOLINVED", "48V 400W 3.8TON 47M", 166.99),
            ("GES", "SOLINVED", "48V 500W 1.7TON 109M", 176.81),
            ("GES", "SOLINVED", "72V 1100W 6.5TON 86M (3X550W)", 206.28),
            ("GES", "SOLINVED", "72V 1100W 3.8TON 123M", 201.37),
            ("GES", "SOLINVED", "96V 1500W 6TON 125M", 211.19),
            ("GES", "SOLINVED", "96V 1500W 6.5TON 135M (4X550W)", 216.11),
            ("GES", "SOLINVED", "110V 1300W 3.8TON 155M", 294.69),
            ("GES", "SOLINVED", "110V 1300W 6.5TON 112M", 304.51),
            ("GES", "SOLINVED", "AC-DC 2200W 9.5TON 125M", 314.34),
            ("GES", "SOLINVED", "AC-DC 2200W 22TON 70M", 348.72),
            ("GES", "SOLINVED", "AC-DC 2200W 14TON 125M", 333.98),
            ("GES", "SOLINVED", "1HP 750W 72V MAX 20M UZAKLIK", 128.21),
            ("GES", "SOLINVED", "1.5HP 1100W 96V MAX 17M UZAKLIK", 135.14),
            ("GES", "SOLINVED", "2HP 1500W 110V MAX 13M UZAKLIK", 155.93),
            ("GES", "DEYE", "DEYE 5 KW STRING", 515.71),
            ("GES", "DEYE", "DEYE 8 KW STRING", 525.53),
            ("GES", "DEYE", "DEYE 10 KW STRING", 540.27),
            ("GES", "DEYE", "DEYE 12 KW STRING", 564.82),
            ("GES", "DEYE", "DEYE 15 KW STRING", 776.02),
            ("GES", "DEYE", "DEYE 20 KW STRING", 859.51),
            ("GES", "DEYE", "DEYE 25 KW STRING", 933.19),
            ("GES", "DEYE", "DEYE 30 KW STRING", 1129.65),
            ("GES", "DEYE", "DEYE 40 KW STRING", 1719.03),
            ("GES", "DEYE", "DEYE 50 KW STRING", 2286.90),
            ("GES", "DEYE", "DEYE 60 KW STRING", 2529.45),
            ("GES", "DEYE", "DEYE 80 KW STRING", 2910.60),
            ("GES", "DEYE", "DEYE 100 KW STRING", 3326.40),
            ("GES", "DEYE", "DEYE WİFİ STICK", 58.94),
            ("GES", "DEYE", "DEYE LAN STICK", 68.76),
            ("GES", "DEYE", "MONO PHASE SMART METER", 44.20),
            ("GES", "DEYE", "THREE PHASE SMART METER", 108.05),
            ("GES", "DEYE", "DEYE 5KW MONOFAZE LV HİBRİT", 1031.42),
            ("GES", "DEYE", "DEYE 6KW MONOFAZE LV HİBRİT", 1154.20),
            ("GES", "DEYE", "DEYE 10KW MONOFAZE LV HİBRİT", 1964.60),
            ("GES", "DEYE", "DEYE 16KW MONOFAZE LV HİBRİT", 2701.33),
            ("GES", "DEYE", "DEYE 8KW TRİFAZE LV HİBRİT", 2161.06),
            ("GES", "DEYE", "DEYE 10KW TRİFAZE LV HİBRİT", 2259.29),
            ("GES", "DEYE", "DEYE 12KW TRİFAZE LV HİBRİT", 2357.52),
            ("GES", "DEYE", "DEYE 15KW TRİFAZE LV HİBRİT", 2553.98),
            ("GES", "DEYE", "DEYE 20KW TRİFAZE LV HİBRİT", 3438.05),
            ("GES", "DEYE", "DEYE 10KW TRİFAZE HV HİBRİT", 1719.03),
            ("GES", "DEYE", "DEYE 12KW TRİFAZE HV HİBRİT", 2062.83),
            ("GES", "DEYE", "DEYE 15KW TRİFAZE HV HİBRİT", 2210.18),
            ("GES", "DEYE", "DEYE 20KW TRİFAZE HV HİBRİT", 2357.52),
            ("GES", "DEYE", "DEYE 25KW TRİFAZE HV HİBRİT", 2750.44),
            ("GES", "DEYE", "DEYE 30KW TRİFAZE HV HİBRİT", 3830.97),
            ("GES", "DEYE", "DEYE 40KW TRİFAZE HV HİBRİT", 5402.65),
            ("GES", "DEYE", "DEYE 50KW TRİFAZE HV HİBRİT", 5893.80),
            ("GES", "DEYE", "DEYE 80KW TRİFAZE HV HİBRİT", 8103.98)
        ]
        conn.executemany("INSERT INTO urunler (modul, marka, urun_adi, fiyat) VALUES (?, ?, ?, ?)", ges_urunleri)
        conn.commit()

    # Elektrik Ürünleri Kontrolü ve Yüklemesi
    sayi_elektrk = conn.execute("SELECT COUNT(*) FROM urunler WHERE modul='ELEKTRIK'").fetchone()[0]
    if sayi_elektrk == 0:
        zeybek_urunleri = [
            ("ELEKTRIK", "Cata", "Ct-5223 Pars Kare Spot Siyah Kasa", 57.82),
            ("ELEKTRIK", "Cata", "Ct-4221 3W Led Kapsül Ampul G9 220V / Günışığı", 36.70),
            ("ELEKTRIK", "Cata", "Ct-4222 4W Led Kapsül Ampul G9 220V / Günışığı", 52.79),
            ("ELEKTRIK", "Ledrox", "Hologram Fan 100 Cm 3D Video", 45600.00),
            ("ELEKTRIK", "Ledrox", "Hologram Fan 65 Cm 3D Video", 25200.00),
            ("ELEKTRIK", "Ledrox", "Hologram Fan 42 Cm 3D Video", 4500.00),
            ("ELEKTRIK", "Cata", "Ct-5224 Pars Yuvarlak Siyah Kasa", 57.82),
            ("ELEKTRIK", "Cata", "Ct-5258 6W Zebra Led Armatür (Siyah-Krom Kasa) 3 Renk", 40.22),
            ("ELEKTRIK", "Cata", "Ct-4041 Etna Güç Kaynağı 300W", 5028.00),
            ("ELEKTRIK", "Cata", "Ct-8640 Zen Sarkıt Led Armatür", 4022.40),
            ("ELEKTRIK", "Cata", "Ct-7313 Nepal Solar Set Üstü 50W", 754.20),
            ("ELEKTRIK", "Cata", "Ct-5333 30W Babil Ray Tipi Led Armatür Beyaz Kasa / Günışığı", 138.27),
            ("ELEKTRIK", "Cata", "Ct-4650 300W Amazon Solar Led Projektör", 2262.60),
            ("ELEKTRIK", "Cata", "Ct-5110 Tezgah Altı Priz Siyah Kasa / Günışığı", 263.97),
            ("ELEKTRIK", "Cata", "Ct-4694 6W Gold Wallwasher 20 Cm / Amber", 628.50),
            ("ELEKTRIK", "Cata", "Ct-3012 Kristal Led Tavan Armatür", 2891.10),
            ("ELEKTRIK", "Fujiled", "12V COB Şerit Led 4000K 288 Ledli", 94.60),
            ("ELEKTRIK", "Fujiled", "12V COB Şerit Led Günışığı 288 Ledli", 94.60),
            ("ELEKTRIK", "Viko", "Karre Anahtar Beyaz - Çerçevesiz", 78.34),
            ("ELEKTRIK", "Viko", "Karre Çocuk Korumalı Topraklı Priz Beyaz - Çerçevesiz", 128.11),
            ("ELEKTRIK", "Viko", "Karre Kapaklı Topraklı Çocuk Korumalı Priz - Çerçevesiz", 138.72),
            ("ELEKTRIK", "Viko", "Karre Dimmer 600W Beyaz - Çerçevesiz", 514.90),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 2x1.5 mm", 1250.00),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 2x2.5 mm", 1950.00),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 3x1.5 mm", 1750.00),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 3x2.5 mm", 2800.00),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 3x4 mm", 4350.00),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 4x1.5 mm", 2350.00),
            ("ELEKTRIK", "Öznur Kablo", "NYM (TTR) Kablo 4x2.5 mm", 3750.00),
            ("ELEKTRIK", "Öznur Kablo", "NYA Tek Damar Kablo 1.5 mm", 650.00),
            ("ELEKTRIK", "Öznur Kablo", "NYA Tek Damar Kablo 2.5 mm", 1050.00),
            ("ELEKTRIK", "Öznur Kablo", "NYA Tek Damar Kablo 4 mm", 1680.00),
            ("ELEKTRIK", "Öznur Kablo", "NYA Tek Damar Kablo 6 mm", 2500.00),
            ("ELEKTRIK", "Öznur Kablo", "NYY Yeraltı Kablosu 3x1.5 mm", 2100.00),
            ("ELEKTRIK", "Öznur Kablo", "NYY Yeraltı Kablosu 3x2.5 mm", 3250.00),
            ("ELEKTRIK", "Öznur Kablo", "NYY Yeraltı Kablosu 4x4 mm", 5900.00),
            ("ELEKTRIK", "Solar Kablo", "H1Z2Z2-K 1x4 mm² Solar Kablo (Kırmızı)", 14.50),
            ("ELEKTRIK", "Solar Kablo", "H1Z2Z2-K 1x4 mm² Solar Kablo (Siyah)", 14.50),
            ("ELEKTRIK", "Solar Kablo", "H1Z2Z2-K 1x6 mm² Solar Kablo (Kırmızı)", 21.00),
            ("ELEKTRIK", "Solar Kablo", "H1Z2Z2-K 1x6 mm² Solar Kablo (Siyah)", 21.00),
            ("ELEKTRIK", "Cetinkaya", "Kablo Bağı 2.5 x 100 mm (100'lü Paket)", 45.00),
            ("ELEKTRIK", "Cetinkaya", "Kablo Bağı 3.6 x 200 mm (100'lü Paket)", 95.00),
            ("ELEKTRIK", "Cetinkaya", "Kablo Bağı 4.8 x 300 mm (100'lü Paket)", 185.00),
            ("ELEKTRIK", "Cetinkaya", "Kablo Bağı 4.8 x 350 mm (100'lü Paket)", 220.00),
            ("ELEKTRIK", "Caspian", "Wago Tip 3lü Kollu Wago Klemens (50'li Paket)", 320.00),
            ("ELEKTRIK", "Caspian", "Wago Tip 5li Kollu Wago Klemens (50'li Paket)", 480.00),
            ("ELEKTRIK", "Caspian", "Skor Klemens / Buat Klemensi 2.5 mm² (100'lü)", 150.00),
            ("ELEKTRIK", "Caspian", "Sıkmalı Kablo Yüksüğü 1.5 mm² (100'lü Paket)", 65.00),
            ("ELEKTRIK", "Caspian", "Sıkmalı Kablo Yüksüğü 2.5 mm² (100'lü Paket)", 85.00),
            ("ELEKTRIK", "Caspian", "Delikli Boru Kelepçesi 1/2 inç", 12.50),
            ("ELEKTRIK", "Caspian", "Delikli Boru Kelepçesi 3/4 inç", 15.00),
            ("ELEKTRIK", "Caspian", "Plastik Spiral Boru 16 mm (50 Metre Top)", 450.00),
            ("ELEKTRIK", "Caspian", "Plastik Spiral Boru 20 mm (50 Metre Top)", 580.00),
            ("ELEKTRIK", "Caspian", "Duvaklı / Vidalı Dubel 8 mm (100'lü Paket)", 75.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Üstü Şeffaf Kapaklı Sigorta Kutusu 2'li", 85.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Üstü Şeffaf Kapaklı Sigorta Kutusu 4'lü", 120.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Üstü Şeffaf Kapaklı Sigorta Kutusu 6'lı", 165.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Üstü Şeffaf Kapaklı Sigorta Kutusu 9'lu", 230.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Üstü Şeffaf Kapaklı Sigorta Kutusu 12'li", 310.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Altı Şeffaf Kapaklı Sigorta Kutusu 12'li", 340.00),
            ("ELEKTRIK", "Kardeşler", "Sıva Altı Şeffaf Kapaklı Sigorta Kutusu 24'lü", 650.00),
            ("ELEKTRIK", "Sigma", "Boş Plastik Pano 20x30x13 cm (IP65)", 420.00),
            ("ELEKTRIK", "Sigma", "Boş Plastik Pano 30x40x17 cm (IP65)", 680.00),
            ("ELEKTRIK", "Sigma", "Boş Plastik Pano 40x50x20 cm (IP65)", 1050.00),
            ("ELEKTRIK", "Sigma", "Boş Plastik Pano 50x60x22 cm (IP65)", 1550.00),
            ("ELEKTRIK", "Caspian", "Plastik Buat Kutusu 8x8 cm (Klemensli)", 35.00),
            ("ELEKTRIK", "Caspian", "Plastik Buat Kutusu 10x10 cm (Klemensli)", 48.00),
            ("ELEKTRIK", "Caspian", "Plastik Buat Kutusu 12x12 cm (Klemensli)", 65.00)
        ]
        conn.executemany("INSERT INTO urunler (modul, marka, urun_adi, fiyat) VALUES (?, ?, ?, ?)", zeybek_urunleri)
        conn.commit()

    conn.close()

# Otomatik olarak katalog verilerini veritabanına işleyelim
katalog_urunlerini_ekle()

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
if "usd_kuru" not in st.session_state: st.session_state.usd_kuru = 46.35
if "paket_GES" not in st.session_state: st.session_state.paket_GES = []
if "paket_ELEKTRIK" not in st.session_state: st.session_state.paket_ELEKTRIK = []

# --- YAN MENÜ ---
with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    
    # GÜÇLENDİRİLMİŞ CANLI KUR ÇEKME SİSTEMİ
    try:
        res = requests.get("https://open.er-api.com/v6/latest/USD", timeout=3)
        data_json = res.json()
        if "rates" in data_json and "TRY" in data_json["rates"]:
            st.session_state.usd_kuru = float(data_json["rates"]["TRY"])
    except:
        pass

    st.metric("📊 CANLI USD/TL", f"{st.session_state.usd_kuru:.4f}")
    
    secim = st.radio("DEPARTMAN", ["☀️ GES (USD)", "⚡ ELEKTRİK (TL)"])
    aktif_modul = "GES" if "GES" in secim else "ELEKTRIK"
    aktif_paket = st.session_state.paket_GES if aktif_modul == "GES" else st.session_state.paket_ELEKTRIK
    
    st.write("---")
    st.subheader("⏳ BEKLEYEN İŞLER")
    yeni_is = st.text_input("Yeni iş ekle...", key="yeni_is")
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
    for i, item in enumerate(aktif_paket):
        st.write(f"✅ {item['marka']} | {item['urun']} | {item['fiyat']}")
    
    if aktif_modul == "GES":
        st.info(f"💰 TOPLAM: ${toplam:,.2f} | ₺{(toplam * st.session_state.usd_kuru):,.2f} TL")
    else:
        st.info(f"💰 TOPLAM: {toplam:,.2f} TL")
        
    kur_val = st.session_state.usd_kuru if aktif_modul == "GES" else None
    pdf_buf = pdf_olustur(aktif_paket, toplam, "$" if aktif_modul == "GES" else "TL", kur_val)
    st.download_button("📄 PDF İNDİR", pdf_buf, "hakedis.pdf", "application/pdf")
    if st.button("Listeyi Temizle"):
        if aktif_modul == "GES": st.session_state.paket_GES = []
        else: st.session_state.paket_ELEKTRIK = []
        st.rerun()
