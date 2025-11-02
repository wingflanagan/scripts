    note\_polyphony - SFZ Format                    Top

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

note\_polyphony
===============

Polyphony limit for playing the same note repeatedly.

[](#example)Example
-------------------

```
note_polyphony=3

```

The difference between applying [polyphony](../polyphony/) across one note and using `note_polyphony` is that note\_polyphony also uses [note\_selfmask](../note_selfmask/) which opens up some additional options. Default self-masking behavior is that higher-or-equal-velocity notes turn off lower-velocity notes, but lower-velocity notes do not turn off higher-velocity notes. A new note will always play.

To be more precise, assuming a `note_polyphony`\=1, the self-masking behavior by default is: - If a low-velocity note is playing, a higher-or-equal velocity note kills the low-velocity note. - If a high-velocity note is playing, a strictly-lower-velocity note will play without killing the high-velocity note.

The `note_polyphony` opcode is thus not a strict polyphony limit but more of a hint for the instrument behavior. This behavior is indeed generally desirable when playing repeated piano notes, hammered dulcimers, etc. It can also be useful for cymbals, although especially with hi-hats, those will often use different notes for different articulations, and `note_polyphony` would be limited to working within an articulation.

The note polyphony is checked within a polyphony group, set by the [group](../group/) or [polyphony\_group](../polyphony_group/) opcodes. If no group is specified on the region (or its group, master or globally) the note polyphony applies to the default group as if [group](../group/)\=0 was specified.

This means that instruments where one note needs to trigger multiple layers, for example drums with separate microphone samples, will usually need to set a separate group number for each microphone position, so the note polyphony limit is tracked separately for each mic.

Name

Version

Type

Default

Range

Unit

note\_polyphony

SFZ v2

integer

N/A

N/A

Category: [Instrument Settings](_misc_categories.md), Voice Lifecycle

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/note_polyphony.md)

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