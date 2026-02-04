import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import io

# --- MASAÜSTÜ KLASÖR YAPILANDIRMASI ---
# Programın çalıştığı klasörü baz alır
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "mary_hotels_database_v33.xlsx")
UPLOAD_DIR = os.path.join(BASE_DIR, "mary_arsiv_dosyalari")

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- VERİ YÖNETİMİ ---
def load_db():
    status_list = ["BEKLEMEDE", "SAVUNMA GÖNDERİLDİ", "TAM RED", "KABUL", "KISMİ KABUL"]
    if os.path.exists(DB_FILE):
        try:
            df = pd.read_excel(DB_FILE)
            return df, status_list
        except: pass
    return pd.DataFrame(columns=["Voucher", "Acente", "Misafir", "Kayit_Tarihi", "Vade_Tarihi", 
                                 "Acente_Sikayeti", "Otel_Arastirmasi", "Otel_Savunmasi", 
                                 "Talep_Eur", "Kesinti_Eur", "Durum"]), status_list

df, STATUS_LIST = load_db()

# --- KURUMSAL LOGO VE BAŞLIK ---
st.markdown(f"""
    <div style="background-color: #0c2461; padding: 20px; border-radius: 10px; text-align: center; border-bottom: 5px solid #f1c40f;">
        <h1 style="color: white; margin: 0;">MARY HOTELS SIDE</h1>
        <p style="color: #f1c40f; margin: 0; font-weight: bold;">Masaüstü Reklamasyon Yönetim Sistemi</p>
    </div>
""", unsafe_allow_html=True)

st.write("") # Boşluk

# --- 🚨 SAYAÇLI UYARI ---
if not df.empty:
    aktif = df[df['Durum'] == "BEKLEMEDE"]
    for idx, r in aktif.iterrows():
        try:
            vade = pd.to_datetime(r['Vade_Tarihi'])
            kalan = vade - datetime.now()
            if 0 < kalan.total_seconds() <= 86400:
                st.error(f"⚡ **SAVUNMAYI GÖNDER (ACİL):** {r['Acente']} - {r['Voucher']} | Kalan: {kalan.seconds//3600} Saat")
        except: continue

# --- SEKMELER ---
tabs = st.tabs(["📩 YENİ KAYIT", "🔍 ARAŞTIRMA & SAVUNMA", "🗄️ MUTABAKAT", "📊 GM RAPORU", "🛠️ KAYIT YÖNETİMİ"])

# 1. YENİ KAYIT
with tabs[0]:
    with st.form("yeni_form"):
        c1, c2, c3 = st.columns(3)
        v_no = c1.text_input("Voucher No")
        ace = c2.text_input("Acente")
        mis = c3.text_input("Misafir")
        t_eur = c1.number_input("Talep (€)", min_value=0.0)
        v_tar = c2.date_input("Savunma Vadesi", datetime.now() + timedelta(days=4))
        sikayet = st.text_area("Şikayet Metni")
        uploaded_files = st.file_uploader("Evrakları Yükle", accept_multiple_files=True)
        
        if st.form_submit_button("DOSYAYI KAYDET"):
            # Dosyaları Klasöre Kaydet
            if uploaded_files:
                for f in uploaded_files:
                    with open(os.path.join(UPLOAD_DIR, f"{v_no}_{f.name}"), "wb") as file:
                        file.write(f.getbuffer())
            
            new_data = {"Voucher": str(v_no), "Acente": ace, "Misafir": mis, "Kayit_Tarihi": datetime.now().strftime('%d.%m.%Y'), 
                        "Vade_Tarihi": str(v_tar), "Acente_Sikayeti": sikayet, "Talep_Eur": t_eur, "Kesinti_Eur": 0.0, "Durum": "BEKLEMEDE"}
            df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
            df.to_excel(DB_FILE, index=False)
            st.success("Kayıt Masaüstüne İşlendi!"); st.rerun()

# 2. ARAŞTIRMA & SAVUNMA
with tabs[1]:
    bekleyenler = df[df['Durum'].isin(["BEKLEMEDE", "SAVUNMA GÖNDERİLDİ"])]
    for idx, row in bekleyenler.iterrows():
        with st.expander(f"📁 {row['Acente']} - {row['Voucher']}"):
            ca1, ca2 = st.columns(2)
            ara = ca1.text_area("İç Araştırma", value=str(row['Otel_Arastirmasi']), key=f"a_{idx}")
            sav = ca2.text_area("Savunma Notu", value=str(row['Otel_Savunmasi']), key=f"s_{idx}")
            if st.button("Güncelle", key=f"b_{idx}"):
                df.at[idx, 'Otel_Arastirmasi'], df.at[idx, 'Otel_Savunmasi'] = ara, sav
                df.at[idx, 'Durum'] = "SAVUNMA GÖNDERİLDİ"
                df.to_excel(DB_FILE, index=False); st.rerun()

# 4. GM RAPORU
with tabs[3]:
    if not df.empty:
        st.subheader("📊 Finansal Durum")
        m1, m2, m3 = st.columns(3)
        t_ist, t_kes = df['Talep_Eur'].sum(), df['Kesinti_Eur'].sum()
        m1.metric("Toplam Talep", f"{t_ist:,.2f} €")
        m2.metric("Ödenen", f"{t_kes:,.2f} €")
        m3.metric("Kurtarılan", f"{t_ist - t_kes:,.2f} €")
        st.dataframe(df, use_container_width=True)
        # Excel İndir
        buf = io.BytesIO()
        df.to_excel(buf, index=False, engine='openpyxl')
        st.download_button("📥 EXCEL RAPORU AL", data=buf.getvalue(), file_name="Mary_Hotels_Rapor.xlsx", use_container_width=True)

# 5. KAYIT YÖNETİMİ
with tabs[4]:
    st.subheader("🗑️ Kayıt Sil / Düzenle")
    for idx, row in df.iterrows():
        col1, col2 = st.columns([5, 1])
        col1.write(f"**{row['Voucher']}** | {row['Acente']} | {row['Durum']}")
        if col2.button("SİL", key=f"del_{idx}"):
            df = df.drop(idx)
            df.to_excel(DB_FILE, index=False); st.rerun()