\version "2.24.0"

\header {
  title = "Avenir"
  composer = "Louane Emera & Quentin Capron"
  arranger = "Interprété par Louane (2014)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key a \minor
  \time 4/4
  \tempo "Moderato pop" 4 = 118
}

harmonies = \chordmode {
  a1:min f1 c1 g1
  a1:min f1 c1 g1
  a1:min f1 c1 g1
  a1:min f1 c1 g1
}

melody = \relative c' {
  \global
  \clef treble

  \sectionLabel "Couplet"
  e4 e8 e e4 e8 d |
  c8 c c d c4 r |
  e4 e8 e e4 e8 d |
  d8 c c d c4 r |
  e4 e8 e e4 e8 d |
  c8 c c d c4 r |
  e4 e8 e e4 g |
  d2. r4 \bar "||"

  \sectionLabel "Refrain"
  a'8 a a a a b c4 |
  g8 g g g g a b4 |
  e,8 e e e e f g4 |
  d4 d8 e d c d4 |

  a'8 a a a a b c4 |
  g8 g g g g a b4 |
  e,8 e e e e f g4 |
  d4 d8 e d c a4 |
  \bar "|."
}

text = \lyricmode {
  Par -- tis les se -- crets qu'on s'é -- tait di -- vi -- sés,
  J'com -- prends pas pour -- quoi tu as chan -- gé d'a -- vis.
  J'ai lais -- sé mes dé -- mons s'en al -- ler sous la pluie,
  Pour qu'on soit tous les deux réu -- nis.

  J'es -- père que tu vas souf -- frir,
  Et que tu vas mal dor -- mir,
  Et pour un peu, j'vais te dé -- tes -- ter,
  J'vais te dé -- tes -- ter !
  J'es -- père que tu vas souf -- frir,
  Et que tu vas mal dor -- mir,
  Car tout ce qui comp -- tait pour moi,
  C'é -- tait mon a -- ve -- nir.
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
