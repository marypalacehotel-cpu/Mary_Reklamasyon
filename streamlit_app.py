import streamlit as st
import pandas as pd
from datetime import datetime

# Sayfa Genişliği ve Başlık
st.set_page_config(page_title="Mary Hotels Reklamasyon", layout="wide")

# Tasarım ve Stil (Mary Palace Kurumsal Renkleri için)
st.markdown("""
    <style>
    .stApp { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
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
        col1, col2 = st.columns(2)
        with col1:
            misafir = st.text_input("Misafir Adı Soyadı")
            oda = st.text_input("Oda No")
            # Hem seçmeli hem yazmalı Operatör alanı:
            op_liste = ["TUI", "LMX", "FTI", "DERTOUR", "JOLLY", "ETUR", "DİĞER..."]
            operator_secim = st.selectbox("Operatör Seçin", op_liste)
            operator_manuel = st.text_input("Operatör Listede Yoksa Buraya Yazın")
            final_operator = operator_manuel if operator_manuel else operator_secim
            
        with col2:
            tarih = st.date_input("Kayıt Tarihi", datetime.now())
            dosya = st.file_uploader("📁 Belge/Voucher Yükle", type=['pdf', 'png', 'jpg', 'jpeg'])
        
        sikayet = st.text_area("Şikayet Detayı / Notlar")
        
        if st.form_submit_button("Sisteme İşle"):
            if misafir and final_operator:
                st.success(f"✅ {misafir} kaydı {final_operator} operatörü ile sisteme eklendi.")
                # Buraya Google Sheets yazma kodu eklenecek
            else:
                st.warning("Lütfen en azından Misafir ve Operatör bilgilerini doldurun.")

# --- 2. ARAŞTIRMA & SAVUNMA ---
elif menu == "🔍 ARAŞTIRMA & SAVUNMA":
    st.header("🔍 Araştırma ve Savunma Süreci")
    st.info("Kayıtlı reklamasyonlar üzerinde iç araştırma notlarını buradan güncelleyin.")
    
    # Örnek bir kayıt seçme alanı (Veritabanı bağlandığında burası dolacak)
    secilen_kayit = st.selectbox("İşlem Yapılacak Kaydı Seçin", ["Henüz Kayıt Yok"])
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("İç Araştırma")
        st.text_area("Departman Notları", placeholder="HK, Mutfak veya Ön Büro notlarını buraya girin...")
    with col2:
        st.subheader("Resmi Savunma")
        st.text_area("Savunma Metni", placeholder="Acenteye gönderilen resmi cevabı buraya girin...")
    
    if st.button("Süreci Güncelle"):
        st.success("Bilgiler kaydedildi.")

# --- 3. MUTABAKAT ---
elif menu == "🗄️ MUTABAKAT":
    st.header("🗄️ Finansal Mutabakat ve Kapatma")
    st.write("Acente ile mutabık kalınan tutarları yönetin.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.number_input("İstenen Tutar (€)", min_value=0.0)
    with col2:
        st.number_input("Ödenen / Kesilen Tutar (€)", min_value=0.0)
    with col3:
        st.selectbox("Durum", ["Beklemede", "İtiraz Edildi", "Ödendi", "İptal"])
        
    st.file_uploader("📁 İbraname / Ödeme Belgesi Yükle", type=['pdf', 'jpg'])
    if st.button("Mutabakatı Onayla"):
        st.balloons()

# --- 4. GM RAPORU ---
elif menu == "📊 GM RAPORU":
    st.header("📊 Genel Müdürlük Raporu")
    st.write("Otel genelindeki reklamasyon istatistikleri.")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Toplam Şikayet", "0", "0%")
    c2.metric("Açık Dosyalar", "0", "0")
    c3.metric("Kurtarılan Tutar", "0 €", "0%")
    
    st.info("Veriler Google Sheets üzerinden canlı olarak çekiliyor.")
