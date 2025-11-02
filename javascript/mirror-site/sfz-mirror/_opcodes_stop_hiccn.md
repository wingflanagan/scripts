    stop\_loccN / stop\_hiccN - SFZ Format                    Top

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

stop\_loccN / stop\_hiccN
=========================

If a MIDI control message with a value between `stop_loccN` and `stop_hiccN` is received, the region will stop playing. Default value is -1, it means unassigned.

[](#practical-considerations)Practical Considerations
-----------------------------------------------------

This was intended to be used together with [start\_loccN / start\_hiccN](../start_loccN/), but has not yet been implemented, which means this opcode passes the parser in ARIA but has no effect on the region.

Name

Version

Type

Default

Range

Unit

stop\_hiccN

SFZ v2

integer

\-1

0 to 127

N/A

Category: [Region Logic](_misc_categories.md), Triggers

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/stop_hiccN.md)

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