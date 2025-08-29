#!/usr/bin/env python3
"""
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ ██████╗ ███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔═══██╗████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ██║   ██║██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██║   ██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝     ╚═╝
Copyright (c) 2025 Rıza Emre ARAS <r.emrearas@proton.me>

TR: TBD Bilişim Terimleri Sözlüğü Streamlit Web Arayüzü
==================================================

TBD Bilişim Terimleri Sözlüğü'nün modern ve kullanıcı dostu web arayüzü uygulamasıdır. 
Streamlit framework'ü kullanılarak geliştirilen bu uygulama, 28,000'den fazla bilişim 
teriminin hızlı ve verimli bir şekilde aranmasını, görüntülenmesini ve dışa aktarılmasını 
sağlar. Kullanıcılar, İngilizce veya Türkçe terim aramaları yapabilir, sonuçları 
filtreleyebilir ve farklı formatlarda indirebilir.

Uygulamanın temel amacı, TBD sözlüğündeki bilişim terimlerine erişimi kolaylaştırmak 
ve Türkçe bilişim terminolojisinin doğru kullanımını teşvik etmektir. Fuzzy arama 
özelliği sayesinde yazım hatalarına tolerans gösterir, kısmi eşleşmelerle ilgili 
terimleri bulur ve kullanıcı deneyimini iyileştirir.

Arama Özellikleri:
----------------
1. Fuzzy Search: Yazım hatalarına toleranslı, yaklaşık eşleşme
2. Exact Match: Tam eşleşme araması için kesin sonuçlar
3. Partial Match: Kısmi eşleşme ile ilgili terimleri bulma
4. Çift Yönlü Arama: İngilizce'den Türkçe'ye veya Türkçe'den İngilizce'ye
5. Skor Tabanlı Sıralama: Benzerlik skoruna göre sonuç sıralaması

Kullanıcı Arayüzü Bileşenleri:
----------------------------
- Arama Kutusu: Gerçek zamanlı terim araması
- Ayarlar Paneli: Arama modu, dil ve sonuç sayısı kontrolleri
- Sonuç Listesi: Sıralı, skorlu ve kopyalanabilir terim listesi
- İstatistikler: Toplam terim sayısı ve versiyon bilgileri
- Rastgele Terim: Keşif için rastgele terim önerisi
- Dışa Aktarım: JSON, CSV, TXT formatlarında indirme

==================================================

EN: TBD IT Terms Dictionary Streamlit Web Interface
==================================================

A modern and user-friendly web interface application for the TBD IT Terms Dictionary. 
Developed using the Streamlit framework, this application enables fast and efficient 
searching, viewing, and exporting of over 28,000 IT terms. Users can search for terms 
in English or Turkish, filter results, and download them in various formats.

The primary purpose of the application is to facilitate access to IT terms in the TBD 
dictionary and promote the correct use of Turkish IT terminology. With fuzzy search 
capability, it tolerates spelling errors, finds related terms with partial matches, 
and improves user experience.

Search Features:
---------------
1. Fuzzy Search: Spelling error tolerant, approximate matching
2. Exact Match: Precise results for exact match searching
3. Partial Match: Finding related terms with partial matching
4. Bidirectional Search: English to Turkish or Turkish to English
5. Score-based Sorting: Result ranking by similarity score

User Interface Components:
-------------------------
- Search Box: Real-time term searching
- Settings Panel: Search mode, language, and result count controls
- Results List: Ordered, scored, and copyable term list
- Statistics: Total term count and version information
- Random Term: Random term suggestion for exploration
- Export: Download in JSON, CSV, TXT formats

"""
import streamlit as st
import json
import logging
import random
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from rapidfuzz import fuzz, process  # type: ignore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="TBD Bilişim Sözlüğü",
    page_icon=":books:",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_database() -> Tuple[Optional[List[Dict]], Dict]:
    """
    TR: JSON dosyasından veritabanını yükler.
    EN: Load database from JSON file.
    
    Returns:
        TR: Terimler listesi ve metadata bilgileri
        EN: Terms list and metadata information
    """
    json_path = Path("output/tbd_dictionary.json")
    
    terms = []
    metadata = {}
    
    if json_path.exists():
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                terms = data.get('terms', [])
                metadata = data.get('metadata', {})
                
            logger.info(f"Loaded {len(terms)} terms from JSON")
            return terms, metadata
        except Exception as e:
            logger.error(f"Failed to load JSON: {e}")
    else:
        logger.error("No JSON file found. Please run convert.py first.")
    
    return None, {}


