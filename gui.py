# Code presenter gui
# by Hwoai#0593 on discord
# 17 - 18 April 2022

from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QComboBox, QFileDialog, QCheckBox
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import QSize

from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.styles import get_style_by_name, get_all_styles

from core import core

# * ANCHOR Functions

def exitHandler():
    print('This is an exit handler')
    exit(0)

def renderPreview():
    if codeBox.text().strip() == '':
        return
    if fontSizeBox.text() == '':
        return
    code = codeBox.text()
    lexer = get_lexer_by_name(langDropdown.currentText().lower())
    theme = get_style_by_name(themeDropdown.currentText().lower())
    font = 'JetBrains Mono' # will change later
    fontSize = int(fontSizeBox.text())
    showNumLines = checkboxShowNums.isChecked()
    htmlProcessing = core(code, lexer, theme, font, fontSize, showNumLines)
    codeBlock.setHtml(htmlProcessing.getHtml())

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
    if filePath.strip() == '':
        labelFilePath.setText('Empty file path.')
        return
    code = codeBox.text()
    lexer = get_lexer_by_name(langDropdown.currentText().lower())
    theme = get_style_by_name(themeDropdown.currentText().lower())
    font = 'JetBrains Mono' # will change later
    choice = typeDropdown.currentText()
    name = fileNameBox.text()
    fontSize = int(fontSizeBox.text())
    showNumLines = checkboxShowNums.isChecked()
    imageRenderer = core(code, lexer, theme, font, fontSize, showNumLines)
    if choice == 'png':
        imageRenderer.exportPNG(name, filePath)
    if choice == 'html':
        imageRenderer.exportHtml(name, filePath)
    print('Exported file')

# * ANCHOR Settings 

settingsLayoutMaxWidth = 175
settingsLayoutMaxHeight = 32
exportLayoutMaxWidth = 175
slash = '/' # or \\ if you're a windows user
filePath = ''

# * ANCHOR GUI

app = QApplication([])
app.aboutToQuit.connect(exitHandler)
window = QWidget()
window.setWindowTitle('Code Presenter')
window.resize(1000, 500)

# * ANCHOR Layouts

mainLayout = QVBoxLayout()
subMainLayout = QHBoxLayout()

settingsLayout = QVBoxLayout()
rendererLayout = QVBoxLayout()
exportLayout = QHBoxLayout()

settingsLayout.addStretch()
mainLayout.addLayout(subMainLayout)
subMainLayout.addLayout(settingsLayout)
subMainLayout.addLayout(rendererLayout)
mainLayout.addLayout(exportLayout)

# * ANCHOR Settings widgets

labelCode = QLabel('Code (Paste code here)')
labelCode.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
settingsLayout.addWidget(labelCode)

codeBox = QLineEdit()
codeBox.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
codeBox.textChanged.connect(renderPreview)
settingsLayout.addWidget(codeBox)

labelLang = QLabel('Language')
labelLang.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
settingsLayout.addWidget(labelLang)

langDropdown = QComboBox()
langDropdown.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
langDropdown.currentTextChanged.connect(renderPreview)
lang = list(get_all_lexers())
langlist = []
for i in range(len(lang)):
    langlist.append(lang[i][0])
langDropdown.addItems(langlist)
langDropdown.setCurrentText('Python')
settingsLayout.addWidget(langDropdown)

labelTheme = QLabel('Theme')
labelTheme.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
settingsLayout.addWidget(labelTheme)

themeDropdown = QComboBox()
themeDropdown.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
themeDropdown.currentTextChanged.connect(renderPreview)
theme = list(get_all_styles())
themeDropdown.addItems(theme)
themeDropdown.setCurrentText('one-dark')
settingsLayout.addWidget(themeDropdown)

checkboxShowNums = QCheckBox('   Show Number Lines')
checkboxShowNums.clicked.connect(renderPreview)
checkboxShowNums.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
settingsLayout.addWidget(checkboxShowNums)

labelFontSize = QLabel('Font Size')
labelFontSize.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
settingsLayout.addWidget(labelFontSize)

fontSizeBox = QLineEdit()
fontSizeBox.textChanged.connect(renderPreview)
fontSizeBox.setValidator(QIntValidator())
fontSizeBox.setText('12') # Default
fontSizeBox.setMaximumSize(QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight))
settingsLayout.addWidget(fontSizeBox)

# * ANCHOR Render Widget

codeBlock = QWebEngineView()
rendererLayout.addWidget(codeBlock)

# * ANCHOR Export Widgets

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

# * Base settings

codeBox.setText("""def somefunc(param1, param2):
    print(f'param1: {0}, param2: {1}').format(param1, param2)""")

window.setLayout(mainLayout)
window.show()
app.exec()