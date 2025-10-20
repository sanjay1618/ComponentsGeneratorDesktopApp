from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QCheckBox, QGroupBox, QFormLayout
)
from PyQt5.QtGui import QFont

class CardsSectionForm(QWidget):
    component_type = 'cards_section'

    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout()

        # Section heading
        heading = QLabel("Cards Section")
        heading.setFont(QFont('Arial', 20, QFont.Bold))
        layout.addWidget(heading)

        self.cards = []

        for i in range(3):
            group = QGroupBox(f"Card {i+1}")
            form = QFormLayout()

            image_src = QLineEdit()
            image_alt = QLineEdit()
            title = QLineEdit()
            button_text = QLineEdit()
            button_link = QLineEdit()
            bordered = QCheckBox("Bordered Image")

            form.addRow("Image URL:", image_src)
            form.addRow("Alt Text:", image_alt)
            form.addRow("Title:", title)
            form.addRow("Button Text:", button_text)
            form.addRow("Button Link:", button_link)
            form.addRow("", bordered)

            group.setLayout(form)
            layout.addWidget(group)

            self.cards.append({
                'image_src': image_src,
                'image_alt': image_alt,
                'title': title,
                'button_text': button_text,
                'button_link': button_link,
                'bordered': bordered
            })

        self.setLayout(layout)

        # Load existing data if available
        if data:
            cards_data = data.get("cards", [])
            for i in range(min(3, len(cards_data))):
                card = cards_data[i]
                self.cards[i]['image_src'].setText(card.get("image_src", ""))
                self.cards[i]['image_alt'].setText(card.get("image_alt", ""))
                self.cards[i]['title'].setText(card.get("title", ""))
                self.cards[i]['button_text'].setText(card.get("button_text", ""))
                self.cards[i]['button_link'].setText(card.get("button_link", ""))
                self.cards[i]['bordered'].setChecked(card.get("bordered", False))

    def get_data(self):
        result = []
        for card in self.cards:
            result.append({
                "image_src": card['image_src'].text().strip(),
                "image_alt": card['image_alt'].text().strip(),
                "title": card['title'].text().strip(),
                "button_text": card['button_text'].text().strip(),
                "button_link": card['button_link'].text().strip(),
                "bordered": card['bordered'].isChecked()
            })
        return {"cards": result}
