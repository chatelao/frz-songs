\version "2.24.0"

\header {
  title = "Santiano"
  subtitle = "Chant de marins adapté en français"
  composer = "Traditionnel (« Santianna »)"
  poet = "Paroles françaises : Jacques Plante"
  arranger = "Interprété par Hugues Aufray (1961)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key a \minor
  \time 4/4
  \tempo "Allant" 4 = 104
}

harmonies = \chordmode {
  \partial 4 r4
  a1:min g1 a1:min e1:min
  a1:min g1 a2:min e2:min a1:min
  a1:min g1 a1:min e1:min
  a1:min g1 a2:min e2:min a1:min
}

melody = \relative c' {
  \global
  \clef treble

  \partial 4 e4 |
  \sectionLabel "Couplet"
  a4 a a b8 c |
  b4 g g a8 b |
  c4 c c d8 e |
  b2. e,4 |
  a4 a a b8 c |
  b4 g g a8 b |
  c4 a b gis |
  a2. r4 \bar "||"

  \sectionLabel "Refrain"
  a4 a a b8 c |
  b4 g g a8 b |
  c4 c c d8 e |
  b2. e,4 |
  a4 a a b8 c |
  b4 g g a8 b |
  c4 a b gis |
  a2. r4 |
  \bar "|."
}

text = \lyricmode {
  C'est un fa -- meux trois- -- mâts, fin comme un oi -- seau,
  His -- se_et ho, San -- tia -- no !
  Dix- -- huit nœuds, qua -- tre- -- cents ton -- neaux,
  Je suis fier d'y ê -- tre ma -- te -- lot.

  Tiens bon la bar -- re_et tiens bon le vent,
  His -- se_et ho, San -- tia -- no !
  Si Dieu veut, tou -- jours droit de -- vant,
  Nous i -- rons jus -- qu'à San Fran -- cis -- co.
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
