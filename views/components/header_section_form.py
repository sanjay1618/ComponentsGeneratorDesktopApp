from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont

class HeaderSectionForm(QWidget):
    component_type = 'header_section'

    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout()

        heading_label = QLabel("Header Section")
        heading_label.setFont(QFont('Arial', 20, QFont.Bold))
        layout.addWidget(heading_label)

        self.heading = QLineEdit()
        layout.addWidget(QLabel("Heading:"))
        layout.addWidget(self.heading)

        self.paragraphs = QTextEdit()
        layout.addWidget(QLabel("Paragraphs (one per line):"))
        layout.addWidget(self.paragraphs)

        self.image_src = QLineEdit()
        layout.addWidget(QLabel("Image URL:"))
        layout.addWidget(self.image_src)

        self.image_alt = QLineEdit()
        layout.addWidget(QLabel("Image Alt Text:"))
        layout.addWidget(self.image_alt)

        self.image_caption = QTextEdit()
        layout.addWidget(QLabel("Image Caption:"))
        layout.addWidget(self.image_caption)

        self.button_text = QLineEdit()
        layout.addWidget(QLabel("Button Text:"))
        layout.addWidget(self.button_text)

        self.button_link = QLineEdit()
        layout.addWidget(QLabel("Button Link:"))
        layout.addWidget(self.button_link)

        if data:
            self.heading.setText(data.get('heading', ''))
            self.paragraphs.setText('\n'.join(data.get('paragraphs', [])))
            self.image_src.setText(data.get('image_src', ''))
            self.image_alt.setText(data.get('image_alt', ''))
            self.image_caption.setText(data.get('image_caption', ''))

            buttons = data.get('buttons', [])
            if buttons:
                self.button_text.setText(buttons[0]['text'])
                self.button_link.setText(buttons[0]['link'])

        self.setLayout(layout)

    def get_data(self):
        return {
            "heading": self.heading.text(),
            "paragraphs": self.paragraphs.toPlainText().split('\n'),
            "image_src": self.image_src.text(),
            "image_alt": self.image_alt.text(),
            "image_caption": self.image_caption.toPlainText(),
            "buttons": [{
                "text": self.button_text.text(),
                "link": self.button_link.text()
            }]
        }
