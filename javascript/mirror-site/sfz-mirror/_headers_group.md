    ‹group› - SFZ Format                    Top

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

‹group›
=======

Multiple regions can be arranged in a group. Groups allow entering common parameters for multiple regions.

The group header is different than the [group](../../opcodes/group/) opcode, and it's important to avoid confusing the two. ARIA adds the [polyphony\_group](../../opcodes/polyphony_group/) opcode as an alias for group, to reduce this confusion.

Groups allow entering common parameters for multiple regions. A group is defined with the `‹group›` opcode, and the parameters enumerated on it last till the next group opcode, or till the end of the file.

```
<group>
ampeg_attack=0.04 ampeg_release=0.45
<region> sample=trumpet_pp_c4.wav key=c4
<region> sample=trumpet_pp_c#4.wav key=c#4
<region> sample=trumpet_pp_d4.wav key=d4
<region> sample=trumpet_pp_d#4.wav key=d#4

<group>
ampeg_attack=0.03 ampeg_release=0.42
<region> sample=trumpet_pp_e4.wav key=e4
<region> sample=trumpet_pp_f4.wav key=f4

```

If the same opcode is defined at both the group and region levels, the region setting overrides the group setting and is used. If an opcode is defined under the global level and group level but not region, the group setting overrides the global setting. For example:

```
<group>
ampeg_attack=0.04 ampeg_release=0.45
<region> sample=trumpet_pp_c4.wav key=c4
<region> ampeg_attack=0.05 sample=trumpet_pp_c#4.wav key=c#4
<region> sample=trumpet_pp_d4.wav key=d4
<region> sample=trumpet_pp_d#4.wav key=d#4

```

With the above code, C#4 would use an attack time of 0.05 seconds, while C4, D4 and D#4 would use the 0.04 seconds set at the group level.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/headers/group.md)

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