    tune / pitch - SFZ Format                    Top

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

tune / pitch
============

The fine tuning for the sample, in cents.

Range of `tune` in the SFZ1 spec is ±1 semitone, from -100 to 100, though at least in ARIA, it seems a broader range is supported, at least -2400 to 2400 cents.

[](#examples)Examples
---------------------

```
tune=33
tune=-30
tune=94

```

Uses include correcting the intonation of naturally off-pitch samples, and detuning unison voices.

Modulating pitch with MIDI CC to create a tune control is possible in SFZ2. If the control needs to go both up and down, there are two ways to do this. One is to move the pitch down by the tuning range, then have modulation move it up by twice the tuning range, so that when the control is at the midpoint, the region will play at its orignal, unmodulated pitch. For a range of 100 cents this would look like this:

```
tune=-100
pitch_oncc27=200

```

Another way is to use default [‹curve›](../../headers/curve/) 1 which ranges from -1 to 1, and set the pitch control to the tuning range.

```
pitch_oncc27=100
pitch_curvecc27=1

```

[](#practical-considerations)Practical Considerations
-----------------------------------------------------

In ARIA, `tune_*ccN` can also be used as an alias for `pitch_*ccN` (see below).

Name

Version

Type

Default

Range

Unit

tune

SFZ v1

integer

0

\-100 to 100

cents

Modulations

pitch\_onccN

SFZ v2

N/A

N/A

\-9600 to 9600

cents

pitch\_curveccN

SFZ v2

integer

0

0 to 255

N/A

pitch\_smoothccN

SFZ v2

float

0

0 to ?

ms

pitch\_stepccN

SFZ v2

N/A

0

0 to ?

N/A

Category: [Performance Parameters](_misc_categories.md), Pitch

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/tune.md)

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