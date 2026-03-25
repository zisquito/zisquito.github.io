import os
import re

os.makedirs('en', exist_ok=True)
os.makedirs(os.path.join('en', 'articulos'), exist_ok=True)

common_map = {
    'lang="es"': 'lang="en"',
    'href="/sobre-mi"': 'href="/en/sobre-mi"',
    'href="/blog"': 'href="/en/blog"',
    'href="/contacto"': 'href="/en/contacto"',
    '>Sobre mí<': '>About me<',
    '>Contáctame<': '>Contact me<',
    '>Descargar CV<': '>Download CV<',
    'href="CV_FranciscoRobles.pdf"': 'href="/CV_FranciscoRobles.pdf"',  # fix path to root
    'id="langToggle" aria-label="Switch to English"': 'id="langToggle" aria-label="Switch to Spanish"',
    '>EN</button>': '>ES</button>',
    "onclick=\"window.location.href='/en/": "onclick=\"window.location.href='/",
    "onclick=\"window.location.href='/en'": "onclick=\"window.location.href='/'",
    'Cambiar modo oscuro': 'Toggle dark mode',
    ' placeholder="Tu nombre"': ' placeholder="Your name"',
    ' placeholder="Tu email"': ' placeholder="Your email"',
    ' placeholder="Tu mensaje"': ' placeholder="Your message"',
    ' placeholder="¿En qué te puedo ayudar?"': ' placeholder="How can I help you?"',
    '>Enviar mensaje<': '>Send message<',
    '>Enviar mensaje <i': '>Send message <i',
    '>5 Herramientas de Analítica Fundamentales<': '>5 Fundamental Analytics Tools<',
    '>Febrero 2026<': '>February 2026<',
    '>Proyecto Unibite: Idea de negocio en la facultad<': '>Unibite Project: Business idea at university<',
    '>Marzo 2026<': '>March 2026<',
    '>El dilema del Checkout y el coste oculto de la fricción<': '>The Checkout Dilemma and the hidden cost of friction<',
    '>Auditoría SEO de mi web: los errores que encontré<': '>SEO Audit of my website: the errors I found<',
    '>De la gestión manual a la IA: Mi transición a Antigravity y MCP<': '>From manual management to AI: My transition to Antigravity and MCP<',
    '>Optimización SEO básica para WordPress: Por dónde empezar<': '>Basic SEO optimization for WordPress: Where to start<',
    '>Qué es el CRO y por qué lo necesitas<': '>What is CRO and why do you need it<',
    'href="/articulos/': 'href="/en/articulos/',
}

sobre_mi_map = {
    'content="Soy Francisco Andrés Robles Muñoz, graduado en Marketing e Investigación de Mercados (UMA). Especializado en analítica digital, CRO y marketing online. Siempre aprendiendo."': 'content="I am Francisco Andrés Robles Muñoz, a graduate in Marketing and Market Research (UMA). Specialized in digital analytics, CRO, and online marketing. Always learning."',
    'Portfolio y blog de Francisco Andrés Robles Muñoz sobre marketing digital, analítica y CRO.': 'Portfolio and blog of Francisco Andrés Robles Muñoz on digital marketing, analytics, and CRO.',
    '>Hola, soy Francisco 👋<': '>Hi, I am Francisco 👋<',
    '>Graduado en <strong>Marketing e Investigación de Mercados</strong> (UMA).<': '>Graduate in <strong>Marketing and Market Research</strong> (UMA).<',
    '>Me interesan la <strong>analítica digital</strong>, el <strong>CRO</strong> y el <strong>marketing online</strong>.<': '>Interested in <strong>digital analytics</strong>, <strong>CRO</strong>, and <strong>online marketing</strong>.<',
    '>Siempre aprendiendo y buscando nuevos retos.<': '>Always learning and looking for new challenges.<',
    '> <strong>Curioso</strong> por naturaleza.<': '><strong>Curious</strong> by nature.<',
    '>Blog<': '>Blog<',
    '>Ver todos &rarr;<': '>View all &rarr;<',
}

blog_map = {
    'content="Artículos y proyectos de Francisco Andrés Robles Muñoz sobre marketing digital, SEO, analítica web, CRO y experiencias en la universidad."': 'content="Articles and projects by Francisco Andrés Robles Muñoz on digital marketing, SEO, web analytics, CRO, and university experiences."',
    '>Blog y Proyectos | Francisco Andrés Robles Muñoz<': '>Blog and Projects | Francisco Andrés Robles Muñoz<',
    'Artículos y proyectos de Francisco Andrés Robles Muñoz sobre marketing digital, SEO, analítica web y CRO.': 'Articles and projects by Francisco Andrés Robles Muñoz on digital marketing, SEO, web analytics and CRO.',
    '>Mis Artículos y Proyectos<': '>My Articles and Projects<',
    'Inicio': 'Home',
}

contacto_map = {
    'content="Contacta con Francisco Andrés Robles Muñoz para oportunidades laborales en marketing digital, analítica web o colaboraciones. Envía tu mensaje directamente."': 'content="Contact Francisco Andrés Robles Muñoz for job opportunities in digital marketing, web analytics or collaborations. Send your message directly."',
    '>Contáctame | Francisco Andrés Robles Muñoz<': '>Contact me | Francisco Andrés Robles Muñoz<',
    'Contacta con Francisco Andrés Robles Muñoz para oportunidades laborales en marketing digital, analítica web o colaboraciones.': 'Contact Francisco Andrés Robles Muñoz for job opportunities in digital marketing, web analytics or collaborations.',
    '>¿Buscas talento para tu equipo?<': '>Looking for talent for your team?<',
    '>Datos de contacto<': '>Contact details<',
    'Página de contacto de Francisco Andrés Robles Muñoz.': 'Contact page for Francisco Andrés Robles Muñoz.',
    'Contacto': 'Contact',
    'Inicio': 'Home',
}

def translate_file(filepath, specific_map):
    if not os.path.exists(filepath):
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for k, v in common_map.items():
        content = content.replace(k, v)
        
    for k, v in specific_map.items():
        content = content.replace(k, v)
        
    # fix langToggle onclick to go back to root spanish
    # e.g. onclick="window.location.href='/en/blog';" inside english pages should point to "/blog"
    # Wait, the common map did this: "onclick=\"window.location.href='/en/": "onclick=\"window.location.href='/"
    # It replaced `onclick="window.location.href='/en/blog';"` with `onclick="window.location.href='/blog';"`
    # So it should already be correct!
        
    out_path = os.path.join('en', os.path.basename(filepath))
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Translated to {out_path}")

translate_file('sobre-mi.html', sobre_mi_map)
translate_file('blog.html', blog_map)
translate_file('contacto.html', contacto_map)
