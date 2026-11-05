#!/usr/bin/env python3
"""
ly2abc.py - LilyPond to ABC notation derivation script.
Converts LilyPond (.ly) master files into ABC (.abc) notation for browser rendering.
"""

import sys
import os
import re
import fractions
import ly.document
import ly.pitch.rel2abs

KEY_ALTERATIONS = {
    'C': {}, 'Am': {},
    'G': {'f': 1}, 'Em': {'f': 1},
    'D': {'f': 1, 'c': 1}, 'Bm': {'f': 1, 'c': 1},
    'A': {'f': 1, 'c': 1, 'g': 1}, 'F#m': {'f': 1, 'c': 1, 'g': 1},
    'E': {'f': 1, 'c': 1, 'g': 1, 'd': 1},
    'F': {'b': -1}, 'Dm': {'b': -1},
    'Bb': {'b': -1, 'e': -1}, 'Gm': {'b': -1, 'e': -1},
    'Eb': {'b': -1, 'e': -1, 'a': -1}, 'Cm': {'b': -1, 'e': -1, 'a': -1},
    'Ab': {'b': -1, 'e': -1, 'a': -1, 'd': -1}, 'Fm': {'b': -1, 'e': -1, 'a': -1, 'd': -1},
}

NOTE_PITCH_MAP = {
    'c': ('c', 0), 'cis': ('c', 1), 'des': ('d', -1),
    'd': ('d', 0), 'dis': ('d', 1), 'es': ('e', -1), 'ees': ('e', -1),
    'e': ('e', 0),
    'f': ('f', 0), 'fis': ('f', 1), 'ges': ('g', -1),
    'g': ('g', 0), 'gis': ('g', 1), 'as': ('a', -1), 'aes': ('a', -1),
    'a': ('a', 0), 'ais': ('a', 1), 'bes': ('b', -1), 'b': ('b', 0), 'bis': ('b', 1)
}

def parse_lilypond_header(content):
    headers = {}
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
    return headers

def parse_time_signature(content):
    m = re.search(r'\\time\s+([0-9]+/[0-9]+)', content)
    if m:
        return m.group(1)
    return "4/4"

def parse_key_signature(content):
    m = re.search(r'\\key\s+([a-gA-G](?:es|is|s)?)\s+\\([a-zA-Z]+)', content)
    if m:
        note = m.group(1).lower()
        mode = m.group(2).lower()

        note_map = {
            'c': 'C', 'cis': 'C#', 'des': 'Db',
            'd': 'D', 'dis': 'D#', 'es': 'Eb', 'ees': 'Eb',
            'e': 'E',
            'f': 'F', 'fis': 'F#', 'ges': 'Gb',
            'g': 'G', 'gis': 'G#', 'as': 'Ab', 'aes': 'Ab',
            'a': 'A', 'ais': 'A#', 'bes': 'Bb', 'b': 'B', 'bis': 'B#'
        }
        abc_note = note_map.get(note, 'C')
        if mode in ['major', 'dur']:
            return abc_note
        elif mode in ['minor', 'moll']:
            return abc_note + "m"
        return abc_note
    return "C"

def parse_tempo(content):
    m = re.search(r'\\tempo\s+([0-9]+(?:\.)?)\s*=\s*([0-9]+)', content)
    if m:
        base, bpm = m.group(1), m.group(2)
        if '.' in base:
            denom = int(base.replace('.', '')) * 2
            return f"3/{denom}={bpm}"
        return f"1/{base}={bpm}"
    return "1/4=100"

def lilypond_duration_to_fraction(dur_str, prev_frac):
    if not dur_str:
        return prev_frac
    dots = dur_str.count('.')
    base_num = int(dur_str.replace('.', ''))
    frac = fractions.Fraction(1, base_num)
    dot_val = frac / 2
    for _ in range(dots):
        frac += dot_val
        dot_val /= 2
    return frac

def fraction_to_abc_multiplier(frac, unit_frac):
    mult = frac / unit_frac
    if mult == 1:
        return ""
    if mult.denominator == 1:
        return str(mult.numerator)
    if mult.numerator == 1:
        return f"/{mult.denominator}"
    return f"{mult.numerator}/{mult.denominator}"

def pitch_to_abc(pitch_step, ly_alter, octaves, key_name):
    if octaves <= 0:
        base_char = pitch_step.upper()
        oct_marks = ',' * (-octaves)
    else:
        base_char = pitch_step.lower()
        oct_marks = "'" * (octaves - 1)

    key_alt = KEY_ALTERATIONS.get(key_name, {}).get(pitch_step, 0)
    accidental = ""
    if ly_alter != key_alt:
        if ly_alter == 1:
            accidental = "^"
        elif ly_alter == -1:
            accidental = "_"
        elif ly_alter == 0:
            accidental = "="
        elif ly_alter == 2:
            accidental = "^^"
        elif ly_alter == -2:
            accidental = "__"

    return f"{accidental}{base_char}{oct_marks}"

