import os
import glob
import re

files = glob.glob('*.html') + glob.glob('articulos/*.html') + glob.glob('en/*.html') + glob.glob('en/articulos/*.html')

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'(<div class="nav-actions"[^>]*>.*?)(<a [^>]*href="[^"]*CV[^"]*"[^>]*>.*?</a>)\s*</div>', content, re.DOTALL | re.IGNORECASE)
    if match:
        before_button = match.group(1)
        button_html = match.group(2)
        
        # Construct the new HTML by closing the nav-actions div early, then appending the button
        new_chunk = before_button.rstrip() + '\n    </div>\n    ' + button_html
        
        full_match = match.group(0)
        content = content.replace(full_match, new_chunk)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Extracted button in", filepath)
    else:
        print("Regex did not match in", filepath)
