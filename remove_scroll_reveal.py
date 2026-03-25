import os
import glob

files = ['blog.html', 'contacto.html', 'sobre-mi.html'] + glob.glob('articulos/*.html')

css_addition = """
  /* Scroll Reveal Styles */
  .reveal {
    opacity: 0;
    transform: translateY(30px);
    transition: all 0.8s cubic-bezier(0.5, 0, 0, 1);
  }
  .reveal.active {
    opacity: 1;
    transform: translateY(0);
  }
"""

js_addition = """
<script>
  // Scroll Reveal functionality
  document.addEventListener("DOMContentLoaded", () => {
    // Add reveal class dynamically to elements we want to animate
    const elementsToAnimate = document.querySelectorAll(
      ".blog-card, .section-title, .container p, .container h2, .container h3, .container img, .container ul, footer"
    );
    
    elementsToAnimate.forEach(el => el.classList.add("reveal"));

    const revealOnScroll = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("active");
          observer.unobserve(entry.target); // Optional: only animate once
        }
      });
    }, {
      root: null,
      rootMargin: "0px",
      threshold: 0.1 
    });

    const reveals = document.querySelectorAll(".reveal");
    reveals.forEach(reveal => {
      revealOnScroll.observe(reveal);
    });
  });
</script>
"""

for filepath in files:
    if not os.path.exists(filepath):
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove CSS
    content = content.replace(css_addition, '')
                         
    # Remove JS
    content = content.replace(js_addition + '\n', '')
    content = content.replace(js_addition, '') # fallback
         
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Reverted {filepath}")
