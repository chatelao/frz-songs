#!/usr/bin/env python3
"""
generate_catalog.py - Scans src/songs/ and build outputs to construct build/catalog.json manifest.
"""

import os
import sys
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
SONGS_DIR = os.path.join(REPO_ROOT, "src", "songs")
BUILD_DIR = os.path.join(REPO_ROOT, "build")

def parse_lilypond_headers(ly_filepath):
    headers = {
        "title": os.path.basename(os.path.dirname(ly_filepath)).replace('_', ' ').title(),
        "composer": "Traditionnel",
        "poet": ""
    }
    if not os.path.exists(ly_filepath):
        return headers

    try:
        with open(ly_filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        header_match = re.search(r'\\header\s*\{([^}]+)\}', content, re.DOTALL)
        if header_match:
            header_block = header_match.group(1)
            for line in header_block.splitlines():
                line = line.strip()
                if '=' in line:
                    k, v = line.split('=', 1)
                    k = k.strip().lower()
                    v = v.strip().strip('"').strip("'")
                    headers[k] = v
    except Exception as e:
        print(f"Warning reading headers from {ly_filepath}: {e}")

    return headers

def generate_catalog():
    songs = []

    if not os.path.exists(SONGS_DIR):
        print(f"Warning: {SONGS_DIR} directory does not exist.")
        return

    song_dirs = sorted([d for d in os.listdir(SONGS_DIR) if os.path.isdir(os.path.join(SONGS_DIR, d))])

    for idx, song_id in enumerate(song_dirs, start=1):
        song_folder = os.path.join(SONGS_DIR, song_id)
        ly_file = os.path.join(song_folder, f"{song_id}.ly")

        headers = parse_lilypond_headers(ly_file)

        pdf_path = f"pdf/{song_id}.pdf"
        abc_path = f"abc/{song_id}.abc"
        mp3_path = f"mp3/{song_id}.mp3"
        midi_path = f"midi/{song_id}.midi"
        lyrics_md_path = f"lyrics/{song_id}.md"
        lyrics_pdf_path = f"lyrics_pdf/{song_id}_lyrics.pdf"
        ly_rel_path = f"src/songs/{song_id}/{song_id}.ly"

        entry = {
            "id": song_id,
            "number": idx,
            "title": headers.get("title", song_id.replace('_', ' ').title()),
            "composer": headers.get("composer", "Traditionnel"),
            "poet": headers.get("poet", ""),
            "assets": {
                "ly": ly_rel_path if os.path.exists(ly_file) else None,
                "pdf": pdf_path if os.path.exists(os.path.join(BUILD_DIR, pdf_path)) else None,
                "abc": abc_path if os.path.exists(os.path.join(BUILD_DIR, abc_path)) else None,
                "mp3": mp3_path if os.path.exists(os.path.join(BUILD_DIR, mp3_path)) else None,
                "midi": midi_path if os.path.exists(os.path.join(BUILD_DIR, midi_path)) else None,
                "lyrics_md": lyrics_md_path if os.path.exists(os.path.join(BUILD_DIR, lyrics_md_path)) else None,
                "lyrics_pdf": lyrics_pdf_path if os.path.exists(os.path.join(BUILD_DIR, lyrics_pdf_path)) else None,
            }
        }
        songs.append(entry)

    booklet_pdf = "pdf/franzosische_lieder_liederbuch.pdf"
    catalog_data = {
        "count": len(songs),
        "booklet": {
            "title": "Französische Lieder - Chansons Françaises - Das Liederbuch",
            "pdf": booklet_pdf if os.path.exists(os.path.join(BUILD_DIR, booklet_pdf)) else None
        },
        "songs": songs
    }

    os.makedirs(BUILD_DIR, exist_ok=True)
    catalog_path = os.path.join(BUILD_DIR, "catalog.json")

    with open(catalog_path, 'w', encoding='utf-8') as f:
        json.dump(catalog_data, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated song catalog at '{catalog_path}' ({len(songs)} song(s)).")

if __name__ == "__main__":
    generate_catalog()
