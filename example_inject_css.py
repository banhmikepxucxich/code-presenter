from bs4 import BeautifulSoup

doc = open('asd.html', 'r')
doc = doc.read()
print(doc)
soup = BeautifulSoup(doc, 'html.parser')
soup.select_one('style').append("""
@font-face {
    font-family: 'JetBrains Mono', monospace;
    src: url(fonts/JetBrainsMono.ttf) format(ttf);
    font-size: 12px;
}

html * {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
}
""")

print(soup)