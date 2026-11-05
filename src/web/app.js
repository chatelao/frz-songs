/**
 * app.js - Interactive French Songs (Chansons Françaises) Web Player
 * Powered by abcjs and Web Audio API.
 */

document.addEventListener("DOMContentLoaded", () => {
  const state = {
    catalog: [],
    currentSong: null,
    abcString: "",
    visualObj: null,
    synthControl: null,
    isPlaying: false,
    tempoMultiplier: 1.0,
    activeTab: "score" // 'score' or 'lyrics'
  };

  // DOM Elements
  const songSearchInput = document.getElementById("song-search");
  const songListEl = document.getElementById("song-list");
  const songTitleEl = document.getElementById("current-song-title");
  const songMetaEl = document.getElementById("current-song-meta");
  const btnPlay = document.getElementById("btn-play");
  const btnStop = document.getElementById("btn-stop");
  const tempoSlider = document.getElementById("tempo-slider");
  const tempoValueEl = document.getElementById("tempo-value");
  const toggleScoreBtn = document.getElementById("toggle-score");
  const toggleLyricsBtn = document.getElementById("toggle-lyrics");
  const scoreViewEl = document.getElementById("score-view");
  const lyricsViewEl = document.getElementById("lyrics-view");
  const paperEl = document.getElementById("paper");
  const lyricsContentEl = document.getElementById("lyrics-content");
  const mp3AudioEl = document.getElementById("mp3-audio");

  // Download links
  const dlBooklet = document.getElementById("dl-booklet");
  const dlPdf = document.getElementById("dl-pdf");
  const dlMp3 = document.getElementById("dl-mp3");
  const dlLyricsPdf = document.getElementById("dl-lyrics-pdf");
  const dlLyricsMd = document.getElementById("dl-lyrics-md");
  const dlAbc = document.getElementById("dl-abc");
  const dlLy = document.getElementById("dl-ly");

  /**
   * Initialize Application
   */
  async function init() {
    setupEventListeners();
    await loadCatalog();
  }

  /**
   * Set up DOM Event Listeners
   */
  function setupEventListeners() {
    // Search Filter
    if (songSearchInput) {
      songSearchInput.addEventListener("input", (e) => {
        const query = e.target.value.toLowerCase().trim();
        filterCatalog(query);
      });
    }

    // View Toggles
    if (toggleScoreBtn && toggleLyricsBtn) {
      toggleScoreBtn.addEventListener("click", () => switchTab("score"));
      toggleLyricsBtn.addEventListener("click", () => switchTab("lyrics"));
    }

    // Audio Controls
    if (btnPlay) {
      btnPlay.addEventListener("click", togglePlay);
    }

    if (btnStop) {
      btnStop.addEventListener("click", stopPlayback);
    }

    // Tempo Control
    if (tempoSlider) {
      tempoSlider.addEventListener("input", (e) => {
        const val = parseInt(e.target.value, 10);
        state.tempoMultiplier = val / 100;
        if (tempoValueEl) {
          tempoValueEl.textContent = `${val}%`;
        }
        if (state.isPlaying) {
          // Restart synth audio playback with new tempo if active
          stopPlayback();
          startPlayback();
        }
      });
    }
  }

  /**
   * Get relative asset prefix based on current location
   */
  function getAssetPrefix() {
    if (window.location.pathname.includes('/src/web/')) {
      return '../../build/';
    }
    return '';
  }

  /**
   * Fetch Catalog Manifest JSON
   */
  async function loadCatalog() {
    const catalogPaths = [
      "catalog.json",
      "../catalog.json",
      "build/catalog.json",
      "../../build/catalog.json"
    ];
    let data = null;

    for (const path of catalogPaths) {
      try {
        const response = await fetch(path);
        if (response.ok) {
          data = await response.json();
          break;
        }
      } catch (e) {
        // Try next path
      }
    }

    if (!data || !data.songs || data.songs.length === 0) {
      if (songListEl) {
        songListEl.innerHTML = '<li class="placeholder-msg">Keine Lieder gefunden.</li>';
      }
      return;
    }

    state.catalog = data.songs;
    renderCatalogList(state.catalog);

    // Auto-select first carol
    if (state.catalog.length > 0) {
      selectSong(state.catalog[0]);
    }
  }

  /**
   * Render Song List Sidebar
   */
  function renderCatalogList(songs) {
    if (!songListEl) return;
    songListEl.innerHTML = "";

    songs.forEach((song) => {
      const li = document.createElement("li");
      li.className = "song-item";
      if (state.currentSong && state.currentSong.id === song.id) {
        li.classList.add("active");
      }
      li.dataset.songId = song.id;

      li.innerHTML = `
        <span class="song-item-title">${song.number}. ${song.title}</span>
      `;

      li.addEventListener("click", () => selectSong(song));
      songListEl.appendChild(li);
    });
  }

  /**
   * Filter Song Catalog List by Search Query
   */
  function filterCatalog(query) {
    if (!query) {
      renderCatalogList(state.catalog);
      return;
    }

    const filtered = state.catalog.filter((song) => {
      const titleMatch = song.title && song.title.toLowerCase().includes(query);
      const poetMatch = song.poet && song.poet.toLowerCase().includes(query);
      const composerMatch = song.composer && song.composer.toLowerCase().includes(query);
      return titleMatch || poetMatch || composerMatch;
    });

    renderCatalogList(filtered);
  }

  /**
   * Select and Load a Carol
   */
  async function selectSong(song) {
    if (state.isPlaying) {
      stopPlayback();
    }

    state.currentSong = song;

    // Update active state in sidebar list
    const items = songListEl.querySelectorAll(".song-item");
    items.forEach((item) => {
      if (item.dataset.songId === song.id) {
        item.classList.add("active");
      } else {
        item.classList.remove("active");
      }
    });

    // Update Header Metadata
    if (songTitleEl) {
      songTitleEl.textContent = `${song.title}`;
    }

    if (songMetaEl) {
      const metaParts = [];
      if (song.composer) metaParts.push(`Melodie: ${song.composer}`);
      if (song.poet) metaParts.push(`Text: ${song.poet}`);
      songMetaEl.textContent = metaParts.join(" | ");
    }

    // Update Download Links & Audio Stream Source
    updateAssetLinks(song);

    // Load ABC Notation and render score
    await loadAndRenderAbc(song);

    // Load Pure Text Lyrics
    await loadLyrics(song);
  }

  /**
   * Update Asset & Download Links
   */
  function updateAssetLinks(song) {
    const id = song.id;
    const prefix = getAssetPrefix();

    const pdfPath = song.assets && song.assets.pdf ? prefix + song.assets.pdf : `${prefix}pdf/${id}.pdf`;
    const mp3Path = song.assets && song.assets.mp3 ? prefix + song.assets.mp3 : `${prefix}mp3/${id}.mp3`;
    const abcPath = song.assets && song.assets.abc ? prefix + song.assets.abc : `${prefix}abc/${id}.abc`;
    const lyPath = window.location.pathname.includes('/src/web/') ? `../../src/songs/${id}/${id}.ly` : `src/songs/${id}/${id}.ly`;
    const lyricsPdfPath = `${prefix}lyrics_pdf/${id}_lyrics.pdf`;
    const lyricsMdPath = `${prefix}lyrics/${id}.md`;

    if (dlBooklet) dlBooklet.href = `${prefix}pdf/franzosische_lieder_liederbuch.pdf`;
    if (dlPdf) dlPdf.href = pdfPath;
    if (dlMp3) dlMp3.href = mp3Path;
    if (dlAbc) dlAbc.href = abcPath;
    if (dlLy) dlLy.href = lyPath;
    if (dlLyricsPdf) dlLyricsPdf.href = lyricsPdfPath;
    if (dlLyricsMd) dlLyricsMd.href = lyricsMdPath;

    // MP3 Audio Player
    if (mp3AudioEl) {
      mp3AudioEl.src = mp3Path;
      mp3AudioEl.load();
    }
  }

  /**
   * Load and Render ABC Notation Sheet Music
   */
  async function loadAndRenderAbc(song) {
    if (!paperEl) return;

    paperEl.innerHTML = '<div class="placeholder-msg">Lade Notenbild...</div>';
    state.abcString = "";
    state.visualObj = null;

    const prefix = getAssetPrefix();
    const abcPaths = [
      song.assets && song.assets.abc ? prefix + song.assets.abc : null,
      song.assets && song.assets.abc ? song.assets.abc : null,
      `abc/${song.id}.abc`,
      `../abc/${song.id}.abc`,
      `../../build/abc/${song.id}.abc`,
      `build/abc/${song.id}.abc`
    ].filter(Boolean);

    let fetchedAbc = null;
    for (const path of abcPaths) {
      try {
        const res = await fetch(path);
        if (res.ok) {
          fetchedAbc = await res.text();
          break;
        }
      } catch (e) {
        // Try next path
      }
    }

    if (!fetchedAbc) {
      paperEl.innerHTML = '<div class="placeholder-msg">ABC-Notendatei konnte nicht geladen werden.</div>';
      return;
    }

    state.abcString = fetchedAbc;

    if (typeof ABCJS !== "undefined") {
      try {
        const visualObj = ABCJS.renderAbc("paper", fetchedAbc, {
          responsive: "resize",
          paddingtop: 10,
          paddingbottom: 10,
          paddingright: 15,
          paddingleft: 15
        });

        if (visualObj && visualObj.length > 0) {
          state.visualObj = visualObj[0];
        }
      } catch (e) {
        console.error("Error rendering ABC score:", e);
        paperEl.innerHTML = '<div class="placeholder-msg">Fehler beim Rendern der Noten.</div>';
      }
    } else {
      paperEl.innerHTML = '<pre style="text-align:left; background:#f4f4f4; padding:1rem; border-radius:4px;">' +
        escapeHtml(fetchedAbc) + '</pre>';
    }
  }

  /**
   * Load and Display Pure Text Lyrics
   */
  async function loadLyrics(song) {
    if (!lyricsContentEl) return;

    lyricsContentEl.innerHTML = '<p class="placeholder-msg">Lade Liedtext...</p>';

    const prefix = getAssetPrefix();
    const lyricsPaths = [
      `${prefix}lyrics/${song.id}.md`,
      `lyrics/${song.id}.md`,
      `../lyrics/${song.id}.md`,
      `../../build/lyrics/${song.id}.md`,
      `build/lyrics/${song.id}.md`
    ].filter(Boolean);

    let lyricsText = null;
    for (const path of lyricsPaths) {
      try {
        const res = await fetch(path);
        if (res.ok) {
          lyricsText = await res.text();
          break;
        }
      } catch (e) {
        // Try next path
      }
    }

    if (!lyricsText) {
      // Fallback display
      lyricsContentEl.innerHTML = `<div class="lyrics-body">
        <h3>${escapeHtml(song.title)}</h3>
        <p class="placeholder-msg">Pure Text Liedtext wird nach dem Build-Pipeline Lauf verfügbar sein.</p>
      </div>`;
      return;
    }

    // Format plain Markdown lyrics into clean HTML paragraphs/stanzas
    const formattedHtml = formatMarkdownLyrics(lyricsText);
    lyricsContentEl.innerHTML = formattedHtml;
  }

  /**
   * Format Markdown Lyrics text into clean HTML blocks
   */
  function formatMarkdownLyrics(markdown) {
    const lines = markdown.split("\n");
    let html = "";
    let inStanza = false;

    lines.forEach((line) => {
      const trimmed = line.trim();
      if (trimmed.startsWith("# ")) {
        html += `<h2>${escapeHtml(trimmed.substring(2))}</h2>`;
      } else if (trimmed.startsWith("## ")) {
        html += `<h3>${escapeHtml(trimmed.substring(3))}</h3>`;
      } else if (trimmed.startsWith("**") && trimmed.endsWith("**")) {
        html += `<p class="stanza-header"><strong>${escapeHtml(trimmed.slice(2, -2))}</strong></p>`;
      } else if (trimmed === "") {
        if (inStanza) {
          html += "</p>";
          inStanza = false;
        }
      } else {
        if (!inStanza) {
          html += '<p class="stanza-body">';
          inStanza = true;
        } else {
          html += "<br>";
        }
        html += escapeHtml(trimmed);
      }
    });

    if (inStanza) {
      html += "</p>";
    }

    return html;
  }

  /**
   * Switch View Tab (Score vs Lyrics)
   */
  function switchTab(tabName) {
    state.activeTab = tabName;

    if (tabName === "score") {
      if (toggleScoreBtn) toggleScoreBtn.classList.add("active");
      if (toggleLyricsBtn) toggleLyricsBtn.classList.remove("active");
      if (scoreViewEl) scoreViewEl.classList.replace("hidden-panel", "active-panel") || scoreViewEl.classList.add("active-panel");
      if (lyricsViewEl) lyricsViewEl.classList.replace("active-panel", "hidden-panel") || lyricsViewEl.classList.add("hidden-panel");
    } else {
      if (toggleLyricsBtn) toggleLyricsBtn.classList.add("active");
      if (toggleScoreBtn) toggleScoreBtn.classList.remove("active");
      if (lyricsViewEl) lyricsViewEl.classList.replace("hidden-panel", "active-panel") || lyricsViewEl.classList.add("active-panel");
      if (scoreViewEl) scoreViewEl.classList.replace("active-panel", "hidden-panel") || scoreViewEl.classList.add("hidden-panel");
    }
  }

  /**
   * Toggle Synth Play / Pause
   */
  function togglePlay() {
    if (state.isPlaying) {
      stopPlayback();
    } else {
      startPlayback();
    }
  }

  /**
   * Start Web Audio API Synth Playback via abcjs
   */
  function startPlayback() {
    state.isPlaying = true;
    updatePlayButtonState();

    if (typeof ABCJS === "undefined" || !ABCJS.synth || !state.visualObj) {
      // Fallback: Use MP3 Audio element
      if (mp3AudioEl && mp3AudioEl.src) {
        mp3AudioEl.play().catch((e) => console.warn("MP3 play error:", e));
      }
      return;
    }

    if (!ABCJS.synth.isSupported()) {
      if (mp3AudioEl && mp3AudioEl.src) {
        mp3AudioEl.play().catch((e) => console.warn("MP3 play error:", e));
      }
      return;
    }

    try {
      const audioContext = new (window.AudioContext || window.webkitAudioContext)();
      state.synthControl = new ABCJS.synth.CreateSynth();

      const options = {
        visualObj: state.visualObj,
        audioContext: audioContext,
        millisecondsPerMeasure: state.visualObj.millisecondsPerMeasure() / state.tempoMultiplier
      };

      state.synthControl.init(options).then(() => {
        return state.synthControl.prime();
      }).then(() => {
        state.synthControl.start();
      }).catch((err) => {
        console.warn("CreateSynth init error, falling back to MP3 audio:", err);
        if (mp3AudioEl) {
          mp3AudioEl.play().catch((e) => console.warn("MP3 fallback error:", e));
        }
      });
    } catch (e) {
      console.warn("Synth playback exception, using MP3 element:", e);
      if (mp3AudioEl) {
        mp3AudioEl.play().catch((e) => console.warn("MP3 exception error:", e));
      }
    }
  }

  /**
   * Stop Playback
   */
  function stopPlayback() {
    state.isPlaying = false;
    updatePlayButtonState();

    if (state.synthControl) {
      try {
        state.synthControl.stop();
      } catch (e) {
        // Ignore synth stop errors
      }
      state.synthControl = null;
    }

    if (mp3AudioEl) {
      try {
        mp3AudioEl.pause();
        mp3AudioEl.currentTime = 0;
      } catch (e) {
        // Ignore pause errors
      }
    }
  }

  /**
   * Update Play Button UI State
   */
  function updatePlayButtonState() {
    if (!btnPlay) return;

    if (state.isPlaying) {
      btnPlay.innerHTML = '<span class="icon">⏸</span> Pause';
      btnPlay.classList.add("playing");
    } else {
      btnPlay.innerHTML = '<span class="icon">▶</span> Abspielen';
      btnPlay.classList.remove("playing");
    }
  }

  /**
   * Utility to Escape HTML special characters
   */
  function escapeHtml(str) {
    if (!str) return "";
    return str
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Initialize App
  init();
});
