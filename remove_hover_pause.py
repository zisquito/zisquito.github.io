import os

for file in ['sobre-mi.html', 'en/sobre-mi.html']:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove the hover pause rule
    old_css = """.logo-slide-track:hover {
      animation-play-state: paused;
  }"""
    
    # In some versions it might have different spacing, let's use replace or regex
    import re
    content = re.sub(r'\.logo-slide-track:hover\s*\{\s*animation-play-state:\s*paused;\s*\}', '', content)

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print("Removed hover pause")
