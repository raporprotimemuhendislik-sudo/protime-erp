import datetime
import requests
import streamlit as st

# Sayfa Yapılandırması (Mobil ve Masaüstü Uyumlu Müşteri Ekranı)
st.set_page_config(
    page_title="PROTIME ERP & Solinved - Akıllı Enerji Sistemleri",
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

# ---------------------------------------------------------
# CSS TASARIM VE GÜNEŞ PANELLİ ARKA PLAN (Solinved & PROTIME)
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Genel Sayfa Arka Planı ve Güneş Paneli Görseli */
    .stApp {
        background-image: linear-gradient(rgba(15, 32, 39, 0.85), rgba(44, 83, 100, 0.85)), 
                          url("https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Metin Renklerinin Okunabilirliği İçin Düzenlemeler */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #ffffff !important;
    }

    .hero-container {
        background: rgba(15, 32, 39, 0.75);
        padding: 3rem 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    
    .product-box {
        background: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        margin-bottom: 1.5rem;
        border-top: 4px solid #f39c12;
        backdrop-filter: blur(8px);
        border-left: 1px solid rgba(255, 255, 255, 0.1);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Sidebar Tasarımı */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 32, 39, 0.95);
        backdrop-filter: blur(10px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# MÜŞTERİ KATALOĞU (Ürünler ve Görseller)
# ---------------------------------------------------------
urunler_db = [
    {
        "id": 1,
        "ad": "Solinved Akıllı Hibrit İnverter 10kW",
        "kategori": "İnverterler",
        "fiyat_usd": 1450,
        "aciklama": "Yüksek verimli tam sinüs hibrit inverter çözümleri.",
        "gorsel": (
            "https://images.unsplash.com/photo-1592838042647-f5c9e2a6d859?q=80&w=600&auto=format&fit=crop"
        ),
    },
    {
        "id": 2,
        "ad": "Solinved Lityum İyon Akü Grubu 5kWh",
        "kategori": "Akü Grupları",
        "fiyat_usd": 1200,
        "aciklama": "Uzun ömürlü, güvenli ve modüler enerji depolama sistemleri.",
        "gorsel": (
            "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=600&auto=format&fit=crop"
        ),
    },
    {
        "id": 3,
        "ad": "Solar DC Kablo 6mm (100m Top)",
        "kategori": "Bağlantı Ekipmanları",
        "fiyat_usd": 110,
        "aciklama": "TUV sertifikalı, güneşe dayanıklı fotovoltaik kablo.",
        "gorsel": (
            "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?q=80&w=600&auto=format&fit=crop"
        ),
    },
    {
        "id": 4,
        "ad": "Solar Pompa Sürücüsü 7.5kW",
        "kategori": "Sürücü Grupları",
        "fiyat_usd": 450,
        "aciklama": "Tarımsal sulama ve endüstriyel su pompaları için özel sürücü.",
        "gorsel": (
            "https://images.unsplash.com/photo-1581092160607-ee22621dd758?q=80&w=600&auto=format&fit=crop"
        ),
    },
    {
        "id": 5,
        "ad": "Monokristal Solar Panel 550W",
        "kategori": "Paneller",
        "fiyat_usd": 135,
        "aciklama": "Yüksek verimli PERC teknoloji güneş paneli.",
        "gorsel": (
            "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=600&auto=format&fit=crop"
        ),
    },
    {
        "id": 6,
        "ad": "AC/DC Koruma Kutusu (Kombinör)",
        "kategori": "Bağlantı Ekipmanları",
        "fiyat_usd": 220,
        "aciklama": "Sigortalı ve surge arrestörlü komple koruma panosu.",
        "gorsel": (
            "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600&auto=format&fit=crop"
        ),
    },
]

# ---------------------------------------------------------
# MÜŞTERİ MENÜSÜ (Sidebar)
# ---------------------------------------------------------
st.sidebar.title("☀️ Müşteri Portal")
sayfa = st.sidebar.radio(
    "Menü",
    [
        "GES Katalog & Ürünler",
        "Teklif Sepetim",
        "Döviz Kuru Bilgisi",
        "İletişim & Talep Formu",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("💱 Güncel Kur Bilgisi")

if st.sidebar.button("🔄 Kuru Yenile"):
  st.session_state.dolar_kur = canli_kur_cek()
  st.sidebar.success("Kur güncellendi!")

st.sidebar.info(f"1 USD = ₺{st.session_state.dolar_kur}")
st.sidebar.caption(
    f"Son Kontrol: {datetime.datetime.now().strftime('%d.%m.%Y %H:%M')}"
)

# ---------------------------------------------------------
# SAYFA 1: GES KATALOG & ÜRÜNLER
# ---------------------------------------------------------
if sayfa == "GES Katalog & Ürünler":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.3rem; margin-bottom: 10px; color: #ffffff !important;">Solinved & PROTIME ERP Müşteri Kataloğu</h1>
            <p style="font-size: 1.1rem; color: #e0e0e0 !important;">Projeleriniz için yüksek verimli güneş enerjisi sistemleri ve anlık kur entegreli fiyatlar.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  col_f1, col_f2 = st.columns([2, 2])
  with col_f1:
    kategori_secim = st.selectbox(
        "Kategori Seçin",
        [
            "Tümü",
            "İnverterler",
            "Akü Grupları",
            "Bağlantı Ekipmanları",
            "Sürücü Grupları",
            "Paneller",
        ],
    )
  with col_f2:
    arama_metni = st.text_input("🔍 Ürün Ara", placeholder="Arama yapın...")

  st.markdown("### 📦 Ürün Listesi")

  col1, col2, col3 = st.columns(3)
  kolonlar = [col1, col2, col3]

  gorunen_urun_sayisi = 0
  for index, urun in enumerate(urunler_db):
    if kategori_secim != "Tümü" and urun["kategori"] != kategori_secim:
      continue
    if (
        arama_metni
        and arama_metni.lower() not in urun["ad"].lower()
        and arama_metni.lower() not in urun["aciklama"].lower()
    ):
      continue

    fiyat_tl = urun["fiyat_usd"] * st.session_state.dolar_kur
    hedef_kolon = kolonlar[gorunen_urun_sayisi % 3]
    gorunen_urun_sayisi += 1

    with hedef_kolon:
      with st.container():
        st.markdown(f'<div class="product-box">', unsafe_allow_html=True)
        st.image(urun["gorsel"], use_container_width=True)
        st.markdown(
            f"""
                <span style="background: rgba(44, 83, 100, 0.9); padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; color: #fff; font-weight: bold;">{urun["kategori"]}</span>
                <h3 style="color: #ffffff; font-size: 1.05rem; margin-top: 8px; min-height: 45px;">{urun["ad"]}</h3>
                <p style="color: #dddddd; font-size: 0.8rem; min-height: 35px;">{urun["aciklama"]}</p>
                <h4 style="color: #f39c12; margin: 3px 0;">${urun["fiyat_usd"]:,} <span style="font-size: 0.75rem; color: #bbb;">(USD)</span></h4>
                <p style="color: #2ecc71; font-size: 0.95rem; font-weight: bold;">₺{fiyat_tl:,.2f} <span style="font-size: 0.7rem; color: #bbb;">(KDV Hariç)</span></p>
            """,
            unsafe_allow_html=True,
        )
        if st.button(f"➕ Sepete Ekle", key=f"ekle_{urun['id']}"):
          st.session_state.sepet.append(
              {
                  "id": urun["id"],
                  "ad": urun["ad"],
                  "fiyat_usd":urun["fiyat_usd"],
                  "fiyat_tl": fiyat_tl,
              }
          )
          st.success(f"'{urun['ad']}' sepete eklendi!")
        st.markdown(f"</div>", unsafe_allow_html=True)

  if gorunen_urun_sayisi == 0:
    st.info("Aradığınız kriterlere uygun ürün bulunamadı.")

# ---------------------------------------------------------
# SAYFA 2: TEKLİF SEPETİM
# ---------------------------------------------------------
elif sayfa == "Teklif Sepetim":
  st.subheader("🛒 Teklif Sepetiniz")

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
        st.info(
            f"Genel Toplam: ₺{toplam_tl:,.2f} ($ {toplam_usd:,.2f} - Kur:"
            f" {st.session_state.dolar_kur})"
        )
      else:
        st.warning("Lütfen adınızı veya firma adını giriniz.")

    if st.button("Sepeti Temizle"):
      st.session_state.sepet = []
      st.rerun()

# ---------------------------------------------------------
# SAYFA 3: DÖVİZ KURU BİLGİSİ
# ---------------------------------------------------------
elif sayfa == "Döviz Kuru Bilgisi":
  st.subheader("💱 Anlık Kur Entegrasyonu ve Fiyatlandırma Politikası")
  st.write(
      "Sistemimiz, piyasa koşullarına bağlı olarak döviz kurunu otomatik"
      " olarak takip eder ve tüm GES bileşenlerinin TL karşılıklarını anlık"
      " günceller."
  )

  st.markdown("### 📊 Aktif Kur Değeri")
  st.info(f"Geçerli Dolar Kuru: **{st.session_state.dolar_kur} TL**")

  st.markdown("### 📋 Katalog Ürünlerinin Güncel TL Karşılıkları")
  for u in urunler_db:
    hesaplanan_tl = u["fiyat_usd"] * st.session_state.dolar_kur
    st.write(
        f"- **{u['ad']}** | Liste Fiyatı: ${u['fiyat_usd']} | Güncel Satış"
        f" Fiyatı: ₺{hesaplanan_tl:,.2f}"
    )

# ---------------------------------------------------------
# SAYFA 4: İLETİŞİM & TALEP FORMU
# ---------------------------------------------------------
elif sayfa == "İletişim & Talep Formu":
  st.subheader("📍 İletişim ve Proje Başvurusu")

  col_i1, col_i2 = st.columns(2)

  with col_i1:
    st.markdown(
        """
            **Şirket Bilgileri:**
            * **Yetkili:** Efe Ceylan
            * **Faaliyet Alanı:** Güneş Enerjisi Sistemleri (GES) & Elektrik Mühendisliği
            * **E-posta:** bilgi@solinvedornegi.com
            * **Telefon:** +90 (312) 000 00 00
            * **Konum:** Ankara / Türkiye
        """
    )

  with col_i2:
    st.markdown("### 💬 Hızlı Proje Talep Formu")
    ad_input = st.text_input("Ad Soyad / Firma")
    tel_input = st.text_input("Telefon Numarası")
    detay_input = st.text_area("Proje Detayları / İhtiyacınız Olan Sistemler")

    if st.button("Talebi Gönder"):
      if ad_input and tel_input:
        st.success(
            f"Teşekkürler {ad_input}, talebiniz sisteme kaydedilmiştir. En kısa"
            " sürede sizinle iletişime geçilecektir."
        )
      else:
        st.warning("Lütfen zorunlu alanları (Ad ve Telefon) doldurunuz.")