def search_terms(
    terms: List[Dict],
    query: str,
    mode: str = "fuzzy",
    lang: str = "both",
    limit: int = 10,
    min_score: float = 60.0
) -> List[Tuple[Dict, Optional[float]]]:
    """
    TR: Farklı modlarla terim araması yapar.
    EN: Search terms with different modes.
    
    Args:
        terms: TR: Terim listesi / EN: List of terms
        query: TR: Arama sorgusu / EN: Search query
        mode: TR: Arama modu (fuzzy/exact/partial) / EN: Search mode
        lang: TR: Arama dili (both/en/tr) / EN: Search language
        limit: TR: Maksimum sonuç sayısı / EN: Maximum result count
        min_score: TR: Minimum benzerlik skoru / EN: Minimum similarity score
        
    Returns:
        TR: Terim ve skor çiftlerinin listesi
        EN: List of term and score pairs
    """
    if not query:
        return []
    
    results = []
    query_lower = query.lower()
    
    if mode == "exact":
        for term in terms:
            if lang in ["en", "both"] and term["en"].lower() == query_lower:
                results.append((term, 100.0))
            elif lang in ["tr", "both"] and term["tr"].lower() == query_lower:
                results.append((term, 100.0))
            
            if len(results) >= limit:
                break
    
    elif mode == "partial":
        for term in terms:
            if lang in ["en", "both"] and query_lower in term["en"].lower():
                results.append((term, None))
            elif lang in ["tr", "both"] and query_lower in term["tr"].lower():
                results.append((term, None))
            
            if len(results) >= limit:
                break
    
    elif mode == "fuzzy":
        candidates = []
        
        if lang in ["en", "both"]:
            en_terms = [(term["en"], term) for term in terms]
            en_matches = process.extract(  # type: ignore
                query,
                [t[0] for t in en_terms],
                scorer=fuzz.WRatio,
                limit=limit if lang == "en" else limit // 2
            )
            for match_text, score, idx in en_matches:
                if score >= min_score:
                    candidates.append((en_terms[idx][1], score))
        
        if lang in ["tr", "both"]:
            tr_terms = [(term["tr"], term) for term in terms]
            tr_matches = process.extract(  # type: ignore
                query,
                [t[0] for t in tr_terms],
                scorer=fuzz.WRatio,
                limit=limit if lang == "tr" else limit // 2
            )
            for match_text, score, idx in tr_matches:
                if score >= min_score:
                    candidates.append((tr_terms[idx][1], score))
        
        # Sort by score and remove duplicates
        seen = set()
        for term, score in sorted(candidates, key=lambda x: x[1], reverse=True):
            term_key = (term["en"], term["tr"])
            if term_key not in seen:
                seen.add(term_key)
                results.append((term, score))
                if len(results) >= limit:
                    break
    
    return results


