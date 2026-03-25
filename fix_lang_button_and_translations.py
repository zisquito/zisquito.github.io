import os
import glob
import re

files_es = ['blog.html', 'contacto.html', 'sobre-mi.html'] + glob.glob('articulos/*.html')
files_en = ['en/blog.html', 'en/contacto.html', 'en/sobre-mi.html'] + glob.glob('en/articulos/*.html')

# 1. Fix ES files (Language Toggle)
for filepath in files_es:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    en_path = "/en/" + filepath.replace("\\", "/").replace(".html", "")
    if en_path == "/en/index": en_path = "/en/sobre-mi"
        
    lang_toggle_html = f'<div id="langToggle" style="font-weight: 800; margin-right: 20px; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; cursor: default;"><span>ES</span> <span style="color: var(--text-gray); font-weight: 400;">|</span> <a href="{en_path}" style="color: var(--text-gray); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color=\'var(--primary-blue)\'" onmouseout="this.style.color=\'var(--text-gray)\'">EN</a></div>'
    
    content = re.sub(r'<button id="langToggle".*?</button>', lang_toggle_html, content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# 2. Fix EN files (Language Toggle + Missing Translations)
for filepath in files_en:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    es_path = "/" + filepath.replace("en/", "", 1).replace("en\\\\", "", 1).replace("\\", "/").replace(".html", "")
    if es_path == "/index": es_path = "/sobre-mi"
    
    lang_toggle_html = f'<div id="langToggle" style="font-weight: 800; margin-right: 20px; font-size: 0.95rem; display: flex; align-items: center; gap: 8px; cursor: default;"><a href="{es_path}" style="color: var(--text-gray); text-decoration: none; transition: 0.3s;" onmouseover="this.style.color=\'var(--primary-blue)\'" onmouseout="this.style.color=\'var(--text-gray)\'">ES</a> <span style="color: var(--text-gray); font-weight: 400;">|</span> <span>EN</span></div>'
    
    content = re.sub(r'<button id="langToggle".*?</button>', lang_toggle_html, content)
    
    # Missing translations (due to spaces)
    content = content.replace('> Contáctame<', '> Contact me<')
    content = content.replace('> Descargar CV<', '> Download CV<')
    content = content.replace(' Descargar CV</a>', ' Download CV</a>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("All files updated with ES | EN toggle and fixed translations.")
