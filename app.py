if st.button("Taktiksel Çözümü Hesapla", type="primary"):
    current_problem = problem_input.strip() or st.session_state.problem_text.strip()
    if not current_problem:
        st.warning("Lütfen bir problem açıklaması girin veya şablonlardan birini seçin.")
    elif not api_key:
        st.error("API Anahtarı bulunamadı!")
    else:
        prompt = f"""
Sen uzman bir Oxygen Not Included (ONI) mühendisisin.
Koloni Durumu: Döngü {cycle}, Nüfus {dupes}, Sektör {category}
Sorun: {current_problem}

Doğrudan ve pratik şekilde şu 4 başlık altında taktik ver:
### 1. Kök Neden
### 2. Acil Eylem Planı (Adım Adım)
### 3. Malzeme ve Mimari Kurallar
### 4. Döngü {cycle + 50} Önleyici Tedbir
"""
        client = genai.Client(api_key=api_key.strip())
        
        with st.spinner("⚡ Termodinamik simülasyon hesaplanıyor, kriz senaryosu çözülüyor..."):
            try:
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt
                )
                st.markdown("---")
                st.markdown("## 📋 Mühendislik Raporu")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"Hata: {e}")
