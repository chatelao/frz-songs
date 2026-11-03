\version "2.24.0"

\header {
  title = "Alouette, gentille alouette"
  subtitle = "Comptine traditionnelle (Körperteile und Wortschatz)"
  composer = "Traditionnel canadien-français"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key g \major
  \time 4/4
  \tempo "Gaiement" 4 = 116
}

harmonies = \chordmode {
  g1 d2:7 g2
  g1 d2:7 g2
  g1 d2:7 g2
  g2 c2 g2 d2:7
  g1
}

melody = \relative c' {
  \global
  \clef treble

  \sectionLabel "Refrain"
  d4. e8 d4 e |
  fis8 fis fis fis g4 d |
  d4. e8 d4 e |
  fis8 fis fis fis g2 \bar "||"

  \sectionLabel "Couplet"
  d'4 d8 d b4 g |
  a8 b c a g2 |
  d'4 b c a |
  b8 b g4 a d, |
  g1 |
  \bar "|."
}

text = \lyricmode {
  A -- lou -- et -- te, gen -- til -- le_A -- lou -- et -- te,
  A -- lou -- et -- te, je te plu -- me -- rai.

  Je te plu -- me -- rai la tê -- te,
  A -- lou -- et -- te, je te plu -- me -- rai.
  Et la tê -- te, et la tê -- te,
  A -- lou -- ette ! Ah ! __
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
