\version "2.24.0"

\header {
  title = "Frère Jacques"
  subtitle = "Traditionnel français (Canon à 4 voix)"
  composer = "Traditionnel / Jean-Philippe Rameau"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key f \major
  \time 4/4
  \tempo "Allegretto" 4 = 112
}

harmonies = \chordmode {
  f1 f1 f1 f1
  f1 f1 f2 c2:7 f1
}

melody = \relative c' {
  \global
  \clef treble
  f4 g a f |
  f4 g a f |
  a4 bes c2 |
  a4 bes c2 |
  c8 d c bes a4 f |
  c'8 d c bes a4 f |
  f4 c f2 |
  f4 c f2 |
  \bar "|."
}

text = \lyricmode {
  Frè -- re Jac -- ques,
  Frè -- re Jac -- ques,
  Dor -- mez- -- vous ?
  Dor -- mez- -- vous ?
  Son -- nez les ma -- ti -- nes !
  Son -- nez les ma -- ti -- nes !
  Ding, daing, dong !
  Ding, daing, dong !
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
