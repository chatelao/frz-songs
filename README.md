# Französische Lieder - Chansons Françaises

Willkommen zur Notensammlung **Französische Lieder (Chansons Françaises)** — eine Open-Source-Bibliothek mit 10 ausgewählten französischen Liedern, vom traditionellen Kinderlied über Chansons bis hin zu modernem Pop.

Alle Notensätze werden mit **GNU LilyPond (`.ly`)** gepflegt und automatisch in verschiedene Formate gerendert.

---

## 🌐 Interaktiver Web-Player

Greifen Sie auf den interaktiven Web-Noten- und Audioplayer zu, der über GitHub Pages bereitgestellt wird:
👉 **[Interaktiver Web-Player](https://chatelao.github.io/frz-songs)**

---

## 🎼 Übersicht & Formate

Dieses Repository bietet alle Lieder in einer vollständigen Toolchain und CI/CD-Pipeline:
- **LilyPond (`.ly`)**: Typografische Master-Quelldateien mit Melodiestimme, Akkorden und französischem Text.
- **ABC Notation (`.abc`)**: Leichtgewichtige Notationsformate für interaktive Web-Visualisierung (abcjs).
- **PDF-Dokumente (Noten)**: Hochwertige Vektor-Notenblätter direkt aus LilyPond.
- **Vollständiges Liederbuch (PDF)**: Konsolidiertes Gesamtbuch (`franzosische_lieder_liederbuch.pdf` / `booklet.pdf`) mit Kunst-Cover, durchgehender Seitennummerierung und abschließendem Inhaltsverzeichnis (TOC).
- **MP3-Audio**: Hochwertige Piano-Aufnahmen, synthetisiert aus LilyPond-MIDI über FluidSynth & SoundFont.
- **Liedtexte (Markdown & PDF)**: Reine Text-Liedtexte zum Singen und Drucken ohne Notenbild.

---

## 📜 Liedverzeichnis

| Nr. | Titel | Interpret / Ursprung | Eignung / pädagogischer Nutzen | Datei |
|---|---|---|---|---|
| 1 | Frère Jacques | Traditionell / Jean-Philippe Rameau | Klassiker für Aussprache und Kanonsingen | `01_frere_jacques.ly` |
| 2 | Alouette, gentille alouette | Traditionell kanadisch-französisch | Körperteile und Wortschatz | `02_alouette.ly` |
| 3 | Sur le pont d'Avignon | Traditionell (15. Jh.) | Kultur und einfache Satzstrukturen | `03_sur_le_pont_davignon.ly` |
| 4 | Les Champs-Élysées | Joe Dassin | Sehr bekannt, leicht verständlicher Text | `04_les_champs_elysees.ly` |
| 5 | Santiano | Hugues Aufray | Klare Aussprache, Seemannslied-Refrain | `05_santiano.ly` |
| 6 | Avenir | Louane | Modernes Französisch, emotionaler Poptext | `06_avenir.ly` |
| 7 | Dernière danse | Indila | Dramatischer Gesang, einfache Refrainstrukturen | `07_derniere_danse.ly` |
| 8 | Alors on danse | Stromae | Hoher Bekanntheitsgrad, modernes Vokabular | `08_alors_on_danse.ly` |
| 9 | Papaoutai | Stromae | Eingängiger Rhythmus, oft im Französischunterricht | `09_papaoutai.ly` |
| 10 | On écrit sur les murs | Kids United (orig. Demis Roussos) | Ideal für Schulklassen und gemeinsames Singen | `10_on_ecrit_sur_les_murs.ly` |

---

## 🛠 Build-Pipeline & Entwicklung

### Installation der Abhängigkeiten
```bash
chmod +x src/install.sh test/install.sh
./src/install.sh
./test/install.sh
```

### Gesamte Pipeline ausführen
```bash
chmod +x src/scripts/build_pipeline.sh
./src/scripts/build_pipeline.sh
```
Das Build-Skript erzeugt alle Artefakte unter `build/` (PDF, MP3, ABC, MIDI, Liedtexte, Liederbuch und statische Website für GitHub Pages).

### Tests ausführen
```bash
# Unit-Tests
python3 -m unittest discover test/unit/

# E2E-Playwright-Tests
python3 -m unittest discover test/e2e/
```
