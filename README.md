# Catmander

## Overview

Catmander is a MIDI sequencer based on the [Kittenbot Meowbit](https://www.kittenbot.cc/blogs/learn/meowbit-micropython-programming). The Meowbit's pin 9 is used to used MIDI data.

Each column in the `sequence` has values from 0-127 and represents the
velocity of the note to be played. Each row corresponds to a
particular note. The sequencer moves from left to right, playing the
sets of notes in the current column on each step.

The `A` button selects 8 random spots and sets their values to 0,
while the `B` button picks 8 random spots and sets their values to
something between 0 and 127.