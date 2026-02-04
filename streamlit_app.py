import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Sayfa Ayarları
st.set_page_config(page_title="Mary Hotels Reklamasyon", layout="wide")

# Stil Düzenleme
st.markdown("""
    <style>
    .stApp { background-color: #f4f7f6; }
    [data-testid="stMetricValue"] { font-size: 1.8rem; color: #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# Yan Menü
st.sidebar.title("🏨 MARY HOTELS SIDE")
st.sidebar.subheader("Yönetim Paneli")
menu = st.sidebar.radio("MENÜ", ["📩 YENİ KAYIT", "🔍 ARAŞTIRMA & SAVUNMA", "🗄️ MUTABAKAT", "📊 GM RAPORU"])

# --- 1. YENİ KAYIT ---
if menu == "📩 YENİ KAYIT":
    st.header("📩 Yeni Reklamasyon Kaydı")
    
    with st.form("kayit_formu"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            misafir = st.text_input("Misafir Adı Soyadı")
            oda = st.text_input("Oda No")
            op_liste = ["TUI", "LMX", "FTI", "DERTOUR", "JOLLY", "ETUR", "DİĞER..."]
            operator_secim = st.selectbox("Operatör Seçin", op_liste)
            operator_manuel = st.text_input("Operatör Listede Yoksa Yazın")
            final_operator = operator_manuel if operator_manuel else operator_secim
            
        with col2:
            kayit_tarihi = st.date_input("Kayıt Tarihi", datetime.now())
            # Otomatik 14 gün sonrası 'Son Cevaplama' olarak atanır
            varsayilan_deadline = kayit_tarihi + timedelta(days=14)
            son_cevap_tarihi = st.date_input("⚠️ Son Cevaplama Tarihi", varsayilan_deadline)
            
        with col3:
            st.write("📁 Evrak Yükleme")
            dosya = st.file_uploader("Voucher/Resim Seç", type=['pdf', 'png', 'jpg', 'jpeg'])
        
        sikayet = st.text_area("Şikayet Detayı / Notlar")
        
        if st.form_submit_button("Sisteme İşle ve Takvime Ekle"):
            if misafir and final_operator:
                st.success(f"✅ Kayıt Alındı! Son Cevaplama: {son_cevap_tarihi.strftime('%d.%m.%Y')}")
                # Google Sheets'e 'son_cevap_tarihi' sütunuyla birlikte yazılacak
            else:
                st.warning("Lütfen zorunlu alanları (Misafir, Operatör) doldurun.")

# --- 2. ARAŞTIRMA & SAVUNMA ---
elif menu == "🔍 ARAŞTIRMA & SAVUNMA":
    st.header("🔍 Araştırma ve Savunma Süreci")
    
    # Süre Takibi İçin Uyarı Paneli
    st.warning("⏰ Yaklaşan Cevaplama Süreleri: 2 Dosya Süresi Dolmak Üzere!")
    
    st.subheader("Dosya Güncelle")
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("İç Araştırma (Departman Görüşleri)")
    with col2:
        st.text_area("Resmi Savunma (Acenteye Yazılan)")
        
    st.button("Süreci Kaydet")

# Diğer menüler stabil...
elif menu == "🗄️ MUTABAKAT":
    st.header("🗄️ Finansal Mutabakat")
    st.number_input("Mutabık Kalınan Tutar (€)", min_value=0.0)
    st.button("Mutabakatı Kapat")

elif menu == "📊 GM RAPORU":
    st.header("📊 Genel Müdürlük Özeti")
    st.columns(3)[0].metric("Kayıp Riski", "1.250 €", "Yüksek")
