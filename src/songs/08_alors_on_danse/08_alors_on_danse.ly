\version "2.24.0"

\header {
  title = "Alors on danse"
  composer = "Stromae (Paul Van Haver)"
  arranger = "Interprété par Stromae (2009)"
  tagline = ##f
}

\paper {
  #(set-paper-size "a4")
}

global = {
  \key c \minor
  \time 4/4
  \tempo "Dance beat" 4 = 120
}

harmonies = \chordmode {
  c1:min aes1 ees1 f1:min
  c1:min aes1 ees1 f1:min
  c1:min aes1 ees1 f1:min
  c1:min aes1 ees1 f1:min
}

melody = \relative c' {
  \global
  \clef treble

  \sectionLabel "Couplet"
  c8 c c c c4 c8 d |
  ees8 ees ees ees ees4 d8 c |
  bes8 bes bes bes bes4 c8 d |
  c8 c c bes c4 r |

  c8 c c c c4 c8 d |
  ees8 ees ees ees ees4 d8 c |
  bes8 bes bes bes bes4 c8 d |
  c8 c c bes c4 r \bar "||"

  \sectionLabel "Refrain"
  c4 c8 c ees4 ees8 d |
  c4 aes8 aes c4 c8 bes |
  bes4 g8 g bes4 bes8 c |
  aes4 f8 f aes4 f |
  \bar "|."
}

text = \lyricmode {
  Qui dit é -- tu -- de dit tra -- vail,
  qui dit taf te dit les thunes,
  Qui dit ar -- gent dit dé -- pen -- ses,
  qui dit cré -- dit dit créan -- ce.
  Qui dit det -- te te dit huis -- sier,
  oui dit as -- sis dans la mer -- de,
  Qui dit a -- mour dit les gos -- ses,
  dit tou -- jours et dit di -- vorce.

  A -- lors on danse...
  A -- lors on danse...
  A -- lors on danse...
  A -- lors on danse...
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
