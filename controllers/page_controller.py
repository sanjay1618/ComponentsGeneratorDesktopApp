from database.db_handler import DBHandler

class PageController:
    def __init__(self):
        self.db = DBHandler()

    def create_page(self, title):
        return self.db.create_page(title)

    def get_all_pages(self):
        return self.db.get_pages()

    def get_page_details(self, page_id):
        return {
            'page': [p for p in self.db.get_pages() if p['id'] == page_id][0],
            'components': self.db.get_page_components(page_id)
        }

    def save_page(self, page_id, title, components):
        self.db.update_page_title(page_id, title)
        position = 1
        for comp in components:
            if comp['id'] is None:
                self.db.add_component(page_id, comp['type'], comp['data'], position)
            else:
                self.db.update_component(comp['id'], comp['data'], position)
            position += 1

    def delete_component(self, component_id):
        self.db.delete_component(component_id)

    def delete_page(self, page_id):
        self.db.delete_page(page_id)
