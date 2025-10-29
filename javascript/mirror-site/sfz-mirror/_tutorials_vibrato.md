    Vibrato - SFZ Format                    Top

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

Vibrato
=======

[](#basic-lfo-vibrato)Basic LFO vibrato
---------------------------------------

Emulating vibrato for solo instruments or voices with LFOs is not difficult. The challenges are understanding the key aspects of vibrato on the real instrument, and keeping the number of parameters from growing too large to be easy to use. The examples here use SFZ 2 spec [numbered LFOs](../../modulations/lfo/), rather than the [dedicated pitch, volume and filter LFOs](../../opcodes/amplfo_depth/) and envelopes of SFZ 1. A lot of this can be done under the SFZ 1 specification as well, but there are some limitations.

The most basic, typical vibrato is pitch vibrato - just an LFO modulating pitch. Making the minimum and maximum rates and depths that would be used by players in real life is important, of course. The numbers here are examples which would be decent for bowed strings - it has a rate of 2-10 Hz and a maximum depth of 35 cents. Wider and slower are certainly possible on real instruments, but isn't commonly used in performance.

```
lfo01_pitch_oncc111=35
lfo01_freq=2
lfo01_freq_oncc112=8

```

[](#additional-parameters)Additional parameters
-----------------------------------------------

In real life, however, players and singers will often start a note without vibrato, and add vibrato a fraction of a second later. This is where modulating the [LFO delay parameter](../../opcodes/lfoN_delay/) becomes useful, and possibly [LFO fade](../../opcodes/lfoN_fade/) as well. Delay seems like enough for most wind instruments and vocals, but having both delay and fade seems effective with bowed strings.

```
lfo01_pitch_oncc111=35
lfo01_freq=2
lfo01_freq_oncc112=8
lfo01_delay_oncc115=0.500
lfo01_fade_oncc116=0.500

```

Vibrato on many instruments doesn't just affect pitch; on bowed strings, it seems to have a subtle effect on volume and timbre as well. We can have the same MIDI CC parameter control how much the vibrato LFO affects pitch, volume, and an EQ band, with the latter two being quite subtle.

This is a good a time as any to note that not all vibrato is equal - it's not really practical to add vibrato to the lowest note playable on a cello, for example, or to a natural harmonic. With pizzicato, vibrato is possible, but probably should not affect the EQ band, and either only affect pitch or pitch plus a subtle effect on volume. The below will work reasonably for most bowed notes, however.

```
lfo01_pitch_oncc111=35
lfo01_volume_oncc111=1
lfo01_freq=2
lfo01_freq_oncc112=8
lfo01_delay_oncc115=0.500
lfo01_fade_oncc116=0.500
eq1_freq=2000
eq1_bw=2
lfo01_eq1gain_oncc111=2
lfo01_eq1freq_oncc111=500

```

[](#humanization)Humanization
-----------------------------

Vibrato can also be humanized, by varying the rate of the vibrato LFO. This can be done by modulating the rate of the vibrato LFO with another LFO. The ARIA sample & hold [waveform](../../opcodes/lfoN_wave/) can be used here, and the modulation depth controlled by MIDI CC, so when that's at zero, no humanization happens.

```
lfo02_freq=1
lfo02_wave=12 //Sample & hold LFO waveform number
lfo02_freq_lfo01_oncc117=1

```

Or, to stay in the SFZ 2 spec and not use ARIA extensions, a sine wave with randomized [starting phase](../../opcodes/lfoN_phase/) will also work:

```
lfo02_freq=1
lfo02_phase_oncc135=1
lfo02_freq_lfo01_oncc117=1

```

However, when playing multiple layers, such as sustain samples with crossfaded dynamics or multiple mic positions, this can cause each layer's vibrato to drift out of sync and sound like separate instruments. This is generally not desirable, so it is possible to pseudo-randomize the starting phase using a non-random [CC, such as velocity](../../extensions/midi_ccs/) (which is often otherwise unused in sustain sounds with crossfaded dynamics). If the SFZ player can have a global sample and hold LFO which does not retrigger for each note, this would also be a solution, though ARIA does not allow this.

```
lfo02_freq=1
lfo02_phase_oncc132=0.7
lfo02_freq_lfo01_oncc117=1

```

This will vary the rate of the vibrato, but the depth will be constant. It is possible to have an LFO modulate the depth of another LFO, measured as a percentage, for example 120% for 20% variation:

```
lfo02_freq=1
lfo02_phase_oncc132=0.7
lfo02_freq_lfo01_oncc117=1
lfo02_depth_lfo01=120

```

For additional complexity, it's also possible to have the random LFO itself modulate pitch, which will create some pitch drift, and have more than two LFOs involved. Here is a fairly sophisticated example.

```
//Vibrato
lfo01_pitch_oncc21=29 //Vibrato LFO
lfo01_freq=2 //Any slower than this sounds really lousy
lfo01_freq_oncc112=6 //8 Hz is about as fast as vibrato on cello can go
lfo01_delay_oncc115=0.500
lfo01_fade_oncc116=0.500
//This LFO also does tremolo
lfo01_volume_oncc21=1 //Not much - just a subtle effect on volume
eq1_freq=2200 //EQ band for vibrato
eq1_bw=2
lfo01_eq1gain_oncc21=3 //Again, pretty subtle

lfo02_wave=1 //Second LFO to make things wobblier
lfo02_phase=0
lfo02_phase_oncc131=0.7 //Phase affected by velocity, to pseudo-randomize while keeping both mics' LFOs in sync
lfo02_freq=0.01 //Basically no movement at very slow speeds, just randomization
lfo02_freq_oncc117=1 //Max rate is not very high, so it doesn't sound too obvious
lfo02_pitch_oncc117=6 //Slight pitch wobbliness
lfo02_freq_lfo01_oncc117=1 //Affect the rate of the other LFO for unsteady vibrato

lfo03_wave=1 //And a third LFO for secondhand complex wobbliness
lfo03_phase=0.4
lfo03_phase_oncc131=0.479 //Different phase response to velocity than the second LFO
lfo03_freq=0.5
lfo03_freq_oncc117=-0.4
lfo03_freq_lfo02_oncc117=1
lfo03_pitch_oncc117=-4

```

However, note that the depth modulation is fixed, and not modulated by cc117 like the frequency modulation is. This is because having a CC modulate the depth modulation does not appear to be implemented in ARIA. It is, however, possible to modulate the depth of a flex envelope with MIDI CC, and then have that envelope depth modulate the depth of the secondary LFO. This is, admittedly, very much a kludge, but it appears to work.

```
lfo02_freq=1
lfo02_phase_oncc132=0.7
lfo02_freq_lfo01_oncc117=1
lfo02_depth_lfo01=120
eg1_level0_oncc117=1
eg1_level1_oncc117=1
eg1_depth_lfo02=100

```

However, when the depth of lfo02 is zero, this will effectively also make lfo01's depth zero, so there will be no vibrato at all unless cc117 is turned up. Getting around this requires another kludge, which is leaving lfo01 with fixed depth and creating yet another LFO for the variable part of the depth.

```
//Vibrato
lfo01_pitch_oncc21=29 //Vibrato LFO
lfo01_freq=2 //Any slower than this sounds really lousy
lfo01_freq_oncc112=6 //8 Hz is about as fast as vibrato on cello can go
lfo01_delay_oncc115=0.500
lfo01_fade_oncc116=0.500
//This LFO also does tremolo
lfo01_volume_oncc21=1 //Not much - just a subtle effect on volume
eq1_freq=2200 //EQ band for vibrato
eq1_bw=2
lfo01_eq1gain_oncc21=3 //Again, pretty subtle

lfo02_pitch_oncc21=19 //Extra LFO for variable depth, shallower than main and pitch only
lfo02_freq=2 //Same timing as first LFO
lfo02_freq_oncc112=6
lfo02_delay_oncc115=0.500
lfo02_fade_oncc116=0.500

lfo03_wave=1 //Third LFO to make the flrst two LFOs wobblier
lfo03_phase=0
lfo03_phase_oncc131=0.7 //Phase affected by velocity, to pseudo-randomize while keeping both mics' LFOs in sync
lfo03_freq=0.01 //Basically no movement at very slow speeds, just randomization
lfo03_freq_oncc117=1 //Max rate is not very high, so it doesn't sound too obvious
lfo03_pitch=6 //Slight pitch wobbliness
lfo03_freq_lfo01=1
lfo03_freq_lfo02=1 //Affect the rate of the vibrato LFOs for unsteady vibrato

lfo04_wave=1 //And a fourth LFO for secondhand complex wobbliness
lfo04_phase=0.4
lfo04_phase_oncc131=0.479 //Different phase response to velocity than the second LFO
lfo04_freq=0.5
lfo04_freq_oncc117=-0.4
lfo04_freq_lfo03=1
lfo04_pitch=-4

lfo03_depth_lfo02=100
lfo04_depth_lfo02=100
eg1_level0_oncc117=1
eg1_level1_oncc117=1
eg1_depth_lfo03=100
eg1_depth_lfo04=100

```

[](#asymmetrical-vibrato)Asymmetrical vibrato
---------------------------------------------

Something similar to the above will work fairly well for a range of strings and voices. However, there are cases where vibrato should only go in one direction - for example, bending guitar strings only moves the pitch upwards, while on saxophone it's possible to play vibrato centered around the pitch, but most of the time players will go only below the pitch. Let's use saxophone vibrato as an example. To keep it simple, let's just go back to a simple, non-humanized vibrato with only depth and rate paremeters.

To have vibrato which will go below the main pitch is simple - the LFO phase can be set so the wave starts at the top, and the note [tuned](../../opcodes/tune/) down by the vibrato depth amount.

```
lfo01_pitch_oncc111=20
lfo01_phase=0.25
lfo01_freq=1.5
lfo01_freq_oncc112=6
pitch_oncc111=-20

```

This will work fine, as long as we don't try to apply delay or fade to the LFO, which would result in the note starting out flat with no vibrato. To solve that problem, we can combine the LFO with a pitch [envelope](../../modulations/envelope_generators/). Here is an example with just delay:

```
lfo01_pitch_oncc111=20
lfo01_freq=1.5
lfo01_freq_oncc112=6
lfo01_phase=0.25
lfo01_delay_oncc116=1
pitcheg_delay_oncc116=1
pitcheg_depth_oncc111=-20

```

To have the choice of idiomatic sax vibrato and violin-style vibrato centered around the pitch can be done separate LFOs and separate depth controls. It's also possible to duplicate all the regions and use [loccN/hiccN](../../opcodes/loccN/) to select between ones with different styles of vibrato.

```
lfo01_pitch_oncc111=20 //Sax vibrato LFO - goes down from the main pitch
lfo01_freq=1.5
lfo01_freq_oncc112=6
lfo01_phase=0.25 //Starts at top
lfo01_delay_oncc116=1
pitcheg_delay_oncc116=1 //Pitch envelope to drop the central pitch when sax vibrato kicks in
pitcheg_depth_oncc111=-20

lfo02_pitch_oncc114=20 //Violin vibrato LFO - goes below and above main pitch
lfo02_freq=1.5
lfo02_freq_oncc112=6 //Same rate as the first LFO
lfo02_phase=0.5 //Starts in the middle, goes down first before going up
lfo02_delay_oncc116=1 //Same delay, too

```

This covers jaw vibrato, but sax players also use diaphragm vibrato, which changes volume and has no effect on pitch, which means there are now three vibrato depths. Having the volume modulated by the second LFO is a little easier, as the phase setting of the first LFO would mean having to apply a volume envelope as well.

```
lfo01_pitch_oncc111=20 //Sax vibrato LFO - goes down from the main pitch
lfo01_freq=1.5
lfo01_freq_oncc112=6
lfo01_phase=0.25 //Starts at top
lfo01_delay_oncc116=1
pitcheg_delay_oncc116=1 //Pitch envelope to drop the central pitch when sax vibrato kicks in
pitcheg_depth_oncc111=-20

lfo02_pitch_oncc114=20 //Violin vibrato LFO - goes below and above main pitch
lfo02_freq=1.5
lfo02_freq_oncc112=6 //Same rate as the first LFO
lfo02_delay_oncc116=1 //Same delay, too
lfo02_phase=0.5 //Starts in the middle, goes down first before going up
lfo02_volume=0 //This LFO also does tremolo
lfo02_volume_oncc113=3

```

There is one additional consideration with diaphragm vibrato - when the volume of the note drops down, the breath noise can become more prominent, especially on quiet notes or when using the subtone technique. If the volume of the breath noise can be modulated separately, the noise regions should not be affected by pitch vibrato, and be affected by the diaphragm vibrato in an opposite direction to the notes. So, if the above vibrato settings are set under a [‹global›](../../headers/global/) header, the breath noise sample regions could have settings similar to this.

```
lfo01_pitch_oncc111=0 //LFOs do not affect pitch
pitcheg_depth_oncc111=0
lfo02_pitch_oncc114=0
lfo02_volume_oncc113=-3 //Diaphragm vibrato affects volume in the opposite direction

```

Humanization and having the diaphragm vibrato affect timbre can be done similarly as with the strings above, ensuring both LFOs are humanized in sync with each other, so they do not drift apart.

[](#more-special-cases)More special cases
-----------------------------------------

Some instruments will have vibrato types which require special treatment, for example guitar tremolo bridges will bend each string's pitch by a different amount when playing chords. This requires different pitch modulation depths for each string. Vibrato can also be used to modulate [filter cutoffs](../../opcodes/cutoff/), which is commonly used in synthesizers to create evolving pads or wobble basses. This is not difficult to implement. Here is an example of a synthesizer style vibrato with a typical lowpass filter, and vibrato which can affect pitch, volume or filter cutoff.

```
//Filter
//Lowpass filter
cutoff=120
cutoff_cc120=13200
fil_keytrack=100
resonance=0
resonance_cc121=12

//Vibrato
lfo01_freq=1
lfo01_freq_oncc112=11
lfo01_delay_oncc115=0.500
lfo01_fade_oncc116=0.500
lfo01_pitch_oncc111=22 //Vibrato LFO affects pitch
lfo01_volume_oncc114=6 //Volume tremolo
lfo01_cutoff=0 //Filter wobble
lfo01_cutoff_oncc113=3600

```

An unusual use of extremely deep vibrato and tremolo plus humanization is emulating vinyl scratching. Pitch sweeps of 2+ octaves with strongly humanized LFO rate can resemble vinyl scratching, though unlike real scratching, these LFOs are not controllable, and therefore rhythmic scratching is not an option.

```
//Extreme vibrato that can resemble vinyl scratching
//The depths are high but will be made even higher by the modulation of the LFO depth
lfo01_pitch_oncc21=1333 //Extremely deep vibrato for vinyl emulation
lfo01_freq=1
lfo01_freq_oncc112=9
//No delay but there is fade
lfo01_fade_oncc116=0.5
//This LFO also does tremolo
lfo01_volume_oncc21=7 //Again very heavy

lfo02_wave=1 //Second LFO to make things wobblier
lfo02_phase=0
lfo02_phase_oncc135=1 //Random
lfo02_freq=0.01 //Basically no movement at very slow speeds, just randomization
lfo02_freq_oncc117=1 //Max rate is not very high, so it doesn't sound too obvious
lfo02_freq_lfo01_oncc117=1 //Affect the rate of the other LFO for unsteady vibrato

lfo03_wave=1 //And a third LFO for secondhand complex wobbliness
lfo03_phase=0.4
lfo03_phase_oncc135=0.479 //Different phase response to velocity than the second LFO
lfo03_freq=0.5
lfo03_freq_oncc117=-0.4
lfo03_freq_lfo2_oncc117=1

lfo03_depth_lfo01=200
lfo02_depth_lfo01=233
eg1_level0_oncc117=1
eg1_level1_oncc117=1
eg1_depth_lfo2=100
eg1_depth_lfo3=100

```

This by no means exhausts all the possibilties of vibrato. It does provide a decent combination of control and realism for a lot of common instrument types, as well as some wild possibilities.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/vibrato.md)

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