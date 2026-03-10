import os, re

def update_file(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if not content.strip():
        print(f"File is empty: {filepath}")
        return

    # SEO metadata replacements (Name)
    content = content.replace('content="Francisco Robles"', 'content="Francisco Andrés Robles Muñoz"')
    content = content.replace('>Francisco Robles |', '>Francisco Andrés Robles Muñoz |')
    content = content.replace('© 2026 Francisco Robles', '© 2026 Francisco Andrés Robles Muñoz')
    content = content.replace('© 2026 Francisco Andrés Robles Muñoz', '© 2026 Francisco Robles') # Revert footer to Francisco Robles, user requested!
    # Ensure visual name is Francisco Robles
    content = content.replace('<div class="brand">Francisco Andrés Robles Muñoz', '<div class="brand">Francisco Robles')

    # Specific modifications for blog.html
    if 'blog.html' in filepath:
        # Remove all article/project badges
        content = re.sub(r'\s*<span class="card-badge[^>]+>.*?</span>', '', content)
        
        # Replace the cro_checkout.webp image block with cro.webp
        old_picture_block = r'''          <picture>
            <source srcset="img/blog/cro_checkout.webp" type="image/webp">
            <img src="img/blog/cro_checkout.webp" alt="Portada del artículo sobre CRO y Checkout" class="blog-card-img" width="800" height="500" loading="lazy" decoding="async">
          </picture>'''
        
        new_picture_block = '''          <picture>
            <source srcset="img/blog/cro.webp" type="image/webp">
            <img src="img/blog/cro.webp" alt="Portada del artículo sobre CRO" class="blog-card-img" width="800" height="500" loading="lazy" decoding="async">
          </picture>'''
          
        content = content.replace(old_picture_block, new_picture_block)
        
        # Change the title
        content = content.replace('<h3>El dilema del Checkout: El coste oculto de la fricción</h3>', '<h3>El dilema del Checkout y el coste oculto de la fricción</h3>')

    # Specific specific modifications for auditoria seo title
    if 'auditoria-seo.html' in filepath or 'index.html' in filepath or 'blog.html' in filepath:
        content = content.replace('Auditoría SEO de mi web: los errores que encontré y cómo los solucioné', 'Auditoría SEO de mi web: los errores que encontré')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Successfully processed {filepath}")

update_file('index.html')
update_file('blog.html')
update_file('articulos/auditoria-seo.html')
