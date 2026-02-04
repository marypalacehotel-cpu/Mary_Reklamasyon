import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="Mary Palace Reklamasyon v1.2", layout="wide")

# --- GOOGLE SHEETS BAĞLANTISI ---
# Tablonuzun ID'si ve CSV formatında çekim linki
SHEET_ID = "1LJ9wiT2IcSycoVrmpoZ1D5yUwS1WGb3oKuC_0LlbzA4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=10) # 10 saniyede bir veriyi tazeler
def verileri_yukle():
    try:
        data = pd.read_csv(SHEET_URL)
        # Sütun isimlerindeki boşlukları temizle (Hata önleyici)
        data.columns = data.columns.str.strip()
        # 'Misafir' sütunu boş olan satırları dikkate alma
        data = data.dropna(subset=['Misafir'])
        return data
    except Exception as e:
        # Hata durumunda boş bir şablon döndür
        return pd.DataFrame(columns=["ID", "Misafir", "Oda", "Operator", "Kayit_Tarihi", "Deadline", "Durum", "Tutar", "Savunma"])

df = verileri_yukle()

# --- YAN PANEL ---
st.sidebar.markdown("## 🏨 MARY HOTELS SIDE")
st.sidebar.markdown("---")
menu = st.sidebar.radio("İŞLEM MERKEZİ", ["📩 YENİ KAYIT", "🔍 ARAŞTIRMA & SAVUNMA", "🗄️ MUTABAKAT", "📊 GM RAPORU"])

# --- 1. YENİ KAYIT ---
if menu == "📩 YENİ KAYIT":
    st.header("📩 Yeni Reklamasyon Kaydı")
    with st.form("yeni_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            misafir = st.text_input("Misafir Ad Soyad")
            oda = st.text_input("Oda No")
        with c2:
            op_list = ["TUI", "LMX", "FTI", "DERTOUR", "JOLLY", "ETUR", "DİĞER..."]
            secilen_op = st.selectbox("Operatör", op_list)
            manuel_op = st.text_input("Listede yoksa yazın")
            op = manuel_op if manuel_op else secilen_op
        with c3:
            tarih = st.date_input("Kayıt Tarihi", datetime.now())
            deadline = st.date_input("⚠️ Son Cevaplama", tarih + timedelta(days=14))
        
        st.file_uploader("📁 Belge/Voucher Yükle", type=['pdf','jpg','png'])
        sikayet = st.text_area("Şikayet Detayı")
        
        if st.form_submit_button("Sisteme İşle"):
            if misafir:
                st.success(f"✅ {misafir} için kayıt simüle edildi. Google Sheet'e eklemeyi unutmayın!")
            else:
                st.error("Lütfen Misafir Adı alanını doldurun.")

# --- 2. ARAŞTIRMA & SAVUNMA ---
elif menu == "🔍 ARAŞTIRMA & SAVUNMA":
    st.header("🔍 Araştırma ve Savunma Süreci")
    
    # Hata kontrolü: Eğer tablo boşsa veya isimler düzgün gelmediyse
    isim_listesi = [x for x in df["Misafir"].unique() if str(x) != 'nan'] if not df.empty else []
    
    if not isim_listesi:
        st.warning("⚠️ Tabloda henüz kayıtlı dosya bulunamadı. Lütfen Google Sheet'e veri ekleyin.")
    else:
        secilen_isim = st.selectbox("İşlem Yapılacak Misafiri Seçin", isim_listesi)
        
        # Seçilen isme göre veriyi çek
        kisi_verisi = df[df["Misafir"] == secilen_isim]
        
        if not kisi_verisi.empty:
            kisi = kisi_verisi.iloc[0]
            
            c1, c2 = st.columns(2)
            with c1:
                st.info(f"**Oda:** {kisi.get('Oda', 'Bilinmiyor')} | **Acente:** {kisi.get('Operator', 'Bilinmiyor')}")
                st.text_area("🏢 İç Araştırma (Departman Notları)", height=150)
            with c2:
                st.error(f"**⏰ Son Cevaplama Tarihi:** {kisi.get('Deadline', 'Belirtilmedi')}")
                st.text_area("✉️ Resmi Savunma (Acenteye Yazılan)", height=150)
            
            st.button("💾 Gelişmeleri Kaydet")

# --- 3. MUTABAKAT ---
elif menu == "🗄️ MUTABAKAT":
    st.header("🗄️ Finansal Mutabakat")
    isim_listesi = [x for x in df["Misafir"].unique() if str(x) != 'nan'] if not df.empty else []
    
    if not isim_listesi:
        st.info("Mutabakat yapılacak dosya bulunamadı.")
    else:
        st.selectbox("Dosya Seç", isim_listesi)
        c1, c2 = st.columns(2)
        c1.number_input("Anlaşılan Tutar (€)", 0.0)
        c2.selectbox("Durum", ["Açık", "Ödeme Bekliyor", "Kapandı", "İptal"])
        st.button("Mutabakatı Onayla")

# --- 4. GM RAPORU ---
elif menu == "📊 GM RAPORU":
    st.header("📊 Genel Müdürlük Raporu")
    
    t1, t2, t3 = st.columns(3)
    t1.metric("Toplam Dosya", len(df))
    t2.metric("Açık Dosya", len(df[df["Durum"] != "Kapandı"]) if "Durum" in df.columns else "0")
    t3.metric("Kurtarılan Tutar", "0 €")
    
    st.subheader("📋 Güncel Kayıt Listesi")
    st.dataframe(df, use_container_width=True)