def extract_bars_and_note_counts(ly_content, key_name, unit_frac=fractions.Fraction(1, 8)):
    # Resolves relative pitches to absolute pitches
    doc = ly.document.Document(ly_content)
    cursor = ly.document.Cursor(doc)
    ly.pitch.rel2abs.rel2abs(cursor)
    abs_content = doc.plaintext()

    m = re.search(r'(?:soprano|melody)\s*=\s*\{([^}]+)\}', abs_content, re.DOTALL)
    if not m:
        m = re.search(r'\{([^}]+)\}', abs_content, re.DOTALL)
    notes_text = m.group(1) if m else abs_content

    # Remove comments
    notes_text = re.sub(r'%.*', '', notes_text)

    tokens = notes_text.split()
    bars = []
    current_bar = []
    prev_frac = fractions.Fraction(1, 4)

    for tok in tokens:
        tok = tok.strip()
        if not tok or tok.startswith('\\') or tok in ['}', '\\bar', '"|."']:
            continue
        if tok == '|':
            if current_bar:
                bars.append(current_bar)
                current_bar = []
            continue

        clean_tok = re.sub(r'[\(\)\~\.\!]', '', tok)

        m_rest = re.match(r'^r([0-9]*\.?)$', clean_tok)
        if m_rest:
            dur_str = m_rest.group(1)
            frac = lilypond_duration_to_fraction(dur_str, prev_frac)
            prev_frac = frac
            dur_abc = fraction_to_abc_multiplier(frac, unit_frac)
            current_bar.append((f"z{dur_abc}", False))
            continue

        m_note = re.match(r'^([a-gA-G](?:es|is|s)?)([\'\,]*)([0-9]*\.?)$', clean_tok)
        if m_note:
            pitch_str = m_note.group(1).lower()
            octave_str = m_note.group(2)
            dur_str = m_note.group(3)

            frac = lilypond_duration_to_fraction(dur_str, prev_frac)
            prev_frac = frac
            dur_abc = fraction_to_abc_multiplier(frac, unit_frac)

            if pitch_str in NOTE_PITCH_MAP:
                step, alter = NOTE_PITCH_MAP[pitch_str]
                net_octaves = octave_str.count("'") - octave_str.count(",") - 1
                abc_pitch = pitch_to_abc(step, alter, net_octaves, key_name)
                current_bar.append((f"{abc_pitch}{dur_abc}", True))

    if current_bar:
        bars.append(current_bar)

    return bars

def extract_stanzas(content):
    stanzas = []
    matches = re.findall(r'([a-zA-Z0-9_]+)\s*=\s*\\lyricmode\s*\{([^}]+)\}', content, re.DOTALL)
    if not matches:
        matches = [(f"verse{i+1}", body) for i, body in enumerate(re.findall(r'\\lyricmode\s*\{([^}]+)\}', content, re.DOTALL))]

    for name, body in matches:
        tokens = [t for t in body.split() if not t.startswith('%')]
        syllables = []
        i = 0
        while i < len(tokens):
            tok = tokens[i]
            if tok == '--':
                i += 1
                continue
            if tok.startswith('\\') or tok in ['}', '{']:
                i += 1
                continue
            if i + 1 < len(tokens) and tokens[i+1] == '--':
                syllables.append(tok + '-')
                i += 2
            else:
                syllables.append(tok)
                i += 1
        if syllables:
            stanzas.append((name, syllables))
    return stanzas

def ly2abc(ly_content):
    headers = parse_lilypond_header(ly_content)
    title = headers.get('title', 'Unbekanntes Lied')
    composer = headers.get('composer', 'Volkslied')
    poet = headers.get('poet', '')
    meter = parse_time_signature(ly_content)
    key = parse_key_signature(ly_content)
    tempo = parse_tempo(ly_content)

    abc_lines = [
        "X:1",
        f"T:{title}",
        f"C:{composer}",
    ]
    if poet:
        abc_lines.append(f"O:{poet}")
    abc_lines.extend([
        f"M:{meter}",
        "L:1/8",
        f"Q:{tempo}",
        f"K:{key}",
        "V:1 clef=treble",
    ])

    bars = extract_bars_and_note_counts(ly_content, key)
    stanzas = extract_stanzas(ly_content)

    BARS_PER_SYSTEM = 4
    system_chunks = [bars[i:i + BARS_PER_SYSTEM] for i in range(0, len(bars), BARS_PER_SYSTEM)]
    stanza_indices = {name: 0 for name, _ in stanzas}

    for chunk in system_chunks:
        music_line_parts = []
        for bar in chunk:
            bar_tokens = [tok for tok, is_n in bar]
            music_line_parts.append(" ".join(bar_tokens))

        abc_lines.append(" | ".join(music_line_parts) + " |")

        for name, syllables in stanzas:
            cur_idx = stanza_indices[name]
            chunk_syls = []
            for bar in chunk:
                bar_syl_list = []
                for tok, is_n in bar:
                    if is_n:
                        if cur_idx < len(syllables):
                            bar_syl_list.append(syllables[cur_idx])
                            cur_idx += 1
                        else:
                            bar_syl_list.append("*")
                chunk_syls.append(" ".join(bar_syl_list))
            stanza_indices[name] = cur_idx
            abc_lines.append("w: " + " | ".join(chunk_syls) + " |")

    return "\n".join(abc_lines) + "\n"

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 ly2abc.py <input.ly> <output.abc>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)

    with open(input_file, 'r', encoding='utf-8') as f:
        ly_content = f.read()

    abc_content = ly2abc(ly_content)

    os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(abc_content)

    print(f"Successfully converted '{input_file}' to '{output_file}'.")

if __name__ == "__main__":
    main()
