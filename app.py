if st.button("Taktiksel Çözümü Hesapla", type="primary"):
    current_problem = problem_input.strip() or st.session_state.problem_text.strip()
    if not current_problem:
        st.warning("Lütfen bir problem açıklaması girin veya şablonlardan birini seçin.")
    elif not api_key:
        st.error("API Anahtarı bulunamadı! Settings -> Secrets kontrol edilmeli.")
    else:
        prompt = f"""
Sen dünya çapında tecrübeli bir Oxygen Not Included (ONI) mühendisisin.
Koloni: Döngü {cycle}, Nüfus {dupes}, Sektör {category}
Sorun: {current_problem}

Lütfen yanıtını doğrudan aşağıdaki 4 ana başlık altında, net ve pratik ver:
### 1. Kök Neden & Fiziksel Mekanik
### 2. Adım Adım Müdahale Protokolü
### 3. Malzeme ve Mimari Kurallar
### 4. Döngü {cycle + 50} Önleyici Tedbir
"""
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": api_key.strip()
        }
        
        # thinking_budget: 0 düşünme gecikmesini sıfırlar
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "thinkingConfig": {
                    "thinkingBudget": 0
                }
            }
        }

        # streamGenerateContent uç noktası canlı veri akışı sağlar
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:streamGenerateContent?alt=sse"

        st.markdown("---")
        st.markdown("## 📋 Mühendislik Raporu")
        report_placeholder = st.empty()
        full_text = ""

        try:
            with requests.post(url, headers=headers, json=payload, stream=True, timeout=30) as r:
                if r.status_code == 200:
                    import json
                    for line in r.iter_lines(decode_unicode=True):
                        if line and line.startswith("data: "):
                            data_str = line[6:]
                            try:
                                chunk = json.loads(data_str)
                                text_part = chunk["candidates"][0]["content"]["parts"][0]["text"]
                                full_text += text_part
                                report_placeholder.markdown(full_text + "▌")
                            except Exception:
                                continue
                    report_placeholder.markdown(full_text)
                else:
                    st.error(f"Hata Kodu ({r.status_code}): {r.text}")
        except Exception as e:
            st.error(f"Bağlantı hatası: {e}")
