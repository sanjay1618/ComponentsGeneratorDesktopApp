from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QTextEdit, QGroupBox, QFormLayout
)
from PyQt5.QtGui import QFont

class CardGrid4Form(QWidget):
    component_type = 'card_grid_4'

    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout()

        heading = QLabel("4-Card Grid Section")
        heading.setFont(QFont("Arial", 20, QFont.Bold))
        layout.addWidget(heading)

        self.cards = []

        for i in range(4):
            group = QGroupBox(f"Card {i + 1}")
            form = QFormLayout()

            image_src = QLineEdit()
            image_alt = QLineEdit()
            title = QLineEdit()
            description = QTextEdit()
            button_text = QLineEdit()
            button_link = QLineEdit()

            form.addRow("Image URL:", image_src)
            form.addRow("Image Alt Text:", image_alt)
            form.addRow("Title:", title)
            form.addRow("Description:", description)
            form.addRow("Button Text:", button_text)
            form.addRow("Button Link:", button_link)

            group.setLayout(form)
            layout.addWidget(group)

            self.cards.append({
                "image_src": image_src,
                "image_alt": image_alt,
                "title": title,
                "description": description,
                "button_text": button_text,
                "button_link": button_link
            })

        self.setLayout(layout)

        if data:
            cards_data = data.get("cards", [])
            for i in range(min(4, len(cards_data))):
                card = cards_data[i]
                self.cards[i]["image_src"].setText(card.get("image_src", ""))
                self.cards[i]["image_alt"].setText(card.get("image_alt", ""))
                self.cards[i]["title"].setText(card.get("title", ""))
                self.cards[i]["description"].setText(card.get("description", ""))
                self.cards[i]["button_text"].setText(card.get("button_text", ""))
                self.cards[i]["button_link"].setText(card.get("button_link", ""))

    def get_data(self):
        cards_output = []
        for card in self.cards:
            cards_output.append({
                "image_src": card["image_src"].text().strip(),
                "image_alt": card["image_alt"].text().strip(),
                "title": card["title"].text().strip(),
                "description": card["description"].toPlainText().strip(),
                "button_text": card["button_text"].text().strip(),
                "button_link": card["button_link"].text().strip()
            })
        return {"cards": cards_output}
