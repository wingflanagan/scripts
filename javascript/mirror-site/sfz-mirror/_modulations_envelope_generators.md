    Envelope Generators - SFZ Format                    Top

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

Envelope Generators
===================

Envelope Generator opcodes are part of the [Modulation](../../misc/categories/#modulation.md) category of opcodes:

[](#traditional-sfz-10)Traditional (SFZ 1.0)
--------------------------------------------

Traditional envelope generators using ADSR phases can be set using the SFZ 1.0 **ampeg** (amplitude), **pitcheg** (pitch) and **fileg** (filter) opcodes. These opcodes also support additional delay and hold phases. The phases in order are: **Delay-Attack-Hold-Decay-Sustain-Release**. See below for the full list of relevant opcodes.

[](#flex-sfz-20)Flex (SFZ 2.0)
------------------------------

With SFZ 2.0, you can create one or more "flex" envelope generators. Each flex EG is mapped to a destination (amplitude, pitch, etc.) and contains two or more points with a duration and level determined at each point. The duration indicates the amount of time it takes from the previous envelope point to the current. In this way, you can use flex EGs to essentially draw any envelope shape you desire.

Here is an example flex EG:

```
eg01_pitch=1200
eg01_time1=0 eg01_level1=0
eg01_time2=1 eg01_level2=1
eg01_time3=2 eg01_level3=0.5 eg01_sustain=3
eg01_time4=1 eg01_level4=0

```

How to interpret the opcodes in the example above:

*   All of these opcodes begin with "eg01\_", indicating the first flex EG for the current region. A second flex EG would begin with "eg02\_", and so on.
*   The first opcode determines that the envelope will affect note pitch to a maximum of 1200 cents (one octave).
*   Each envelope point is numbered, and these numbers appear at the end of the opcode name (this opcode has four envelope points). There should be both a "time" and and a "level" opcode specified for each envelope point.
*   The "time" opcodes indicate time duration in seconds from the previous envelope point.
*   The "level" opcodes indicate the level percentage at each envelope point (0-1, with "1" meaning "100%").
*   The optional "sustain" opcode determines which envelope point will function as "sustain" in the traditional ADSR model.

So here is what happens in the four envelope points in the example:

1.  Note starts at original pitch.
2.  Pitch takes one second to rise 1200 cents (one octave).
3.  Pitch takes two seconds to lower to 50% of 1200 cents. The pitch will remain at this level as long as the note is held.
4.  After releasing the note, the note will take one second to lower to the original pitch.

[](#envelope-curves)Envelope Curves
-----------------------------------

SFZ—at least the ARIA Engine and sfizz implementations—uses the following curves for SFZ 1.0 envelopes (**ampeg**, **pitcheg**, **fileg**, probably others but not tested):

*   **Attack:** linear (convex in dB)
*   **Decay:** convex (linear in dB)
*   **Release:** convex (linear in dB)

ARIA supports changing the shape of each phase curve via opcodes such as `ampeg_attack_shape`, `fileg_decay_shape`, etc. Setting the value for any of these to 0 will result in a linear curve shape, with positive and negative values resulting in concave and convex curves, respectively.

Flex EGs (SFZ 2.0) phases all use a linear curve shape by default, but this can be bent into a logarithmic curve using positive/negative values as described in the above paragraph. For example, the following opcode will set the shape of the first eg01 phase to match the convex curve used in the SFZ 1.0 ampeg decay/release: `eg01_shape2=-10.36`

Note that the shape opcode should be placed on the second point affected by the curve. In other words, `eg01_shape2=-10.36` will affect the curve between envelope points 1 and 2.

It is also important to know that ampeg/pitcheg/fileg decay (both SFZ & SF2) behaves differently than flex EG in relation to the sustain level:

*   **ampeg decay:** The level in the decay phase descends at the rate determined by `ampeg_decay` but stops once it hits the sustain level. If your decay phase length is 1 second and sustain is 50%, the sustain level is reached after only half a second in the decay phase (assuming linear phase curve).
*   **flex EG phase:** The level always scales from starting to ending value over the full duration of the phase. When emulating an ADSR envelope using a flex EG, if your decay phase length is 1 second and sustain is 50%, the volume level won't reach 50% until the end of that one second.

If trying to match a SoundFont instrument's logarithmic curves, set the phase's shape to 6 (concave) or -6 (convex). This is only an approximation, as the curve is not identical.

If you wish to use a flex EG to replace the SFZ 1.0 ampeg, set the destination as `eg01_ampeg=100` rather than `eg01_amplitude=100`. This will disable the SFZ 1.0 ampeg and allow the flex EG to provide a release phase.

[](#sfz-1-eg-opcodes)SFZ 1 EG Opcodes
-------------------------------------

The 3 EG destinations in the SFZ 1 standard are: ampeg (amplitude), fileg (filter) and pitcheg (pitch).

The EG destinations are represented by (eg type) in the below list - so `ampeg_attack` would be the amplitude envelope attack, `pitcheg_sustain` would be the pitch envelope sustain level etc.

These are 6-points Delay-Attack-Hold-Decay-Sustain-Release.

*   [(eg type)\_attack](../../opcodes/ampeg_attack/)
*   [(eg type)\_attack\_oncc](../../opcodes/ampeg_attack/)
*   [(eg type)\_decay](../../opcodes/ampeg_decay/)
*   [(eg type)\_decay\_oncc](../../opcodes/ampeg_decay/)
*   [(eg type)\_delay](../../opcodes/ampeg_delay/)
*   [(eg type)\_delay\_oncc](../../opcodes/ampeg_delay/)
*   [(eg type)\_depth](../../opcodes/fileg_depth/)
*   [(eg type)\_dynamic](../../opcodes/ampeg_dynamic/)
*   [(eg type)\_hold](../../opcodes/ampeg_hold/)
*   [(eg type)\_hold\_oncc](../../opcodes/ampeg_hold/)
*   [(eg type)\_release](../../opcodes/ampeg_release/)
*   [(eg type)\_release\_oncc](../../opcodes/ampeg_release/)
*   [(eg type)\_start](../../opcodes/ampeg_start/)
*   [(eg type)\_start\_oncc](../../opcodes/ampeg_start/)
*   [(eg type)\_sustain](../../opcodes/ampeg_sustain/)
*   [(eg type)\_sustain\_oncc](../../opcodes/ampeg_sustain/)
*   [(eg type)\_vel2attack](../../opcodes/ampeg_vel2attack/)
*   [(eg type)\_vel2decay](../../opcodes/ampeg_vel2decay/)
*   [(eg type)\_vel2delay](../../opcodes/ampeg_vel2delay/)
*   [(eg type)\_vel2hold](../../opcodes/ampeg_vel2hold/)
*   [(eg type)\_vel2release](../../opcodes/ampeg_vel2release/)
*   [(eg type)\_vel2sustain](../../opcodes/ampeg_vel2sustain/)

[](#flex-egs-sfz-2-opcodes)Flex EGs (SFZ 2) Opcodes
---------------------------------------------------

Flexible EG can have as many points as needed. level and time for each point is set accordingly.

*   [egN\_curveX](../../opcodes/egN_curveX/)
*   [egN\_dynamic](../../opcodes/egN_dynamic/)
*   [egN\_levelX](../../opcodes/egN_levelX/)
*   [egN\_levelX\_onccY](../../opcodes/egN_levelX/)
*   [egN\_loop](../../opcodes/egN_loop/)
*   [egN\_points](../../opcodes/egN_points/)
*   [egN\_shapeX](../../opcodes/egN_shapeX/)
*   [egN\_sustain](../../opcodes/egN_sustain/)
*   [egN\_timeX](../../opcodes/egN_timeX/)
*   [egN\_timeX\_onccY](../../opcodes/egN_timeX/)

[](#flex-egs-destinations)Flex EGs Destinations
-----------------------------------------------

These destinations are added as a suffix to 'egN\_' - for example, eg01\_pitch=2400 would have envelope 01 modulate pitch, with an envelope depth of 2400 cents.

*   amplitude
*   amplitude\_oncc
*   depth
*   depth\_lfoX
*   depth\_oncc
*   depthadd\_lfoX
*   freq\_lfoX
*   pitch
*   pitch\_oncc
*   cutoff
*   cutoff\_oncc
*   cutoff2
*   cutoff2\_oncc
*   eqNbw
*   eqNbw\_oncc
*   eqNfreq
*   eqNfreq\_oncc
*   eqNgain
*   eqNgain\_oncc
*   pan
*   pan\_oncc
*   resonance
*   resonance\_oncc
*   resonance2
*   resonance2\_oncc
*   volume
*   volume\_oncc
*   width
*   width\_oncc

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/modulations/envelope_generators.md)

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