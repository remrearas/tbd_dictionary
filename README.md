# TBD Bilişim Terimleri Sözlüğü

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://tbd-dictionary.streamlit.app/)

🔗 **Canlı Demo:** [https://tbd-dictionary.streamlit.app/](https://tbd-dictionary.streamlit.app/)

Türkiye Bilişim Derneği (TBD) tarafından hazırlanan İngilizce-Türkçe Bilişim Terimleri Sözlüğü'nün modern, dijital ve gelişmiş arama özelliklerine sahip Streamlit tabanlı web uygulaması.

## Özellikler

- **28,000+ bilişim terimi** İngilizce-Türkçe karşılıkları
- **Akıllı arama özellikleri:**
  - **Fuzzy Search**: Yazım hatalarına toleranslı arama
  - **Exact Match**: Tam eşleşme araması
  - **Partial Match**: Kısmi eşleşme araması
- **Çift yönlü arama**: İngilizce veya Türkçe terim arayabilme
- **Modern web arayüzü** ile kolay kullanım
- **Dışa aktarım**: JSON, CSV, TXT formatlarında

## Kurulum

### 1. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 2. PDF'den Veri Çıkarımı

PDF dosyasını JSON formatına dönüştürün:

```bash
python convert.py
```

Bu komut `data/TBD-Bilisim-Sozlugu-Ingilizce-Turkce-2025-08-04.pdf` dosyasını okuyarak `output/tbd_dictionary.json` dosyasını oluşturur.

### 3. Web Uygulamasını Başlatın

```bash
streamlit run serve.py
```

Uygulama otomatik olarak tarayıcınızda açılacaktır: `http://localhost:8501`

## Dosya Yapısı

```
tbd_dictionary/
├── data/                           # PDF kaynak dosyası
│   └── TBD-Bilisim-Sozlugu-*.pdf
├── output/                         # Üretilen JSON dosyası
│   └── tbd_dictionary.json
├── convert.py                      # PDF → JSON dönüştürücü
├── serve.py                        # Streamlit web uygulaması
├── requirements.txt                # Python bağımlılıkları
└── README.md                       # Bu dosya
```

## Kullanım

### Web Arayüzü Kullanımı

1. **Arama**: Ana sayfadaki arama kutusuna İngilizce veya Türkçe terim girin
2. **Arama Ayarları**: Sol panelden arama modunu ve dilini seçin
3. **Sonuçlar**: Eşleşen terimler benzerlik skorları ile listelenir
4. **Rastgele Terim**: Sol panelden rastgele bir terim görüntüleyin
5. **Dışa Aktarım**: Arama sonuçlarını JSON/CSV/TXT formatında indirin

### Arama Modları

| Mod         | Açıklama                     | Örnek                                 |
|-------------|------------------------------|---------------------------------------|
| **Fuzzy**   | Yazım hatalarına toleranslı  | "claud" → "cloud" bulur               |
| **Exact**   | Tam eşleşme gerektirir       | Sadece birebir eşleşmeleri bulur      |
| **Partial** | İçinde geçen terimleri bulur | "data" → "database", "metadata" bulur |

### Programatik Kullanım

```python
import json

# JSON dosyasını yükle
with open('output/tbd_dictionary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Terimlere eriş
terms = data['terms']
print(f"Toplam {len(terms)} terim yüklendi")

# Örnek arama
search_term = "cloud"
results = [t for t in terms if search_term.lower() in t['en'].lower()]
for term in results[:5]:
    print(f"{term['en']} → {term['tr']}")
```

## Veri Formatı

JSON dosyası şu yapıdadır:

```json
{
  "metadata": {
    "source": "TBD Bilişim Terimleri Sözlüğü",
    "total_terms": 28360,
    "version": "2025-08-04"
  },
  "terms": [
    {
      "en": "cloud computing",
      "tr": "bulut bilişim"
    }
  ]
}
```

## Hazırlayanlar

**Türkiye Bilişim Derneği (TBD)**  
**Bilişimde Özenli Türkçe Çalışma Grubu**

- Emeritüs Prof. Dr. Tuncer Ören
- Ahmet Pekel
- Koray Özer
- İ. İlker Tabak
- Eymen Y. Görgülü

**Bilgiağı:** Mehmet Pektaş  
**Güncelleme:** 2025-08-04

**Kaynak:** [Bilişimde Özenli Türkçe - Önerilen Tüm Terimler](https://bilisimde.ozenliturkce.org.tr/onerilen-tum-terimler-ingilizce-turkce/)

---

Copyright (c) 2025 Rıza Emre ARAS