\version "2.24.0"

\header {
  title = "Sur le pont d'Avignon"
  subtitle = "Ronde traditionnelle française"
  composer = "Traditionnel (XVe siècle)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key c \major
  \time 2/4
  \tempo "Allegro vivace" 4 = 116
}

harmonies = \chordmode {
  c2 g2:7 c2 g2:7
  c2 g2:7 c4 g4:7 c2
  c2 g2:7 c2 g2:7
  c2 g2:7 c4 g4:7 c2
}

melody = \relative c' {
  \global
  \clef treble

  \sectionLabel "Refrain"
  c8 c c4 |
  d8 d d4 |
  e8 f g e |
  d4 g, |
  c8 c c4 |
  d8 d d4 |
  e8 f g d |
  c2 \bar "||"

  \sectionLabel "Couplet"
  e8 e e e |
  d8 d d4 |
  e8 f g e |
  d4 g, |
  e'8 e e e |
  d8 d d4 |
  e8 f g d |
  c2 \bar "|."
}

text = \lyricmode {
  Sur le pont d'A -- vi -- gnon,
  On y dan -- se, on y dan -- se,
  Sur le pont d'A -- vi -- gnon,
  On y dan -- se tous en rond.

  Les bel -- les da -- mes font comm' ça,
  Et puis en -- cor' comm' ça.
  Les bel -- les da -- mes font comm' ça,
  Et puis en -- cor' comm' ça.
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
