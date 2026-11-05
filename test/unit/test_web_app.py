"""
test_web_app.py - Unit test suite for validating Web Application HTML, CSS, and JS structure.
"""

import os
import unittest
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
WEB_DIR = os.path.join(REPO_ROOT, "src", "web")

class TestWebApp(unittest.TestCase):

    def test_files_exist(self):
        """Verify that index.html, style.css, and app.js exist in src/web/."""
        self.assertTrue(os.path.isfile(os.path.join(WEB_DIR, "index.html")), "index.html missing in src/web/")
        self.assertTrue(os.path.isfile(os.path.join(WEB_DIR, "style.css")), "style.css missing in src/web/")
        self.assertTrue(os.path.isfile(os.path.join(WEB_DIR, "app.js")), "app.js missing in src/web/")

    def test_html_structure(self):
        """Verify index.html contains key elements and script bindings."""
        html_path = os.path.join(WEB_DIR, "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn('<script src="app.js"></script>', content)
        self.assertIn('id="song-search"', content)
        self.assertIn('id="song-list"', content)
        self.assertIn('id="paper"', content)
        self.assertIn('id="lyrics-view"', content)
        self.assertIn('id="mp3-audio"', content)
        self.assertIn('id="dl-pdf"', content)
        self.assertIn('id="dl-mp3"', content)
        self.assertIn('id="dl-lyrics-pdf"', content)
        self.assertIn('id="dl-lyrics-md"', content)

    def test_app_js_contents(self):
        """Verify app.js contains catalog fetching and abcjs score rendering logic."""
        js_path = os.path.join(WEB_DIR, "app.js")
        with open(js_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("loadCatalog", content)
        self.assertIn("ABCJS.renderAbc", content)
        self.assertIn("ABCJS.synth", content)
        self.assertIn("selectSong", content)
        self.assertIn("formatMarkdownLyrics", content)

    def test_css_sidebar_scroll_structure(self):
        """Verify style.css sets flex container and overflow on catalog-container and song-list for smooth scrolling."""
        css_path = os.path.join(WEB_DIR, "style.css")
        with open(css_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn(".catalog-container", content)
        self.assertIn("min-height: 0", content)
        self.assertIn("overflow-y: auto", content)

if __name__ == "__main__":
    unittest.main()
