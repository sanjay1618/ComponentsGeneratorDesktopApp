from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QTextEdit
from PyQt5.QtGui import QFont

class FactsTableForm(QWidget):
    component_type = 'facts_table'

    def __init__(self, data=None):
        super().__init__()
        layout = QVBoxLayout()

        # Large heading clearly added at the top
        heading_label = QLabel("Facts Table Section")
        heading_label.setFont(QFont('Arial', 20, QFont.Bold))
        layout.addWidget(heading_label)

        # Lists to hold fact number and description fields
        self.fact_numbers = []
        self.fact_descriptions = []

        for i in range(3):
            layout.addWidget(QLabel(f"Fact {i+1} Number:"))
            number = QLineEdit()
            layout.addWidget(number)
            self.fact_numbers.append(number)

            layout.addWidget(QLabel(f"Fact {i+1} Description:"))
            description = QTextEdit()
            layout.addWidget(description)
            self.fact_descriptions.append(description)

        # If editing existing data, populate fields
        if data:
            facts = data.get('facts', [])
            for i in range(min(3, len(facts))):
                self.fact_numbers[i].setText(facts[i]['number'])
                self.fact_descriptions[i].setText(facts[i]['description'])

        self.setLayout(layout)

    def get_data(self):
        facts = []
        for i in range(3):
            number = self.fact_numbers[i].text().strip()
            description = self.fact_descriptions[i].toPlainText().strip()
            facts.append({"number": number, "description": description})
        return {"facts": facts}
