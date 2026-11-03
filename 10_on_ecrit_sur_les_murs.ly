\version "2.24.0"

\header {
  title = "On écrit sur les murs"
  composer = "Romano Musumarra"
  poet = "Jean-Marie Moreau"
  arranger = "Créé par Demis Roussos (1989), repris par Kids United (2015)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key e \minor
  \time 4/4
  \tempo "Andante cantabile" 4 = 96
}

harmonies = \chordmode {
  e1:min c1 d1 g2 b2:7
  e1:min c1 d1 b1:7
  e1:min c1 d1 g2 b2:7
  e1:min c1 d1 e1:min
}

melody = \relative c' {
  \global
  \clef treble

  \sectionLabel "Couplet"
  e4 e8 fis g4 fis8 e |
  g4 e8 d e4 r |
  fis4 fis8 g a4 g8 fis |
  g4 fis8 e b2 |

  e4 e8 fis g4 fis8 e |
  g4 e8 d e4 r |
  fis4 fis8 g a4 g8 fis |
  b2. r4 \bar "||"

  \sectionLabel "Refrain"
  b4. a8 g4 fis8 e |
  g4. fis8 e4 r |
  a4. g8 fis4 e8 d |
  g4. fis8 b4 r |

  b4. a8 g4 fis8 e |
  g4. fis8 e4 r |
  a4 a8 g fis4 g8 a |
  e2. r4 |
  \bar "|."
}

text = \lyricmode {
  C'est un che -- min tout tracé d'a -- van -- ce,
  une his -- toire d'a -- mour et d'es -- pé -- ran -- ce,
  Un gra -- phi -- ti du fond du cœur,
  qui s'en -- vole vers le ciel en cou -- leur.

  On é -- crit sur les murs le nom de ceux qu'on ai -- me,
  Des mes -- sa -- ges pour les jours à ve -- nir.
  On é -- crit sur les murs à l'en -- cre de nos vei -- nes,
  On des -- si -- ne tout ce que l'on vou -- drait di -- re.
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
