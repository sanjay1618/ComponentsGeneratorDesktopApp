from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QScrollArea,
    QMenu, QMessageBox, QFileDialog, QHBoxLayout, QFrame
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

        # We keep a synchronized list of component "records":
        # each item: {"id": comp_id or None, "type": str, "form": QWidget, "container": QWidget}
        self.component_records = []

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Page Title:"))
        self.page_title = QLineEdit()
        layout.addWidget(self.page_title)

        self.components_area = QScrollArea()
        self.components_area.setWidgetResizable(True)

        self.components_container = QWidget()
        self.components_layout = QVBoxLayout()
        self.components_layout.setContentsMargins(0, 0, 0, 0)
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

    # ---------- helpers ----------

    def _component_title_from_type(self, component_type: str) -> str:
        mapping = {
            'facts_table': 'Facts Table',
            'header_section': 'Header Section',
            'info_section': 'Info Section',
            'cards_section': 'Cards Section',
            'card_grid_4': '4-Card Grid Section',
        }
        return mapping.get(component_type, component_type)

    def _make_separator(self) -> QFrame:
        sep = QFrame()
        sep.setFrameShape(QFrame.HLine)
        sep.setFrameShadow(QFrame.Sunken)
        return sep

    def _add_component_row(self, comp_id, component_type, form_widget):
        """
        Wrap a form in a container with a header (title + delete button) and
        append it to the layout and the internal records list (no duplicates).
        """
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(8, 8, 8, 8)
        container_layout.setSpacing(8)

        # Header with title + delete
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(self._component_title_from_type(component_type))
        title_label.setStyleSheet("font-weight: 600;")
        header_layout.addWidget(title_label)
        header_layout.addStretch(1)

        del_btn = QPushButton("🗑️ Delete Component")
        del_btn.setToolTip("Remove this component from the page")
        del_btn.setStyleSheet("QPushButton{padding:4px 8px;} QPushButton:hover{opacity:0.95;}")
        header_layout.addWidget(del_btn)

        container_layout.addWidget(header)
        container_layout.addWidget(form_widget)
        container_layout.addWidget(self._make_separator())

        # Hook delete
        del_btn.clicked.connect(lambda: self._delete_component_clicked(container, comp_id))

        # Add to UI
        self.components_layout.addWidget(container)

        # Track record synchronized with layout
        record = {
            "id": comp_id,
            "type": component_type,
            "form": form_widget,
            "container": container
        }
        self.component_records.append(record)

    def _clear_components_ui_and_records(self):
        """Remove all component containers from the layout and clear records."""
        for i in reversed(range(self.components_layout.count())):
            w = self.components_layout.itemAt(i).widget()
            if w:
                w.setParent(None)
        self.component_records.clear()

    # ---------- main flows ----------

    def load_page_details(self, page_id):
        """Populate page title and components from DB for a selected page."""
        self.current_page_id = page_id

        # Always clear before reloading to avoid duplicates
        self._clear_components_ui_and_records()

        # Set page title
        page_data = [p for p in self.db.get_pages() if p['id'] == page_id][0]
        self.page_title.setText(page_data['title'])

        # Load components from DB and render
        page_components = self.db.get_page_components(page_id)
        for comp in page_components:
            form_widget = self.get_component_form(comp['type'], comp['data'])
            if form_widget:
                self._add_component_row(comp['id'], comp['type'], form_widget)

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
        menu.addAction("Facts Table",      lambda: self.add_new_component('facts_table'))
        menu.addAction("Header Section",   lambda: self.add_new_component('header_section'))
        menu.addAction("Info Section",     lambda: self.add_new_component('info_section'))
        menu.addAction("Cards Section",    lambda: self.add_new_component('cards_section'))
        menu.addAction("4-Card Grid Section", lambda: self.add_new_component('card_grid_4'))
        menu.exec_(self.add_component_btn.mapToGlobal(self.add_component_btn.rect().bottomLeft()))

    def add_new_component(self, component_type):
        form_widget = self.get_component_form(component_type)
        if form_widget:
            # comp_id is None for new unsaved components
            self._add_component_row(None, component_type, form_widget)

    def _delete_component_clicked(self, container, comp_id):
        """
        Delete handler:
        - Confirm with the user.
        - If comp is saved (comp_id not None): delete from DB.
        - Remove container from UI.
        - Remove matching record from component_records.
        - Do NOT full-reload here to avoid losing unsaved components and to avoid duplicates.
        """
        confirm = QMessageBox.question(
            self,
            "Confirm Delete",
            "Delete this component from the page?",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.Yes:
            return

        # Delete from DB if needed
        if comp_id is not None:
            try:
                self.db.delete_component(comp_id)
            except Exception as e:
                QMessageBox.critical(self, "Delete Failed", f"Could not delete component:\n{e}")
                return

        # Remove container from UI
        container.setParent(None)

        # Remove from records (by identity on container)
        self.component_records = [
            rec for rec in self.component_records if rec["container"] is not container
        ]

        QMessageBox.information(self, "Deleted", "Component deleted.")

        # Optional: if you want to normalize positions visually right away
        # (no DB write yet), you could re-render titles or numbers here.
        # Positions are ultimately written on Save.

    def save_changes(self):
        if not self.current_page_id:
            QMessageBox.warning(self, "Save Error", "Please select or create a page first!")
            return

        # Update page title
        self.db.update_page_title(self.current_page_id, self.page_title.text())

        # Persist components in current on-screen order (1..N)
        position = 1
        for rec in self.component_records:
            comp_id = rec["id"]
            form_widget = rec["form"]
            comp_type = rec["type"]
            comp_data = form_widget.get_data()

            if comp_id is None:
                new_id = self.db.add_component(self.current_page_id, comp_type, comp_data, position)
                rec["id"] = new_id  # update record with real id
            else:
                self.db.update_component(comp_id, comp_data, position)
            position += 1

        QMessageBox.information(self, "Saved", "Changes saved successfully!")
        # Let the left panel update titles if changed
        self.parent().left_panel.load_pages_from_db()

    def export_page(self):
        if not self.current_page_id:
            QMessageBox.warning(self, "Export Error", "Please select or create a page first!")
            return

        components_data = []
        for rec in self.component_records:
            components_data.append({
                'type': rec["type"],
                'data': rec["form"].get_data()
            })

        generator = PageGenerator()
        html_css = generator.generate_page_content(components_data)

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save HTML+CSS",
            f"page_{self.current_page_id}.txt",
            "Text Files (*.txt)"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(html_css)
            QMessageBox.information(self, "Exported", f"Page successfully exported to:\n{file_path}")
