#!/usr/bin/env bash
# src/scripts/build_pipeline.sh - Complete build & asset generation toolchain

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"

BUILD_DIR="${REPO_ROOT}/build"
PDF_DIR="${BUILD_DIR}/pdf"
ABC_DIR="${BUILD_DIR}/abc"
MIDI_DIR="${BUILD_DIR}/midi"
WAV_DIR="${BUILD_DIR}/wav"
MP3_DIR="${BUILD_DIR}/mp3"
LYRICS_DIR="${BUILD_DIR}/lyrics"
LYRICS_PDF_DIR="${BUILD_DIR}/lyrics_pdf"
SONGS_DIR="${REPO_ROOT}/src/songs"

SOUNDFONT="/usr/share/sounds/sf2/FluidR3_GM.sf2"
if [ ! -f "${SOUNDFONT}" ]; then
  SOUNDFONT="/usr/share/sounds/sf2/default-GM.sf2"
fi

echo "==> Preparing build output directories..."
mkdir -p "${PDF_DIR}" "${ABC_DIR}" "${MIDI_DIR}" "${WAV_DIR}" "${MP3_DIR}" "${LYRICS_DIR}" "${LYRICS_PDF_DIR}"

if [ ! -d "${SONGS_DIR}" ] || [ -z "$(ls -A "${SONGS_DIR}" 2>/dev/null)" ]; then
  echo "No song directories found in ${SONGS_DIR}."
  exit 0
fi

echo "==> Starting compilation pipeline..."

for song_dir in "${SONGS_DIR}"/*; do
  if [ -d "${song_dir}" ]; then
    song_id="$(basename "${song_dir}")"
    ly_file="${song_dir}/${song_id}.ly"

    if [ -f "${ly_file}" ]; then
      echo "--> Processing Song: ${song_id}"

      # 1. Compile PDF document
      echo "    [1/4] Compiling LilyPond PDF..."
      lilypond --pdf -o "${PDF_DIR}/${song_id}" "${ly_file}"

      # 2. Extract MIDI file
      echo "    [2/4] Extracting MIDI from LilyPond..."
      lilypond -dno-point-and-click -o "${MIDI_DIR}/${song_id}" "${ly_file}"

      # 3. Synthesize MIDI to WAV and encode to MP3
      mid_file="${MIDI_DIR}/${song_id}.midi"
      if [ ! -f "${mid_file}" ]; then
        mid_file="${MIDI_DIR}/${song_id}.mid"
      fi

      if [ -f "${mid_file}" ] && [ -f "${SOUNDFONT}" ]; then
        echo "    [3/4] Synthesizing SoundFont acoustic piano audio (WAV -> MP3)..."
        fluidsynth -ni -g 1.0 -F "${WAV_DIR}/${song_id}.wav" "${SOUNDFONT}" "${mid_file}" >/dev/null 2>&1 || true
        if [ -f "${WAV_DIR}/${song_id}.wav" ]; then
          lame --preset standard "${WAV_DIR}/${song_id}.wav" "${MP3_DIR}/${song_id}.mp3" >/dev/null 2>&1 || true
        fi
      else
        echo "    [3/4] Warning: MIDI file or SoundFont not found, skipping MP3 synthesis."
      fi

      # 4. Derive ABC Notation
      echo "    [4/5] Deriving ABC notation..."
      if [ -f "${SCRIPT_DIR}/ly2abc.py" ]; then
        python3 "${SCRIPT_DIR}/ly2abc.py" "${ly_file}" "${ABC_DIR}/${song_id}.abc" || true
      fi

      # 5. Extract Pure Text Lyrics and Compile Lyrics PDF
      echo "    [5/5] Extracting lyrics and compiling lyrics PDF..."
      if [ -f "${SCRIPT_DIR}/ly2lyrics.py" ]; then
        python3 "${SCRIPT_DIR}/ly2lyrics.py" "${ly_file}" "${LYRICS_DIR}/${song_id}.md" "${LYRICS_PDF_DIR}/${song_id}_lyrics.pdf" || true
      fi
    fi
  fi
done

# 5. Compile Complete Christmas Songs Booklet PDF (with Cover, Page Numbers & End TOC)
if [ -f "${SCRIPT_DIR}/generate_booklet.py" ]; then
  echo "==> Compiling complete Christmas Song Booklet PDF..."
  python3 "${SCRIPT_DIR}/generate_booklet.py" "${PDF_DIR}/franzosische_lieder_liederbuch.pdf" || true
fi

# 6. Generate Catalog Manifest
if [ -f "${SCRIPT_DIR}/generate_catalog.py" ]; then
  echo "==> Generating song catalog manifest build/catalog.json..."
  python3 "${SCRIPT_DIR}/generate_catalog.py"
fi

# 6. Assemble Site Package
SITE_DIR="${BUILD_DIR}/site"
echo "==> Assembling static site in ${SITE_DIR}..."
mkdir -p "${SITE_DIR}"
if [ -d "${REPO_ROOT}/src/web" ]; then
  cp -r "${REPO_ROOT}/src/web/"* "${SITE_DIR}/"
fi
if [ -f "${BUILD_DIR}/catalog.json" ]; then
  cp "${BUILD_DIR}/catalog.json" "${SITE_DIR}/"
fi

for sub in abc mp3 pdf midi lyrics lyrics_pdf; do
  if [ -d "${BUILD_DIR}/${sub}" ]; then
    mkdir -p "${SITE_DIR}/${sub}"
    cp -r "${BUILD_DIR}/${sub}/"* "${SITE_DIR}/${sub}/" 2>/dev/null || true
  fi
done

if [ -d "${REPO_ROOT}/src/songs" ]; then
  mkdir -p "${SITE_DIR}/src/songs"
  cp -r "${REPO_ROOT}/src/songs/"* "${SITE_DIR}/src/songs/" 2>/dev/null || true
fi

echo "==> Asset generation pipeline build complete!"
