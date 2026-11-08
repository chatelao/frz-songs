"""
test_web_player_e2e.py - Playwright E2E integration test suite for French Songs Web Player.
"""

import os
import sys
import time
import socket
import threading
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "screenshots")

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]

class QuietHTTPRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_ROOT, **kwargs)

    def log_message(self, format, *args):
        pass

class TestWebPlayerE2E(unittest.TestCase):
    server = None
    server_thread = None
    port = None
    playwright = None
    browser = None

    @classmethod
    def setUpClass(cls):
        os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
        cls.port = find_free_port()
        cls.server = HTTPServer(('127.0.0.1', cls.port), QuietHTTPRequestHandler)
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()

        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=True)

    @classmethod
    def tearDownClass(cls):
        if cls.browser:
            cls.browser.close()
        if cls.playwright:
            cls.playwright.stop()
        if cls.server:
            cls.server.shutdown()
            cls.server.server_close()

    def setUp(self):
        self.context = self.browser.new_context(
            viewport={'width': 1280, 'height': 800}
        )
        self.page = self.context.new_page()
        self.app_url = f"http://127.0.0.1:{self.port}/src/web/index.html"

    def tearDown(self):
        self.context.close()

    def test_catalog_loading_and_first_carol(self):
        """Verify web player loads catalog and auto-selects first song."""
        self.page.goto(self.app_url)
        self.page.wait_for_selector("#song-list .song-item", timeout=5000)

        title = self.page.title()
        self.assertIn("Französische Lieder", title)

        song_items = self.page.query_selector_all("#song-list .song-item")
        self.assertEqual(len(song_items), 11)

        active_title = self.page.locator("#current-song-title").text_content()
        self.assertIn("Frère Jacques", active_title)

        # Screenshot initial state
        self.page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "01_initial_catalog.png"))

    def test_score_rendering(self):
        """Verify ABC score SVG rendering in paper container."""
        self.page.goto(self.app_url)
        self.page.wait_for_selector("#paper svg", timeout=5000)

        svg = self.page.locator("#paper svg")
        self.assertTrue(svg.is_visible())

        # Screenshot rendered score
        self.page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "02_score_rendered.png"))

    def test_search_and_select_carol(self):
        """Verify search filtering and selecting 'Santiano'."""
        self.page.goto(self.app_url)
        self.page.wait_for_selector("#song-list .song-item", timeout=5000)

        # Type in search
        self.page.fill("#song-search", "Santiano")
        self.page.wait_for_timeout(300)

        filtered_items = self.page.query_selector_all("#song-list .song-item")
        self.assertGreaterEqual(len(filtered_items), 1)

        # Click Santiano
        self.page.click("#song-list .song-item:has-text('Santiano')")
        self.page.wait_for_timeout(500)

        active_title = self.page.locator("#current-song-title").text_content()
        self.assertIn("Santiano", active_title)

        # Check score SVG updated
        self.page.wait_for_selector("#paper svg", timeout=5000)
        self.assertTrue(self.page.locator("#paper svg").is_visible())

        self.page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "03_search_santiano.png"))

    def test_audio_playback_controls(self):
        """Verify Play / Stop buttons and Tempo slider controls."""
        self.page.goto(self.app_url)
        self.page.wait_for_selector("#paper svg", timeout=5000)
        self.page.wait_for_selector("#btn-play", timeout=5000)

        # Play
        self.page.click("#btn-play")
        self.page.wait_for_selector("#btn-play.playing", timeout=5000)
        btn_text = self.page.locator("#btn-play").text_content()
        self.assertIn("Pause", btn_text)

        # Stop
        self.page.click("#btn-stop")
        self.page.wait_for_timeout(300)
        btn_text = self.page.locator("#btn-play").text_content()
        self.assertIn("Abspielen", btn_text)

        # Tempo slider
        self.page.fill("#tempo-slider", "120")
        self.page.dispatch_event("#tempo-slider", "input")
        self.page.wait_for_timeout(200)

        tempo_val = self.page.locator("#tempo-value").text_content()
        self.assertEqual(tempo_val, "120%")

    def test_view_tab_toggle(self):
        """Verify switching between Sheet Music score view and Pure Text lyrics view."""
        self.page.goto(self.app_url)
        self.page.wait_for_selector("#toggle-lyrics", timeout=5000)

        # Switch to Lyrics tab
        self.page.click("#toggle-lyrics")
        self.page.wait_for_timeout(500)

        lyrics_view = self.page.locator("#lyrics-view")
        self.assertTrue(lyrics_view.is_visible())

        # Check lyrics content rendered
        lyrics_content = self.page.locator("#lyrics-content").text_content()
        self.assertTrue(len(lyrics_content) > 0)

        self.page.screenshot(path=os.path.join(SCREENSHOTS_DIR, "04_lyrics_view.png"))

        # Switch back to Score tab
        self.page.click("#toggle-score")
        self.page.wait_for_timeout(500)

        score_view = self.page.locator("#score-view")
        self.assertTrue(score_view.is_visible())

    def test_sidebar_scroll_reachability(self):
        """Verify that scrolling the song list in the sidebar smoothly displays all songs within the sidebar container."""
        self.page.goto(self.app_url)
        self.page.wait_for_selector("#song-list .song-item", timeout=5000)

        last_item = self.page.locator("#song-list .song-item").last
        self.page.evaluate("document.getElementById('song-list').scrollTop = document.getElementById('song-list').scrollHeight")
        self.page.wait_for_timeout(300)

        self.assertTrue(last_item.is_visible())
        sidebar_box = self.page.locator(".sidebar").bounding_box()
        item_box = last_item.bounding_box()
        self.assertIsNotNone(sidebar_box)
        self.assertIsNotNone(item_box)
        self.assertLessEqual(item_box["y"] + item_box["height"], sidebar_box["y"] + sidebar_box["height"] + 5)

if __name__ == "__main__":
    unittest.main()
