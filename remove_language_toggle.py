import os
import glob

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

js_addition = """<div id="google_translate_element" style="display:none;"></div>
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
<script src="//translate.google.com/translate_a/element.js?cb=googleTranslateElementInit"></script>"""

button_html = '<button id="langToggle" aria-label="Switch to English" style="background: none; border: none; font-size: 1rem; font-weight: 700; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\'rgba(128,128,128,0.1)\'" onmouseout="this.style.background=\'none\'">EN</button>\n    '

for filepath in files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = content.replace(css_addition, "")
    content = content.replace(js_addition + "\n", "")
    content = content.replace(js_addition, "")
    content = content.replace(button_html, "")
         
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Reverted {filepath}")
