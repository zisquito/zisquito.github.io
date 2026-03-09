import codecs, re

# General fixes for Francisco Andres Robles Muñoz
files = ['index.html', 'blog.html', 'articulos/auditoria-seo.html']
for f in files:
    text = codecs.open(f, 'r', 'utf-8').read()
    text = text.replace('"Francisco Robles"', '"Francisco Andrés Robles Muñoz"')
    text = text.replace('>Francisco Robles |', '>Francisco Andrés Robles Muñoz |')
    text = text.replace('content="Francisco Robles"', 'content="Francisco Andrés Robles Muñoz"')
    text = text.replace('<div class="brand">Francisco Andrés Robles Muñoz', '<div class="brand">Francisco Robles')
    text = text.replace('© 2026 Francisco Andrés Robles Muñoz', '© 2026 Francisco Robles')
    codecs.open(f, 'w', 'utf-8').write(text)

# Specific fixes for blog.html
f = 'blog.html'
text = codecs.open(f, 'r', 'utf-8').read()

# Remove badges
text = re.sub(r'\s*<span class="card-badge[^>]+>.*?</span>', '', text)

# Insert the new article card
new_card = """
      <a href="/articulos/el-dilema-del-checkout" style="text-decoration: none; color: inherit; display: block;">
        <div class="blog-card">
          <picture>
            <source srcset="img/blog/cro.webp" type="image/webp">
            <img src="img/blog/cro.webp" alt="Portada del artículo sobre CRO" class="blog-card-img" width="800" height="500" loading="lazy" decoding="async">
          </picture>
          <h3>El dilema del Checkout y el coste oculto de la fricción</h3>
          <p>Marzo 2026</p>
          <div class="card-line"></div>
        </div>
      </a>
"""
text = text.replace('<div class="blog-grid-full">', '<div class="blog-grid-full">' + new_card)
codecs.open(f, 'w', 'utf-8').write(text)

# Specific fixes for auditoria-seo.html
for f in ['articulos/auditoria-seo.html', 'index.html']:
    text = codecs.open(f, 'r', 'utf-8').read()
    text = text.replace('Auditoría SEO de mi web: los errores que encontré y cómo los solucioné', 'Auditoría SEO de mi web: los errores que encontré')
    codecs.open(f, 'w', 'utf-8').write(text)

print("Files successfully repaired.")
