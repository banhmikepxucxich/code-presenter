# use carbon bruh -> https://github.com/carbon-app/carbon

from PIL import Image
from pygments import highlight
from pygments.formatters import HtmlFormatter
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

            body {{ background-color: transparent; }}

            body .box {{
                background-color: {4};
                width: fit-content;
                padding-right: 20px;
                padding-left: 20px;
                padding-top: 6px;
                padding-bottom: 2px;
                border-radius: 10px;
                box-shadow: 0 5px 10px 0 rgba(0, 0, 0, 0.5);
            }}

            body .dot {{
                height: 9px;
                width: 9px;
                border-radius: 50%;
                display: inline-block;
            }}

            body .btn-g {{ background-color: #00ca4e; }}

            body .btn-y {{ background-color: #ffbd44; }}

            body .btn-r {{ background-color: #ff605c; }}

            body .bar {{
                margin: 0px;
                padding: 0px;
                margin-top: 2px;
                margin-bottom: -8px;
            }}
        """
        self.additional_css = self.additional_css.format(self.font, './fonts/' + self.font.replace(' ', '') + '.' + self.fontFormat, self.fontSize, self.fontFormat, self.theme.background_color)
        self.additional_html = """
        <div class="box">
            <div class="bar">
                <span class="dot btn-r"></span>
                <span class="dot btn-y"></span>
                <span class="dot btn-g"></span>
            </div>
                {0}
                {1}
        </div>
        """
        self.formatter = HtmlFormatter(style=self.theme, full=True, linenos=self.showNumbers)
        self.html = highlight(self.code, self.lexer, self.formatter)

    def exportHtml(self, name, filepath):
        self.name = name
        self.filepath = filepath

        with open(self.filepath + self.name + '.html', 'w') as self.f:
            self.f.write(self.returnHtml())

    def exportPNG(self, name, filepath):
        self.name = name
        self.filepath = filepath

        Html2Image().screenshot(html_str=self.returnHtml(), save_as=self.name + '.png')
            
        # * Move file or python will complain

        os.replace(self.name + '.png', self.filepath + self.name + '.png')

        self.display = Image.open(self.filepath + self.name + '.png')
        self.display = self.display.crop(self.display.getbbox())
        self.display.save(self.filepath + self.name + '.png')

    def returnHtml(self):
        self.soup = BeautifulSoup(self.html, 'html.parser')
        self.soup.select_one('style').append(self.additional_css)
        self.contents = self.soup.find('body')
        self.contents = self.contents.findChildren(recursive=False)
        self.soup.body.clear()
        self.soup.body.append(BeautifulSoup(self.additional_html.format(self.contents[0], self.contents[1]), 'html.parser'))
        self.formatted_html = self.soup.prettify()

        return str(self.formatted_html)

class themeHandler:
    def __init__(self, theme):
        self.theme = theme

    def getAppStyle(self):
        self.cssFile = open('themes/' + self.theme + '.css')
        self.css = self.cssFile.read()
        return self.css