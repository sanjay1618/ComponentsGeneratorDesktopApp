from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import sys
from typing import List, Dict, Any

def _base_path() -> str:
    # Works from source and when bundled with PyInstaller (onefile/onedir)
    return getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))

class PageGenerator:
    def __init__(self):
        base = _base_path()
        self.html_dir = os.path.join(base, "templates", "components_html")
        self.css_dir  = os.path.join(base, "templates", "components_css")

        # Ensure directories exist (helps produce a clear error early)
        if not os.path.isdir(self.html_dir):
            raise FileNotFoundError(
                f"Templates folder not found: {self.html_dir}"
            )

        self.env = Environment(loader=FileSystemLoader(self.html_dir))

    def generate_page_content(self, components: List[Dict[str, Any]]) -> str:
        """
        components = [{ 'type': 'facts_table', 'data': {...}}, ...]
        Returns a single string with HTML followed by a <style> block containing CSS.
        """
        html_parts: List[str] = []
        css_parts: List[str] = []

        for comp in components:
            ctype = comp.get("type")
            cdata = comp.get("data", {}) or {}

            if not ctype:
                raise ValueError("Component is missing 'type'.")

            # --- Render HTML ---
            try:
                template = self.env.get_template(f"{ctype}.html")
            except TemplateNotFound as e:
                raise FileNotFoundError(
                    f"Template not found for component '{ctype}': "
                    f"{os.path.join(self.html_dir, ctype + '.html')}"
                ) from e

            try:
                html_parts.append(template.render(**cdata))
            except Exception as e:
                # Bubble up with context so your UI error dialog is helpful
                raise RuntimeError(
                    f"Error rendering template '{ctype}.html' with data keys: {list(cdata.keys())}"
                ) from e

            # --- Append CSS if present ---
            css_path = os.path.join(self.css_dir, f"{ctype}.css")
            if os.path.exists(css_path):
                try:
                    with open(css_path, "r", encoding="utf-8") as f:
                        css_parts.append(f.read())
                except Exception as e:
                    raise RuntimeError(f"Failed reading CSS file: {css_path}") from e
            # If CSS file is missing, that’s fine—just skip.

        html_content = "\n\n".join(html_parts).strip()
        css_content  = "\n\n".join(css_parts).strip()

        final = html_content
        if css_content:
            final += f"\n\n<style>\n{css_content}\n</style>\n"

        if not final.strip():
            raise ValueError("Generated content is empty. Check components and templates.")

        return final
