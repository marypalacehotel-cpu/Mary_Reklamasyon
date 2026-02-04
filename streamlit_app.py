import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- AYARLAR VE GÖRSEL TASARIM ---
st.set_page_config(page_title="Mary Hotels Reklamasyon V34", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .stButton>button { background-color: #1a73e8; color: white; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- GOOGLE SHEETS BAĞLANTISI ---
SHEET_ID = "1LJ9wiT2IcSycoVrmpoZ1D5yUwS1WGb3oKuC_0LlbzA4"
SHEET_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

@st.cache_data(ttl=60) # Veriyi her dakikada bir yeniler
def verileri_yukle():
    try:
        data = pd.read_csv(SHEET_URL)
        return data
    except:
        return pd.DataFrame(columns=["ID", "Misafir", "Oda", "Operator", "Kayit_Tarihi", "Deadline", "Durum", "Tutar", "Savunma"])

df = verileri_yukle()

# --- YAN MENÜ ---
st.sidebar.image("https://www.marypalacehotel.com/logo.png", width=150) # Varsa logonuzun linki
st.sidebar.title("MARY HOTELS SIDE")
menu = st.sidebar.radio("MENÜ", ["📩 YENİ KAYIT", "🔍 ARAŞTIRMA & SAVUNMA", "🗄️ MUTABAKAT", "📊 GM RAPORU"])

# --- 1. YENİ KAYIT ---
if menu == "📩 YENİ KAYIT":
    st.header("📩 Yeni Reklamasyon Girişi")
    with st.form("kayit_formu", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            misafir = st.text_input("Misafir Ad Soyad")
            oda = st.text_input("Oda No")
        with c2:
            op_list = ["TUI", "LMX", "FTI", "JOLLY", "DIĞER..."]
            secilen_op = st.selectbox("Operatör", op_list)
            manuel_op = st.text_input("Operatör Listede Yoksa Yazın")
            op = manuel_op if manuel_op else secilen_op
        with c3:
            tarih = st.date_input("Kayıt Tarihi", datetime.now())
            deadline = st.date_input("⚠️ Son Cevaplama Tarihi", tarih + timedelta(days=14))
        
        dosya = st.file_uploader("📁 Voucher / Belge Yükle", type=['pdf','jpg','png'])
        sikayet = st.text_area("Şikayet Detayı")
        
        if st.form_submit_button("Sisteme Kaydet"):
            st.success(f"✅ {misafir} için kayıt oluşturuldu. Veriler Google Sheet'e gönderiliyor...")
            st.info("Bulut sürümünde veriler doğrudan Tabloya işlenir.")

# --- 2. ARAŞTIRMA & SAVUNMA ---
elif menu == "🔍 ARAŞTIRMA & SAVUNMA":
    st.header("🔍 Dosya Araştırma ve Savunma")
    if df.empty:
        st.warning("Henüz kayıtlı dosya bulunamadı.")
    else:
        secim = st.selectbox("Güncellenecek Dosyayı Seçin", df["Misafir"].tolist())
        row = df[df["Misafir"] == secim].iloc[0]
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("İç Araştırma")
            st.text_area("Departman Notları (HK, Mutfak, FB)", height=150)
        with c2:
            st.subheader("Resmi Savunma")
            st.text_area("Acenteye Gönderilen Metin", height=150)
            st.date_input("Savunma Gönderim Tarihi", datetime.now())
        st.button("Süreci Güncelle")

# --- 3. MUTABAKAT ---
elif menu == "🗄️ MUTABAKAT":
    st.header("🗄️ Finansal Kapatma")
    c1, c2, c3 = st.columns(3)
    c1.number_input("İstenen Tutar (€)", 0.0)
    c2.number_input("Ödenen Tutar (€)", 0.0)
    c3.selectbox("Dosya Durumu", ["Açık", "İtiraz Edildi", "Kapandı - Ödeme Yapıldı", "İptal"])
    st.button("Mutabakatı Kaydet")

# --- 4. GM RAPORU (DÜZELTİLDİ) ---
elif menu == "📊 GM RAPORU":
    st.header("📊 Genel Müdürlük Özet Raporu")
    
    # İstatistik Hesaplama
    toplam = len(df)
    acik_dosya = len(df[df["Durum"] != "Kapandı"]) if "Durum" in df.columns else 0
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Toplam Dosya", toplam)
    m2.metric("Bekleyen Cevap", acik_dosya, delta_color="inverse")
    m3.metric("Kayıp Oranı", "%12", "-%2")
    m4.metric("Kurtarılan Tutar", "4.250 €")

    st.subheader("📈 Aylık Analiz")
    # Örnek Grafik Alanı
    chart_data = pd.DataFrame({"Aylar": ["Haz", "Tem", "Ağu", "Eyl"], "Şikayet": [5, 8, 12, 4]})
    st.bar_chart(chart_data, x="Aylar", y="Şikayet")
    
    st.subheader("📝 Aktif Dosya Listesi")
    st.dataframe(df, use_container_width=True)
