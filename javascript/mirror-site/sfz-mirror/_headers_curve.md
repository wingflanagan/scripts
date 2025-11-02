    ‹curve› - SFZ Format                    Top

[![Logo image](images/logo_svg)](../..)

*   [Syntax](#)
    *   [Headers](_headers_.md)
    *   [Opcodes](_opcodes_.md)
    
    *   [Modulations](_modulations_.md)
    *   [Envelope Generators](_modulations_envelope_generators.md)
    *   [LFO](_modulations_lfo.md)
    
    *   [Extended MIDI CCs](_extensions_midi_ccs.md)
    
    *   [Types & Categories](_misc_categories.md)
    *   [Versions](_versions.md)
*   [Software](#)
    *   [Players](_software_players.md)
    *   [Tools](_software_tools.md)
*   [Tutorials](#)
    *   [Basics](_tutorials_basics.md)
    
    *   [Basic / Template](_tutorials_basic_sfz_file.md)
    *   [Sustained Note Basics](_tutorials_sustained_note_basics.md)
    *   [Vibrato](_tutorials_vibrato.md)
    *   [Legato](_tutorials_legato.md)
    *   [Unison](_tutorials_unison.md)
    *   [Range Extension](_tutorials_range_extension.md)
    *   [Modular Instruments](_tutorials_modular_instruments.md)
    *   [Subtractive Synthesizers](_tutorials_subtractive_synths.md)
    *   [Strumming](_tutorials_strum.md)
    *   [Sympathetic Resonance](_tutorials_sympathetic_resonance.md)
    
    *   [Drum & Round Robin Basics](_tutorials_drum_basics.md)
    *   [Cymbal Muting](_tutorials_cymbal_muting.md)
    *   [Epic Drums](_tutorials_epic_drums.md)
    *   [Brush Stirs](_tutorials_brush_stirs.md)
    
    *   [Envelope Generators](_tutorials_envelope_generators.md)
    *   [SFZ 1 Modulations](_tutorials_sfz1_modulations.md)
    *   [SFZ 2 Modulations](_tutorials_sfz2_modulations.md)
    *   [Pitch LFO Examples](_tutorials_lfo.md)
    
    *   [Video Tutorials](_tutorials_videos.md)
*   [Instruments](https://sfzinstruments.github.io)
*   [News](_news.md)

*   [Search](#)
*   Toggle theme
    *   Light
    *   Dark
    *   Auto

‹curve›
=======

A header for defining curves for MIDI CC controls.

One curve header is used to define each curve. The values for various points along the curve can then be set, from `v000` to `v127`. The default is `v000=0` and `v127=1`. Any points along the curve not defined explicitly will be interpolated linearly between points which are defined.

There are default built-in curves in ARIA. If no curve is specified for a modulation, curve 0 is used. The built-in ARIA curves are:

Number

Description

Range

Notes

0

Default

0 to 1

Linear

1

Bipolar

\-1 to 1

Linear, used by CC10 panning by defeault

2

Inverted

1 to 0

Linear

3

Bipolar inverted

1 to -1

Linear

4

Concave

0 to 1

Nonlinear, used for CC7 volume tracking and amp\_veltrack

5

Xfin power curve

0 to 1

Based on Dimension Pro behavior

6

Xfout power curve

1 to 0

Based on Dimension Pro behavior

These cannot be overwritten. Use `curve_index` numbers of 7 and above for custom curves. Curve\_index in ARIA can be any integer from 0 to 254.

[](#examples)Examples
---------------------

```
<curve>curve_index=17
v000=0
v095=1
v127=1

<curve>curve_index=18
v000=0
v095=0.5
v127=1

```

Here's a scenario using one MIDI CC to control the amplitude of two samples along two different curves.

```
<region>
amplitude_oncc110=100
amplitude_curvecc110=9
sample=bigger.wav

<region>
amplitude_oncc110=100
amplitude_curvecc110=10
sample=smaller.wav

//The curves for the room ambiences - bigger room first

<curve>curve_index=9
v000=0
v063=0
v127=1

<curve>curve_index=10
v000=0
v063=1
v127=0.1

```

And how to use the default curve 1 to create a tuning control which goes down and up, with the pitch unmodulated when the control is in the middle.

```
pitch_oncc27=100
pitch_curvecc27=1

```

Follow us

*   [GitHub Organization](https://github.com/sfz/ "GitHub Organization")
*   [News Atom Feed](_atom_xml.md)
*   [Discord Chat](https://discord.gg/t7nrZ6d "Discord Chat")
*   [IRC](https://kiwiirc.com/nextclient/#irc://irc.libera.chat:+6697/#sfzformat "Internet Relay Chat")

Quick links

*   [Old rgc:audio SFZ page](_legacy.md)
*   [Peter L. Jones' SFZ page](http://www.drealm.info/sfz/ "Peter L. Jones' SFZ page")
*   [KVR Forum SFZ post](https://www.kvraudio.com/forum/viewtopic.php?f=42&t=508861 "KVR Forum SFZ post")
*   [Plogue Forum](https://www.plogue.com/plgfrms/viewforum.php?f=14 "Plogue Forum")
*   [rgc:audio SFZ test suite](https://github.com/sfz/tests/ "rgc:audio SFZ test suite")
*   [Opcode suggestions](https://github.com/sfz/opcode-suggestions/ "Opcode suggestions")

* * *

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/headers/curve.md)

var base\_url = "../..", shortcuts = {"help": 191, "next": 78, "previous": 80, "search": 83}; hljs.highlightAll(); window.addEventListener("load", function (event) { if (anchors) { anchors.options.placement = 'left'; anchors.add(); } });

#### [](#searchModalLabel)Search

From here you can search these documents. Enter your search terms below.

#### [](#keyboardModalLabel)Keyboard Shortcuts

× Close

Keys

Action

?

Open this help

n

Next page

p

Previous page

s

Search