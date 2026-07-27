import datetime
import requests
import streamlit as st

# Sayfa Yapılandırması (Mobil ve Masaüstü Uyumlu)
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

if "yonetici_giris" not in st.session_state:
  st.session_state.yonetici_giris = False

if "urunler_db" not in st.session_state:
  st.session_state.urunler_db = [
      {
          "id": 1,
          "ad": "Solinved Akıllı Hibrit İnverter 10kW",
          "kategori": "İnverterler",
          "fiyat_usd": 1450,
          "stok": 15,
          "aciklama": "Yüksek verimli tam sinüs hibrit inverter çözümleri.",
          "gorsel": (
              "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?q=80&w=600&auto=format&fit=crop"
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
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1592838042647-f5c9e2a6d859?q=80&w=600&auto=format&fit=crop"
          ),
      },
      {
          "id": 3,
          "ad": "Solar DC Kablo 6mm (100m Top)",
          "kategori": "Bağlantı Ekipmanları",
          "fiyat_usd": 110,
          "stok": 50,
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
          "stok": 10,
          "aciklama": (
              "Tarımsal sulama ve endüstriyel su pompaları için özel sürücü."
          ),
          "gorsel": (
              "https://images.unsplash.com/photo-1581092160607-ee22621dd758?q=80&w=600&auto=format&fit=crop"
          ),
      },
      {
          "id": 5,
          "ad": "Monokristal Solar Panel 550W",
          "kategori": "Paneller",
          "fiyat_usd": 135,
          "stok": 100,
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
          "stok": 30,
          "aciklama": "Sigortalı ve surge arrestörlü komple koruma panosu.",
          "gorsel": (
              "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?q=80&w=600&auto=format&fit=crop"
          ),
      },
  ]

