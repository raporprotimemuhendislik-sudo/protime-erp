import datetime
import requests
import streamlit as st

# Sayfa Yapılandırması (Mobil ve Masaüstü Uyumlu)
st.set_page_config(
    page_title="PROTIME Mühendislik - Akıllı Enerji Sistemleri & ERP",
    page_icon="☀️",
    layout="wide",
)


# ---------------------------------------------------------
# CANLI DOLAR KURU ÇEKME FONKSİYONU (API)
# ---------------------------------------------------------
def canli_kur_cek():
  try:
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url, timeout=3)
    data = response.json()
    tl_kur = data["rates"]["TRY"]
    return round(tl_kur, 2)
  except:
    return 33.50


# ---------------------------------------------------------
# OTURUM DURUMU (SESSION STATE) TANIMLAMALARI
# ---------------------------------------------------------
if "sepet" not in st.session_state:
  st.session_state.sepet = []

if "dolar_kur" not in st.session_state:
  st.session_state.dolar_kur = canli_kur_cek()

if "yonetici_giris" not in st.session_state:
  st.session_state.yonetici_giris = False

if "gelen_talepler" not in st.session_state:
  st.session_state.gelen_talepler = []

if "aktif_detay_urun" not in st.session_state:
  st.session_state.aktif_detay_urun = None

if "ana_sayfa_kategori" not in st.session_state:
  st.session_state.ana_sayfa_kategori = "Tümü"

