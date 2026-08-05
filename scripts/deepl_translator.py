#!/usr/bin/env python3
import os
import json
import time
import requests

# DeepL desteklenen diller: 
# (Farsça (fa) ve Azerice (az) DeepL tarafından doğrudan desteklenmez, bu nedenle atlanır)
DEEPL_SUPPORTED = {
    "en": "EN-US",
    "de": "DE",
    "fr": "FR",
    "zh": "ZH",
    "ar": "AR",
    "ru": "RU",
    "es": "ES"
}

# --- KULLANICI AYARLARI ---
import os
AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "BURAYA_API_ANAHTARINI_GİRİN")
URL = "https://api-free.deepl.com/v2/translate"
LOCALES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "mintsky", "locales")
FORCE_ALL = False # True yapılırsa mevcut tüm çevirileri baştan DeepL ile değiştirir. False ise sadece eksikleri çevirir.

# Ekstra çevrilecek kelimeleri sabitlerden topla
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from mintsky.constants import HADISE, WMO_HADISE
    extra_texts = []
    for val in HADISE.values():
        extra_texts.extend([val[1], val[2]])
    for val in WMO_HADISE.values():
        extra_texts.extend([val[1], val[2]])
    
    extra_texts.extend([
        "İyi", "Orta", "Hassas", "Kötü", "Çok Kötü", "Tehlikeli", 
        "Düşük", "Yüksek", "Çok Yüksek", "Aşırı",
        "Saatlik", "Günlük", "SAATLİK TAHMİN", "GÜNLÜK TAHMİN",
        "🕐  SAATLİK TAHMİN (Kaynak: MGM + Open-Meteo)",
        "🕐  SAATLİK TAHMİN (Kaynak: Open-Meteo)",
        "📅  5 GÜNLÜK TAHMİN (Kaynak: MGM + Open-Meteo)",
        "📅  5 GÜNLÜK TAHMİN (Kaynak: Open-Meteo)",
        "Güncelleniyor...", "Uygulama Güncel", "Güncelleme Kontrolü Başarısız"
    ])
except Exception as e:
    print(f"Uyarı: Sabitler okunamadı, sadece tr.json kullanılacak. Hata: {e}")
    extra_texts = []

def translate_deepl(text, target_lang):
    if not text or text == "—": return text
    
    tl = DEEPL_SUPPORTED.get(target_lang)
    if not tl:
        print(f"Uyarı: '{target_lang}' DeepL tarafından desteklenmiyor. Atlanıyor.")
        return text

    headers = {
        "Authorization": f"DeepL-Auth-Key {AUTH_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": [text],
        "target_lang": tl
    }
    
    try:
        response = requests.post(URL, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()["translations"][0]["text"]
        else:
            print(f"Hata: DeepL API {response.status_code} döndürdü. ({response.text})")
            return text
    except Exception as e:
        print(f"Hata: {e}")
        return text

def main():
    print("🚀 DeepL Çeviri Robotu Başlatılıyor...")
    
    tr_path = os.path.join(LOCALES_DIR, "tr.json")
    if not os.path.exists(tr_path):
        print(f"Hata: {tr_path} bulunamadı.")
        return
        
    with open(tr_path, "r", encoding="utf-8") as f:
        tr_data = json.load(f)
        
    # Tüm Türkçe metin havuzunu oluştur (tr.json + sabitler)
    all_tr_strings = set(tr_data.keys())
    all_tr_strings.update(tr_data.values())
    all_tr_strings.update(extra_texts)
    
    for filename in os.listdir(LOCALES_DIR):
        if not filename.endswith(".json") or filename == "tr.json":
            continue
            
        lang_code = filename.replace(".json", "")
        filepath = os.path.join(LOCALES_DIR, filename)
        
        with open(filepath, "r", encoding="utf-8") as f:
            lang_data = json.load(f)
            
        updated = False
        print(f"\n--- {lang_code.upper()} İşleniyor ---")
        
        if lang_code not in DEEPL_SUPPORTED:
            print(f"{lang_code} DeepL tarafından desteklenmiyor, atlanıyor...")
            continue
            
        for text in all_tr_strings:
            # Sadece çevirisi olmayanları veya FORCE_ALL açıksa hepsini çevir
            if text not in lang_data or FORCE_ALL:
                # Orijinal string Türkçe karakter içermeyen bir KEY ise, value'yu çevir
                # (örneğin "btn_search", "title_hourly" gibi)
                source_text = tr_data.get(text, text) 
                
                translated = translate_deepl(source_text, lang_code)
                if translated and translated != source_text:
                    lang_data[text] = translated
                    print(f"✔️ Çevrildi: {source_text[:30]}... -> {translated[:30]}...")
                    updated = True
                    time.sleep(0.3) # API limitini yormamak için kısa bekleme
                    
        if updated:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(lang_data, f, ensure_ascii=False, indent=4)
            print(f"💾 {filename} kaydedildi!")
        else:
            print("Zaten güncel, değişiklik yapılmadı.")
            
    print("\n✅ Tüm çeviri işlemleri tamamlandı!")

if __name__ == "__main__":
    main()
