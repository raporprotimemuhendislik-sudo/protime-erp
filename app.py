import datetime
import requests
import streamlit as st

# Sayfa Yapılandırması (Mobil ve Masaüstü Uyumlu)
st.set_page_config(
    page_title="Solinved - Akıllı Enerji Sistemleri & PROTIME ERP",
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

if "urunler_db" not in st.session_state:
  st.session_state.urunler_db = [
      {
          "id": 1,
          "ad": "Solinved Akıllı Hibrit Inverter 10kW",
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
          "ad": "Solinved Lityum İyon Akü Grubu 5kWh",
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
          "id": 3,
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
          "id": 4,
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
          "id": 5,
          "ad": "Monokristal Solar Panel 550W",
          "kategori": "Paneller",
          "fiyat_usd": 135,
          "stok": 100,
          "aciklama": (
              "Yüksek verimli PERC teknoloji güneş paneli. Düşük ışıkta"
              " maksimum güç üretimi."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 6,
          "ad": "AC/DC Koruma Kutusu (Kombinör)",
          "kategori": "Bağlantı Ekipmanları",
          "fiyat_usd": 220,
          "stok": 30,
          "aciklama": "Sigortalı ve surge arrestörlü komple koruma panosu.",
          "gorsel": (
              "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 7,
          "ad": "Solinved 5kW Kurulu GES Paketi",
          "kategori": "Kurulu GES Sistemleri",
          "fiyat_usd": 3800,
          "stok": 8,
          "aciklama": (
              "Inverter, akü ve paneller dahil komple villa/tarla paket"
              " sistemi. Anahtar teslim çözüm."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=800&auto=format&fit=crop"
          ),
      },
      {
          "id": 8,
          "ad": "Solinved 10kW Ticari Çatı Kurulu GES Paketi",
          "kategori": "Kurulu GES Sistemleri",
          "fiyat_usd": 7500,
          "stok": 5,
          "aciklama": (
              "İşletmeler ve fabrikalar için anahtar teslim yüksek verimli"
              " paket sistem."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1497435334941-8c899ee9e8e9?q=80&w=800&auto=format&fit=crop"
          ),
      },
  ]

# ---------------------------------------------------------
# PROFESYONEL SOLINVED & PROTIME ERP CSS STİLLERİ
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(10, 25, 47, 0.90), rgba(16, 42, 77, 0.90)), 
                          url("https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=1920&auto=format&fit=crop");
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
        background: linear-gradient(135deg, rgba(13, 37, 63, 0.85) 0%, rgba(26, 75, 132, 0.85) 100%);
        padding: 3rem 2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .product-box {
        background: rgba(18, 43, 75, 0.65);
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
# NAVİGASYON (AYRI AYRI KATEGORİ SEÇENEKLERİ)
# ---------------------------------------------------------
st.sidebar.title("☀️ SOLINVED / PROTIME")
nav_secenekleri = [
    "GES Katalog & Tüm Ürünler",
    "İnverterler",
    "Paneller",
    "Kurulu GES Sistemleri",
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


# Ürünleri listeleme yardımcı fonksiyonu
def urunleri_grid_listele(filtre_kategori=None):
  if st.session_state.aktif_detay_urun is not None:
    # --- ÖZEL ÜRÜN SAYFASI / DETAY EKRANI ---
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

  # Normal Grid Listeleme
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

        # Ürün Detay Sayfasına Git Butonu
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
# SAYFALARIN YÖNETİMİ
# ---------------------------------------------------------
if sayfa == "GES Katalog & Tüm Ürünler":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.5rem; margin-bottom: 10px; color: #ffffff !important;">Solinved Akıllı Enerji Sistemleri</h1>
            <p style="font-size: 1.15rem; color: #cbd5e1 !important;">Yüksek verimli invertörler, paneller ve anahtar teslim kurulu paket sistemlerimiz.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  st.markdown("### 📦 Tüm Ürün ve Ekipman Kataloğu")
  urunleri_grid_listele(None)

elif sayfa == "İnverterler":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.3rem; margin-bottom: 10px; color: #ffffff !important;">Solinved İnverter Çözümleri</h1>
            <p style="font-size: 1.1rem; color: #cbd5e1 !important;">Yüksek verimli hibrit ve şebeke bağlantılı akıllı inverter modellerimiz.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  st.markdown("### ⚡ İnverter Modelleri")
  urunleri_grid_listele("İnverterler")

elif sayfa == "Paneller":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.3rem; margin-bottom: 10px; color: #ffffff !important;">Solinved Solar Paneller</h1>
            <p style="font-size: 1.1rem; color: #cbd5e1 !important;">Yüksek PERC verimliliğine sahip monokristal güneş paneli serimiz.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  st.markdown("### ☀️ Solar Paneller")
  urunleri_grid_listele("Paneller")

elif sayfa == "Kurulu GES Sistemleri":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.3rem; margin-bottom: 10px; color: #ffffff !important;">Anahtar Teslim Kurulu GES Paketleri</h1>
            <p style="font-size: 1.1rem; color: #cbd5e1 !important;">Villa, tarla ve endüstriyel tesisler için komple kurulu enerji paketleri.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )
  st.markdown("### ⚡ Kurulu Paket Sistemlerimiz")
  urunleri_grid_listele("Kurulu GES Sistemleri")

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
      " takip eder ve tüm Solinved GES bileşenlerinin maliyetlerini otomatik"
      " günceller."
  )
  st.markdown(f"Geçerli Dolar Kuru: **{st.session_state.dolar_kur} TL**")

elif sayfa == "İletişim & Talep Formu":
  st.subheader("📍 İletişim ve Proje Başvurusu")
  col_i1, col_i2 = st.columns(2)
  with col_i1:
    st.markdown(
        """
            **Şirket Bilgileri:**
            * **Yetkili:** Efe Ceylan
            * **Faaliyet Alanı:** Güneş Enerjisi Sistemleri (GES)
            * **E-posta:** bilgi@solinvedornegi.com
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
        st.success("Talebiniz yönetim paneline iletildi!")
      else:
        st.warning("Zorunlu alanları doldurun.")

elif sayfa == "Yönetim Paneli":
  st.subheader("🔐 PROTIME ERP - Yönetim Paneli Girişi")
  if not st.session_state.yonetici_giris:
    with st.form("giris_formu"):
      kullanici_adi = st.text_input("Kullanıcı Adı")
      sifre = st.text_input("Şifre", type="password")
      if st.form_submit_button("Giriş Yap"):
        if kullanici_adi == "protime" and sifre == "protime5151":
          st.session_state.yonetici_giris = True
          st.rerun()
        else:
          st.error("Hatalı giriş!")
  else:
    st.success("✅ Yönetici oturumu açık.")
    if st.button("Oturumu Kapat"):
      st.session_state.yonetici_giris = False
      st.rerun()

    st.markdown("### 🔔 Müşteri Talepleri")
    for idx, talep in enumerate(st.session_state.gelen_talepler):
      st.write(
          f"**{talep['ad']}** - {talep['telefon']} | Detay: {talep['detay']}"
      )
      if st.button(f"Sil {idx}", key=f"t_{idx}"):
        st.session_state.gelen_talepler.pop(idx)
        st.rerun()

    st.markdown("### 🛠️ Ürün ve Stok Ekle")
    with st.expander("Yeni Ürün Ekle"):
      y_ad = st.text_input("Ürün Adı")
      y_kat = st.selectbox(
          "Kategori",
          [
              "İnverterler",
              "Paneller",
              "Kurulu GES Sistemleri",
              "Akü Grupları",
              "Sürücü Grupları",
              "Bağlantı Ekipmanları",
          ],
      )
      y_fiy = st.number_input("Fiyat ($)", value=100.0)
      y_stk = st.number_input("Stok", value=10, step=1)
      y_ack = st.text_area("Açıklama")
      y_grs = st.text_input("Görsel URL")
      if st.button("Kaydet"):
        if y_ad:
          st.session_state.urunler_db.append({
              "id": len(st.session_state.urunler_db) + 1,
              "ad": y_ad,
              "kategori": y_kat,
              "fiyat_usd": y_fiy,
              "stok": y_stk,
              "aciklama": y_ack,
              "gorsel": y_grs,
          })
          st.success("Eklendi!")
