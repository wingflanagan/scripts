    sample - SFZ Format                    Top

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

sample
======

Defines which sample file the region will play.

Possibly the most important opcode, this is the one that tells the sampler which sample file to actually play. This should include a relative file path from the folder where the SFZ file is.

In most cases, there will be a sample opcode in every region of an SFZ file, though not always.

If the sample file is not found, the player will ignore the whole region contents as there's nothing to play. Long names and names with blank spaces and other special characters (excepting the = character) are allowed in the sample definition.

Getting the sample to play back at the correct pitch is not automatic, and generally can't be done with the sample opcode alone, even if the file name includes pitch information. Assuming that the tune or transpose opcodes are not used to change the pitch, the sample will play unchanged in pitch when a note equal to the [pitch\_keycenter](../pitch_keycenter/) opcode value is played. If [pitch\_keycenter](../pitch_keycenter/) is not defined for the region, sample will play unchanged on note 60 (middle C). If [pitch\_keytrack](../pitch_keytrack/) is set to 0, the sample will also play unchanged in pitch, regardless of how [pitch\_keycenter](../pitch_keycenter/) is set. If the key opcode is used to define the range of the sample (instead of [lokey](../lokey/), [hikey](../hikey/) and [pitch\_keycenter](../pitch_keycenter/)) the sample will also be unchanged in pitch.

[](#formats)Formats
-------------------

At the SFZ1 specification level, the supported sample formats are: + WAV of any sample rate + Ogg Vorbis compressed samples

For SFZ2, the Cakewalk book specifies the following sample types in addition of the above: + AIFF of any sample rate + [FLAC](https://en.wikipedia.org/wiki/FLAC) support is not specified as mandatory, though FLAC was supported by Cakewalk Session Drummer, and is supported by ARIA

See also [Features](#features) section in the home page.

WAV is usually the first choice, or perhaps AIFF when using macOS. FLAC is the second choice, as it is [lossless](https://en.wikipedia.org/wiki/Lossless_compression) compression audio is always preferable, though it needs to be decoded which can cause slower performance compared to WAV. Other compressed formats can be used for test cases or situations where keeping the file size small is more important than audio quality.

See also the table of supported sample [formats](../../software/engines/) by some engines for more details.

[](#examples)Examples
---------------------

```
sample=A3.wav
sample=..\Samples\close\c4_pp_rr3.wav

```

Each engine can also support custom oscillators. For example, ARIA supports using this opcode for some basic synthesized sound waves such as:

```
sample=*sine
sample=*saw
sample=*square
sample=*triangle
sample=*tri
sample=*noise
sample=*silence

```

Tri is an alias for triangle. For cases where we don't want to actually play a sample but want a region to exist and be played (for example, to mute other sounds when using [group](../group/) and [off\_by](../off_by/), the silence value can be very convenient).

Note that in this case the `*` is a real character and not a wildcard.

Name

Version

Type

Default

Range

Unit

sample

SFZ v1

string

N/A

N/A

Category: [Sound Source](_misc_categories.md), Sample Playback

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/opcodes/sample.md)

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