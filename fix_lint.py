import os
import glob

files = glob.glob('*.html') + glob.glob('articulos/*.html') + glob.glob('en/*.html') + glob.glob('en/articulos/*.html')

for filepath in files:
    if not os.path.exists(filepath): continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace("this.style.background=\\'rgba(128,128,128,0.1)\\'", "this.style.background='rgba(128,128,128,0.1)'")
    content = content.replace("this.style.background=\\'none\\'", "this.style.background='none'")
             
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
print("Fixed lints")
