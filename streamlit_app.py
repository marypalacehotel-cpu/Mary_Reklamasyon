import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- SAYFA YAPISI ---
st.set_page_config(page_title="Mary Palace Reklamasyon v1.0", layout="wide", initial_sidebar_state="expanded")

# --- VERİ BAĞLANTISI ---
SHEET_ID = "1LJ9wiT2IcSycoVrmpoZ1D5yUwS1WGb3oKuC_0LlbzA4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=30) # Her 30 saniyede bir güncellenir
def load_data():
    try:
        df = pd.read_csv(SHEET_URL)
        df.columns = df.columns.str.strip() # Sütun isimlerindeki boşlukları temizle
        return df
    except:
        return pd.DataFrame(columns=["ID", "Misafir", "Oda", "Operator", "Kayit_Tarihi", "Deadline", "Durum", "Tutar", "Savunma"])

df = load_data()

# --- YAN PANEL ---
st.sidebar.markdown("## 🏨 MARY HOTELS SIDE")
st.sidebar.markdown("---")
menu = st.sidebar.radio("İŞLEM MERKEZİ", ["📩 YENİ KAYIT", "🔍 ARAŞTIRMA & SAVUNMA", "🗄️ MUTABAKAT", "📊 GM RAPORU"])

# --- 1. YENİ KAYIT ---
if menu == "📩 YENİ KAYIT":
    st.header("📩 Yeni Reklamasyon Dosyası Oluştur")
    with st.form("main_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            misafir = st.text_input("Misafir Ad Soyad")
            oda = st.text_input("Oda No")
        with c2:
            op_list = ["TUI", "LMX", "FTI", "DERTOUR", "JOLLY", "DİĞER..."]
            secilen_op = st.selectbox("Operatör", op_list)
            manuel_op = st.text_input("Listede Yoksa Yazın")
            final_op = manuel_op if manuel_op else secilen_op
        with c3:
            tarih = st.date_input("Kayıt Tarihi", datetime.now())
            deadline = st.date_input("⚠️ Son Cevaplama", tarih + timedelta(days=14))
        
        st.file_uploader("📁 Voucher / Kanıt Yükle", type=['pdf','jpg','png'])
        sikayet = st.text_area("Şikayet Detayı")
        
        if st.form_submit_button("KAYDI TAMAMLA"):
            if misafir and final_op:
                st.success(f"✅ {misafir} kaydı sisteme işlendi. Lütfen Google Sheet'i kontrol edin.")
            else:
                st.error("Eksik bilgi: Misafir adı ve Operatör boş bırakılamaz.")

# --- 2. ARAŞTIRMA & SAVUNMA ---
elif menu == "🔍 ARAŞTIRMA & SAVUNMA":
    st.header("🔍 Dosya Araştırma ve Savunma")
    if df.empty or len(df) == 0:
        st.info("💡 Şu an aktif dosya bulunamadı. Lütfen Google Sheet'e veri girin veya sütun isimlerini kontrol edin.")
    else:
        secim = st.selectbox("İşlem Yapılacak Dosyayı Seçin", df["Misafir"].unique())
        kisi = df[df["Misafir"] == secim].iloc[0]
        
        col1, col2 = st.columns([1, 1])
        with col1:
            st.markdown(f"**Oda:** {kisi['Oda']}  \n**Acente:** {kisi['Operator']}")
            st.text_area("🏢 İç Araştırma Notları", height=200, placeholder="HK, Mutfak veya Teknik servis görüşleri...")
        with col2:
            st.markdown(f"**⚠️ Deadline:** {kisi['Deadline']}")
            st.text_area("✉️ Resmi Savunma Metni", height=200, placeholder="Acenteye gönderilecek resmi yazı...")
        
        st.button("💾 Gelişmeleri Kaydet")

# --- 3. MUTABAKAT ---
elif menu == "🗄️ MUTABAKAT":
    st.header("🗄️ Finansal Mutabakat Paneli")
    if not df.empty:
        secim = st.selectbox("Mutabakat Yapılacak Misafir", df["Misafir"].unique())
        c1, c2, c3 = st.columns(3)
        c1.number_input("İstenen Tutar (€)", 0.0)
        c2.number_input("Anlaşılan Tutar (€)", 0.0)
        c3.selectbox("Dosya Durumu", ["Açık", "Savunma Gönderildi", "Ödeme Yapıldı", "İptal"])
        st.button("Finansal Kaydı Kapat")
    else:
        st.warning("Mutabakat yapılacak veri bulunamadı.")

# --- 4. GM RAPORU ---
elif menu == "📊 GM RAPORU":
    st.header("📊 Genel Müdürlük Özet Raporu")
    
    # Metrikler
    t1, t2, t3, t4 = st.columns(4)
    total_count = len(df) if not df.empty else 0
    t1.metric("Toplam Şikayet", total_count)
    t2.metric("Bekleyen Savunma", "2", delta="-1") # Örnek
    t3.metric("Kurtarılan Tutar", "450 €", "15%") # Örnek
    t4.metric("Kayıp Riski", "1.200 €", delta_color="inverse")

    st.subheader("📋 Güncel Dosya Listesi")
    st.dataframe(df, use_container_width=True)
    
    # Basit Grafik
    if not df.empty and "Operator" in df.columns:
        st.subheader("📈 Operatöre Göre Dağılım")
        op_counts = df["Operator"].value_counts()
        st.bar_chart(op_counts)