# ---------------------------------------------------------
# CSS TASARIM VE KESİN BUTON OKUNABİLİRLİK AYARLARI
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-image: linear-gradient(rgba(15, 32, 39, 0.85), rgba(44, 83, 100, 0.85)), 
                          url("https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #ffffff !important;
    }
    
    /* Tüm Butonlar İçin Kesin Çözüm: Turuncu Arka Plan ve Beyaz Yazı */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #f39c12 !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: 2px solid #ffffff !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
    }
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background-color: #e67e22 !important;
        color: #ffffff !important;
        border-color: #f39c12 !important;
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
    [data-testid="stSidebar"] {
        background-color: rgba(15, 32, 39, 0.95);
        backdrop-filter: blur(10px);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# NAVİGASYON
# ---------------------------------------------------------
st.sidebar.title("☀️ PROTIME ERP")
nav_secenekleri = [
    "GES Katalog & Ürünler",
    "Teklif Sepetim",
    "Döviz Kuru Bilgisi",
    "İletişim & Talep Formu",
    "Yönetim Paneli",
]
sayfa = st.sidebar.radio("Navigasyon", nav_secenekleri)

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
# 1. GES KATALOG & ÜRÜNLER (Müşteri Ekranı)
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
  for index, urun in enumerate(st.session_state.urunler_db):
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
                <p style="color: #a0e0ff; font-size: 0.85rem; margin: 0;">Stok: <b>{urun["stok"]} Adet</b></p>
                <h4 style="color: #f39c12; margin: 3px 0;">${urun["fiyat_usd"]:,} <span style="font-size: 0.75rem; color: #bbb;">(USD)</span></h4>
                <p style="color: #2ecc71; font-size: 0.95rem; font-weight: bold;">₺{fiyat_tl:,.2f} <span style="font-size: 0.7rem; color: #bbb;">(KDV Hariç)</span></p>
            """,
            unsafe_allow_html=True,
        )
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
          st.warning("Stok Tükendi")
        st.markdown(f"</div>", unsafe_allow_html=True)

  if gorunen_urun_sayisi == 0:
    st.info("Aradığınız kriterlere uygun ürün bulunamadı.")

# ---------------------------------------------------------
# 2. TEKLİF SEPETİM
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
# 3. DÖVİZ KURU BİLGİSİ
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
  for u in st.session_state.urunler_db:
    hesaplanan_tl = u["fiyat_usd"] * st.session_state.dolar_kur
    st.write(
        f"- **{u['ad']}** | Liste Fiyatı: ${u['fiyat_usd']} | Güncel Satış"
        f" Fiyatı: ₺{hesaplanan_tl:,.2f}"
    )

# ---------------------------------------------------------
# 4. İLETİŞİM & TALEP FORMU
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

# ---------------------------------------------------------
# 5. YÖNETİM PANELİ (Giriş Korumalı)
# ---------------------------------------------------------
elif sayfa == "Yönetim Paneli":
  st.subheader("🔐 PROTIME ERP - Yönetim Paneli Girişi")

  if not st.session_state.yonetici_giris:
    with st.form("giris_formu"):
      kullanici_adi = st.text_input("Kullanıcı Adı")
      sifre = st.text_input("Şifre", type="password")
      giris_buton = st.form_submit_button("Giriş Yap")

      if giris_buton:
        if kullanici_adi == "protime" and sifre == "protime5151":
          st.session_state.yonetici_giris = True
          st.success("Giriş başarılı! Yönetim paneli açılıyor...")
          st.rerun()
        else:
          st.error(
              "Hatalı giriş yaptınız! Kullanıcı adı veya şifre yanlış."
          )
  else:
    st.success("✅ Yönetici oturumu açık.")
    if st.button("Oturumu Kapat"):
      st.session_state.yonetici_giris = False
      st.rerun()

    st.markdown("---")
    st.markdown("### 🛠️ Ürün ve Stok Kontrol Paneli")

    with st.expander("➕ Yeni Ürün Ekle / Görsel Tanımla"):
      yeni_ad = st.text_input("Ürün Adı")
      yeni_kategori = st.selectbox(
          "Kategori",
          [
              "İnverterler",
              "Akü Grupları",
              "Bağlantı Ekipmanları",
              "Sürücü Grupları",
              "Paneller",
          ],
      )
      yeni_fiyat = st.number_input("Birim Fiyat (USD)", min_value=0.0, value=100.0)
      yeni_stok = st.number_input(
          "Stok Miktarı", min_value=0, value=10, step=1
      )
      yeni_aciklama = st.text_area("Ürün Açıklaması")
      yeni_gorsel = st.text_input(
          "Görsel URL (Ürün Resim Bağlantısı)",
          value=(
              "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=600&auto=format&fit=crop"
          ),
      )

      if st.button("Ürünü Sisteme Kaydet / Ekle"):
        if yeni_ad:
          yeni_id = (
              max([u["id"] for u in st.session_state.urunler_db]) + 1
              if st.session_state.urunler_db
              else 1
          )
          st.session_state.urunler_db.append({
              "id": yeni_id,
              "ad": yeni_ad,
              "kategori": yeni_kategori,
              "fiyat_usd": yeni_fiyat,
              "stok": yeni_stok,
              "aciklama": yeni_aciklama,
              "gorsel": yeni_gorsel,
          })
          st.success(f"'{yeni_ad}' başarıyla sisteme eklendi!")
        else:
          st.warning("Lütfen ürün adını giriniz.")

    st.markdown("### 📋 Mevcut Ürünler, Görseller ve Stok Listesi")
    for idx, urun in enumerate(st.session_state.urunler_db):
      col_m1, col_m2, col_m3, col_m4 = st.columns([3, 2, 2, 1])
      with col_m1:
        st.write(f"**{urun['ad']}** ({urun['kategori']})")
        st.image(urun["gorsel"], width=100)
      with col_m2:
        yeni_f = st.number_input(
            f"Fiyat ($) ID:{urun['id']}",
            value=float(urun["fiyat_usd"]),
            key=f"fiyat_{urun['id']}",
        )
        st.session_state.urunler_db[idx]["fiyat_usd"] = yeni_f
      with col_m3:
        yeni_s = st.number_input(
            f"Stok ID:{urun['id']}",
            value=int(urun["stok"]),
            key=f"stok_{urun['id']}",
            step=1,
        )
        st.session_state.urunler_db[idx]["stok"] = yeni_s
      with col_m4:
        if st.button("🗑️ Sil", key=f"sil_urun_{urun['id']}"):
          st.session_state.urunler_db.pop(idx)
          st.rerun()
      st.markdown("---")
