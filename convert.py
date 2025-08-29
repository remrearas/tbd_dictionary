#!/usr/bin/env python3
"""
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
Copyright (c) 2025 Rıza Emre ARAS <r.emrearas@proton.me>

TR: TBD Bilişim Terimleri Sözlüğü PDF Dönüştürücü
==================================================

Türkiye Bilişim Derneği (TBD) tarafından hazırlanan İngilizce-Türkçe bilişim terimleri 
sözlüğünün PDF formatından dijital ve aranabilir JSON formatına dönüştürülmesi için 
geliştirilmiş özel bir dönüştürücü scriptidir. Bu araç, basılı sözlük içeriğini modern 
web uygulamalarında kullanılabilecek yapılandırılmış veri formatına çevirir.

Script'in temel amacı, TBD Bilişimde Özenli Türkçe Çalışma Grubu tarafından hazırlanan 
ve 28,000'den fazla bilişim terimini içeren kapsamlı sözlüğü, programatik erişime uygun 
hale getirmektir. PDF içerisindeki yapılandırılmamış metin verisi, düzenli ifadeler ve 
metin işleme teknikleri kullanılarak İngilizce-Türkçe terim çiftlerine ayrıştırılır.

Dönüştürme Süreci:
-----------------
1. PDF Okuma: pdfplumber kütüphanesi ile sayfa sayfa metin çıkarımı
2. Metin Temizleme: Gereksiz başlıklar, semboller ve formatlamaların temizlenmesi
3. Terim Ayrıştırma: ' : ' ayracı kullanılarak İngilizce-Türkçe çiftlerinin tespiti
4. Veri Doğrulama: Uzunluk kontrolü ve boş değer filtreleme
5. JSON Çıktı: Metadata ve terimler içeren yapılandırılmış JSON dosyası üretimi

Çıktı Formatı:
-------------
- metadata: Kaynak, toplam terim sayısı ve versiyon bilgileri
- terms: İngilizce (en) ve Türkçe (tr) alanları içeren terim listesi
- UTF-8 kodlaması ile Türkçe karakterlerin korunması

Kullanım Senaryoları:
-------------------
- Web tabanlı sözlük uygulaması için veri kaynağı
- Terminoloji standardizasyonu çalışmaları
- Otomatik çeviri sistemleri için referans veritabanı
- Bilişim Türkçesi araştırmaları için analiz verisi

==================================================

EN: TBD IT Terms Dictionary PDF Converter
==================================================

A specialized converter script developed to transform the English-Turkish IT terms 
dictionary prepared by the Turkish Informatics Association (TBD) from PDF format 
into a digital and searchable JSON format. This tool converts printed dictionary 
content into structured data format suitable for modern web applications.

The primary purpose of this script is to make the comprehensive dictionary containing 
over 28,000 IT terms, prepared by TBD's Careful Turkish in Informatics Working Group, 
suitable for programmatic access. The unstructured text data within the PDF is parsed 
into English-Turkish term pairs using regular expressions and text processing techniques.

Conversion Process:
------------------
1. PDF Reading: Page-by-page text extraction using pdfplumber library
2. Text Cleaning: Removal of unnecessary headers, symbols, and formatting
3. Term Parsing: Detection of English-Turkish pairs using ' : ' separator
4. Data Validation: Length checking and empty value filtering
5. JSON Output: Generation of structured JSON file with metadata and terms

Output Format:
-------------
- metadata: Source, total term count, and version information
- terms: List of terms containing English (en) and Turkish (tr) fields
- UTF-8 encoding preserving Turkish characters

Use Cases:
---------
- Data source for web-based dictionary application
- Terminology standardization efforts
- Reference database for automatic translation systems
- Analysis data for IT Turkish research

"""
import pdfplumber
import json
import logging
from pathlib import Path
from typing import List, Dict


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def parse_tbd_dictionary(pdf_path: str) -> List[Dict[str, str]]:
    """
    TR: TBD sözlük PDF dosyasını ayrıştırır ve terimleri çıkarır.
    EN: Parse TBD dictionary PDF and extract terms.
    
    Args:
        pdf_path: TR: PDF dosyasının yolu / EN: Path to PDF file
        
    Returns:
        TR: İngilizce-Türkçe terim çiftlerinin listesi
        EN: List of English-Turkish term pairs
    """
    term_list = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            logger.info(f"Processing page {page_num + 1}...")

            text = page.extract_text()
            if not text:
                continue

            # Split into lines
            lines = text.split('\n')

            for line in lines:
                # Skip headers and unnecessary lines
                if any(skip in line for skip in ['English', 'Türkçe', 'terms', 'Symbols', 'Numbers', ':', '--']):
                    if ' : ' not in line or line.count(':') > 2:
                        continue

                # Skip empty lines
                if not line.strip():
                    continue

                # Find terms separated by " : "
                if ' : ' in line:
                    parts = line.split(' : ', 1)
                    if len(parts) == 2:
                        english = parts[0].strip()
                        turkish = parts[1].strip()

                        # Cleanup
                        if english and turkish and len(english) < 200 and len(turkish) < 200:
                            term_list.append({
                                'en': english,
                                'tr': turkish
                            })

    return term_list


def save_as_json(term_list: List[Dict[str, str]], output_path: Path):
    """
    TR: Terimleri JSON formatında kaydeder.
    EN: Save terms as JSON format.
    
    Args:
        term_list: TR: Terim listesi / EN: List of terms
        output_path: TR: Çıktı dizini / EN: Output directory
        
    Returns:
        TR: Oluşturulan JSON dosyasının yolu
        EN: Path to created JSON file
    """
    output = {
        'metadata': {
            'source': 'TBD Bilişim Terimleri Sözlüğü',
            'total_terms': len(term_list),
            'version': '2025-08-04'
        },
        'terms': term_list
    }
    
    output_file = output_path / 'tbd_dictionary.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    logger.info(f"JSON file saved: {output_file}")
    logger.info(f"Total {len(term_list)} terms saved")
    return output_file


# Usage
if __name__ == "__main__":
    pdf_file = "data/TBD-Bilisim-Sozlugu-Ingilizce-Turkce-2025-08-04.pdf"
    try:
        # Parse PDF
        parsed_terms = parse_tbd_dictionary(pdf_file)
        
        # Create output directory if it doesn't exist
        output_dir = Path('output')
        output_dir.mkdir(exist_ok=True)
        
        # Save as JSON
        logger.info("Saving dictionary in JSON format")
        save_as_json(parsed_terms, output_dir)
        
        logger.info(f"Total {len(parsed_terms)} terms successfully converted")

        # Show first 5 terms as example
        logger.info("First 5 terms:")
        for i, term in enumerate(parsed_terms[:5]):
            logger.info(f"{i + 1}. {term['en']} -> {term['tr']}")

    except Exception as e:
        logger.error(f"Error: {e}")
        logger.error("Please make sure the PDF file path is correct.")