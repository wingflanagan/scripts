    sw\_last - SFZ Format                    Top

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

sw\_last
========

Enables the region to play if the last key pressed in the range specified by [sw\_lokey and sw\_hikey](_opcodes_sw_lokey.md) is equal to the `sw_last` value.

`sw_last` can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)

[](#example)Example
-------------------

```
sw_last=49

```

This is commonly used to select articulations, for example to switch between sustain, staccato, spiccato and pizzicato in a violin. With the SFZ 1 or SFZ 2 spec, an instrument which uses `sw_last` to select articulations will not have a default articulation preselected, meaning when loaded, it will play no sound until one of the keyswitches is pressed - only after that will the instrument respond to notes. The ARIA extensions include [sw\_default](../sw_default/) as a solution to this.

The difference between this and [sw\_down](../sw_down/) is that sw\_last is a "sticky" keyswitch - after releasing the keyswitch note, it continues to affect notes until another keyswitch is pressed. [sw\_down](../sw_down/), on the other hand, is "non-sticky" and only affects notes played while the switch is held down. This makes `sw_last` a good choice for keyswitching articulations which are often used for many notes in a row, such as sustain or staccato. An example of using `sw_last` to select oscillator waves, with [sw\_default](../sw_default/) used to set the sine to default as well.

```
// **********************************************************************
// A Keyswitching Example
//
// Notes 36,38 and 40 serve as switches to trigger sine, triangle or saw oscillators.
// you can expand on this concept to create your own KeySwitching instruments.
// **********************************************************************
<global>
 sw_lokey=36 sw_hikey=40 sw_default=36

<region> sw_last=36 sw_label=Sine lokey=41 sample=*sine
<region> sw_last=38 sw_label=Triangle lokey=41 sample=*triangle
<region> sw_last=40 sw_label=Saw lokey=41 sample=*saw

```

Name

Version

Type

Default

Range

Unit

sw\_last

SFZ v1

integer

0

0 to 127

N/A

Category: [Region Logic](_misc_categories.md), MIDI Conditions

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/sw_last.md)

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