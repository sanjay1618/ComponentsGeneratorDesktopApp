from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QScrollArea, QMessageBox
from PyQt5.QtCore import Qt
from database.db_handler import DBHandler

class LeftPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.db = DBHandler()
        self.selected_page_id = None  # track current selection

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

        # Create / Delete buttons (delete is hidden until a page is selected)
        new_page_btn = QPushButton("➕ New Page")
        new_page_btn.clicked.connect(self.create_new_page)
        layout.addWidget(new_page_btn)

        self.delete_page_btn = QPushButton("🗑️ Delete Page")
        self.delete_page_btn.setVisible(False)  # only show when a page is selected
        self.delete_page_btn.clicked.connect(self.delete_selected_page)
        layout.addWidget(self.delete_page_btn)

        self.setLayout(layout)

    def load_pages_from_db(self):
        self.page_list_widget.clear()
        pages = self.db.get_pages()
        for page in pages:
            self.page_list_widget.addItem(f"{page['id']}: {page['title']}")

    def page_selected(self, item):
        page_id = int(item.text().split(":")[0])
        self.selected_page_id = page_id
        self.delete_page_btn.setVisible(True)  # show delete now that we have a selection
        # Load details into the right panel editor
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

    def delete_selected_page(self):
        if self.selected_page_id is None:
            QMessageBox.warning(self, "Delete Error", "Please select a page first!")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete this page and all its components? This action cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm != QMessageBox.Yes:
            return

        # Perform deletion
        try:
            self.db.delete_page(self.selected_page_id)
        except Exception as e:
            QMessageBox.critical(self, "Delete Failed", f"Could not delete page:\n{e}")
            return

        # Reset selection & UI
        self.selected_page_id = None
        self.delete_page_btn.setVisible(False)
        self.load_pages_from_db()
        self.page_list_widget.clearSelection()

        # Clear the right panel editor contents
        rp = self.parent().right_panel  # RightPanel instance
        rp.current_page_id = None
        rp.page_title.clear()
        # remove any component widgets
        for i in reversed(range(rp.components_layout.count())):
            w = rp.components_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        QMessageBox.information(self, "Deleted", "Page deleted successfully.")
