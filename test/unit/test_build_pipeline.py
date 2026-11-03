import unittest
import os
import json
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
SONGS_DIR = os.path.join(REPO_ROOT, "src", "songs")

EXPECTED_SONGS = sorted([
    d for d in os.listdir(SONGS_DIR)
    if os.path.isdir(os.path.join(SONGS_DIR, d))
])

class TestBuildPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Run build pipeline
        build_script = os.path.join(REPO_ROOT, "src", "scripts", "build_pipeline.sh")
        res = subprocess.run([build_script], capture_output=True, text=True)
        assert res.returncode == 0, f"Build pipeline failed with output:\n{res.stderr}"

    def test_pdf_generation_for_all_songs(self):
        for song_id in EXPECTED_SONGS:
            pdf_path = os.path.join(REPO_ROOT, "build", "pdf", f"{song_id}.pdf")
            self.assertTrue(os.path.exists(pdf_path), f"PDF asset for {song_id} does not exist")
            self.assertGreater(os.path.getsize(pdf_path), 0, f"PDF asset for {song_id} is empty")

    def test_abc_generation_for_all_songs(self):
        for song_id in EXPECTED_SONGS:
            abc_path = os.path.join(REPO_ROOT, "build", "abc", f"{song_id}.abc")
            self.assertTrue(os.path.exists(abc_path), f"ABC asset for {song_id} does not exist")
            self.assertGreater(os.path.getsize(abc_path), 0, f"ABC asset for {song_id} is empty")

            with open(abc_path, 'r', encoding='utf-8') as f:
                content = f.read()
                self.assertIn("X:1", content)
                self.assertIn("T:", content)

    def test_mp3_generation_for_all_songs(self):
        for song_id in EXPECTED_SONGS:
            mp3_path = os.path.join(REPO_ROOT, "build", "mp3", f"{song_id}.mp3")
            self.assertTrue(os.path.exists(mp3_path), f"MP3 asset for {song_id} does not exist")
            self.assertGreater(os.path.getsize(mp3_path), 0, f"MP3 asset for {song_id} is empty")

    def test_midi_generation_for_all_songs(self):
        for song_id in EXPECTED_SONGS:
            midi_path = os.path.join(REPO_ROOT, "build", "midi", f"{song_id}.midi")
            if not os.path.exists(midi_path):
                midi_path = os.path.join(REPO_ROOT, "build", "midi", f"{song_id}.mid")
            self.assertTrue(os.path.exists(midi_path), f"MIDI asset for {song_id} does not exist")
            self.assertGreater(os.path.getsize(midi_path), 0, f"MIDI asset for {song_id} is empty")

    def test_lyrics_md_generation_for_all_songs(self):
        for song_id in EXPECTED_SONGS:
            md_path = os.path.join(REPO_ROOT, "build", "lyrics", f"{song_id}.md")
            self.assertTrue(os.path.exists(md_path), f"Lyrics MD asset for {song_id} does not exist")
            self.assertGreater(os.path.getsize(md_path), 0, f"Lyrics MD asset for {song_id} is empty")

    def test_lyrics_pdf_generation_for_all_songs(self):
        for song_id in EXPECTED_SONGS:
            pdf_path = os.path.join(REPO_ROOT, "build", "lyrics_pdf", f"{song_id}_lyrics.pdf")
            self.assertTrue(os.path.exists(pdf_path), f"Lyrics PDF asset for {song_id} does not exist")
            self.assertGreater(os.path.getsize(pdf_path), 0, f"Lyrics PDF asset for {song_id} is empty")

    def test_catalog_json_generation(self):
        catalog_path = os.path.join(REPO_ROOT, "build", "catalog.json")
        self.assertTrue(os.path.exists(catalog_path), "catalog.json does not exist")

        with open(catalog_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.assertIn("songs", data)
            self.assertEqual(data["count"], len(EXPECTED_SONGS))

            catalog_song_ids = [song["id"] for song in data["songs"]]
            for song_id in EXPECTED_SONGS:
                self.assertIn(song_id, catalog_song_ids)

            for song in data["songs"]:
                self.assertIsNotNone(song["assets"]["pdf"])
                self.assertIsNotNone(song["assets"]["abc"])
                self.assertIsNotNone(song["assets"]["mp3"])
                self.assertIsNotNone(song["assets"]["midi"])
                self.assertIsNotNone(song["assets"]["lyrics_md"])
                self.assertIsNotNone(song["assets"]["lyrics_pdf"])
                self.assertIsNotNone(song["assets"]["ly"])

    def test_site_assembly_all_formats(self):
        site_dir = os.path.join(REPO_ROOT, "build", "site")
        self.assertTrue(os.path.exists(site_dir))
        for format_dir in ["pdf", "abc", "mp3", "midi", "lyrics", "lyrics_pdf", "src/songs"]:
            path = os.path.join(site_dir, format_dir)
            self.assertTrue(os.path.exists(path), f"Site format directory missing: {format_dir}")

if __name__ == "__main__":
    unittest.main()
