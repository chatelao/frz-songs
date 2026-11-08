#!/usr/bin/env python3
"""
generate_booklet.py - Generates a consolidated French songs booklet PDF.
Includes:
1. Cover page with festive vector graphics and typography.
2. All song sheet music scores with dynamic page numbering overlay.
3. Table of Contents (Inhaltsverzeichnis) placed at the end of the booklet.
"""

import os
import sys
import math
import io
import json
import re
from fpdf import FPDF
import pypdf

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../.."))
BUILD_DIR = os.path.join(REPO_ROOT, "build")
PDF_DIR = os.path.join(BUILD_DIR, "pdf")
SONGS_DIR = os.path.join(REPO_ROOT, "src", "songs")
CATALOG_PATH = os.path.join(BUILD_DIR, "catalog.json")

def sanitize_text(text):
    if not text:
        return ""
    replacements = {
        '’': "'",
        '‘': "'",
        '“': '"',
        '”': '"',
        '„': '"',
        '–': '-',
        '—': '-',
        '…': '...',
        'œ': 'oe',
        'Œ': 'Oe',
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

def draw_star(pdf, cx, cy, r_outer, r_inner, points=5, fill_color=(255, 215, 0)):
    pdf.set_fill_color(*fill_color)
    angle_step = math.pi / points
    coords = []
    start_angle = -math.pi / 2
    for i in range(2 * points):
        r = r_outer if i % 2 == 0 else r_inner
        ang = start_angle + i * angle_step
        x = cx + r * math.cos(ang)
        y = cy + r * math.sin(ang)
        coords.append((x, y))

    pdf.polygon(coords, style='F')

def create_cover_page():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)

    # French Bleu de France background
    pdf.set_fill_color(0, 35, 90)
    pdf.rect(0, 0, 210, 297, style='F')

    # Tricolore accent bar on top
    pdf.set_fill_color(0, 85, 164)
    pdf.rect(10, 10, 63, 6, style='F')
    pdf.set_fill_color(255, 255, 255)
    pdf.rect(73, 10, 64, 6, style='F')
    pdf.set_fill_color(239, 65, 53)
    pdf.rect(137, 10, 63, 6, style='F')

    # Gold Ornamental Double Border
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(1.2)
    pdf.rect(10, 10, 190, 277)
    pdf.set_line_width(0.4)
    pdf.rect(13, 13, 184, 271)

    corners = [(13, 13), (197, 13), (13, 284), (197, 284)]
    for cx, cy in corners:
        draw_star(pdf, cx, cy, 4, 1.8, points=4, fill_color=(255, 223, 0))

    stars = [
        (30, 45, 2.5), (180, 50, 3.0), (45, 70, 2.0), (165, 85, 2.8),
        (25, 120, 3.0), (185, 130, 2.2), (35, 170, 2.5), (175, 180, 3.2),
        (28, 230, 2.0), (182, 240, 2.8), (40, 265, 2.5), (170, 270, 2.0),
        (60, 55, 1.8), (150, 60, 2.0), (105, 35, 2.5)
    ]
    for sx, sy, sr in stars:
        draw_star(pdf, sx, sy, sr, sr * 0.45, points=4, fill_color=(255, 235, 150))

    # Main Title Header Banner
    pdf.set_y(45)
    pdf.set_font('Helvetica', 'B', 30)
    pdf.set_text_color(255, 220, 75)
    pdf.cell(0, 14, sanitize_text("Chansons Françaises"), align='C', new_x='LMARGIN', new_y='NEXT')

    # Subtitle
    pdf.set_y(63)
    pdf.set_font('Helvetica', 'I', 16)
    pdf.set_text_color(230, 235, 245)
    pdf.cell(0, 8, sanitize_text("Französische Lieder - Das Liederbuch"), align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_y(73)
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(200, 210, 225)
    pdf.cell(0, 6, sanitize_text("Noten, Akkorde, französischer Text & Liedtexte"), align='C', new_x='LMARGIN', new_y='NEXT')

    # Central Lyre / Emblem Representation
    lyre_y = 100
    pdf.set_draw_color(255, 220, 75)
    pdf.set_line_width(1.5)
    pdf.ellipse(75, lyre_y, 60, 70)
    pdf.set_fill_color(20, 45, 105)
    pdf.ellipse(78, lyre_y + 3, 54, 64, style='F')

    draw_star(pdf, 105, lyre_y + 35, 12, 5, points=5, fill_color=(255, 215, 0))

    # Ribbon
    ribbon_y = 195
    pdf.set_fill_color(180, 20, 40)
    pdf.rect(35, ribbon_y, 140, 18, style='F')
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(0.6)
    pdf.rect(35, ribbon_y, 140, 18)

    pdf.set_y(ribbon_y + 3)
    pdf.set_font('Helvetica', 'B', 13)
    pdf.set_text_color(255, 245, 220)
    pdf.cell(0, 12, sanitize_text("Ausgewählte Klassiker & moderne Hits"), align='C', new_x='LMARGIN', new_y='NEXT')

    # Features List
    pdf.set_y(225)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(215, 225, 240)
    pdf.cell(0, 5, sanitize_text("Von Kinderliedern über Chansons bis zu zeitgenössischem Pop"), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_y(232)
    pdf.cell(0, 5, sanitize_text("Melodielinien mit Akkordbezifferung und vollständigen Texten"), align='C', new_x='LMARGIN', new_y='NEXT')

    # Bottom Edition
    pdf.set_y(260)
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(212, 175, 55)
    pdf.cell(0, 5, sanitize_text("Open Source Musiksammlung"), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.set_y(266)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(180, 190, 205)
    pdf.cell(0, 5, sanitize_text("GNU LilyPond Edition | Vollständiges Liederbuch"), align='C', new_x='LMARGIN', new_y='NEXT')

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return pypdf.PdfReader(buf).pages[0]

def create_page_number_overlay(page_number, total_pages=None):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=False)
    pdf.set_y(285)
    pdf.set_font('Helvetica', '', 9)
    pdf.set_text_color(100, 100, 100)
    text = f"- {page_number} -"
    pdf.cell(0, 8, text, align='C')

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    return pypdf.PdfReader(buf).pages[0]

class TOCPDF(FPDF):
    def __init__(self, start_page_num=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_page_num = start_page_num

    def footer(self):
        self.set_y(285)
        self.set_font('Helvetica', '', 9)
        self.set_text_color(100, 100, 100)
        curr = self.start_page_num + self.page_no() - 1
        self.cell(0, 8, f"- {curr} -", align='C')

def create_toc_pages(song_entries, start_page_num):
    pdf = TOCPDF(start_page_num)
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()

    # Decorative header
    pdf.set_draw_color(212, 175, 55)
    pdf.set_line_width(0.8)
    pdf.line(20, 20, 190, 20)

    pdf.set_y(24)
    pdf.set_font('Helvetica', 'B', 22)
    pdf.set_text_color(20, 35, 65)
    pdf.cell(0, 12, sanitize_text("Inhaltsverzeichnis / Sommaire"), align='C', new_x='LMARGIN', new_y='NEXT')

    pdf.set_font('Helvetica', 'I', 11)
    pdf.set_text_color(110, 110, 110)
    pdf.cell(0, 7, sanitize_text("Übersicht aller Lieder der Sammlung"), align='C', new_x='LMARGIN', new_y='NEXT')
    pdf.ln(4)

    pdf.set_line_width(0.4)
    pdf.line(20, 48, 190, 48)
    pdf.set_y(54)

    for idx, title, composer, page_num in song_entries:
        if pdf.get_y() > 260:
            pdf.add_page()
            pdf.set_draw_color(212, 175, 55)
            pdf.set_line_width(0.8)
            pdf.line(20, 20, 190, 20)

            pdf.set_y(24)
            pdf.set_font('Helvetica', 'B', 18)
            pdf.set_text_color(20, 35, 65)
            pdf.cell(0, 10, sanitize_text("Inhaltsverzeichnis (Fortsetzung)"), align='C', new_x='LMARGIN', new_y='NEXT')
            pdf.ln(4)
            pdf.set_line_width(0.4)
            pdf.line(20, 40, 190, 40)
            pdf.set_y(46)

        y = pdf.get_y()
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(30, 30, 30)

        num_str = f"{idx}."
        pdf.set_xy(20, y)
        pdf.cell(10, 7, num_str)

        pdf.set_xy(30, y)
        clean_title = sanitize_text(title)
        pdf.cell(90, 7, clean_title)

        pdf.set_font('Helvetica', 'I', 9)
        pdf.set_text_color(110, 110, 110)
        clean_comp = sanitize_text(composer)
        if len(clean_comp) > 35:
            clean_comp = clean_comp[:32] + "..."
        pdf.cell(48, 7, clean_comp)

        # Leader dots
        pdf.set_xy(168, y)
        pdf.set_font('Helvetica', '', 10)
        pdf.set_text_color(140, 140, 140)
        pdf.cell(8, 7, "...", align='R')

        # Page number
        pdf.set_xy(176, y)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(20, 35, 65)
        pdf.cell(14, 7, str(page_num), align='R')

        pdf.set_y(y + 8)

    buf = io.BytesIO()
    pdf.output(buf)
    buf.seek(0)
    reader = pypdf.PdfReader(buf)
    return list(reader.pages)

def load_songs_catalog():
    if os.path.exists(CATALOG_PATH):
        try:
            with open(CATALOG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get("songs", [])
        except Exception as e:
            print(f"Warning: Failed to load catalog from {CATALOG_PATH}: {e}")

    songs = []
    if os.path.exists(SONGS_DIR):
        dirs = sorted([d for d in os.listdir(SONGS_DIR) if os.path.isdir(os.path.join(SONGS_DIR, d))])
        for idx, sid in enumerate(dirs, start=1):
            ly_path = os.path.join(SONGS_DIR, sid, f"{sid}.ly")
            headers = {}
            if os.path.exists(ly_path):
                from generate_catalog import parse_lilypond_headers
                headers = parse_lilypond_headers(ly_path)
            songs.append({
                "id": sid,
                "number": idx,
                "title": headers.get("title", sid.replace('_', ' ').title()),
                "composer": headers.get("composer", "Traditionnel")
            })
    return songs

def generate_booklet(output_pdf_path=None):
    if output_pdf_path is None:
        output_pdf_path = os.path.join(PDF_DIR, "franzosische_lieder_liederbuch.pdf")

    os.makedirs(os.path.dirname(output_pdf_path), exist_ok=True)
    print(f"==> Generating complete French Songs Booklet: '{output_pdf_path}'...")

    songs_data = load_songs_catalog()
    if not songs_data:
        print("Error: No song records found to compile booklet.")
        return False

    writer = pypdf.PdfWriter()

    print("    [1/3] Rendering cover page with vector graphics...")
    cover_page = create_cover_page()
    writer.add_page(cover_page)

    current_page = 2
    song_toc_entries = []

    print("    [2/3] Merging song sheet music pages and stamping page numbers...")
    for song in songs_data:
        song_id = song.get("id")
        title = song.get("title", song_id)
        composer = song.get("composer", "")
        number = song.get("number", len(song_toc_entries) + 1)

        song_pdf_file = os.path.join(PDF_DIR, f"{song_id}.pdf")
        if not os.path.exists(song_pdf_file):
            print(f"    Warning: Missing PDF for song '{song_id}', skipping in booklet.")
            continue

        reader = pypdf.PdfReader(song_pdf_file)
        start_song_page = current_page
        song_toc_entries.append((number, title, composer, start_song_page))

        for page in reader.pages:
            overlay_page = create_page_number_overlay(current_page)
            new_page = writer.add_page(page)
            new_page.merge_page(overlay_page)
            current_page += 1

    print(f"    [3/3] Generating Table of Contents at page {current_page}...")
    toc_pages = create_toc_pages(song_toc_entries, start_page_num=current_page)
    for toc_page in toc_pages:
        writer.add_page(toc_page)
        current_page += 1

    with open(output_pdf_path, 'wb') as f:
        writer.write(f)

    booklet_alias = os.path.join(PDF_DIR, "booklet.pdf")
    try:
        if os.path.exists(booklet_alias):
            os.remove(booklet_alias)
        with open(booklet_alias, 'wb') as f:
            with open(output_pdf_path, 'rb') as src_f:
                f.write(src_f.read())
    except Exception as e:
        print(f"Notice: Could not write booklet alias: {e}")

    total_pages = len(writer.pages)
    print(f"==> Successfully generated booklet: {output_pdf_path} ({total_pages} pages).")
    return True

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else None
    generate_booklet(out)
