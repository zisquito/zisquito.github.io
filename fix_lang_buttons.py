import os
import glob
import re

files_es = ['blog.html', 'contacto.html', 'sobre-mi.html'] + glob.glob('articulos/*.html')
files_en = ['en/blog.html', 'en/contacto.html', 'en/sobre-mi.html'] + glob.glob('en/articulos/*.html')

# Fix ES files
for filepath in files_es:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    en_path = "/en/" + filepath.replace("\\", "/").replace(".html", "")
        
    button_html = f'<button id="langToggle" aria-label="Switch to English" onclick="window.location.href=\'{en_path}\';" style="background: none; border: none; font-size: 1rem; font-weight: 700; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\'rgba(128,128,128,0.1)\'" onmouseout="this.style.background=\'none\'">EN</button>'
    
    content = re.sub(r'<button id="langToggle".*?</button>', button_html, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed", filepath)

# Fix EN files
for filepath in files_en:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    es_path = "/" + filepath.replace("en/", "", 1).replace("en\\\\", "", 1).replace("\\", "/").replace(".html", "")
    
    button_html = f'<button id="langToggle" aria-label="Cambiar a Español" onclick="window.location.href=\'{es_path}\';" style="background: none; border: none; font-size: 1rem; font-weight: 700; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\'rgba(128,128,128,0.1)\'" onmouseout="this.style.background=\'none\'">ES</button>'
    
    content = re.sub(r'<button id="langToggle".*?</button>', button_html, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed", filepath)
