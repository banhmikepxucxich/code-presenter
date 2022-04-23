# Code presenter core
# by Hwoai#0593
# 17 - 18 April 2022

from PIL import Image
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from pygments.style import Style
from html2image import Html2Image
from bs4 import BeautifulSoup

import os
import math

class imgRender:
    def __init__(self, code, lexer, theme, font, fontSize, showNumbers, fontFormat):
        # Init configurations
        self.code = code
        self.lexer = lexer
        self.theme = theme
        self.font = font
        self.fontSize = fontSize
        self.showNumbers = showNumbers
        self.fontFormat = fontFormat

        self.additional_css = """
            @font-face {{
                font-family: '{0}', monospace;
                src: url({1}) format({3});
                font-size: {2}px;
            }}

            html * {{
                font-family: '{0}', monospace;
                font-size: {2}px;
            }}
        """
        self.additional_css = self.additional_css.format(self.font, './fonts/' + self.font.replace(' ', '') + '.' + self.fontFormat, self.fontSize, self.fontFormat)
        self.formatter = HtmlFormatter(style=self.theme, full=True, linenos=self.showNumbers)
        self.html = highlight(self.code, self.lexer, self.formatter)

    def drawImage(self): # ! No longer used now uses webview.
        self.codeList = self.code.splitlines()
        self.codeListLen = []

        for i in range(len(self.codeList)):
            self.codeListLen.append(len(self.codeList[i]))

        self.imgLen = math.ceil((max(self.codeListLen) * self.fontSize) * (7/10))
        self.imgWidth = math.ceil((len(self.codeList) * self.fontSize * 1.3) + self.fontSize + 5)

        Html2Image().screenshot(html_str=self.html, save_as='display.png', size=(self.imgLen, self.imgWidth))

        self.display = Image.open('display.png')
        self.display = self.display.crop(self.display.getbbox())
        self.display.crop((0, 0, self.imgLen, 0))
        self.display = self.display.resize((round(self.display.size[0]*0.5), round(self.display.size[1]*0.5)))
        self.display.save('display.png')

    def exportHtml(self, name, filepath):
        self.name = name
        self.filepath = filepath

        with open(self.filepath + self.name + '.html', 'w') as self.f:
            self.f.write(self.html)

    def exportPNG(self, name, filepath):
        self.name = name
        self.filepath = filepath

        Html2Image().screenshot(html_str=self.injectCss(), save_as=self.name + '.png', size=(self.imgLen, self.imgWidth))
            
        # * Move file or python will complain

        os.replace(self.name + '.png', self.filepath + self.name + '.png')

        self.display = Image.open(self.filepath + self.name + '.png')
        self.display = self.display.crop(self.display.getbbox())
        self.display.crop((0, 0, self.imgLen, 0))
        self.display.save(self.filepath + self.name + '.png')

    def getHtml(self): # ! No longer used, use returnHtml for injected font into html doc.
        return self.html

    def returnHtml(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.soup.select_one('style').append(self.additional_css)

        return str(self.soup)

class themeHandler:
    def __init__(self, theme):
        self.theme = theme

    def getAppStyle(self):
        self.cssFile = open('themes/' + self.theme + '.css')
        self.css = self.cssFile.read()
        return self.css