import os
import glob
import re

files = ['blog.html', 'contacto.html', 'sobre-mi.html'] + glob.glob('articulos/*.html')

css_addition = """
  /* Dark Mode Styles */
  body.dark-mode {
    --bg-light: #111827;
    --text-dark: #f3f4f6;
    --white: #1f2937;
    --text-gray: #9ca3af;
    background-image: radial-gradient(#374151 1px, transparent 1px);
  }
  body.dark-mode .blog-img-placeholder {
    background: #374151;
    color: #4b5563;
  }
  body.dark-mode nav {
    box-shadow: 0 2px 10px rgba(255,255,255,0.05);
  }
  /* Optional generic card borders in dark mode for more contrast */
  body.dark-mode .blog-card {
    border: 1px solid #374151;
  }
"""

js_addition = """
<script>
  // Dark mode functionality
  document.addEventListener("DOMContentLoaded", () => {
    const darkModeToggle = document.getElementById("darkModeToggle");
    const body = document.body;
    const icon = darkModeToggle ? darkModeToggle.querySelector("i") : null;
    
    // Check saved preference
    const isDarkMode = localStorage.getItem("darkMode") === "true";
    if (isDarkMode) {
      body.classList.add("dark-mode");
      if(icon) {
          icon.classList.remove("fa-moon");
          icon.classList.add("fa-sun");
      }
    }
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener("click", () => {
          body.classList.toggle("dark-mode");
          const isDarkNow = body.classList.contains("dark-mode");
          localStorage.setItem("darkMode", isDarkNow);
          
          if(icon) {
              if (isDarkNow) {
                icon.classList.remove("fa-moon");
                icon.classList.add("fa-sun");
              } else {
                icon.classList.remove("fa-sun");
                icon.classList.add("fa-moon");
              }
          }
        });
    }
  });
</script>
"""

for filepath in files:
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Add CSS before </style>
    if 'body.dark-mode' not in content:
        content = content.replace('</style>', f'{css_addition}</style>')
        
    # 2. Add Button before CV button
    if 'id="darkModeToggle"' not in content:
        content = re.sub(
            r'(<a href="[^"]*CV_[^"]*"\s*class="btn-primary[^>]*>)', 
            r'<button id="darkModeToggle" aria-label="Cambiar modo oscuro" style="background: none; border: none; font-size: 1.3rem; cursor: pointer; color: var(--text-dark); margin-right: 15px; display: flex; align-items: center; justify-content: center; width: 40px; height: 40px; border-radius: 50%; transition: 0.3s;" onmouseover="this.style.background=\'rgba(128,128,128,0.1)\'" onmouseout="this.style.background=\'none\'"><i class="fa-solid fa-moon"></i></button>\n    \1', 
            content
        )
                         
    # 3. Add JS before </body>
    if '// Dark mode functionality' not in content:
         content = content.replace('</body>', f'{js_addition}\n</body>')
         
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {filepath}")
