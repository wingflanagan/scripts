    seq\_position - SFZ Format                    Top

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

seq\_position
=============

Sequence position. The region will play if the internal sequence counter is equal to `seq_position`.

This is used together with [seq\_length](../seq_length/) to use samples as round robins. The player will keep an internal counter creating a consecutive note-on sequence for each region, starting at 1 and resetting at seq\_length. Maximum allowed value is 100.

[](#example)Example
-------------------

```
seq_length=4 seq_position=2

```

In above example, the region will play on the second note every four notes.

A typical usage for a kick drum with four round robins, and a snare with three round robins, would look like this:

```
<group>key=36 seq_length=4
<region>seq_position=1 sample=kick_rr1.wav
<region>seq_position=2 sample=kick_rr2.wav
<region>seq_position=3 sample=kick_rr3.wav
<region>seq_position=4 sample=kick_rr4.wav

<group>key=38 seq_length=3
<region>seq_position=1 sample=snare_rr1.wav
<region>seq_position=2 sample=snare_rr2.wav
<region>seq_position=3 sample=snare_rr3.wav

```

An alternative to this is using [lorand / hirand](../lorand/) for random, instead of sequential, round robins. If there are enough samples available, both methods can also be combined - the combination is described on the [lorand / hirand](../lorand/) page. However, lorand/hirand might not be a good idea to use with samples which have multiple microphone positions, and sticking to `seq_position` and [seq\_length](../seq_length/) might be necessary.

[](#practical-considerations)Practical Considerations
-----------------------------------------------------

In at least some SFZ players, sequence position is not tracked together for all regions, which means `seq_position` is not a practical way to implement alternating left/right hand or up/down bowing samples.

Some players also match velocity ranges for each step in the sequence, which can cause problems when the sequence steps do not have the same velocity layer split points. For example, this can produce occasional silence, depending on the velocity of incoming MIDI notes, the velocity of the previous MIDI note, and the current point in the sequence:

```
<global>
seq_length=2
key=48

<group> seq_position=1
<region> lovel=1 hivel=31 sample=*noise
<region> lovel=32 hivel=127 sample=*saw

<group> seq_position=2
<region> lovel=1 hivel=95 sample=*noise
<region> lovel=96 hivel=127 sample=*saw

```

This will also happen in cases where, for example, one step in the sequence has three velocity layers and the other step has four, as it's not possible to make the layer split points match then.

In those players, this is a workaround:

```
<global>
seq_length=2
key=48

<group> seq_position=1
<region> lovel=1 hivel=31 sample=*noise
<region> lovel=32 hivel=95 sample=*saw
<region> lovel=96 hivel=127 sample=*saw

<group> seq_position=2
<region> lovel=1 hivel=31 sample=*noise
<region> lovel=32 hivel=95 sample=*noise
<region> lovel=96 hivel=127 sample=*saw

```

Setting `seq_position` to 0 will cause the region to not play in most sfz player, except for sfizz where it will behave the same as setting `seq_position` to 1.

Name

Version

Type

Default

Range

Unit

seq\_position

SFZ v1

integer

1

1 to 100

N/A

Category: [Region Logic](_misc_categories.md), Internal Conditions

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/seq_position.md)

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