    SFZ2 modulations - SFZ Format                    Top

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

SFZ2 modulations
================

The [modulations](../../modulations/) available under SFZ2 are much more flexible than the fixed set [specified by SFZ1](../sfz1_modulations/). All SFZ1 modulations are still available under the SFZ2 spec, and will often be easier to use in cases such as envelopes where the standard AHDSR shape is all that's needed.

The basic difference is that SFZ1 has three envelopes - one assigned to volume, one to pitch, and one to filter cutoff. There are also three LFOs, one for each of those modulation targets. SFZ2 can have an arbitraty number of envelopes and LFOs, with the ability to specify one or more modulation targets from a list. It is even possible for LFOs to modulate other LFOs and envelopes to modulate LFOs (but not for LFOs to modulate envelopes). In addition, SFZ2 envelopes can have an arbitrary number of points.

[](#additional-midi-cc-modulation)Additional MIDI CC modulation
---------------------------------------------------------------

SFZ2 adds one more paramter which can be modulated with MIDI CC - [stereo width](../../opcodes/width_onccN/). Also need to document pan\_onccX and find out whether it's SFZ1 or SFZ2 - currently not sure, needs testing.

[](#lfos)LFOs
-------------

For each LFO, an LFO number must be specified - lfo01, lfo02 etc. Each LFO has the following parameters:

[lfoN\_wave](../../opcodes/lfoN_freq/) [lfoN\_freq\_onccX](../../opcodes/lfoN_freq_smoothccX/) [lfoN\_freq\_stepccX](../../opcodes/lfoN_delay/) [lfoN\_delay\_onccX](../../opcodes/lfoN_fade/) [lfoN\_fade\_onccX](../../opcodes/lfoN_phase/) [lfoN\_phase\_onccX](../../opcodes/lfoN_count/)

Click on each link for a detailed description. Similarly to SFZ1 LFOs, there's a frequency, a delay and a fade-in time. In addition, the waveform shape and initial phase can be specified and the LFO can be configured to run for a limited number of counts.

The frequency, delay, fade and initial phase can all be modulated by MIDI CC. There is no modulation for LFO depth - to control the depth of vibrato etc, use MIDI CC to modulate how much the LFO affects the desired target.

[](#available-lfo-targets)Available LFO targets
-----------------------------------------------

The available modulation targets for LFOs are These destinations are added as a suffix to 'lfoN\_'. For example

```
lfo01_pitch=100

```

makes LFO 01 affect pitch with a max depth of 100 cents.

```
lfo03_freq_lfo01_oncc117=1.3

```

would make LFO 03 add up to 1.3 Hertz to the frequency of LFO 01, with the amount modulated by MIDI CC 117.

The avaialble targets related to volume and stereo positioning are:

*   volume
*   volume\_oncc
*   volume\_smoothcc
*   volume\_stepcc
*   amplitude
*   amplitude\_oncc
*   amplitude\_smoothcc
*   amplitude\_stepcc
*   pan
*   pan\_oncc
*   pan\_smoothcc
*   pan\_stepcc
*   width
*   width\_oncc
*   width\_smoothcc
*   width\_stepcc

The targets for pitch modulation are:

*   pitch
*   pitch\_oncc
*   pitch\_smoothcc
*   pitch\_stepcc

The targets for filter modulation are cutoff and resonance, for both the first and second filter:

*   cutoff
*   cutoff\_oncc
*   cutoff\_smoothcc
*   cutoff\_stepcc
*   resonance
*   resonance\_oncc
*   resonance\_smoothcc
*   resonance\_stepcc
*   cutoff2
*   cutoff2\_oncc
*   cutoff2\_smoothcc
*   cutoff2\_stepcc
*   resonance2
*   resonance2\_oncc
*   resonance2\_smoothcc
*   resonance2\_stepcc

The modulations of the EQ bands are:

*   eqNfreq
*   eqNfreq\_oncc
*   eqNfreq\_smoothcc
*   eqNfreq\_stepcc
*   eqNbw
*   eqNbw\_oncc
*   eq1bw\_smoothcc
*   eqNbw\_stepcc
*   eqNgain
*   eqNgain\_oncc
*   eqNgain\_smoothcc
*   eqNgain\_stepcc

The following targets affect other LFOs:

*   freq\_lfoX
*   depth\_lfoX
*   depthadd\_lfoX

Some Cakewalk instruments can also modulate the decim and bitred effects:

*   decim
*   decim\_oncc
*   decim\_smoothcc
*   decim\_stepcc
*   bitred
*   bitred\_oncc
*   bitred\_smoothcc
*   bitred\_stepcc

[](#lfo-examples)LFO examples
-----------------------------

Here is an example of how one LFO could be used to control both pitch vibrato and volume vibrato (tremolo) with the rate, pitch vibrato depth, tremolo depth, delay and fade each controlled by a separate MIDI CC parameter:

```
lfo01_pitch_oncc111=22 // Vibrato LFO
lfo01_freq=2
lfo01_freq_oncc113=7
lfo01_delay_oncc114=0.500
lfo01_fade_oncc115=0.500
lfo01_volume=0 // This LFO also does tremolo
lfo01_volume_oncc112=2

```

And an LFO which does just pitch vibrato, and has a second LFO modulating its rate to create some unsteadiness:

```
lfo01_pitch_oncc111=22 // Vibrato LFO
lfo01_freq=2
lfo01_freq_oncc113=7
lfo01_delay_oncc114=0.500
lfo01_fade_oncc115=0.500

lfo2_freq_lfo1_oncc116=3   //Affect the rate of the other LFO for unsteady vibrato
lfo02_wave=1
lfo02_freq=0.1
lfo02_freq_oncc116=0.9

```

For randomized humanization, the extended MIDI CC 135 can be used to randomize the initial phase and speed of the second LFO.

```
lfo01_pitch_oncc111=22 // Vibrato LFO
lfo01_freq=2
lfo01_freq_oncc113=7
lfo01_delay_oncc114=0.500
lfo01_fade_oncc115=0.500

lfo2_freq_lfo1_oncc116=3   //Affect the rate of the other LFO for unsteady vibrato
lfo02_wave=1
lfo02_freq=0.1
lfo02_freq_oncc116=0.8
lfo02_phase_oncc135=1
lfo02_freq_oncc135=0.2

```

[](#envelopes)Envelopes
-----------------------

SFZ2 envelopes are numbered and can have an arbitrary number of points, with the level at each point and its modulation set separately. The opcodes used to create these envelopes are:

*   [egN\_points](../../opcodes/egN_points/)
*   [egN\_levelX](../../opcodes/egN_levelX/)
*   [egN\_levelX\_onccY](../../opcodes/egN_levelX/)
*   [egN\_timeX](../../opcodes/egN_timeX/)
*   [egN\_timeX\_onccY](../../opcodes/egN_timeX/)
*   [egN\_shapeX](../../opcodes/egN_shapeX/)
*   [egN\_curveX](../../opcodes/egN_curveX/)
*   [egN\_sustain](../../opcodes/egN_sustain/)
*   [egN\_loop](../../opcodes/egN_loop/)

[](#envelope-targets)Envelope targets
-------------------------------------

Similarly to LFOs, envelopes have assignable modulation targets. These destinations are added as a suffix to ‘egN\_’ - so, for example:

```
eg01_pitch=2400

```

would have envelope 01 modulate pitch, with an envelope depth of 2400 cents.

These are the available targets related to amplitude and stereo positioning:

*   amplitude
*   amplitude\_oncc
*   volume
*   volume\_oncc
*   pan
*   pan\_oncc
*   width
*   width\_oncc

Targets for pitch:

*   pitch
*   pitch\_oncc

Targets for filters:

*   cutoff
*   cutoff\_oncc
*   resonance
*   resonance\_oncc
*   cutoff2
*   cutoff2\_oncc
*   resonance2
*   resonance2\_oncc

Targets for EQ bands:

*   eqNbw
*   eqNbw\_oncc
*   eqNfreq
*   eqNfreq\_oncc
*   eqNgain
*   eqNgain\_oncc

Targets for modulating LFOs:

*   depth\_lfo
*   depthadd\_lfo
*   freq\_lfo

These two need to be tested - are they for envelopes to modulate other envelopes?

*   depth
*   depth\_oncc

Targets for modulating decim and bitred do not appear to have been included in the specification.

[](#example-envelope)Example envelope
-------------------------------------

Here is a simple pitch envelope which will start a note with a glide from up to an octave lower, with the depth and time modulated by MIDI CCs. The envelope will statt at a lower value at envelope point 0, and return the pitch to normal at envelope point 1.

```
eg01_sustain=1 //Pitch envelope setup for slides
eg01_level0=1
eg01_level1=0
eg01_time0=0
eg01_time1=0
eg01_pitch_oncc100=-1200
eg01_time1_oncc101=1

```

[](#using-lfos-and-envelopes-together)Using LFOs and envelopes together
-----------------------------------------------------------------------

Here is an example of using both an envelope and an LFO to modulate pitch, with common depth and delay parameters. The goal here is asymmetrical pitch vibrato - vibrato which does not go up and down around the original pitch, but instead only goes below it. This is idiomatic with saxophones, and is also how vibrato with certain types of non-floating guitar bridges works (string-bending vibrato is similar, of course, but in the other direction).

Shifting the phase of LFO01 will make the vibrato waveform start at the top. We also need to lower the pitch by the same amount as the vibrato depth. Using an envelope for this allows us to delay the onset of the vibrato (again, an important element of idiomatic saxophone vibrato) without a discontinuous jump in pitch.

```
lfo01_pitch_oncc111=20 //Saxy vibrato LFO - goes down from the main pitch
lfo01_freq=2
lfo01_freq_oncc112=8
lfo01_phase=0.25 //To make it start at the top
lfo01_delay_oncc116=1
eg01_pitch_oncc111=20
eg01_sustain=1
eg01_level0=0
eg01_level1=0
eg01_level2=-1
eg01_time0=0
eg01_time1=0
eg01_time1_oncc116=1
eg01_time2=0

```

[](#using-sfz1-and-sfz2-modulations-together)Using SFZ1 and SFZ2 modulations together
-------------------------------------------------------------------------------------

Both SFZ1 and SFZ2 modulations may be mixed freely. Indeed, it may be simpler to accomplish the above using the SFZ1 pitch envelope, as it is sufficient in this case, with the SFZ2 LFO. Setting the initial phase and modulating the delay with MIDI CC would not be possible with the SFZ1 pitch LFO.

```
lfo01_pitch_oncc111=20 //Saxy vibrato LFO - goes down from the main pitch
lfo01_freq=2
lfo01_freq_oncc112=8
lfo01_phase=0.25 //To make it start at the top
lfo01_delay_oncc116=1
pitcheg_delay_oncc116=1 //Pitch envelope to drop the central pitch when sax vibrato kicks in
pitcheg_depth_oncc111=-20

```

[](#smoothccn-and-stepccn)SmoothccN and stepccN
-----------------------------------------------

Most MIDI CC modulations, though not all, can have use [smoothccN](../../modulations/smoothccN/) and [stepccN](../../modulations/stepccN/). These work similarly to [bend\_smooth](../../opcodes/bend_smooth/) and [bend\_step](../../opcodes/bend_step/).

SmoothccN adds "inertia" to a modulation, so quickly changing the MIDI CC value has a slower effect on the modulation target than it would normally. StepccN causes the modulation to happen in a discrete number of steps. Setting the number of steps to 1 would make the modulation an all-or-nothing control.

This is what's possible under the SFZ2 specification. There are some additional modulations available as [ARIA extensions](../../opcodes/?v=aria), with [amplitude\_onccN](../../opcodes/amplitude/) being a very useful one.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/sfz2_modulations.md)

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