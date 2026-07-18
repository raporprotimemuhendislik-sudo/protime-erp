import streamlit as st
import requests
import time
from datetime import datetime

# ----------------------------------------------------
# 1. KURU YÖNETEN FRAGMENT (SADECE BURASI GÜNCELLENİR)
# ----------------------------------------------------
@st.fragment(run_every="5m") # Streamlit bu parçayı her 5 dakikada bir otomatik tetikler
def kur_gostergesi():
    try:
        # Kur çekme işlemini burada yapıyoruz
        res = requests.get("https://api.frankfurter.app/latest?from=USD&to=TRY", timeout=5)
        kur = float(res.json()["rates"]["TRY"])
    except:
        kur = 34.50
    
    # Session state'e güncel kuru kaydet
    st.session_state.guncel_kur = kur
    
    st.metric(label="📊 CANLI REEL USD/TL KURU", value=f"{kur:.4f} TL")
    st.caption(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")

# ----------------------------------------------------
# 2. ANA UYGULAMA MANTIĞI
# ----------------------------------------------------
# Uygulama başında kur tanımlı değilse başlangıç değeri ata
if "guncel_kur" not in st.session_state:
    st.session_state.guncel_kur = 34.50

with st.sidebar:
    st.title("PROTIME MÜHENDİSLİK")
    # Kur göstergesini sidebar'a fragment olarak çağırıyoruz
    kur_gostergesi()
    st.write("---")
    # ... diğer sidebar içerikleri ...

# ----------------------------------------------------
# 3. KULLANIM
# ----------------------------------------------------
# Artık kodunuzun geri kalanında st.session_state.guncel_kur 
# değişkenini kullanarak her zaman en güncel kuru alabilirsiniz.
# Sayfa yenilenmeyecek, sadece bu küçük alan 5 dakikada bir güncellenecektir.
