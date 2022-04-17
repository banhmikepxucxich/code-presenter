# Code presenter core
# by Hwoai#0593
# 17th April 2022

from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from html2image import Html2Image

import math

class core:
    def __init__(self, code, lexer, theme, font, fontSize, showNumbers):
        # Init configurations
        self.code = code
        self.lexer = lexer
        self.theme = theme
        self.font = font
        self.fontSize = fontSize
        self.showNumbers = showNumbers

        self.additional_css = """
            @font-face {{
                font-family: '{0}', monospace;
                src: url({1});
                font-size: {2}px;
            }}

            html * {{
                font-family: '{0}', monospace;
                font-size: {2}px;
            }}
        """
        self.additional_css = self.additional_css.format(self.font, './fonts/' + self.font.replace(' ', ''), self.fontSize)
        self.formatter = HtmlFormatter(style=self.theme, full=True, linenos=self.showNumbers)
        self.html = highlight(self.code, self.lexer, self.formatter)

    def drawImage(self):
        self.codeList = self.code.splitlines()
        self.codeListLen = []

        for i in range(len(self.codeList)):
            self.codeListLen.append(len(self.codeList[i]))

        self.imgLen = math.ceil((max(self.codeListLen) * self.fontSize) * (2/3))
        self.imgWidth = math.ceil((len(self.codeList) * self.fontSize * 1.25) + 5)

        Html2Image().screenshot(html_str=self.html, save_as='display.png', size=(self.imgLen, self.imgWidth))

        self.display = Image.open('display.png')
        self.display = self.display.crop(self.display.getbbox())
        self.display.crop((0, 0, self.imgLen, 0))
        self.display = self.display.resize((round(self.display.size[0]*0.5), round(self.display.size[1]*0.5)))
        self.display.save('display.png')

    def export(self, option, name, filepath):
        self.option = option
        self.name = name
        self.filepath = filepath

        if self.option == 'html':
            with open(name + '.html', 'w') as self.f:
                self.f.write(self.html)
        elif self.option == 'png':
            Html2Image().screenshot(html_str=self.html, save_as=self.name + '.png', size=(self.imgLen, self.imgWidth))

            self.display = Image.open(self.name + '.png')
            self.display = self.display.crop(self.display.getbbox())
            self.display.crop((0, 0, self.imgLen, 0))
            self.display.save(filepath + self.name + '.png')