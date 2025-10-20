from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont

class InfoSectionForm(QWidget):
    component_type = 'info_section'

    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout()

        heading_label = QLabel("Info Section")
        heading_label.setFont(QFont('Arial', 20, QFont.Bold))
        layout.addWidget(heading_label)

        self.heading = QLineEdit()
        layout.addWidget(QLabel("Heading:"))
        layout.addWidget(self.heading)

        self.paragraphs = QTextEdit()
        layout.addWidget(QLabel("Paragraphs (one per line):"))
        layout.addWidget(self.paragraphs)

        self.button_text = QLineEdit()
        layout.addWidget(QLabel("Button Text:"))
        layout.addWidget(self.button_text)

        self.button_link = QLineEdit()
        layout.addWidget(QLabel("Button Link:"))
        layout.addWidget(self.button_link)

        self.image_src = QLineEdit()
        layout.addWidget(QLabel("Image URL:"))
        layout.addWidget(self.image_src)

        self.image_alt = QLineEdit()
        layout.addWidget(QLabel("Image Alt Text:"))
        layout.addWidget(self.image_alt)

        if data:
            self.heading.setText(data.get('heading', ''))
            self.paragraphs.setText('\n'.join(data.get('paragraphs', [])))
            self.button_text.setText(data.get('button_text', ''))
            self.button_link.setText(data.get('button_link', ''))
            self.image_src.setText(data.get('image_src', ''))
            self.image_alt.setText(data.get('image_alt', ''))

        self.setLayout(layout)

    def get_data(self):
        return {
            "heading": self.heading.text(),
            "paragraphs": self.paragraphs.toPlainText().split('\n'),
            "button_text": self.button_text.text(),
            "button_link": self.button_link.text(),
            "image_src": self.image_src.text(),
            "image_alt": self.image_alt.text()
        }
