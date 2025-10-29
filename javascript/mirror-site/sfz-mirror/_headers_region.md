    ‹region› - SFZ Format                    Top

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

‹region›
========

The basic component of an instrument. An instrument is defined by one or more regions.

Inside the definition file, a region starts with the `‹region›` header. A region is defined between two `‹region›` headers, or between a `‹region›` header and a `‹group›` header, or between a `‹region›` header and the end of the file.

Following the `‹region›` header one or more opcodes can be defined. The opcodes are special keywords which instruct the player on what, when and how to play a sample.

Opcodes within a region can appear in any order, and they have to be separated by one or more spaces or tabulation controls. Opcodes can appear in separated lines within a region.

Opcodes and assigned opcode values are separated by the equal to sign (=), without spaces between the opcode and the sign. For instance:

```
sample=trombone_a4_ff.wav
sample=cello_a5_pp_first_take.wav

```

are valid examples, while:

```
sample = cello_a4_pp.wav

```

Is not (note the spaces at the sides of the = sign). Input Controls and Performance Parameters opcodes are optional, so they might not be present in the definition file. An 'expectable' default value for each parameter is pre-defined, and will be used if there's no definition.

Example region definitions:

```
<region> sample=440.wav

```

This region definition instructs the player to play the sample file '440.wav' for the whole keyboard range.

```
<region> lokey=64 hikey=67 sample=440.wav

```

This region features a very basic set of input parameters (lokey and hikey, which represent the low and high MIDI notes in the keyboard), and the sample definition. This instructs the player to play the sample '440.wav', if a key in the 64-67 range is played.

It is very important to note that all Input Controls defined in a region act using the AND boolean operator. Consequently, all conditions must be matched for the region to play. For instance:

```
<region> lokey=64 hikey=67 lovel=0 hivel=34 locc1=0 hicc1=40 sample=440.wav

```

This region definition instructs the player to play the sample '440.wav' if there is an incoming note event in the 64-67 range AND the note has a velocity in the 0~34 range AND last modulation wheel (cc1) message was in the 0-40 range.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/headers/region.md)

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