def main():
    """
    TR: Ana Streamlit uygulaması.
    EN: Main Streamlit application.
    """
    
    # Load database
    terms, metadata = load_database()
    
    if not terms:
        st.error(":x: Veritabanı bulunamadı! Lütfen önce `python convert.py` komutunu çalıştırın.")
        st.stop()
    
    # Header
    st.title(":books: TBD Bilişim Terimleri Sözlüğü")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header(":gear: Ayarlar")
        
        # Statistics
        st.subheader(":bar_chart: İstatistikler")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Toplam Terim", f"{len(terms):,}")
        with col2:
            st.metric("Versiyon", metadata.get('version', 'N/A'))
        
        st.divider()
        
        # Search settings
        st.subheader(":mag: Arama Ayarları")
        
        search_mode = st.selectbox(
            "Arama Modu",
            ["fuzzy", "exact", "partial"],
            format_func=lambda x: {
                "fuzzy": "Yaklaşık Eşleşme (Fuzzy)",
                "exact": "Tam Eşleşme",
                "partial": "Kısmi Eşleşme"
            }[x]
        )
        
        search_lang = st.selectbox(
            "Arama Dili",
            ["both", "en", "tr"],
            format_func=lambda x: {
                "both": "Her İki Dil",
                "en": "İngilizce (EN)",
                "tr": "Türkçe (TR)"
            }[x]
        )
        
        if search_mode == "fuzzy":
            min_score = st.slider(
                "Minimum Eşleşme Skoru",
                min_value=0,
                max_value=100,
                value=60,
                step=5,
                help="Fuzzy aramada minimum benzerlik skoru"
            )
        else:
            min_score = 60
        
        max_results = st.slider(
            "Maksimum Sonuç",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        )
        
        st.divider()
        
        # Random term
        st.subheader(":game_die: Rastgele Terim")
        if st.button("Rastgele Terim Getir", use_container_width=True):
            random_term = random.choice(terms)
            st.session_state.random_term = random_term
        
        if 'random_term' in st.session_state:
            term = st.session_state.random_term
            with st.container():
                st.info(f"**{term['en']}**")
                st.info(f"**{term['tr']}**")
        
        st.divider()
        
        # Export options
        st.subheader(":floppy_disk: Dışa Aktarım")
        
        export_format = st.selectbox(
            "Format",
            ["JSON", "CSV", "TXT"]
        )
        
        if st.button("Sonuçları İndir", use_container_width=True):
            if 'search_results' in st.session_state and st.session_state.search_results:
                results = st.session_state.search_results
                
                if export_format == "JSON":
                    json_str = json.dumps(
                        [{"en": r[0]["en"], "tr": r[0]["tr"]} for r in results],
                        ensure_ascii=False,
                        indent=2
                    )
                    st.download_button(
                        label=":arrow_down: JSON İndir",
                        data=json_str,
                        file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
                elif export_format == "CSV":
                    csv_str = "English,Turkish\n"
                    for r in results:
                        csv_str += f'"{r[0]["en"]}","{r[0]["tr"]}"\n'
                    st.download_button(
                        label=":arrow_down: CSV İndir",
                        data=csv_str,
                        file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                elif export_format == "TXT":
                    txt_str = ""
                    for r in results:
                        txt_str += f"{r[0]['en']} -> {r[0]['tr']}\n"
                    st.download_button(
                        label=":arrow_down: TXT İndir",
                        data=txt_str,
                        file_name=f"search_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            else:
                st.warning("İndirilecek sonuç yok!")
    
    # Main content
    col1, col2, col3 = st.columns([1, 6, 1])
    
    with col2:
        # Search box
        search_query = st.text_input(
            "Arama",
            placeholder="Terim ara... (örn: cloud, database, yapay zeka)",
            key="search_input",
            label_visibility="collapsed"
        )
        
        # Search button
        if search_query:
            with st.spinner("Aranıyor..."):
                results = search_terms(
                    terms,
                    search_query,
                    mode=search_mode,
                    lang=search_lang,
                    limit=max_results,
                    min_score=min_score
                )
                
                st.session_state.search_results = results
                
                if results:
                    st.success(f":white_check_mark: {len(results)} sonuç bulundu")
                    
                    st.divider()
                    
                    # Display results
                    for i, (term, score) in enumerate(results, 1):
                        with st.container():
                            col_num, col_en, col_tr, col_score, col_copy = st.columns([0.5, 3, 3, 1, 0.5])
                            
                            with col_num:
                                st.write(f"**{i}.**")
                            
                            with col_en:
                                st.write(f"**{term['en']}**")
                            
                            with col_tr:
                                st.write(f"→ {term['tr']}")
                            
                            with col_score:
                                if score:
                                    st.caption(f"Skor: %{score:.0f}")
                            
                            with col_copy:
                                if st.button(":clipboard:", key=f"copy_{i}", help="Kopyala"):
                                    st.toast(f"Kopyalandı: {term['en']} -> {term['tr']}")
                            
                            st.divider()
                    
                else:
                    st.warning(":warning: Sonuç bulunamadı. Farklı bir terim deneyin.")
        else:
            # Welcome message when no search
            st.info(
                """
                :wave: **Hoş Geldiniz!**
                
                **Türkiye Bilişim Derneği (TBD)**  
                **Bilişimde Özenli Türkçe Çalışma Grubu**
                
                **Hazırlayanlar:**  
                • Emeritüs Prof. Dr. Tuncer Ören  
                • Ahmet Pekel  
                • Koray Özer  
                • İ. İlker Tabak  
                • Eymen Y. Görgülü
                
                **Bilgiağı:** Mehmet Pektaş  
                **Güncelleme:** 2025-08-04 (yyyy-aa-gg)
                
                **Nasıl kullanılır:**
                - Yukarıdaki arama kutusuna İngilizce veya Türkçe terim girin
                - Sol menüden arama modunu seçin
                - Rastgele terim özelliğini keşfedin
                
                **Örnekler:** cloud, database, artificial intelligence, yapay zeka, bulut, veri
                """
            )
            
            # Show some sample terms
            st.subheader(":pushpin: Örnek Terimler")
            sample_terms = random.sample(terms, min(5, len(terms)))
            
            for term in sample_terms:
                with st.container():
                    col_en, col_tr = st.columns(2)
                    with col_en:
                        st.write(f"**{term['en']}**")
                    with col_tr:
                        st.write(f"→ {term['tr']}")
                    st.divider()
    
    # Footer
    st.divider()
    with st.container():
        st.caption(
            "Copyright (c) 2025 Rıza Emre ARAS"
        )


if __name__ == "__main__":
    main()