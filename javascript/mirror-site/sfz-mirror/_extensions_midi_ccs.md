    Extended MIDI CCs - SFZ Format                    Top

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

Extended MIDI CCs
=================

In the MIDI specification, [MIDI Control Change Messages](https://www.midi.org/specifications-old/item/table-3-control-change-messages-data-bytes-2) can have numbers from 0 to 127.

[SFZ 2](../../opcodes/?v=2) and [ARIA](../../opcodes/?v=aria) add some special CCs numbered 128 and above.

The additions in SFZ 2 are:

*   pitch bend: 128
*   channel aftertouch: 129
*   polyphonic aftertouch: 130
*   note on velocity: 131
*   note off velocity: 132
*   keyboard note number: 133
*   keyboard note gate: 134
*   unipolar random: 135
*   bipolar random: 136
*   alternate: 137

Values such as note on velocity and MIDI note number, when used as CCs, do not behave exactly the same as note number or velocity of the note itself, in some contexts. This is because once a note is played, its MIDI note number and note on velocity remain the same for that note. MIDI CC, however, is shared across the entire instrument, and this means another note on or note off event will change CC 131, 132 and 133. This can give unexpected results when using these CCs to adjust keytracking or velocity tracking of various parameters, especially in polyphonic instruments with long-sustaining sounds.

Note gate is an on/off - it's 0 when no MIDI notes are pressed, and 1 when at least one note is currently pressed. Unipolar random is from 0 to 1. Bipolar random is from -1 to 1. Alternate changes between 0 and 1 every time a note on message is received.

Some of the parameters, such as aftertouch and note off velocity, are rarely supported by modern MIDI hardware controllers, though they are part of the MIDI specification and can be edited in DAWs. Many MIDI keyboards will send a default note off velocity, such as 64, with every note off event regardless of how fast the key was actually moving at the time.

Anything above 137 is not specified in the SFZ 2 standard and strictly engine-dependent. ARIA adds more. Some of these might not work properly in all DAWs.

*   keydelta: 140
*   keydelta absolute: 141
*   host tempo (bpm): 142
*   host transport status (0 is off, 1 on in non-loop mode, 2 is playing in loop mode): 143
*   host sample rate: 144
*   time since the engine has been up: 145
*   current time signature numerator: 146
*   current time signature denominator: 147
*   position since song start in PPQ (pulses per quarter note): 148
*   position since bar start in PPQ: 149
*   time since the instrument has been up: 150
*   time since last key on (in seconds): 151
*   time since last key off (in seconds): 152
*   number of keys currently down: 153
*   number of currently active voices: 154
*   last playahead (offset) of any sample in the instrument: 155

[](#practical-considerations)Practical Considerations
-----------------------------------------------------

While all the "regular" CCs have the same range of 0 to 127, and some of these extended CCs behave the same way (for example CC 131 or note on velocity), others do not. CC136 or bipolar random can have a negative value, for example. Many will often have non-integer values. These CCs will not always behave the same as others and have not been thoroughly documented.

Some of the additional CCs are shared across all instances of the ARIA engine currently running, for example the host tempo. Others can have concurrently have a different value for different instances or different instruments concurrently, for example keydelta.

CC 140 and 141 are measured in half-steps. So, the below will result in an envelope with a depth of 100 cents per half-step. This is typically what would be used for portamento glides.

```
eg07_pitch_oncc140=100

```

Using locc and hicc with CC 140 and 141 does not work the same as for other CCs. However, they can be used with lohdcc and hihdcc. For example, the below will restrict a region to play only when the interval between the current note and the previous one is an octave, ascending. Whether the decimal is necessary needs to be tested, but the below is confirmed to work.

```
lohdcc140=12
hihdcc140=12.1

```

Using lohdcc alone does not work and will result in the region not triggering, but adding hihdcc with a high value will. The below example was tested in an instrument with a range of less than two octaves, and there works as a way to trigger some regions only when the interval is more than one octave in either direction.

```
lohdcc141=12.1
hihdcc141=24

```

CC 151 is reset as soon as a new note is hit, so it cannot be used to measure the time between the previous note and the current one, for adaptive legato speed purposes. It can, however, be used to control the triggering of release samples. Like CC140 and CC141, it also requires using hdcc to function properly - which makes sense, as time since note-on as measured in seconds usually involves fractions of a second in real scenarios.

In Cakewalk Dimension Pro, 140 is bitred and 141 is decim.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/extensions/midi_ccs.md)

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