import urllib.request
import urllib.parse
import json
import os
import glob
import re
import time

def translate_bulk(texts):
    if not texts: return []
    chunk_size = 30
    translated_texts = []
    
    for i in range(0, len(texts), chunk_size):
        chunk = texts[i:i+chunk_size]
        delimiter = "\n||\n"
        joined_text = delimiter.join(chunk)
        
        url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=es&tl=en&dt=t&q=" + urllib.parse.quote(joined_text)
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            response = urllib.request.urlopen(req)
            result = json.loads(response.read().decode('utf-8'))
            translated_joined = "".join([item[0] for item in result[0] if item[0]])
            res_chunk = [t.strip() for t in translated_joined.split("||")]
            
            if len(res_chunk) < len(chunk):
                # if splitting failed perfectly, fallback to single translation for this chunk
                for single_text in chunk:
                    s_url = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=es&tl=en&dt=t&q=" + urllib.parse.quote(single_text)
                    s_req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0'})
                    s_res = urllib.request.urlopen(s_req)
                    s_result = json.loads(s_res.read().decode('utf-8'))
                    translated_texts.append("".join([item[0] for item in s_result[0] if item[0]]).strip())
                    time.sleep(0.2)
            else:
                translated_texts.extend(res_chunk[:len(chunk)])
        except Exception as e:
            print("Error translating chunk:", e)
            translated_texts.extend(chunk)
            
        time.sleep(1)
        
    return translated_texts

# Fix image paths
def fix_images(content):
    content = content.replace('src="../img/', 'src="/img/')
    content = content.replace('src="img/', 'src="/img/')
    content = content.replace('srcset="../img/', 'srcset="/img/')
    content = content.replace('srcset="img/', 'srcset="/img/')
    # fix href to pdf
    content = content.replace('href="../CV_', 'href="/CV_')
    content = content.replace('href="CV_', 'href="/CV_')
    return content

# 1. Fix images in main EN pages
for main_page in ['en/blog.html', 'en/sobre-mi.html', 'en/contacto.html']:
    if os.path.exists(main_page):
        with open(main_page, 'r', encoding='utf-8') as f:
            c = f.read()
        with open(main_page, 'w', encoding='utf-8') as f:
            f.write(fix_images(c))

common_map = {
    'lang="es"': 'lang="en"',
    'href="/sobre-mi"': 'href="/en/sobre-mi"',
    'href="/blog"': 'href="/en/blog"',
    'href="/contacto"': 'href="/en/contacto"',
    '>Sobre mí<': '>About me<',
    '>Contáctame<': '>Contact me<',
    '>Descargar CV<': '>Download CV<',
    'href="CV_FranciscoRobles.pdf"': 'href="/CV_FranciscoRobles.pdf"',  
    'id="langToggle" aria-label="Switch to English"': 'id="langToggle" aria-label="Switch to Spanish"',
    '>EN</button>': '>ES</button>',
    "onclick=\"window.location.href='/en/": "onclick=\"window.location.href='/",
    "onclick=\"window.location.href='/en'": "onclick=\"window.location.href='/'",
    'Cambiar modo oscuro': 'Toggle dark mode',
    'href="/articulos/': 'href="/en/articulos/',
}

# 2. Retranslate articles from SPANISH original files
files = glob.glob('articulos/*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for k, v in common_map.items():
        content = content.replace(k, v)
        
    content = fix_images(content)
        
    # Translate title tag
    title_match = re.search(r'<title>(.*?)</title>', content)
    if title_match:
        original_title = title_match.group(1)
        # short single request
        turl = "https://translate.googleapis.com/translate_a/single?client=gtx&sl=es&tl=en&dt=t&q=" + urllib.parse.quote(original_title)
        treq = urllib.request.Request(turl, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            tres = urllib.request.urlopen(treq)
            tresult = json.loads(tres.read().decode('utf-8'))
            translated_title = "".join([i[0] for i in tresult[0] if i[0]])
            content = content.replace(f'<title>{original_title}</title>', f'<title>{translated_title}</title>')
        except: pass

    main_match = re.search(r'<main.*?</main>', content, flags=re.DOTALL)
    if main_match:
        main_content = main_match.group(0)
        
        # Extract text nodes
        texts_to_translate = []
        matches = list(re.finditer(r'>([^<]+)<', main_content))
        
        for m in matches:
            text = m.group(1).strip()
            # Only translate substantial text
            if re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', text) and not text.startswith(('{', '(', 'function', 'var', 'let', 'const', 'import', '//')):
                texts_to_translate.append(text)
                
        # Deduplicate to save some API calls, preserving order
        unique_texts = list(dict.fromkeys(texts_to_translate))
        print(f"Translating {len(unique_texts)} unique strings for {filepath}...")
        
        translated_texts = translate_bulk(unique_texts)
        translations_dict = {orig: trans for orig, trans in zip(unique_texts, translated_texts)}
        
        def replace_text(m):
            original = m.group(1)
            striped = original.strip()
            if striped in translations_dict:
                # Replace just the stripped part inside the original whitespace to avoid breaking spacing
                return '>' + original.replace(striped, translations_dict[striped]) + '<'
            return m.group(0)

        new_main = re.sub(r'>([^<]+)<', replace_text, main_content)
        content = content.replace(main_content, new_main)
    
    out_path = os.path.join('en', filepath.replace('\\', '/'))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Translated and fixed {out_path}")
