\version "2.24.0"
\header {
title = "Bella Ciao (Versione delle Mondine & dei Partigiani)"
subtitle = "Kritische Edition nach Milva (Fonit Cetra SP 1283 / LP Canti della libertà, 1965)"
composer = "Tradizionale (Arr. Iller Pattacini 1965 / Roberto Negri 1971)"
tagline = "Geprüft gegen LilyPond Notation Reference v2.24"
}
% --- HARMONIESCHEMA (Synchronisiert mit 3/8-Auftakt über s4.) ---
harmonies = \chordmode {
\set chordChanges = ##t
\partial 4. s4. |
% Teil I: Delle Mondine (Fis-Moll)
fis1:m | fis1:m | fis1:m | cis2:7 fis2:7 |
b1:m | fis1:m | cis1:7 | fis1:m |
% Teil II: Dei Partigiani (A-Moll)
a1:m | a1:m | a1:m | a1:7 |
d1:m | a1:m | e1:7 | a1:m |
% Teil III: Finale / Modulation (+1 Ganzton nach H-Moll)
b1:m | b1:m | b1:m | b1:7 |
e1:m | b1:m | fis1:7 | b1:m |
}
% --- MELODIE-STIMME ---
melody = \relative c' {
\clef treble
\time 4/4
% TEIL I: BELLA CIAO DELLE MONDINE (Andante sostenuto, Fis-Moll)
\key fis \minor
\tempo "Andante sostenuto (Mondine)" 4 = 74
\partial 4. cis8 fis8 gis8 |
a4 fis4 r8 cis8 fis8 gis8 |
a4 fis4 r8 cis8 fis8 gis8 |
a4 gis8 fis8 a4 gis8 fis8 |
\octaveCheck cis''
cis'4 cis4 cis8 b8 cis8 d8 |
d4 d4 r8 d8 cis8 b8 |
d4 cis4 r8 cis8 b8 a8 |
gis4 cis4 a4 gis4 |
fis2 r8 e8 a8 b8 \bar "||"
% TEIL II: BELLA CIAO DEI PARTIGIANI (Allegro marziale, A-Moll)
\key a \minor
\tempo "Allegro marziale (Partigiani)" 4 = 128
\octaveCheck c''
c4 a4 r8 e8 a8 b8 |
c4 a4 r8 e8 a8 b8 |
c4 b8 a8 c4 b8 a8 |
\octaveCheck e''
e'4 e4 e8 d8 e8 f8 |
f4 f4 r8 f8 e8 d8 |
f4 e4 r8 e8 d8 c8 |
b4 e4 c4 b4 |
a2 r8 fis8 b8 cis8 \bar "||"
% TEIL III: MODULATION IN H-MOLL (Dramatisches Finale)
\key b \minor
\octaveCheck d''
d4 b4 r8 fis8 b8 cis8 |
d4 b4 r8 fis8 b8 cis8 |
d4 cis8 b8 d4 cis8 b8 |
\octaveCheck fis''
fis'4 fis4 fis8 e8 fis8 g8 |
g4 g4 r8 g8 fis8 e8 |
g4 fis4 r8 fis8 e8 d8 |
cis4 fis4 d4 cis4 |
b2. r4 \bar "|."
}
% --- TEXT-INCIPIT (2 Zeilen gemäss Editionsrichtlinie) ---
incipitLyrics = \lyricmode {
A -- la ma -- ti -- na a -- pe -- na al -- za -- ta,
o bel -- la ciao, bel -- la ciao, bel -- la ciao, ciao, ciao!
}
\score {
<<
\new ChordNames \harmonies
\new Staff = "gesang" <<
\new Voice = "melodie" \melody
\new Lyrics \lyricsto "melodie" \incipitLyrics
>>
>>




\layout {
indent = 0\mm
\context {
\Score
\override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
}
}
\midi { }
}
