import os
import glob
import re

files = glob.glob('*.html') + glob.glob('articulos/*.html') + glob.glob('en/*.html') + glob.glob('en/articulos/*.html')

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.search(r'(<div id="langToggle".*?</button>\s*<a[^>]*href="[^"]*CV[^"]*"[^>]*>.*?</a>)', content, re.DOTALL | re.IGNORECASE)
    if match:
        original_chunk = match.group(1)
        if 'nav-actions' not in original_chunk:
            # We wrap the elements. gap: 15px handles spacing nicely instead of margins.
            new_chunk = '<div class="nav-actions" style="display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 15px;">\n      ' + original_chunk + '\n    </div>'
            
            # Remove hardcoded margins so they don't break flex spacing
            new_chunk = new_chunk.replace('margin-right: 20px;', 'margin: 0;')
            new_chunk = new_chunk.replace('margin-right: 15px;', 'margin: 0;')
            
            content = content.replace(original_chunk, new_chunk)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print("Wrapped nav actions in", filepath)
    else:
        # Just to know if it failed silently anywhere
        print("Regex did not match in", filepath)
