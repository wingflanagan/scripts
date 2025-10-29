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

Envelope generators (EGs) are used to control the profile of the volume, filter, pitch, or other parameter, based on the timing of the key press and release (including sustain / sostenuto pedal release.) These are often called "ADSRs", after the four parameters (Attack, Decay, Sustain, Release) that were used to control envelopes in early synthesizers (and many current ones as well.)

See [SFZ1 Modulations](../sfz1_modulations/) to see examples of how these can be applied.

SFZ has two types of EGs: SFZ1 and SFZ2.

[](#sfz1-dsahdsr)SFZ1: DSAHDSR
------------------------------

SFZ1 envelopes are sometimes called DSAHDSR after the 7 controls of the envelope, which are applied in the order given below. An EG can control a variety of parameters, but to help understand, you can imagine it controlling the volume, in which case you can substitute "volume" for "EG" below.

Parameter

Suffix

Description

Delay time (s)

\_delay

time to wait after key is depressed until the EG starts

Start **level** (%)

\_start

level at which to start

Attack time (s)

\_attack

time from note start (at start level) to 100% level

Hold time (s)

\_hold

time the volume is held at 100% level

Decay time[1](#fn:1) (s)

\_decay

time[3](#fn:3) for the volume to decrease from 100% to the sustain level

Sustain **level** (%)

\_sustain

the % level at which the EG remains while the key is down or the sustain pedal is down

Release time[2](#fn:2)

\_release

time[3](#fn:3) for the EG to decrease to zero. This begins when both key and sustain pedal are released, even if the prior stages have not completed.

Here is a screenshot of an audio file created using Sforzando, showing the ampeg envelope shape and its stages. Note that this image assumes the Start level is 0. If it were nonzero, the tip of the left-pointing arrow would look chopped off vertically.

![DAHDSR envelope shape image](images/ampeg_env_jpg)

Here's a play-by-play explanation, when using the EG for volume (ampeg\_xxx). When the key is depressed, Delay time elapses and then the note starts (at Start level, which above is the default of 0.) The volume increases (at a constant dB/sec rate) for the Attack time and then reaches the peak level for that note (which is controlled by the velocity and possibly other parameters.) The volume stays at that level for the Hold time, after which it falls off for the Decay time until it reaches the Sustain level. It remains at that level until the key and sustain pedal are both released, when it takes the Release time to fall off to silence.

Note that when using an envelope generator to control volume, it is usually not necessary to adjust release or decay times based on velocity: that will happen naturally. That is, if I configure `ampeg_release`\=1 and play a very loud note, that note will decay with a rate so that one second later it will be about 90 dB quieter than when it started. If I play a very soft note, that note will also decay with the same rate, so that 1 second later it will be 90 dB quieter when it started. That's pretty close to how most natural instruments behave.

Another note when using an envelope to control volume: if you're playing a sample that already has a natural envelope, such as the pluck of a harp string, you normally don't have to configure the envelope because it's already in the sample, which has a natural attack and decay. However, you'll still probably want to configure a release, so that if the key is released before the sample is finished, it doesn't end abruptly. With most natural instruments, this release rate varies with pitch, but not velocity.

[](#sfz2)SFZ2
-------------

The SFZ2 standard has a more flexible generator that can be used in addition to the above. This is briefly described in [SFZ2 Modulations:Envelopes](../sfz2_modulations/#envelopes).

[](#references)References
-------------------------

th:nth-of-type(1){width:20%;}

* * *

1.  Decay time is actually a constant decay **rate** that is specified as the time for the EG to go from 100% to **0%**. However, this can be changed by setting xxx\_decay\_zero=0 to instead mean to decay from 100% to **sustain level** in the given time, from the actual sustain level. [↩](#fnref:1 "Jump back to footnote 1 in the text")
    
2.  Release time is actually a constant decay **rate** that is specified as the time for the EG to go from the **sustain level** to zero. However, this can be changed setting by xxx\_release\_zero=1 to instead mean to decay from **100%** to zero in the given time. [↩](#fnref:2 "Jump back to footnote 2 in the text")
    
3.  When using an amp envelope generator, "0%" means "silence" but it's actually interpreted as -90dBFS for Aria, or -80dBFS for original sfz. This adjustment is needed because volume is contolled in dB, and silence in dB is negative infinity, which complicates the math. [↩](#fnref:3 "Jump back to footnote 3 in the text")[↩](#fnref2:3 "Jump back to footnote 3 in the text")
    

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/envelope_generators.md)

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