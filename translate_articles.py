import urllib.request
import urllib.parse
import json
import os
import glob
import re
import time

def translate_bulk(texts):
    if not texts: return []
    # Split into chunks of 20 to avoid URL length limits
    chunk_size = 20
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
            # Split and clean
            res_chunk = [t.strip() for t in translated_joined.split("||")]
            # Fallback if split mismatch
            if len(res_chunk) != len(chunk):
                print(f"Warning: Chunk size mismatch, got {len(res_chunk)} expected {len(chunk)}. Returning original to be safe.")
                translated_texts.extend(chunk)
            else:
                translated_texts.extend(res_chunk)
        except Exception as e:
            print("Error translating chunk:", e)
            translated_texts.extend(chunk)
            
        time.sleep(1) # rate limit protection
        
    return translated_texts

common_map = {
    'lang="es"': 'lang="en"',
    'href="/sobre-mi"': 'href="/en/sobre-mi"',
    'href="/blog"': 'href="/en/blog"',
    'href="/contacto"': 'href="/en/contacto"',
    '>Sobre mí<': '>About me<',
    '>Contáctame<': '>Contact me<',
    '>Descargar CV<': '>Download CV<',
    'href="CV_FranciscoRobles.pdf"': 'href="/CV_FranciscoRobles.pdf"',  # fix path to root
    'id="langToggle" aria-label="Switch to English"': 'id="langToggle" aria-label="Switch to Spanish"',
    '>EN</button>': '>ES</button>',
    "onclick=\"window.location.href='/en/": "onclick=\"window.location.href='/",
    "onclick=\"window.location.href='/en'": "onclick=\"window.location.href='/'",
    'Cambiar modo oscuro': 'Toggle dark mode',
    'href="/articulos/': 'href="/en/articulos/',
}

files = glob.glob('articulos/*.html')

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for k, v in common_map.items():
        content = content.replace(k, v)
        
    main_match = re.search(r'<main.*?</main>', content, flags=re.DOTALL)
    if main_match:
        main_content = main_match.group(0)
        
        # Extract text nodes
        texts_to_translate = []
        matches = list(re.finditer(r'>([^<]+)<', main_content))
        
        for m in matches:
            text = m.group(1).strip()
            # Only translate substantial text, skip scripts/css formatting
            if re.search(r'[a-zA-ZáéíóúÁÉÍÓÚñÑ]', text) and not text.startswith(('{', '(', 'function', 'var', 'let', 'const', 'import')):
                texts_to_translate.append(text)
                
        print(f"Translating {len(texts_to_translate)} strings for {filepath}...")
        translated_texts = translate_bulk(texts_to_translate)
        
        # Replace in main_content
        new_main = main_content
        for idx, text in enumerate(texts_to_translate):
            if idx < len(translated_texts):
                # We need to replace exactly the full >text< block since multiple same strings might exist
                # But to avoid replacing parts of other words, we replace in the context of the > <
                # Escape for regex replace is risky, so we use string replace
                new_main = new_main.replace('>' + text + '<', '>' + translated_texts[idx] + '<', 1)
                new_main = new_main.replace('> ' + text + ' <', '> ' + translated_texts[idx] + ' <', 1)
                new_main = new_main.replace('>\n' + text + '\n<', '>\n' + translated_texts[idx] + '\n<', 1)

        content = content.replace(main_content, new_main)
    
    out_path = os.path.join('en', filepath.replace('\\', '/'))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Translated to {out_path}")