# --- ZENGİNLEŞTİRİLMİŞ ÜRÜN VE EKİPMAN KATALOĞU (GÖRSELLERİ İLE BİRLİKTE) ---
if "urunler_db" not in st.session_state:
  st.session_state.urunler_db = [
      {
          "id": 1,
          "ad": "PROTIME Akıllı Hibrit Inverter 10kW",
          "kategori": "İnverterler",
          "fiyat_usd": 1450,
          "stok": 15,
          "aciklama": (
              "Yüksek verimli tam sinüs hibrit inverter çözümleri. Şebeke"
              " bağlantılı ve akü destekli çalışabilme özelliği."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 2,
          "ad": "PROTIME Akıllı Hibrit Inverter 5kW",
          "kategori": "İnverterler",
          "fiyat_usd": 950,
          "stok": 25,
          "aciklama": (
              "Evsel ve küçük işletmeler için kompakt, yüksek verimli saf sinüs"
              " inverter."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 3,
          "ad": "PROTIME Endüstriyel Üç Fazlı Inverter 30kW",
          "kategori": "İnverterler",
          "fiyat_usd": 3200,
          "stok": 8,
          "aciklama": (
              "Fabrikalar ve büyük tarımsal sulama projeleri için endüstriyel"
              " güç."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1581092160607-ee22621dd758?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 4,
          "ad": "Monokristal Solar Panel 550W PERC",
          "kategori": "Paneller",
          "fiyat_usd": 135,
          "stok": 120,
          "aciklama": (
              "Yüksek verimli PERC teknoloji güneş paneli. Düşük ışıkta"
              " maksimum güç üretimi."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 5,
          "ad": "Monokristal Bifacial Solar Panel 580W",
          "kategori": "Paneller",
          "fiyat_usd": 155,
          "stok": 90,
          "aciklama": (
              "Çift yüzlü ışık alabilme özelliği ile standart panellere göre"
              " %20 daha fazla verim."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 6,
          "ad": "PROTIME Lityum İyon Akü Grubu 5kWh",
          "kategori": "Akü Grupları",
          "fiyat_usd": 1200,
          "stok": 20,
          "aciklama": (
              "Uzun ömürlü, güvenli ve modüler enerji depolama sistemleri."
              " Yüksek deşarj kapasitesi."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1592838042647-f5c9e2a6d859?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 7,
          "ad": "PROTIME Lityum İyon Akü Grubu 10kWh",
          "kategori": "Akü Grupları",
          "fiyat_usd": 2300,
          "stok": 12,
          "aciklama": (
              "Yüksek kapasiteli depolama ünitesi, akıllı BMS koruma"
              " sistemli."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 8,
          "ad": "PROTIME 5kW Kurulu GES Paketi (Villa / Tarla)",
          "kategori": "Kurulu GES Sistemleri",
          "fiyat_usd": 3800,
          "stok": 8,
          "aciklama": (
              "Inverter, akü ve paneller dahil komple villa/tarla paket"
              " sistemi. Anahtar teslim çözüm."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 9,
          "ad": "PROTIME 10kW Ticari Çatı Kurulu GES Paketi",
          "kategori": "Kurulu GES Sistemleri",
          "fiyat_usd": 7500,
          "stok": 5,
          "aciklama": (
              "İşletmeler ve fabrikalar için anahtar teslim yüksek verimli"
              " paket sistem."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 10,
          "ad": "Solar DC Kablo 6mm (100m Top)",
          "kategori": "Bağlantı Ekipmanları",
          "fiyat_usd": 110,
          "stok": 50,
          "aciklama": (
              "TUV sertifikalı, güneşe dayanıklı fotovoltaik kablo seti."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 11,
          "ad": "Solar Pompa Sürücüsü 7.5kW",
          "kategori": "Sürücü Grupları",
          "fiyat_usd": 450,
          "stok": 10,
          "aciklama": (
              "Tarımsal sulama ve endüstriyel su pompaları için özel sürücü."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1581092160607-ee22621dd758?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 12,
          "ad": "AC/DC Koruma Kutusu (Kombinör)",
          "kategori": "Bağlantı Ekipmanları",
          "fiyat_usd": 220,
          "stok": 30,
          "aciklama": "Sigortalı ve surge arrestörlü komple koruma panosu.",
          "gorsel": (
              "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=800&auto=format&fit=crop"
          ),
      },
  ]

# ---------------------------------------------------------
# PROTIME MÜHENDİSLİK KURUMSAL CSS VE ARKA PLAN GÖRSELİ
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    .stApp {
        background-image: linear-gradient(rgba(11, 19, 43, 0.88), rgba(18, 30, 60, 0.88)), 
                          url("https://images.unsplash.com/photo-1497440001374-f26997328c1b?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    div.stButton > button, div.stFormSubmitButton > button {
        background: linear-gradient(135deg, #f39c12 0%, #d35400 100%) !important;
        color: #ffffff !important;
        font-size: 15px !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 0.6rem 1.2rem !important;
        width: 100% !important;
        box-shadow: 0 4px 10px rgba(243, 156, 18, 0.3);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #e67e22 0%, #b94000 100%) !important;
        box-shadow: 0 6px 15px rgba(243, 156, 18, 0.5);
        transform: translateY(-2px);
    }

    .hero-container {
        background: linear-gradient(135deg, rgba(13, 37, 63, 0.88) 0%, rgba(26, 75, 132, 0.88) 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.15);
    }
    .product-box {
        background: rgba(18, 43, 75, 0.70);
        padding: 1.2rem;
        border-radius: 10px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.3);
        margin-bottom: 1.5rem;
        border-top: 4px solid #f39c12;
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    .product-box:hover {
        transform: translateY(-5px);
    }
    [data-testid="stSidebar"] {
        background-color: rgba(10, 25, 47, 0.95);
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# NAVİGASYON
# ---------------------------------------------------------
st.sidebar.title("☀️ PROTIME MÜHENDİSLİK")
nav_secenekleri = [
    "GES Katalog & Tüm Ürünler",
    "Teklif Sepetim",
    "Döviz Kuru Bilgisi",
    "İletişim & Talep Formu",
    "Yönetim Paneli",
]
sayfa = st.sidebar.radio("Navigasyon Menüsü", nav_secenekleri)

st.sidebar.markdown("---")
st.sidebar.subheader("💱 Anlık Kur Takibi")

if st.sidebar.button("🔄 Kuru Yenile"):
  st.session_state.dolar_kur = canli_kur_cek()
  st.sidebar.success("Kur güncellendi!")

st.sidebar.info(f"1 USD = ₺{st.session_state.dolar_kur}")
st.sidebar.caption(
    f"Son Kontrol: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
)


# Ürünleri listeleme ve detay fonksiyonu
def urunleri_grid_listele(filtre_kategori=None):
  if st.session_state.aktif_detay_urun is not None:
    urun = st.session_state.aktif_detay_urun
    if st.button("⬅️ Katalog Geri Dön"):
      st.session_state.aktif_detay_urun = None
      st.rerun()

    st.markdown("---")
    col_d1, col_d2 = st.columns([1, 1])

    with col_d1:
      gorsel_link = (
          urun["gorsel"]
          if urun.get("gorsel") and urun["gorsel"].startswith("http")
          else "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
      )
      st.image(gorsel_link, use_container_width=True)

    with col_d2:
      st.markdown(f"## {urun['ad']}")
      st.markdown(
          f"**Kategori:** <span style='color: #f39c12;'>{urun['kategori']}</span>",
          unsafe_allow_html=True,
      )
      st.markdown(f"**Açıklama:** {urun['aciklama']}")
      st.markdown(f"**Stok Adedi:** {urun['stok']} Adet")

      fiyat_tl = urun["fiyat_usd"] * st.session_state.dolar_kur
      st.markdown(f"### Birim Fiyat: ${urun['fiyat_usd']:,} USD")
      st.markdown(
          f"### Güncel Tutar: ₺{fiyat_tl:,.2f} <span"
          " style='font-size:0.8rem; color:#94a3b8;'>(KDV Hariç)</span>",
          unsafe_allow_html=True,
      )

      if urun["stok"] > 0:
        if st.button(f"➕ Sepete Ekle - {urun['ad']}", key=f"detay_ekle"):
          st.session_state.sepet.append(
              {
                  "id": urun["id"],
                  "ad": urun["ad"],
                  "fiyat_usd": urun["fiyat_usd"],
                  "fiyat_tl": fiyat_tl,
              }
          )
          st.success(f"'{urun['ad']}' başarıyla sepetinize eklenmiştir!")
      else:
        st.error("Üzgünüz, bu ürünün stoğu tükenmiştir.")
    return

  col1, col2, col3 = st.columns(3)
  kolonlar = [col1, col2, col3]

  gorunen_urun_sayisi = 0
  for index, urun in enumerate(st.session_state.urunler_db):
    if (
        filtre_kategori
        and filtre_kategori != "Tümü"
        and urun["kategori"] != filtre_kategori
    ):
      continue

    fiyat_tl = urun["fiyat_usd"] * st.session_state.dolar_kur
    hedef_kolon = kolonlar[gorunen_urun_sayisi % 3]
    gorunen_urun_sayisi += 1

    with hedef_kolon:
      with st.container():
        st.markdown(f'<div class="product-box">', unsafe_allow_html=True)
        gorsel_link = (
            urun["gorsel"]
            if urun.get("gorsel") and urun["gorsel"].startswith("http")
            else "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
        )
        st.image(gorsel_link, use_container_width=True)

        st.markdown(
            f"""
                <span style="background: rgba(243, 156, 18, 0.2); border: 1px solid #f39c12; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; color: #f39c12; font-weight: bold;">{urun["kategori"]}</span>
                <h3 style="color: #ffffff; font-size: 1.1rem; margin-top: 10px; min-height: 45px;">{urun["ad"]}</h3>
                <p style="color: #cbd5e1; font-size: 0.85rem; min-height: 40px;">{urun["aciklama"]}</p>
                <p style="color: #38bdf8; font-size: 0.85rem; margin: 0 0 5px 0;">Stok: <b>{urun["stok"]} Adet</b></p>
                <h4 style="color: #f39c12; margin: 5px 0;">${urun["fiyat_usd"]:,} <span style="font-size: 0.75rem; color: #94a3b8;">(USD)</span></h4>
                <p style="color: #4ade80; font-size: 1rem; font-weight: bold; margin-bottom: 10px;">₺{fiyat_tl:,.2f} <span style="font-size: 0.7rem; color: #94a3b8;">(KDV Hariç)</span></p>
            """,
            unsafe_allow_html=True,
        )

        if st.button(f"🔍 Ürünü İncele", key=f"incele_{urun['id']}"):
          st.session_state.aktif_detay_urun = urun
          st.rerun()

        if urun["stok"] > 0:
          if st.button(f"➕ Sepete Ekle", key=f"ekle_{urun['id']}"):
            st.session_state.sepet.append(
                {
                    "id": urun["id"],
                    "ad": urun["ad"],
                    "fiyat_usd": urun["fiyat_usd"],
                    "fiyat_tl": fiyat_tl,
                }
            )
            st.success(f"'{urun['ad']}' sepete eklendi!")
        else:
          st.error("Stok Tükendi")
        st.markdown(f"</div>", unsafe_allow_html=True)

  if gorunen_urun_sayisi == 0:
    st.info("Bu kategoride henüz ürün bulunmuyor.")


# ---------------------------------------------------------
# SAYFALAR
# ---------------------------------------------------------
if sayfa == "GES Katalog & Tüm Ürünler":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.5rem; margin-bottom: 10px; color: #ffffff !important;">PROTIME Mühendislik Akıllı Enerji Sistemleri</h1>
            <p style="font-size: 1.15rem; color: #cbd5e1 !important;">Yüksek verimli invertörler, paneller ve anahtar teslim kurulu paket sistemlerimiz.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  # Hızlı Kategori Seçimi Butonları
  st.markdown("### ⚡ Hızlı Kategori Seçimi")
  k_col1, k_col2, k_col3 = st.columns(3)
  with k_col1:
    if st.button("⚡ İnverterler Kategorisi"):
      st.session_state.ana_sayfa_kategori = "İnverterler"
      st.rerun()
  with k_col2:
    if st.button("☀️ Paneller Kategorisi"):
      st.session_state.ana_sayfa_kategori = "Paneller"
      st.rerun()
  with k_col3:
    if st.button("📦 Kurulu GES Sistemleri"):
      st.session_state.ana_sayfa_kategori = "Kurulu GES Sistemleri"
      st.rerun()

  if st.session_state.ana_sayfa_kategori != "Tümü":
    if st.button(
        f"🔙 Tüm Kataloğa Geri Dön (Aktif Filtre:"
        f" {st.session_state.ana_sayfa_kategori})"
    ):
      st.session_state.ana_sayfa_kategori = "Tümü"
      st.rerun()

  st.markdown("---")
  st.markdown(
      f"### 📦 Ürün ve Ekipman Kataloğu ({st.session_state.ana_sayfa_kategori})"
  )
  urunleri_grid_listele(st.session_state.ana_sayfa_kategori)

elif sayfa == "Teklif Sepetim":
  st.subheader("🛒 Teklif Sepetiniz ve Proje Özeti")
  if not st.session_state.sepet:
    st.info(
        "Sepetinizde henüz ürün bulunmuyor. Katalogdan ürün ekleyebilirsiniz."
    )
  else:
    toplam_usd = 0
    toplam_tl = 0
    for i, item in enumerate(st.session_state.sepet):
      col_s1, col_s2, col_s3 = st.columns([3, 2, 1])
      with col_s1:
        st.write(f"**{item['ad']}**")
      with col_s2:
        guncel_item_tl = item["fiyat_usd"] * st.session_state.dolar_kur
        st.write(f"${item['fiyat_usd']:,} ($) | ₺{guncel_item_tl:,.2f} (₺)")
      with col_s3:
        if st.button("🗑️ Sil", key=f"sil_{i}"):
          st.session_state.sepet.pop(i)
          st.rerun()
      toplam_usd += item["fiyat_usd"]
      toplam_tl += item["fiyat_usd"] * st.session_state.dolar_kur

    st.markdown("---")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
      st.metric(label="Toplam Tutar (USD)", value=f"${toplam_usd:,.2f}")
    with col_t2:
      st.metric(label="Toplam Tutar (TL)", value=f"₺{toplam_tl:,.2f}")

    st.markdown("### 📄 Proforma / Teklif Oluştur")
    musteri_adi = st.text_input("Adınız Soyadınız / Firma Adı")
    yetkili_kisi = st.text_input("Yetkili Kişi", value="EFE CEYLAN")

    if st.button("Teklif Talebi Oluştur"):
      if musteri_adi:
        st.success(
            f"Sayın {yetkili_kisi} ({musteri_adi}), teklif talebiniz başarıyla"
            " alınmıştır!"
        )
      else:
        st.warning("Lütfen adınızı veya firma adını giriniz.")

    if st.button("Sepeti Temizle"):
      st.session_state.sepet = []
      st.rerun()

elif sayfa == "Döviz Kuru Bilgisi":
  st.subheader("💱 Anlık Kur Entegrasyonu ve Fiyatlandırma Politikası")
  st.write(
      "Sistemimiz piyasa dalgalanmalarına karşı döviz kurunu canlı olarak"
      " takip eder ve tüm PROTIME Mühendislik GES bileşenlerinin"
      " maliyetlerini otomatik günceller."
  )
  st.markdown(f"Geçerli Dolar Kuru: **{st.session_state.dolar_kur} TL**")

elif sayfa == "İletişim & Talep Formu":
  st.subheader("📍 İletişim ve Proje Başvurusu")
  col_i1, col_i2 = st.columns(2)
  with col_i1:
    st.markdown(
        """
            **Şirket Bilgileri:**
            * **Şirket:** PROTIME Mühendislik
            * **Yetkili:** Efe Ceylan
            * **Faaliyet Alanı:** Güneş Enerjisi Sistemleri (GES) & Elektrik Mühendisliği
            * **E-posta:** bilgi@protimemuhendislik.com
            * **Telefon:** +90 (312) 000 00 00
            * **Konum:** Ankara / Türkiye
        """
    )
  with col_i2:
    st.markdown("### 💬 Hızlı Proje Talep Formu")
    ad_input = st.text_input("Ad Soyad / Firma")
    tel_input = st.text_input("Telefon Numarası")
    detay_input = st.text_area("Proje Detayları")
    if st.button("Talebi Gönder"):
      if ad_input and tel_input:
        st.session_state.gelen_talepler.append({
            "ad": ad_input,
            "telefon": tel_input,
            "detay": detay_input,
            "tarih": datetime.datetime.now().strftime("%d.%m.%Y %H:%M"),
        })
        st.success("Talebiniz PROTIME yönetim paneline iletildi!")
      else:
        st.warning("Zorunlu alanları doldurun.")

elif sayfa == "Yönetim Paneli":
  st.subheader("🔐 PROTIME ERP - Gelişmiş Tam Erişim Yönetim Paneli")

  if not st.session_state.yonetici_giris:
    with st.form("giris_formu"):
      kullanici_adi = st.text_input("Kullanıcı Adı")
      sifre = st.text_input("Şifre", type="password")
      if st.form_submit_button("Giriş Yap"):
        if kullanici_adi == "protime" and sifre == "protime5151":
          st.session_state.yonetici_giris = True
          st.rerun()
        else:
          st.error("Hatalı giriş! Kullanıcı adı veya şifre yanlış.")
  else:
    st.success(
        "✅ Yönetici oturumu aktif. Tüm sistem kontrolü elinizdedir (Efe"
        " Ceylan)."
    )
    if st.button("Oturumu Kapat"):
      st.session_state.yonetici_giris = False
      st.rerun()

    st.markdown("---")

    # --- ÖZET İSTATİSTİKLER ---
    col_stat1, col_stat2, col_stat3 = st.columns(3)
    with col_stat1:
      st.metric(
          label="Toplam Ürün Çeşidi",
          value=len(st.session_state.urunler_db),
      )
    with col_stat2:
      st.metric(
          label="Bekleyen Müşteri Talebi",
          value=len(st.session_state.gelen_talepler),
      )
    with col_stat3:
      st.metric(
          label="Aktif Dolar Kuru (TL)", value=st.session_state.dolar_kur
      )

    st.markdown("---")

    # --- MÜŞTERİ TALEPLERİ YÖNETİMİ ---
    st.markdown("### 🔔 Müşteri Proje ve Talep Bildirimleri")
    if not st.session_state.gelen_talepler:
      st.info("Şu anda bekleyen yeni bir müşteri talep formu bulunmuyor.")
    else:
      st.warning(
          f"Toplam {len(st.session_state.gelen_talepler)} adet yanıtlanmayı"
          " bekleyen talep var."
      )
      for idx, talep in enumerate(st.session_state.gelen_talepler):
        with st.container():
          st.markdown(
              f"""
                    <div style="background: rgba(243, 156, 18, 0.15); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #f39c12;">
                        <b>Müşteri / Firma:</b> {talep['ad']} <br>
                        <b>İletişim Tel:</b> {talep['telefon']} <br>
                        <b>Talep İçeriği:</b> {talep['detay']} <br>
                        <span style="font-size: 0.8rem; color: #94a3b8;">Kayıt Tarihi: {talep['tarih']}</span>
                    </div>
                """,
              unsafe_allow_html=True,
          )
          if st.button(f"Talebi Arşivle / Sil #{idx}", key=f"sil_talep_{idx}"):
            st.session_state.gelen_talepler.pop(idx)
            st.rerun()

    st.markdown("---")

    # --- YENİ ÜRÜN EKLEME ---
    st.markdown("### ➕ Sisteme Yeni Ürün / Paket Ekle")
    with st.expander("Ürün Ekleme Formunu Aç / Kapat"):
      y_ad = st.text_input("Ürün veya Paket Adı")
      y_kat = st.selectbox(
          "Ürün Kategorisi",
          [
              "İnverterler",
              "Paneller",
              "Kurulu GES Sistemleri",
              "Akü Grupları",
              "Sürücü Grupları",
              "Bağlantı Ekipmanları",
          ],
      )
      y_fiy = st.number_input("Birim Fiyat (USD)", min_value=0.0, value=250.0)
      y_stk = st.number_input(
          "Stok Miktarı", min_value=0, value=15, step=1
      )
      y_ack = st.text_area("Ürün Açıklaması / Teknik Detaylar")
      y_grs = st.text_input(
          "Görsel URL Bağlantısı",
          value=(
              "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
          ),
      )

      if st.button("Ürünü Kataloğa Ekle"):
        if y_ad:
          yeni_id = (
              max([u["id"] for u in st.session_state.urunler_db]) + 1
              if st.session_state.urunler_db
              else 1
          )
          st.session_state.urunler_db.append({
              "id": yeni_id,
              "ad": y_ad,
              "kategori": y_kat,
              "fiyat_usd": y_fiy,
              "stok": y_stk,
              "aciklama": y_ack,
              "gorsel": (
                  y_grs
                  if y_grs.startswith("http")
                  else "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
              ),
          })
          st.success(f"'{y_ad}' başarıyla sisteme eklendi!")
          st.rerun()
        else:
          st.warning("Lütfen ürün adını boş bırakmayın.")

    st.markdown("---")

    # --- MEVCUT ÜRÜNLERİ DÜZENLEME VE TAM YÖNETİMİ ---
    st.markdown(
        "### 🛠️ Mevcut Ürünlerin Tam Düzenlenmesi (Fiyat, Stok, Kategori ve"
        " Görsel)"
    )
    st.write(
        "Aşağıdaki alanlardan dilediğiniz ürünün adını, kategorisini, fiyatını,"
        " stok miktarını, açıklamasını ve görsel linkini anlık olarak"
        " güncelleyebilir veya ürünü tamamen silebilirsiniz."
    )

    for idx, urun in enumerate(st.session_state.urunler_db):
      with st.container():
        st.markdown(
            f"""
                <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 8px; margin-bottom: 15px; border: 1px solid rgba(255, 255, 255, 0.1);">
                    <b>Ürün ID:</b> {urun['id']}
                </div>
            """,
            unsafe_allow_html=True,
        )

        col_edit1, col_edit2 = st.columns([1, 2])

        with col_edit1:
          gorsel_guncel = (
              urun["gorsel"]
              if urun.get("gorsel") and urun["gorsel"].startswith("http")
              else "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
          )
          st.image(gorsel_guncel, width=150)
          yeni_gorsel_input = st.text_input(
              f"Görsel URL ID:{urun['id']}",
              value=urun["gorsel"],
              key=f"gorsel_input_{urun['id']}",
          )
          st.session_state.urunler_db[idx]["gorsel"] = yeni_gorsel_input

        with col_edit2:
          yeni_ad_input = st.text_input(
              f"Ürün Adı ID:{urun['id']}",
              value=urun["ad"],
              key=f"ad_input_{urun['id']}",
          )
          st.session_state.urunler_db[idx]["ad"] = yeni_ad_input

          kategoriler_listesi = [
              "İnverterler",
              "Paneller",
              "Kurulu GES Sistemleri",
              "Akü Grupları",
              "Sürücü Grupları",
              "Bağlantı Ekipmanları",
          ]
          kat_index = (
              kategoriler_listesi.index(urun["kategori"])
              if urun["kategori"] in kategoriler_listesi
              else 0
          )
          yeni_kat_input = st.selectbox(
              f"Kategori ID:{urun['id']}",
              kategoriler_listesi,
              index=kat_index,
              key=f"kat_input_{urun['id']}",
          )
          st.session_state.urunler_db[idx]["kategori"] = yeni_kat_input

          col_f_s1, col_f_s2 = st.columns(2)
          with col_f_s1:
            yeni_fiyat_input = st.number_input(
                f"Fiyat ($) ID:{urun['id']}",
                value=float(urun["fiyat_usd"]),
                key=f"fiyat_input_{urun['id']}",
            )
            st.session_state.urunler_db[idx]["fiyat_usd"] = yeni_fiyat_input
          with col_f_s2:
            yeni_stok_input = st.number_input(
                f"Stok Adedi ID:{urun['id']}",
                value=int(urun["stok"]),
                step=1,
                key=f"stok_input_{urun['id']}",
            )
            st.session_state.urunler_db[idx]["stok"] = yeni_stok_input

          yeni_ack_input = st.text_area(
              f"Açıklama ID:{urun['id']}",
              value=urun["aciklama"],
              key=f"ack_input_{urun['id']}",
          )
          st.session_state.urunler_db[idx]["aciklama"] = yeni_ack_input

          if st.button(
              f"🗑️ Bu Ürünü Sistemden Sil ID:{urun['id']}",
              key=f"sil_urun_tam_{urun['id']}",
          ):
            st.session_state.urunler_db.pop(idx)
            st.success("Ürün silindi!")
            st.rerun()

        st.markdown("---")
