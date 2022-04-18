# Code presenter gui
# by Hwoai#0593
# 17th April 2022

from discord import option
from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.styles import get_style_by_name, get_all_styles
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QComboBox, QFileDialog
from PyQt6.QtGui import QPixmap
from pathlib import Path

import math

from core import core

# code = """def exampleFunc(param0, param1):
#     print(param1)
#     print(param2)"""
# lexer = get_lexer_by_name('python3')

# imageRenderer = core(code, lexer, 'dracula', 'JetBrains Mono', 14, True)
# imageRenderer.drawImage()
# imageRenderer.export('png', 'example_output')

# def example_function():
#     print('button clicked, text in textbox is {0}, and current text in combobox is {1}'.format(text.text(), combo.currentText()))
#     output_label.setText(text.text())

def exitHandler():
    deletePreview()
    print('Exiting')
    exit(0)

def deletePreview():
    path = Path('display.png')
    with open(path, 'wb') as file:
        file.write(b'')
    path.unlink()
    display = QPixmap('display.png')
    codeBlock.setPixmap(display)
    window.setBaseSize(settingsLayoutMaxWidth, 200)
    print('Deleted Preview')

def renderPreview():
    if codeBox.text().strip() == '':
        return
    code = codeBox.text()
    lexer = get_lexer_by_name(langDropdown.currentText().lower())
    theme = get_style_by_name(themeDropdown.currentText().lower())
    font = 'JetBrains Mono' # will change later
    imageRenderer = core(code, lexer, theme, font, 14, True)
    imageRenderer.drawImage()
    display = QPixmap('display.png')
    codeBlock.setPixmap(display)
    print('Updated Display')

def filePathDialog():
    global filePath
    filePath = str(QFileDialog.getExistingDirectory(caption='Select a directory')) + slash
    labelFilePath.setText(filePath)
    print('File path added, path=%s' % filePath)

def exportFile():
    if codeBox.text().strip() == '':
        labelFilePath.setText('Empty CodeBox.')
        return
    if filePath.strip() == '/':
        labelFilePath.setText('Empty file path.')
        return
    if filePath.strip() == '    ':
        labelFilePath.setText('Empty file path.')
        return
    code = codeBox.text()
    lexer = get_lexer_by_name(langDropdown.currentText().lower())
    theme = get_style_by_name(themeDropdown.currentText().lower())
    font = 'JetBrains Mono' # will change later
    choice = typeDropdown.currentText()
    imageRenderer = core(code, lexer, theme, font, 14, True)
    imageRenderer.drawImage()
    imageRenderer.export(choice, 'example_output', filePath)
    print('Exported file')

settingsLayoutMaxWidth = 175
exportLayoutMaxWidth = 175
slash = '/' # or \\ if you're a windows user
filePath = ''

app = QApplication([])
app.aboutToQuit.connect(exitHandler)
window = QWidget()
window.setWindowTitle('Code Presenter')
window.setBaseSize(settingsLayoutMaxWidth, 200)

mainLayout = QVBoxLayout()
subMainLayout = QHBoxLayout()

settingsLayout = QVBoxLayout()
settingsLayout
rendererLayout = QVBoxLayout()
exportLayout = QHBoxLayout()

mainLayout.addLayout(subMainLayout)
subMainLayout.addLayout(settingsLayout)
subMainLayout.addLayout(rendererLayout)
mainLayout.addLayout(exportLayout)

delPreview = QPushButton('Delete Preview')
delPreview.setMaximumWidth(settingsLayoutMaxWidth)
delPreview.clicked.connect(deletePreview)
settingsLayout.addWidget(delPreview)

labelCode = QLabel('Code (Paste code here)')
labelCode.setMaximumWidth(settingsLayoutMaxWidth)
settingsLayout.addWidget(labelCode)

codeBox = QLineEdit()
codeBox.setMaximumWidth(settingsLayoutMaxWidth)
settingsLayout.addWidget(codeBox)

labelLang = QLabel('Language')
labelLang.setMaximumWidth(settingsLayoutMaxWidth)
settingsLayout.addWidget(labelLang)

langDropdown = QComboBox()
langDropdown.setMaximumWidth(settingsLayoutMaxWidth)
lang = list(get_all_lexers())
langlist = []
for i in range(len(lang)):
    langlist.append(lang[i][0])
langDropdown.addItems(langlist)
settingsLayout.addWidget(langDropdown)

labelTheme = QLabel('Theme')
labelTheme.setMaximumWidth(settingsLayoutMaxWidth)
settingsLayout.addWidget(labelTheme)

themeDropdown = QComboBox()
themeDropdown.setMaximumWidth(settingsLayoutMaxWidth)
theme = list(get_all_styles())
themeDropdown.addItems(theme)
settingsLayout.addWidget(themeDropdown)

renderButton = QPushButton('Render Preview')
renderButton.setMaximumWidth(settingsLayoutMaxWidth)
renderButton.clicked.connect(renderPreview)
settingsLayout.addWidget(renderButton)

codeBlock = QLabel()
rendererLayout.addWidget(codeBlock)

labelFileName = QLabel('File Name')
labelFileName.setMaximumWidth(exportLayoutMaxWidth)
exportLayout.addWidget(labelFileName)

fileNameBox = QLineEdit()
fileNameBox.setMaximumWidth(exportLayoutMaxWidth)
exportLayout.addWidget(fileNameBox)

typeDropdown = QComboBox()
typeDropdown.setMaximumWidth(exportLayoutMaxWidth)
exportOptions = ['png', 'html']
typeDropdown.addItems(exportOptions)
exportLayout.addWidget(typeDropdown)

filePathButton = QPushButton('Select File Path')
filePathButton.setMaximumWidth(exportLayoutMaxWidth)
filePathButton.clicked.connect(filePathDialog)
exportLayout.addWidget(filePathButton)

labelFilePath = QLabel('')
exportLayout.addWidget(labelFilePath)

exportButton = QPushButton('Export')
exportButton.setMaximumWidth(exportLayoutMaxWidth)
exportButton.clicked.connect(exportFile)
exportLayout.addWidget(exportButton)

# text = QLineEdit()
# layout.addWidget(text)

# combo = QComboBox()
# example_list = ['A', 'B', 'C']
# combo.addItems(example_list)
# layout.addWidget(combo)

# btn = QPushButton('example button')
# layout.addWidget(btn)
# btn.clicked.connect(example_function)

# output_label = QLabel('example label')
# layout.addWidget(output_label)

window.setLayout(mainLayout)
window.show()
app.exec()