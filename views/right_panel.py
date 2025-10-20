from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QScrollArea, 
    QMenu, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt
from database.db_handler import DBHandler
from views.components.facts_table_form import FactsTableForm
from views.components.header_section_form import HeaderSectionForm
from views.components.info_section_form import InfoSectionForm
from controllers.page_generator import PageGenerator
from views.components.cards_section_form import CardsSectionForm
from views.components.card_grid_4_form import CardGrid4Form



class RightPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.db = DBHandler()
        self.current_page_id = None
        self.component_forms = []

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Page Title:"))
        self.page_title = QLineEdit()
        layout.addWidget(self.page_title)

        self.components_area = QScrollArea()
        self.components_area.setWidgetResizable(True)

        self.components_container = QWidget()
        self.components_layout = QVBoxLayout()
        self.components_container.setLayout(self.components_layout)
        self.components_area.setWidget(self.components_container)

        layout.addWidget(QLabel("Components in this Page:"))
        layout.addWidget(self.components_area)

        self.add_component_btn = QPushButton("➕ Add Component")
        self.add_component_btn.clicked.connect(self.show_component_menu)
        layout.addWidget(self.add_component_btn)

        save_btn = QPushButton("💾 Save Changes")
        save_btn.clicked.connect(self.save_changes)
        layout.addWidget(save_btn)

        export_btn = QPushButton("📥 Export HTML+CSS")
        export_btn.clicked.connect(self.export_page)
        layout.addWidget(export_btn)

        self.setLayout(layout)

    def load_page_details(self, page_id):
        self.current_page_id = page_id
        page_components = self.db.get_page_components(page_id)

        for i in reversed(range(self.components_layout.count())):
            widget = self.components_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        self.component_forms.clear()

        page_data = [p for p in self.db.get_pages() if p['id'] == page_id][0]
        self.page_title.setText(page_data['title'])

        for comp in page_components:
            form_widget = self.get_component_form(comp['type'], comp['data'])
            if form_widget:
                self.components_layout.addWidget(form_widget)
                self.component_forms.append((comp['id'], form_widget))

    def get_component_form(self, component_type, data=None):
        if component_type == 'facts_table':
            return FactsTableForm(data)
        elif component_type == 'header_section':
            return HeaderSectionForm(data)
        elif component_type == 'info_section':
            return InfoSectionForm(data)
        elif component_type == 'cards_section':
            return CardsSectionForm(data)
        elif component_type == 'card_grid_4':
            return CardGrid4Form(data)


        else:
            QMessageBox.warning(self, "Component Error", f"Unknown component type: {component_type}")

    def show_component_menu(self):
        menu = QMenu()
        menu.addAction("Facts Table", lambda: self.add_new_component('facts_table'))
        menu.addAction("Header Section", lambda: self.add_new_component('header_section'))
        menu.addAction("Info Section", lambda: self.add_new_component('info_section'))
        menu.addAction("Cards Section", lambda: self.add_new_component('cards_section'))
        menu.addAction("4-Card Grid Section", lambda: self.add_new_component('card_grid_4'))



        menu.exec_(self.add_component_btn.mapToGlobal(self.add_component_btn.rect().bottomLeft()))

    def add_new_component(self, component_type):
        form_widget = self.get_component_form(component_type)
        if form_widget:
            self.components_layout.addWidget(form_widget)
            self.component_forms.append((None, form_widget))

    def save_changes(self):
        self.db.update_page_title(self.current_page_id, self.page_title.text())

        position = 1
        for comp_id, form_widget in self.component_forms:
            comp_data = form_widget.get_data()
            comp_type = form_widget.component_type

            if comp_id is None:
                self.db.add_component(self.current_page_id, comp_type, comp_data, position)
            else:
                self.db.update_component(comp_id, comp_data, position)
            position += 1

        QMessageBox.information(self, "Saved", "Changes saved successfully!")
        self.parent().left_panel.load_pages_from_db()

    def export_page(self):
        if not self.current_page_id:
            QMessageBox.warning(self, "Export Error", "Please select or create a page first!")
            return

        components_data = []
        for _, form_widget in self.component_forms:
            components_data.append({
                'type': form_widget.component_type,
                'data': form_widget.get_data()
            })

        generator = PageGenerator()
        html_css = generator.generate_page_content(components_data)

        file_path, _ = QFileDialog.getSaveFileName(self, "Save HTML+CSS", f"page_{self.current_page_id}.txt", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_css)
            QMessageBox.information(self, "Exported", f"Page successfully exported to:\n{file_path}")
