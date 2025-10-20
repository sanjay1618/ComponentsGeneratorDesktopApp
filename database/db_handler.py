import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app_data.db')

class DBHandler:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS components (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_id INTEGER,
            component_type TEXT NOT NULL,
            component_data TEXT NOT NULL,
            position INTEGER,
            FOREIGN KEY(page_id) REFERENCES pages(id)
        )
        ''')
        self.conn.commit()

    # Create a new page
    def create_page(self, title):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO pages (title) VALUES (?)", (title,))
        self.conn.commit()
        return cursor.lastrowid

    # Add a component to a specific page
    def add_component(self, page_id, component_type, component_data, position):
        cursor = self.conn.cursor()
        component_json = json.dumps(component_data)
        cursor.execute('''
            INSERT INTO components (page_id, component_type, component_data, position)
            VALUES (?, ?, ?, ?)
        ''', (page_id, component_type, component_json, position))
        self.conn.commit()
        return cursor.lastrowid

    # Get all pages
    def get_pages(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pages ORDER BY created_at DESC")
        return cursor.fetchall()

    # Get all components for a given page
    def get_page_components(self, page_id):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM components
            WHERE page_id = ?
            ORDER BY position ASC
        ''', (page_id,))
        rows = cursor.fetchall()
        components = []
        for row in rows:
            component = {
                'id': row['id'],
                'type': row['component_type'],
                'data': json.loads(row['component_data']),
                'position': row['position']
            }
            components.append(component)
        return components

    # Update a page's title
    def update_page_title(self, page_id, new_title):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE pages SET title = ? WHERE id = ?", (new_title, page_id)
        )
        self.conn.commit()

    # Update a component within a page
    def update_component(self, component_id, component_data, position=None):
        cursor = self.conn.cursor()
        component_json = json.dumps(component_data)

        if position is not None:
            cursor.execute('''
                UPDATE components
                SET component_data = ?, position = ?
                WHERE id = ?
            ''', (component_json, position, component_id))
        else:
            cursor.execute('''
                UPDATE components
                SET component_data = ?
                WHERE id = ?
            ''', (component_json, component_id))

        self.conn.commit()

    # Delete a single component from a page
    def delete_component(self, component_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM components WHERE id = ?", (component_id,))
        self.conn.commit()

    # Delete an entire page and all associated components
    def delete_page(self, page_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM components WHERE page_id = ?", (page_id,))
        cursor.execute("DELETE FROM pages WHERE id = ?", (page_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
