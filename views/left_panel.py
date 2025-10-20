from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QScrollArea
from PyQt5.QtCore import Qt
from database.db_handler import DBHandler

class LeftPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.db = DBHandler()

        layout = QVBoxLayout()

        label = QLabel("Pages")
        layout.addWidget(label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.page_list_widget = QListWidget()
        self.load_pages_from_db()

        self.page_list_widget.itemClicked.connect(self.page_selected)

        self.scroll_area.setWidget(self.page_list_widget)
        layout.addWidget(self.scroll_area)

        new_page_btn = QPushButton("➕ New Page")
        new_page_btn.clicked.connect(self.create_new_page)
        layout.addWidget(new_page_btn)

        self.setLayout(layout)

    def load_pages_from_db(self):
        self.page_list_widget.clear()
        pages = self.db.get_pages()
        for page in pages:
            self.page_list_widget.addItem(f"{page['id']}: {page['title']}")

    def page_selected(self, item):
        page_id = int(item.text().split(":")[0])
        self.parent().right_panel.load_page_details(page_id)

    def create_new_page(self):
        page_id = self.db.create_page("New Page")
        self.load_pages_from_db()

        # Safely select newly created page
        for index in range(self.page_list_widget.count()):
            item = self.page_list_widget.item(index)
            if item.text().startswith(f"{page_id}:"):
                self.page_list_widget.setCurrentItem(item)
                self.page_selected(item)
                break
