#!/usr/bin/env python3
"""
ly2lyrics.py - LilyPond to Pure Text Lyrics & PDF Converter.
Extracts lyrics stanzas from LilyPond (.ly) files and generates:
1. Pure text Markdown file (.md)
2. Standalone text-only Lyrics PDF (.pdf)
"""

import sys
import os
import re
from fpdf import FPDF

def parse_header(content):
    headers = {
        "title": "Unbekanntes Lied",
        "composer": "Volkslied",
        "poet": ""
    }
    match = re.search(r'\\header\s*\{([^}]+)\}', content, re.DOTALL)
    if match:
        block = match.group(1)
        for line in block.splitlines():
            line = line.strip()
            if '=' in line:
                k, v = line.split('=', 1)
                k = k.strip().lower()
                v = v.strip().strip('"').strip("'")
                headers[k] = v
    return headers

def clean_lyric_line(raw_line):
    # Remove LilyPond comments
    raw_line = re.sub(r'%.*', '', raw_line).strip()
    if not raw_line:
        return ""
    # Remove \set or \override or \markup commands
    raw_line = re.sub(r'\\set\s+[^=]+=[^ ]+', '', raw_line)
    raw_line = re.sub(r'\\override\s+[^=]+=[^ ]+', '', raw_line)
    raw_line = re.sub(r'\\markup\s*\{[^}]*\}', '', raw_line)

    tokens = raw_line.split()
    cleaned_tokens = []
    for t in tokens:
        if t.startswith('\\'):
            continue
        cleaned_tokens.append(t)

    text = " ".join(cleaned_tokens)
    # Join hyphens: e.g. "Al -- le" -> "Alle"
    text = re.sub(r'\s+--\s+', '', text)
    # Remove standalone ties or underscores
    text = re.sub(r'\s+__?\s+', ' ', text)
    text = re.sub(r'__?', '', text)

    return text.strip()

def extract_stanzas(content):
    blocks = []

    matches = re.findall(r'([a-zA-Z0-9_]+)\s*=\s*\\lyricmode\s*\{([^}]+)\}', content, re.DOTALL)
    if matches:
        for name, body in matches:
            blocks.append((name, body))
    else:
        matches2 = re.findall(r'\\(?:lyricmode|addlyrics)\s*\{([^}]+)\}', content, re.DOTALL)
        for idx, body in enumerate(matches2, start=1):
            blocks.append((f"verse{idx}", body))

    stanzas = []
    for idx, (name, body) in enumerate(blocks, start=1):
        lines = []
        for raw_line in body.splitlines():
            line = clean_lyric_line(raw_line)
            if line:
                lines.append(line)
        if lines:
            stanzas.append((idx, lines))

    return stanzas

def generate_markdown(headers, stanzas):
    title = headers.get('title', 'Unbekanntes Lied')
    composer = headers.get('composer', 'Volkslied')
    poet = headers.get('poet', '')

    md_lines = [f"# {title}", ""]

    meta_parts = []
    if composer:
        meta_parts.append(f"**Melodie:** {composer}")
    if poet:
        meta_parts.append(f"**Text:** {poet}")

    if meta_parts:
        md_lines.append(" | ".join(meta_parts))
        md_lines.append("")

    for stanza_num, lines in stanzas:
        md_lines.append(f"### {stanza_num}. Strophe")
        for line in lines:
            md_lines.append(line)
        md_lines.append("")

    return "\n".join(md_lines)

def sanitize_text_for_pdf(text):
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
        '…': '...'
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode('latin-1', 'replace').decode('latin-1')

class LyricsPDF(FPDF):
    def header(self):
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 9)
        self.cell(0, 10, f'Seite {self.page_no()}', align='C')

def generate_pdf(headers, stanzas, pdf_output_path):
    pdf = LyricsPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    title = sanitize_text_for_pdf(headers.get('title', 'Unbekanntes Lied'))
    composer = sanitize_text_for_pdf(headers.get('composer', 'Volkslied'))
    poet = sanitize_text_for_pdf(headers.get('poet', ''))

    # Title
    pdf.set_font('Helvetica', 'B', 18)
    pdf.cell(0, 12, title, new_x='LMARGIN', new_y='NEXT', align='C')
    pdf.ln(2)

    # Subtitle / Metadata
    pdf.set_font('Helvetica', 'I', 11)
    meta_str = []
    if composer:
        meta_str.append(f"Melodie: {composer}")
    if poet:
        meta_str.append(f"Text: {poet}")
    if meta_str:
        pdf.cell(0, 8, " | ".join(meta_str), new_x='LMARGIN', new_y='NEXT', align='C')
        pdf.ln(5)

    # Stanzas
    for stanza_num, lines in stanzas:
        pdf.set_font('Helvetica', 'B', 12)
        pdf.cell(0, 8, f"{stanza_num}. Strophe", new_x='LMARGIN', new_y='NEXT')
        pdf.set_font('Helvetica', '', 11)
        for line in lines:
            pdf.cell(0, 6, sanitize_text_for_pdf(line), new_x='LMARGIN', new_y='NEXT')
        pdf.ln(4)

    os.makedirs(os.path.dirname(os.path.abspath(pdf_output_path)), exist_ok=True)
    pdf.output(pdf_output_path)

def main():
    if len(sys.argv) < 4:
        print("Usage: python3 ly2lyrics.py <input.ly> <output.md> <output.pdf>")
        sys.exit(1)

    input_ly = sys.argv[1]
    output_md = sys.argv[2]
    output_pdf = sys.argv[3]

    if not os.path.exists(input_ly):
        print(f"Error: '{input_ly}' does not exist.")
        sys.exit(1)

    with open(input_ly, 'r', encoding='utf-8') as f:
        ly_content = f.read()

    headers = parse_header(ly_content)
    stanzas = extract_stanzas(ly_content)

    md_content = generate_markdown(headers, stanzas)
    os.makedirs(os.path.dirname(os.path.abspath(output_md)), exist_ok=True)
    with open(output_md, 'w', encoding='utf-8') as f:
        f.write(md_content)

    generate_pdf(headers, stanzas, output_pdf)

    print(f"Successfully generated lyrics MD ('{output_md}') and PDF ('{output_pdf}').")

if __name__ == "__main__":
    main()
