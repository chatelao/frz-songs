#!/usr/bin/env bash
# src/install.sh - Install build toolchain dependencies for French Songs Collection

set -euo pipefail

echo "==> Installing build dependencies for French Songs Collection..."

SUDO=""
if [ "$(id -u)" -ne 0 ]; then
  if command -v sudo >/dev/null 2>&1; then
    SUDO="sudo"
  else
    echo "Error: This script requires root privileges or sudo." >&2
    exit 1
  fi
fi

# Update apt package index
$SUDO apt-get update -y

# Install build dependencies:
# - lilypond: Master score compiler & MIDI generator
# - python3, python3-pip, python3-ly: Python AST parser for LilyPond and scripting
# - fluidsynth, fluid-soundfont-gm: Software synthesizer & GM SoundFont for acoustic piano audio synthesis
# - lame: MP3 encoder
$SUDO apt-get install -y --no-install-recommends \
  lilypond \
  python3 \
  python3-pip \
  python3-ly \
  fluidsynth \
  fluid-soundfont-gm \
  lame \
  ca-certificates \
  curl

# Ensure python-ly, fpdf2 and pypdf libraries are accessible in current python environment
if command -v python3 >/dev/null 2>&1; then
  python3 -c "import ly" 2>/dev/null || python3 -m pip install python-ly --quiet || true
  python3 -c "import fpdf" 2>/dev/null || python3 -m pip install fpdf2 --quiet || true
  python3 -c "import pypdf" 2>/dev/null || python3 -m pip install pypdf --quiet || true
fi

echo "==> Build dependencies installed successfully!"
