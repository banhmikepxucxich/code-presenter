from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QPlainTextEdit
from PyQt6.QtGui import QFontMetrics, QFont, QFontDatabase

def example_function():
    print(textbox.toPlainText().expandtabs(4))

fonts = [
    QFontDatabase.addApplicationFont(':/fonts/JetBrainsMono.ttf')
]

app = QApplication([])
window = QWidget()
window.setWindowTitle('example app :DDDDD')

layout = QVBoxLayout()

textbox = QPlainTextEdit()
textbox.setFont(QFont('JetBrains Mono', 14))
textbox.setTabStopDistance(QFontMetrics(textbox.font()).horizontalAdvance(' ') * 4)
layout.addWidget(textbox)

button = QPushButton('button')
button.clicked.connect(example_function)
layout.addWidget(button)

window.setLayout(layout)
window.show()
app.exec()