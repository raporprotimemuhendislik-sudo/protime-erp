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

if "urunler_db" not in st.session_state:
  st.session_state.urunler_db = [
      {
          "id": 1,
          "ad": "Solinved Akıllı Hibrit Inverter 10kW",
          "kategori": "İnverterler",
          "fiyat_usd": 1450,
          "stok": 15,
          "aciklama": "Yüksek verimli tam sinüs hibrit inverter çözümleri.",
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
          "aciklama": "TUV sertifikalı, güneşe dayanıklı fotovoltaik kablo.",
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
          "aciklama": "Yüksek verimli PERC teknoloji güneş paneli.",
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
  ]

# ---------------------------------------------------------
# PROFESYONEL SOLINVED & PROTIME ERP CSS STİLLERİ
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    /* Solinved Kurumsal Arka Plan Tema */
    .stApp {
        background-image: linear-gradient(rgba(10, 25, 47, 0.90), rgba(16, 42, 77, 0.90)), 
                          url("https://images.unsplash.com/photo-1509391365330-184511d7fc49?q=80&w=1920&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* Genel Tipografi ve Metin Renkleri */
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #f8f9fa !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Buton Tasarımları (Solinved Turuncu Kurumsal Vurgu) */
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

    /* Kurumsal Manşet Alanı */
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
    
    /* Ürün Kartı Tasarımı */
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
    
    /* Sidebar Kurumsal Görünüm */
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
# KURUMSAL SOLİNVED & PROTIME NAVİGASYON
# ---------------------------------------------------------
st.sidebar.title("☀️ SOLINVED / PROTIME")
nav_secenekleri = [
    "GES Katalog & Ürünler",
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

# ---------------------------------------------------------
# 1. GES KATALOG & ÜRÜNLER (Müşteri Arayüzü)
# ---------------------------------------------------------
if sayfa == "GES Katalog & Ürünler":
  st.markdown(
      """
        <div class="hero-container">
            <h1 style="font-size: 2.5rem; margin-bottom: 10px; color: #ffffff !important;">Solinved Akıllı Enerji Sistemleri</h1>
            <p style="font-size: 1.15rem; color: #cbd5e1 !important;">Yüksek verimli invertörler, endüstriyel akü grupları ve profesyonel güneş enerjisi bileşenleri.</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  col_f1, col_f2 = st.columns([2, 2])
  with col_f1:
    kategori_secim = st.selectbox(
        "Kategori Filtrele",
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
    arama_metni = st.text_input(
        "🔍 Ürün Ara", placeholder="Katalogda ürün arayın..."
    )

  st.markdown("### 📦 Ürün ve Ekipman Kataloğu")

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
                <span style="background: rgba(243, 156, 18, 0.2); border: 1px solid #f39c12; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; color: #f39c12; font-weight: bold;">{urun["kategori"]}</span>
                <h3 style="color: #ffffff; font-size: 1.1rem; margin-top: 10px; min-height: 45px;">{urun["ad"]}</h3>
                <p style="color: #cbd5e1; font-size: 0.85rem; min-height: 40px;">{urun["aciklama"]}</p>
                <p style="color: #38bdf8; font-size: 0.85rem; margin: 0 0 5px 0;">Stok Durumu: <b>{urun["stok"]} Adet</b></p>
                <h4 style="color: #f39c12; margin: 5px 0;">${urun["fiyat_usd"]:,} <span style="font-size: 0.75rem; color: #94a3b8;">(USD)</span></h4>
                <p style="color: #4ade80; font-size: 1rem; font-weight: bold; margin-bottom: 10px;">₺{fiyat_tl:,.2f} <span style="font-size: 0.7rem; color: #94a3b8;">(KDV Hariç)</span></p>
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
          st.error("Stok Tükendi")
        st.markdown(f"</div>", unsafe_allow_html=True)

  if gorunen_urun_sayisi == 0:
    st.info("Aradığınız kriterlere uygun ürün bulunamadı.")

# ---------------------------------------------------------
# 2. TEKLİF SEPETİM
# ---------------------------------------------------------
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
      "Sistemimiz piyasa dalgalanmalarına karşı döviz kurunu canlı olarak"
      " takip eder ve tüm Solinved GES bileşenlerinin maliyetlerini otomatik"
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
# 4. İLETİŞİM & TALEP FORMU (Yönetim Paneline Bildirim Gönderir)
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
        zaman_str = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        st.session_state.gelen_talepler.append({
            "ad": ad_input,
            "telefon": tel_input,
            "detay": detay_input,
            "tarih": zaman_str,
        })
        st.success(
            f"Teşekkürler {ad_input}, talebiniz Solinved yönetim paneline başarıyla"
            " iletildi!"
        )
      else:
        st.warning("Lütfen zorunlu alanları (Ad ve Telefon) doldurunuz.")

# ---------------------------------------------------------
# 5. YÖNETİM PANELİ (Giriş Korumalı & Bildirimler)
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

    # --- MÜŞTERİ TALEP BİLDİRİMLERİ ---
    st.markdown("### 🔔 Müşteri Proje ve Talep Bildirimleri")
    if not st.session_state.gelen_talepler:
      st.info("Henüz gelen yeni bir proje talep formu bulunmuyor.")
    else:
      st.warning(
          f"Toplam {len(st.session_state.gelen_talepler)} adet yeni müşteri"
          " talebi bulunmaktadır."
      )
      for idx, talep in enumerate(st.session_state.gelen_talepler):
        with st.container():
          st.markdown(
              f"""
                    <div style="background: rgba(243, 156, 18, 0.15); padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #f39c12;">
                        <b>Gönderen / Firma:</b> {talep['ad']} <br>
                        <b>Telefon:</b> {talep['telefon']} <br>
                        <b>Talep Detayı:</b> {talep['detay']} <br>
                        <span style="font-size: 0.8rem; color: #94a3b8;">Tarih: {talep['tarih']}</span>
                    </div>
                """,
              unsafe_allow_html=True,
          )
          if st.button(f"Talebi Sil / Arşivle {idx}", key=f"sil_talep_{idx}"):
            st.session_state.gelen_talepler.pop(idx)
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
              "https://images.unsplash.com/photo-1508873696983-2df5c92064c7?q=80&w=800&auto=format&fit=crop"
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
