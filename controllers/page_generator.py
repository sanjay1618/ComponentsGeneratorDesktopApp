from jinja2 import Environment, FileSystemLoader
import os

class PageGenerator:
    def __init__(self):
        templates_path = os.path.join(os.getcwd(), 'templates', 'components_html')
        self.env = Environment(loader=FileSystemLoader(templates_path))

    def generate_page_content(self, components):
        html_content = ""
        css_content = ""

        for comp in components:
            template = self.env.get_template(f"{comp['type']}.html")
            html_content += template.render(**comp['data']) + "\n\n"

            css_path = os.path.join('templates', 'components_css', f"{comp['type']}.css")
            if os.path.exists(css_path):
                with open(css_path, 'r') as css_file:
                    css_content += css_file.read() + "\n\n"

        final_content = f"{html_content}\n<style>\n{css_content}</style>"
        return final_content
