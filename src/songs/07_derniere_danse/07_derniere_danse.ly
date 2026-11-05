\version "2.24.0"

\header {
  title = "Dernière danse"
  composer = "Indila & Skalpovich"
  arranger = "Interprété par Indila (2013)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key c \minor
  \time 4/4
  \tempo "Lento dramatico" 4 = 85
}

harmonies = \chordmode {
  c1:min g1:min/bes aes1 g1
  c1:min g1:min/bes aes1 g1
  c1:min bes1 ees1 f1:min
  c1:min bes1 ees1 g1
}

melody = \relative c' {
  \global
  \clef treble

  \sectionLabel "Couplet"
  c4 c8 c d4 d8 ees |
  d8 c bes c d4 r |
  c4 c8 c d4 d8 ees |
  d8 c b c d4 r |
  c4 c8 c d4 d8 ees |
  d8 c bes c d4 r |
  c8 d ees f g4 f8 ees |
  d2. r4 \bar "||"

  \sectionLabel "Refrain"
  c'4 c8 c c bes aes bes |
  aes4 g8 f g4 r |
  ees4 ees8 ees ees f g aes |
  f4. ees8 d4 r |

  c'4 c8 c c bes aes bes |
  aes4 g8 f g4 r |
  ees8 ees ees ees f g f ees |
  d2. r4 |
  \bar "|."
}

text = \lyricmode {
  Oh ma dou -- ce souf -- fran -- ce,
  pour -- quoi s'a -- char -- ner, tu r'com -- men -- ces,
  Je ne suis qu'un ê -- tre sans im -- por -- tan -- ce,
  sans lui je suis un peu pa -- ro,
  je dé -- am -- bule seu -- le dans le mé -- tro.

  Je re -- mue le ciel, le jour, la nuit,
  je dan -- se_a -- vec le vent, la pluie,
  Un peu d'a -- mour, un brin de miel,
  et je danse, danse, danse...
  Je re -- mue le ciel, le jour, la nuit,
  je dan -- se_a -- vec le vent, la pluie,
  Et dans le bruit, je cours et j'ai peur,
  est- -- ce mon tour ?
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
