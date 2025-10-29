    lokey / hikey - SFZ Format                    Top

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

lokey / hikey
=============

Determine the low boundary of a certain [region](_headers_region.md).

When a region only covers one note, it is generally more convenient to use [key](../key/) instead of `hikey` and `lokey`. When `hikey` and `lokey` are used, they will usually need to be used together with [pitch\_keycenter](../pitch_keycenter/).

These opcodes, as well as [key](../key/), can use either MIDI note numbers (0 to 127) or MIDI note names (e.g. c3 or D#4). Using note numbers is recommended, however, as note numbers are interpreted consistently, while the same note names can be mapped to note numbers an octave or even two apart in different DAWs.

In the SFZ 1 specification, the allowed range is 0 to 127. However, SFZ 2 additionally includes the possibility to set lokey and hikey to -1, to prevent a region from being triggered by any keys. This is a way (though, admittedly, not a very elegant one) to use the [on\_loccN / onhiccN](../on_loccN/) opcodes to trigger, for example, pedal noises which are triggered whether any keys are pressed or not.

[](#examples)Examples
---------------------

```
<region> sample=*sine lokey=72 hikey=84

```

As with the [key](../key/) opcode, the values can also be MIDI note names:

```
<region> sample=*sine lokey=c5 hikey=c6

```

When an instrument is sampled every minor third, this kind of usage will be common:

```
<region> sample=a4.wav  lokey=68 hikey=70 pitch_keycenter=69
<region> sample=c5.wav  lokey=71 hikey=73 pitch_keycenter=72
<region> sample=eb5.wav lokey=74 hikey=76 pitch_keycenter=75

```

Name

Version

Type

Default

Range

Unit

lokey

SFZ v1

integer

0

0 to 127

N/A

Category: [Region Logic](_misc_categories.md), Key Mapping

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/lokey.md)

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