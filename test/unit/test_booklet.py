import unittest
import os
import pypdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
BUILD_DIR = os.path.join(REPO_ROOT, "build")
PDF_DIR = os.path.join(BUILD_DIR, "pdf")
BOOKLET_PATH = os.path.join(PDF_DIR, "franzosische_lieder_liederbuch.pdf")
SONGS_DIR = os.path.join(REPO_ROOT, "src", "songs")

EXPECTED_SONG_COUNT = len([
    d for d in os.listdir(SONGS_DIR)
    if os.path.isdir(os.path.join(SONGS_DIR, d))
])

class TestBookletGeneration(unittest.TestCase):

    def test_booklet_exists_and_not_empty(self):
        self.assertTrue(os.path.exists(BOOKLET_PATH), f"Booklet PDF not found at {BOOKLET_PATH}")
        self.assertGreater(os.path.getsize(BOOKLET_PATH), 10000, "Booklet PDF is smaller than expected")

    def test_booklet_pages_and_structure(self):
        reader = pypdf.PdfReader(BOOKLET_PATH)
        total_pages = len(reader.pages)

        # Total pages should be:
        # 1 cover page + EXPECTED_SONG_COUNT song pages + at least 1 TOC page
        self.assertGreaterEqual(total_pages, 1 + EXPECTED_SONG_COUNT + 1)

        # Check cover page (Page 1)
        cover_page = reader.pages[0]
        cover_text = cover_page.extract_text() or ""
        self.assertIn("Chansons Françaises", cover_text)

        # Check TOC is at the end of the booklet
        last_page = reader.pages[-1]
        last_page_text = last_page.extract_text() or ""

        self.assertIn("Inhaltsverzeichnis", last_page_text)
        self.assertIn("Frère Jacques", last_page_text)

    def test_booklet_alias_exists(self):
        alias_path = os.path.join(PDF_DIR, "booklet.pdf")
        self.assertTrue(os.path.exists(alias_path), f"Booklet alias not found at {alias_path}")
        self.assertEqual(os.path.getsize(alias_path), os.path.getsize(BOOKLET_PATH))

    def test_site_booklet_exists(self):
        site_booklet = os.path.join(BUILD_DIR, "site", "pdf", "franzosische_lieder_liederbuch.pdf")
        self.assertTrue(os.path.exists(site_booklet), f"Site booklet not found at {site_booklet}")
        self.assertGreater(os.path.getsize(site_booklet), 10000)

if __name__ == "__main__":
    unittest.main()
