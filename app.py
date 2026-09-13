import os
import json
import requests
import streamlit as st

st.set_page_config(
    page_title="ONI Tactical Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp {
        background-color: #0b0e14;
        color: #e2e8f0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    section[data-testid="stSidebar"] {
        background-color: #121824;
        border-right: 1px solid #1e293b;
    }
    .metric-card {
        background: linear-gradient(135deg, #161f30 0%, #0f172a 100%);
        border: 1px solid #25334d;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        margin-bottom: 12px;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .stButton > button {
        background: linear-gradient(90deg, #0284c7, #2563eb);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        box-shadow: 0 4px 14px rgba(2, 132, 199, 0.4);
    }
</style>
""", unsafe_allow_html=True)

st.title("⚡ ONI Tactical Terminal")
st.caption("Oxygen Not Included için termodinamik simülasyon ve kriz optimizasyon rehberi.")

api_key = ""
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
elif os.environ.get("GEMINI_API_KEY"):
    api_key = os.environ.get("GEMINI_API_KEY")

with st.sidebar:
    st.markdown("### 📊 Koloni Telemetrisi")
    cycle = st.number_input("Döngü (Cycle):", min_value=1, max_value=5000, value=75, step=5)
    dupes = st.number_input("Duplicant Sayısı:", min_value=1, max_value=50, value=8)
    category = st.selectbox(
        "Kritik Sektör:",
        [
            "🌾 Tarım & Botanik (Sıcaklık / Solma)",
            "🥩 Hayvancılık & Evrim (Hatch, Drecko, Puft)",
            "💨 Oksijen & Gaz Dağılımı (SPOM, Basınç)",
            "❄️ Isı İmhası & Soğutma Döngüleri (AT/ST)",
            "⚡ Güç Ağı, Kömür & Otomasyon Mantığı",
            "🚰 Su Arıtma & Mikroplar (Food Poisoning)"
        ]
    )

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{cycle}</div><div class="metric-label">Döngü</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{dupes} Dup</div><div class="metric-label">Nüfus</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{dupes * 100} g/s</div><div class="metric-label">O₂ İhtiyacı</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><div class="metric-value">{dupes * 1000} kcal</div><div class="metric-label">Günlük Kalori</div></div>', unsafe_allow_html=True)

st.markdown("### 🚨 Kriz Parametreleri")

if "problem_text" not in st.session_state:
    st.session_state.problem_text = ""

def set_text(val):
    st.session_state.problem_text = val

st.write("**Hızlı Kriz Şablonları:**")
c_btn1, c_btn2, c_btn3 = st.columns(3)

with c_btn1:
    st.button("🔥 Mealwood 30°C Üstü", on_click=set_text, args=("Döngü 60 civarı. Kömür jeneratörleri ve makineler yüzünden çiftlik odası 31°C oldu. Mealwood'lar soldu, açlık tehlikesi var. Yakında buz biyomu yok.",))
with c_btn2:
    st.button("⚠️ SPOM Hidrojen Tıkanması", on_click=set_text, args=("Elektrolizör odası kurdum ama hidrojen boruları tıkandı ve oksijen hattına karıştı. Duplicant'lar nefes alamıyor.",))
with c_btn3:
    st.button("🪨 Hatch'ler Taş Vermiyor", on_click=set_text, args=("Standart Hatch çiftliğim var ancak Stone Hatch'e evrilmiyorlar ve kömür üretimim tükenmek üzere. Ne yapmalıyım?",))

problem_input = st.text_area(
    "Karşılaşılan Teknik Tıkanıklık:",
    value=st.session_state.problem_text,
    height=110,
    placeholder="Sistemin patladığı noktayı, ortam sıcaklığını ve elindeki ana materyalleri yaz..."
)

if st.button("Taktiksel Çözümü Hesapla", type="primary"):
    current_problem = problem_input.strip() or st.session_state.problem_text.strip()
    if not current_problem:
        st.warning("Lütfen bir problem açıklaması girin veya şablonlardan birini seçin.")
    elif not api_key:
        st.error("API Anahtarı bulunamadı! Settings -> Secrets kontrol edilmeli.")
    else:
        prompt = f"""
Sen Oxygen Not Included (ONI) baş mühendisisin.
Döngü: {cycle}, Nüfus: {dupes}, Sektör: {category}
Sorun: {current_problem}

Doğrudan kısa, net maddelerle şu 4 başlıkta pratik taktik ver:
### 1. Kök Neden
### 2. Acil Eylem Planı (Adım Adım)
### 3. Kullanılacak Malzeme & Mimari
### 4. Kalıcı Tedbir (Döngü {cycle + 50})
"""
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key.strip()
        }
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "maxOutputTokens": 700
            }
        }
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent"

        with st.spinner("⚡ Termodinamik simülasyon hesaplanıyor..."):
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=12)
                if response.status_code == 200:
                    res_data = response.json()
                    answer = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    st.markdown("---")
                    st.markdown("## 📋 Mühendislik Raporu")
                    st.markdown(answer)
                else:
                    st.error(f"Hata ({response.status_code}): {response.text}")
            except requests.exceptions.Timeout:
                st.error("Bağlantı zaman aşımına uğradı, lütfen tekrar deneyin.")
            except Exception as ex:
                st.error(f"Bağlantı hatası: {ex}")
