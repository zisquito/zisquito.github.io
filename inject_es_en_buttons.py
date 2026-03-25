import os
import glob
import re

files = ['blog.html', 'contacto.html', 'sobre-mi.html'] + glob.glob('articulos/*.html')

for filepath in files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Determine the english URL equivalent
    # filepath is e.g. "blog.html" or "articulos\auditoria-seo.html"
    en_path = "/en/" + filepath.replace("\\", "/").replace(".html", "")
         
    button_html = f'<button id="langToggle" aria-label="Switch to English" onclick="window.location.href=\'{en_path}\';" style="background: none; border: none; font-size: 1rem; font-weight: 700; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\\\'rgba(128,128,128,0.1)\\\' " onmouseout="this.style.background=\\\'none\\\' ">EN</button>'
    
    # We replaced it previously, ensure it's removed just in case
    # Then add it right before darkModeToggle
    if 'id="langToggle"' not in content:
        # replace double quotes from style for regex safety by doing standard injection
        content = content.replace('<button id="darkModeToggle"', 
            f'<button id="langToggle" aria-label="Switch to English" onclick="window.location.href=\'{en_path}\';" style="background: none; border: none; font-size: 1rem; font-weight: 700; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\'rgba(128,128,128,0.1)\'" onmouseout="this.style.background=\'none\'">EN</button>\n    <button id="darkModeToggle"')
         
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath} with EN button pointing to {en_path}")
