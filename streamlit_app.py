import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="Mary Hotels Reklamasyon", layout="wide")

# Google Sheets Linki (Bilgi Amaçlı)
SHEET_ID = "1LJ9wiT2IcSycoVrmpoZ1D5yUwS1WGb3oKuC_0LlbzA4"
# Not: Tam entegrasyon için Google Service Account gerekir. 
# Şimdilik sistemi çalışır hale getirelim.

st.sidebar.title("🏨 MARY HOTELS SIDE")
menu = st.sidebar.radio("MENÜ", ["📩 YENİ KAYIT", "🔍 ARAŞTIRMA & SAVUNMA", "🗄️ MUTABAKAT", "📊 GM RAPORU"])

# --- 1. YENİ KAYIT BÖLÜMÜ ---
if menu == "📩 YENİ KAYIT":
    st.header("📩 Yeni Reklamasyon Kaydı")
    
    with st.form("kayit_formu", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            misafir = st.text_input("Misafir Adı Soyadı")
            oda = st.text_input("Oda No")
            operator = st.selectbox("Operatör", ["TUI", "LMX", "FTI", "Diger"])
        with col2:
            tarih = st.date_input("Kayıt Tarihi", datetime.now())
            dosya = st.file_uploader("📁 Belge/Voucher Yükle (PDF, PNG, JPG)", type=['pdf', 'png', 'jpg', 'jpeg'])
        
        sikayet = st.text_area("Şikayet Detayı")
        
        if st.form_submit_button("Kaydı Tamamla"):
            if misafir and sikayet:
                st.success(f"✅ {misafir} için kayıt oluşturuldu! Dosya: {dosya.name if dosya else 'Yok'}")
                # Veriyi DataFrame'e ekleme ve buluta basma işlemleri burada yapılacak
            else:
                st.error("Lütfen zorunlu alanları doldurun!")

# --- 2. MUTABAKAT BÖLÜMÜ ---
elif menu == "🗄️ MUTABAKAT":
    st.header("🗄️ Finansal Mutabakat")
    st.info("Bu bölümde acente ile sonuçlanan ödeme detaylarını yönetebilirsiniz.")
    
    # Örnek Tablo Gösterimi
    st.write("### Bekleyen Mutabakatlar")
    df_sample = pd.DataFrame({
        "Misafir": ["Deneme Misafir"],
        "Durum": ["Savunma Gönderildi"],
        "Tutar": [0.0]
    })
    st.table(df_sample)

# --- DİĞER MENÜLER ---
else:
    st.info(f"{menu} Modülü üzerinde çalışma devam ediyor...")
