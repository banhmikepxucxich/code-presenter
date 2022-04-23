# Code presenter gui
# by Hwoai#0593 on discord
# 17 - 18 April 2022

from PyQt6.QtWidgets import QLabel, QPushButton, QLineEdit, QComboBox, QFileDialog, QCheckBox, QPlainTextEdit
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtGui import QIntValidator, QFontDatabase, QFont, QFontMetricsF
from PyQt6.QtCore import QSize

from pygments.lexers import get_lexer_by_name, get_all_lexers
from pygments.styles import get_style_by_name, get_all_styles

from core import *

# * ANCHOR Functions

def exitHandler():
    print('This is an exit handler')
    exit(0)

def renderPreview():
    if codeBox.toPlainText().strip() == '':
        return
    if fontSizeBox.text() == '':
        return

    codeBox.setTabStopDistance(QFontMetricsF(codeBox.font()).horizontalAdvance(' ') * int(tabSizeDropdown.currentText()))

    code = codeBox.toPlainText()
    lexer = get_lexer_by_name(langDropdown.currentText().lower(), tabsize=int(tabSizeDropdown.currentText()))
    theme = get_style_by_name(themeDropdown.currentText().lower())
    font = 'JetBrains Mono' # will change later
    fontSize = int(fontSizeBox.text())
    showNumLines = checkboxShowNums.isChecked()
    fontFormat = 'ttf' # TODO Render Html Font
    htmlProcessing = imgRender(code, lexer, theme, font, fontSize, showNumLines, fontFormat)
    codeBlock.setHtml(htmlProcessing.getHtml())

def filePathDialog():
    global filePath
    filePath = str(QFileDialog.getExistingDirectory(caption='Select a directory')) + slash
    labelFilePath.setText(filePath)
    print('File path added, path=%s' % filePath)

def exportFile():
    if codeBox.toPlainText().strip() == '':
        labelFilePath.setText('Empty CodeBox.')
        return
    if filePath.strip() == '/':
        labelFilePath.setText('Empty file path.')
        return
    if filePath.strip() == '':
        labelFilePath.setText('Empty file path.')
        return
    code = codeBox.toPlainText()
    lexer = get_lexer_by_name(langDropdown.currentText().lower())
    theme = get_style_by_name(themeDropdown.currentText().lower())
    font = 'JetBrains Mono' # will change later
    choice = typeDropdown.currentText()
    name = fileNameBox.text()
    fontSize = int(fontSizeBox.text())
    showNumLines = checkboxShowNums.isChecked()
    fontFormat = 'ttf'
    imageRenderer = imgRender(code, lexer, theme, font, fontSize, showNumLines, fontFormat)
    if choice == 'png':
        imageRenderer.exportPNG(name, filePath)
    if choice == 'html':
        imageRenderer.exportHtml(name, filePath)
    print('Exported file')

# * ANCHOR Settings 

settingsLayoutMaxWidth = 175
settingsLayoutMaxHeight = 32
settingsSize = QSize(settingsLayoutMaxWidth, settingsLayoutMaxHeight)
codeBoxMaxWidth = 260
codeBoxMaxHeight = 180
exportLayoutMaxWidth = 175
slash = '/' # or \\ if you're a windows user
filePath = ''

appCss = themeHandler('windows98').getAppStyle()

comboLeftMargin = 5

fonts = [
    QFontDatabase.addApplicationFont(':/fonts/JetBrainsMono.ttf')
]

# * ANCHOR GUI

app = QApplication([])
app.aboutToQuit.connect(exitHandler)
app.setStyleSheet(appCss) # TODO Make the combobox box round
window = QWidget()
window.setWindowTitle('Code Presenter')
window.resize(1000, 500)

# * ANCHOR Layouts

mainLayout = QVBoxLayout()
subMainLayout = QHBoxLayout()
subMainRightLayout = QVBoxLayout()

settingsLayout = QVBoxLayout()
appSettingsLayout = QVBoxLayout()
rendererLayout = QVBoxLayout()
codeLayout = QVBoxLayout()
exportLayout = QHBoxLayout()

settingsLayout.addStretch()
appSettingsLayout.addStretch()
mainLayout.addLayout(subMainLayout)
subMainLayout.addLayout(codeLayout)
subMainLayout.addLayout(rendererLayout)
subMainLayout.addLayout(subMainRightLayout)
subMainRightLayout.addLayout(settingsLayout)
subMainRightLayout.addLayout(appSettingsLayout)
mainLayout.addLayout(exportLayout)

