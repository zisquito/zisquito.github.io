import os
import glob
import re

files = ['blog.html', 'contacto.html', 'sobre-mi.html'] + glob.glob('articulos/*.html')

css_addition = """
  /* Hide Google Translate top bar */
  .goog-te-banner-frame.skiptranslate { display: none !important; }
  body { top: 0px !important; }
  #goog-gt-tt { display: none !important; }
  .goog-tooltip { display: none !important; }
  .goog-tooltip:hover { display: none !important; }
  .goog-text-highlight { background-color: transparent !important; border: none !important; box-shadow: none !important; }
"""

js_addition = """
<div id="google_translate_element" style="display:none;"></div>
<script>
  // Language Toggle Functionality
  document.addEventListener("DOMContentLoaded", () => {
    const langToggle = document.getElementById("langToggle");
    
    const isEnglish = document.cookie.includes("googtrans=/es/en");
    
    if (langToggle) {
        if (isEnglish) {
            langToggle.textContent = "ES";
            langToggle.setAttribute("aria-label", "Cambiar a Español");
        } else {
            langToggle.textContent = "EN";
            langToggle.setAttribute("aria-label", "Switch to English");
        }
    
        langToggle.addEventListener("click", () => {
            if (isEnglish) {
                document.cookie = "googtrans=/es/es; path=/;";
                if (window.location.hostname !== "") {
                    document.cookie = "googtrans=/es/es; path=/; domain=" + window.location.hostname;
                }
                location.reload();
            } else {
                document.cookie = "googtrans=/es/en; path=/;";
                if (window.location.hostname !== "") {
                    document.cookie = "googtrans=/es/en; path=/; domain=" + window.location.hostname;
                }
                location.reload();
            }
        });
    }
  });

  function googleTranslateElementInit() {
    new google.translate.TranslateElement({pageLanguage: 'es', includedLanguages: 'en,es', autoDisplay: false}, 'google_translate_element');
  }
</script>
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>
"""

button_html = r'<button id="langToggle" aria-label="Switch to English" style="background: none; border: none; font-size: 1rem; font-weight: 700; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\'rgba(128,128,128,0.1)\'" onmouseout="this.style.background=\'none\'">EN</button>'

for filepath in files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    already_done = False
                     
    # 1. Add CSS before </style>
    if '.goog-te-banner-frame' not in content:
        content = content.replace('</style>', f'{css_addition}</style>')
    else:
        already_done = True
        
    # 2. Add Button before darkModeToggle
    if 'id="langToggle"' not in content:
        content = re.sub(
            r'(<button id="darkModeToggle")', 
            f'{button_html}\n    \\1', 
            content
        )
                         
    # 3. Add JS before </body>
    if 'google_translate_element' not in content:
         content = content.replace('</body>', f'{js_addition}\n</body>')
         
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    if already_done: print(f"Already injected {filepath}")
    else: print(f"Updated {filepath}")
