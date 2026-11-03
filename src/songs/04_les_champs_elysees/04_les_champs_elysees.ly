\version "2.24.0"

\header {
  title = "Les Champs-Élysées"
  subtitle = "Adaptation française de « Waterloo Road »"
  composer = "Michael Wilshaw & Mike Deighan"
  poet = "Paroles françaises : Pierre Delanoë"
  arranger = "Interprété par Joe Dassin (1969)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key c \major
  \time 4/4
  \tempo "Moderato" 4 = 126
}

harmonies = \chordmode {
  \partial 4 r4
  c1 e1:7 a1:min c1:7/g
  f1 c1 d1:7 g1
  c1 e1:7 a1:min c1:7/g
  f1 c1 d2:min g2:7 c1
  c1 e1:7 a1:min c1:7/g
  f1 c1 d2:min g2:7 c1
}

melody = \relative c'' {
  \global
  \clef treble

  \partial 4 g4 |
  \sectionLabel "Couplet"
  e'4 e e d8 c |
  b4 b b a8 gis |
  a4 a a c |
  g2. g4 |
  a4 a a b8 c |
  g4 g g c |
  d4 d d c8 d |
  b2. g4 |

  e'4 e e d8 c |
  b4 b b a8 gis |
  a4 a a c |
  g2. g4 |
  a4 a a b8 c |
  g4 g g c |
  d4 d e d |
  c2. r4 \bar "||"

  \sectionLabel "Refrain"
  c2 e4. d8 |
  b1 |
  a2 c4. b8 |
  g2. r4 |
  a4 a a b8 c |
  g4 g g c |
  d4 d e d |
  c2. r4 |
  \bar "|."
}

text = \lyricmode {
  Je m'ba -- la -- dais sur l'a -- ve -- nue,
  le cœur ou -- vert à l'in -- con -- nu,
  J'a -- vais en -- vie de di -- re bon -- jour
  à n'im -- por -- te qui.
  N'im -- por -- te qui, et ce fut toi,
  je t'ai dit n'im -- por -- te quoi,
  Il suf -- fi -- sait de te par -- ler
  pour t'ap -- pri -- voi -- ser.

  Aux Champs- -- É -- ly -- sées,
  aux Champs- -- É -- ly -- sées,
  Au so -- leil, sous la pluie,
  à mi -- di ou à mi -- nuit,
  Il y~a tout ce que vous vou -- lez
  aux Champs- -- É -- ly -- sées.
}

\score {
  <<
    \new ChordNames { \harmonies }
    \new Staff {
      \new Voice = "singer" { \melody }
    }
    \new Lyrics \lyricsto "singer" { \text }
  >>
  \layout { }
  \midi { }
}
