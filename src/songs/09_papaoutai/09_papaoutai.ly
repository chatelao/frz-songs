\version "2.24.0"

\header {
  title = "Papaoutai"
  composer = "Stromae (Paul Van Haver)"
  arranger = "Interprété par Stromae (2013)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key e \minor
  \time 4/4
  \tempo "Dance / Electro" 4 = 120
}

harmonies = \chordmode {
  e1:min c1 g1 d1
  e1:min c1 g1 d1
  e1:min c1 g1 d1
  e1:min c1 g1 d1
}

melody = \relative c'' {
  \global
  \clef treble

  \sectionLabel "Couplet"
  b8 b b b b a g a |
  b8 g g4 r4 e8 fis |
  g8 g g g g fis e fis |
  d8 d d4 r2 |

  b'8 b b b b a g a |
  b8 g g4 r4 e8 fis |
  g8 g g g g fis e fis |
  d8 d d4 r2 \bar "||"

  \sectionLabel "Refrain"
  b'4. a8 g e4. |
  b'4. a8 g e4. |
  b'4. a8 g e4. |
  d8 d d e d4 r |

  b'4. a8 g e4. |
  b'4. a8 g e4. |
  b'4. a8 g e4. |
  d8 d d e e4 r |
  \bar "|."
}

text = \lyricmode {
  Di -- tes- -- moi d'où il vient,
  en -- fin je sau -- rai où je vais.
  Ma -- man dit que lors -- qu'on cher -- che bien,
  on fi -- nit par trou -- ver.
  Elle dit qu'il n'est ja -- mais très loin,
  qu'il part très sou -- vent tra -- vail -- ler.
  Elle dit : « Tra -- vail -- ler, c'est bien »,
  bien mieux qu'ê -- tre mal ac -- com -- pa -- gné.

  Où t'es, pa -- pa, où t'es ?
  Où t'es, pa -- pa, où t'es ?
  Où t'es, pa -- pa, où t'es ?
  Où t'es, où t'es, pa -- pa, où t'es ?

  Où t'es, pa -- pa, où t'es ?
  Où t'es, pa -- pa, où t'es ?
  Où t'es, pa -- pa, où t'es ?
  Où t'es, où t'es, pa -- paoutai ?
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
