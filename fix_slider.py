import os

for file in ['sobre-mi.html', 'en/sobre-mi.html']:
    if not os.path.exists(file): continue
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add flex-shrink: 0; to prevent flexbox from collapsing the slides
    old_css = """.slide {
      width: 150px;
      height: 80px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 15px;
      filter: grayscale(100%) opacity(0.6);
      transition: filter 0.3s;
  }"""
    
    new_css = """.slide {
      width: 150px;
      height: 80px;
      flex-shrink: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 15px;
      filter: grayscale(100%) opacity(0.6);
      transition: filter 0.3s;
      background: rgba(0,0,0,0.03);
      border-radius: 12px;
      margin: 0 10px;
  }"""

    # Because adding margin adds 20px per slide, we must adjust the track width!
    # 150px + 20px = 170px per slide
    content = content.replace(old_css, new_css)
    content = content.replace('width: calc(150px * 16);', 'width: calc(170px * 16);')
    content = content.replace('transform: translateX(calc(-150px * 8));', 'transform: translateX(calc(-170px * 8));')

    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
print("Fixed slider collapse")