# * ANCHOR Settings widgets

labelSettings = QLabel('Settings')
labelSettings.setObjectName('Title')
settingsLayout.addWidget(labelSettings)

labelLang = QLabel('Language')
labelLang.setMaximumSize(settingsSize)
settingsLayout.addWidget(labelLang)

langDropdown = QComboBox()
langDropdown.setMaximumSize(settingsSize)
# lang = list(get_all_lexers())
# langlist = []
# for i in range(len(lang)):
#     langlist.append(lang[i][0])
langlist = []
with open('Supported.txt', 'r') as supported:
    for line in supported:
        if line.startswith('#'):
            pass
        else:
            if line.strip() == '':
                pass
            else:
                langlist.append(line.strip())
langDropdown.addItems(langlist)
settingsLayout.addWidget(langDropdown)
langDropdown.currentTextChanged.connect(renderPreview)

labelTheme = QLabel('Theme')
labelTheme.setMaximumSize(settingsSize)
settingsLayout.addWidget(labelTheme)

themeDropdown = QComboBox()
themeDropdown.setMaximumSize(settingsSize)
theme = list(get_all_styles())
themeDropdown.addItems(theme)
settingsLayout.addWidget(themeDropdown)
themeDropdown.currentTextChanged.connect(renderPreview)

checkboxShowNums = QCheckBox('Show Number Lines')
checkboxShowNums.clicked.connect(renderPreview)
checkboxShowNums.setMaximumSize(settingsSize)
settingsLayout.addWidget(checkboxShowNums)

labelFontSize = QLabel('Font Size')
labelFontSize.setMaximumSize(settingsSize)
settingsLayout.addWidget(labelFontSize)

fontSizeBox = QLineEdit()
fontSizeBox.textChanged.connect(renderPreview)
fontSizeBox.setValidator(QIntValidator())
fontSizeBox.setMaximumSize(settingsSize)
settingsLayout.addWidget(fontSizeBox)

labelTabSize = QLabel('Tab Size')
labelTabSize.setMaximumSize(settingsSize)
settingsLayout.addWidget(labelTabSize)

tabSizeDropdown = QComboBox()
tabSizeDropdown.addItems([ '2', '4' ])
tabSizeDropdown.currentTextChanged.connect(renderPreview)
settingsLayout.addWidget(tabSizeDropdown)

# * ANCHOR App Settings Widgets

labelAppSettings = QLabel('App Settings')
labelAppSettings.setObjectName('Title')
appSettingsLayout.addWidget(labelAppSettings)


labelAppTheme = QLabel('App theme')
labelAppTheme.setMaximumSize(settingsSize)
appSettingsLayout.addWidget(labelAppTheme)

appThemeDropdown = QComboBox()
appThemeDropdown.addItems(['test'])
appThemeDropdown.setMaximumSize(settingsSize)
appSettingsLayout.addWidget(appThemeDropdown)

# * ANCHOR Render Widget

codeBlock = QWebEngineView()
rendererLayout.addWidget(codeBlock)

# * ANCHOR Code Widget

codeBox = QPlainTextEdit()
# codeBox.setMaximumSize(QSize(codeBoxMaxWidth, codeBoxMaxHeight))
codeBox.setFont(QFont('JetBrains Mono', 14))
codeBox.setTabStopDistance(QFontMetricsF(codeBox.font()).horizontalAdvance(' ') * int(tabSizeDropdown.currentText()))
codeBox.setPlaceholderText('Put your code here...')
codeBox.textChanged.connect(renderPreview)
codeLayout.addWidget(codeBox)

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

# codeBox.setText("""def somefunc(param1, param2):
#     print(f'param1: {0}, param2: {1}').format(param1, param2)""")
codeBox.setPlainText("""def somefunc(param1, param2):
\tprint(f'param1: {0}, param2: {1}').format(param1, param2)""")
fontSizeBox.setText('12')
langDropdown.setCurrentText('Python')
themeDropdown.setCurrentText('one-dark')
tabSizeDropdown.setCurrentText('4')

window.setLayout(mainLayout)
window.show()
app.exec()