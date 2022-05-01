from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

import codecs

app = QApplication([])
window = QWidget()
window.setWindowTitle('code view test')

layout = QVBoxLayout()

code = QWebEngineView()
html = codecs.open('../test.html')
code.setHtml(html.read())
layout.addWidget(code)

window.setLayout(layout)
window.show()
app.exec()