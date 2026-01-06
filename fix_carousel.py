import os
import re
from pathlib import Path

# Docs klasörü
docs_dir = Path(__file__).parent / "docs"

# Güncellenecek pattern
old_pattern = r'''function updateCarousel\(\) \{
            if\(!track\) return;
            const card = track\.querySelector\('\.tr-card'\);
            if\(!card\) return;

            const cardWidth = card\.offsetWidth;
            const gap = 20; 
            const moveAmount = \(cardWidth \+ gap\) \* currentIndex;
            track\.style\.transform = `translateX\(-\$\{moveAmount\}px\)`;
            
            prevBtn\.disabled = currentIndex === 0;
            const cardsToShow = window\.innerWidth <= 768 \? 1 : 3;
            const totalCards = track\.children\.length;
            nextBtn\.disabled = currentIndex >= totalCards - cardsToShow;
        \}'''

# Yeni kod
new_code = '''function updateCarousel() {
            if(!track) return;
            const card = track.querySelector('.tr-card');
            if(!card) return;

            const cardsToShow = window.innerWidth <= 768 ? 1 : 3;
            const cardWidth = card.offsetWidth;
            const gap = 20; 
            const moveAmount = (cardWidth + gap) * currentIndex * cardsToShow;
            track.style.transform = `translateX(-${moveAmount}px)`;
            
            prevBtn.disabled = currentIndex === 0;
            const totalCards = track.children.length;
            const maxIndex = Math.ceil((totalCards - cardsToShow) / cardsToShow);
            nextBtn.disabled = currentIndex >= maxIndex;
        }'''

# Tüm HTML dosyalarını bul
html_files = list(docs_dir.glob("*.html"))
total_files = len(html_files)
updated_files = 0
failed_files = []

print(f"Toplam {total_files} HTML dosyası bulundu.\n")

for html_file in html_files:
    try:
        # Dosyayı oku
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Eski kodu bul ve değiştir - Pattern matching yerine string replacement kullanalım
        # Çünkü regex çok karmaşık olabilir
        
        # updateCarousel fonksiyonunu bulalım
        old_func_simple = """function updateCarousel() {
            if(!track) return;
            const card = track.querySelector('.tr-card');
            if(!card) return;

            const cardWidth = card.offsetWidth;
            const gap = 20; 
            const moveAmount = (cardWidth + gap) * currentIndex;
            track.style.transform = `translateX(-${moveAmount}px)`;
            
            prevBtn.disabled = currentIndex === 0;
            const cardsToShow = window.innerWidth <= 768 ? 1 : 3;
            const totalCards = track.children.length;
            nextBtn.disabled = currentIndex >= totalCards - cardsToShow;
        }"""
        
        if old_func_simple in content:
            # String replacement yap
            new_content = content.replace(old_func_simple, new_code)
            
            # Dosyayı yaz
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            updated_files += 1
            print(f"✓ {html_file.name} güncellendi")
        else:
            failed_files.append(html_file.name)
            print(f"✗ {html_file.name} - updateCarousel fonksiyonu bulunamadı veya farklı formatta")
    
    except Exception as e:
        failed_files.append(html_file.name)
        print(f"✗ {html_file.name} - Hata: {e}")

print(f"\n{'='*60}")
print(f"Özet:")
print(f"  • Toplam dosya: {total_files}")
print(f"  • Güncellenen: {updated_files}")
print(f"  • Başarısız: {len(failed_files)}")

if failed_files:
    print(f"\nBaşarısız dosyalar:")
    for f in failed_files:
        print(f"  - {f}")
