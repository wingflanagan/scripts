    SFZ Players - SFZ Format                    Top

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

SFZ Players
===========

There are several SFZ players, which are used to play samples as defined in SFZ files.

Sforzando currently offers the most complete SFZ standard support, including [ARIA extensions](../../opcodes/?v=aria), but SFZ files which only use the [SFZ v1](../../opcodes/?v=1) or [SFZ v2](../../opcodes/?v=2) standard will work with multiple SFZ players.

We use "Free and Open Source" (FOSS) as defined by the [OSI](https://opensource.org/licenses) as "software to be freely used, modified, and shared."

[](#supported-opcodes)Supported Opcodes
---------------------------------------

Below are the known links to the various lists of supported opcodes:\\ [BassMIDI](https://www.un4seen.com/doc/#bassmidi/BASS_MIDI_FontInit.html), [Bitwig](https://github.com/sfz/sfz.github.io/pull/48#issuecomment-731244523), [HISE](https://github.com/christophhart/HISE/blob/master/hi_sampler/sampler/SfzImporter.h#L47), [LinuxSampler](http://linuxsampler.org/sfz/), [liquidsfz](https://github.com/swesterfeld/liquidsfz/blob/master/OPCODES.md), [OpenMPT](https://wiki.openmpt.org/Manual:_SFZ_Implementation), [sfizz](https://sfz.tools/sfizz/development/status/opcodes), [zerberus](https://github.com/musescore/MuseScore/blob/3.6.2/audio/midi/zerberus/README) (MuseScore <= v3.6.2) or else in [our Wiki](https://github.com/sfz/sfz.github.io/wiki/Players).

[](#players)Players
-------------------

Name

License

Linux

macOS

Windows

Description

[Calfbox](https://github.com/kfoltman/calfbox)

GPL-3.0-or-later

✓

✓

✓

C library and Python module to build audio applications like MIDI sequencers or samplers (SFZ or SF2 via Fluidsynth).

[Carla (SFZero)](https://kx.studio/Applications:Carla)

GPL-2.0-or-later

✓

✓

✓

Fully-featured audio plugin host, with support for many audio drivers and plugin formats.

[Grace](https://github.com/s-oram/Grace/)

MIT

X

X

✓

[liquidsfz](https://github.com/swesterfeld/liquidsfz/)

LGPL-2.1

✓

X

X

SFZ sampler library with LV2 and JACK support.

[sfizz](https://sfztools.github.io/sfizz/)

BSD-2-Clause

✓

✓

✓

SFZ library, AU/LV2/VST3 plugin with JACK support.

[SFZero](https://github.com/altalogix/SFZero/)

FOSS

✓

✓

✓

An SFZ (and SF2) player and Juce module.

[Zerberus](https://musescore.org/en/handbook/developers-handbook/references/zerberus-musescore-sfz-synthesizer/)

FOSS

✓

✓

✓

MuseScore SFZ synthesizer.

[LinuxSampler](http://linuxsampler.org/)

Custom

✓

✓

✓

[BassMIDI VSTi](http://falcosoft.hu/softwares.html)

Freeware

X

X

✓

Extension to the BASS audio library, enabling the playing of MIDI files and custom event sequences, using SF2 soundfonts and/or SFZ to provide the sounds. MIDI input is also supported.

[HighLife](https://www.discodsp.com/highlife/)

Freeware

✓

✓

✓

A sampler with integrated effects and wave editor, with support for WAV, MP3, OGG, RAW, FLAC, SND (Akai MPC 2000) and even AKP (Akai S5000/S6000) audio formats.

[sforzando](https://plogue.com/products/sforzando.html)

Freeware

✓

✓

✓

A free, highly SFZ 2.0 compliant sample player. Supports almost all SFZ v1 and v2 opcodes, plus ARIA extensions.

[TX16Wx Sampler](https://www.tx16wx.com/)

Freeware

✓

✓

✓

[Zampler](https://www.zampler.de/)

Freeware

X

✓

✓

Synth-based sample player using SFZ format as its sound generator. It supports very minimal SFZ v1 opcodes, only for key-range and velocity-range mapping.

[ARIA](http://ariaengine.com/)

OEM

X

✓

✓

An audio sampling and synthesis Engine based on the SFZ 1.0 / SFZ 2.0 open file formats for instrument programming and the Scala open file format to define scales and temperaments.

[Bliss Sampler](https://www.discodsp.com/bliss/)

Commercial

✓

✓

✓

An UI themable sampler and wave editor in VST2/3 and AU audio plugin format with selectable high quality interpolation and integrated effects.

[Samplelord](https://www.samplelord.com/)

Commercial

X

X

✓

Sample player as standalone or VSTi plugin for Windows 32-bit OS that can load different sounds in different formats. Has basic parameter controls, supports only SFZ v1 opcodes.

[TAL-Sampler](https://tal-software.com/products/tal-sampler)

Commercial

✓

✓

✓

[Unify](https://www.pluginguru.com/products/unify-standard/)

Commercial

X

✓

✓

[Falcon](https://www.uvi.net/falcon.html)

Commercial

X

✓

✓

[Wusik 8008, Wusik One, Wusik EVE V5](https://www.wusik.com/)

Commercial

X

X

✓

[sfz-web-player](https://github.com/kmturley/sfz-web-player)

CC0-1.0

✓

✓

✓

TypeScript/JavaScript SFZ player using the Web Audio API.

[](#import-from-sfz)Import from SFZ
-----------------------------------

Name

License

Linux

macOS

Windows

Description

[Bitwig Studio](https://www.bitwig.com/)

Commercial

✓

✓

✓

Sampler device supports the import of SFZ. Also via drag & drop.

[HISE](http://hise.audio/)

GPL-3.0

✓

✓

✓

[MSoundFactory](https://www.meldaproduction.com/MSoundFactory)

Commercial

X

✓

✓

Sampler module imports/exports SFZ.

[Nexus](https://refx.com/nexus/)

Commercial

X

✓

✓

A 16 layer synthesizer with up to 64 oscillators. Layers can be created from .sfz instruments via drag & drop.

[OpenMPT](https://openmpt.org/)

BSD-3-Clause

X

X

✓

[Poise](https://www.onesmallclue.com/index.html)

Freeware

X

X

✓

Simple 16 drum pads percussion sampler, 8 layers. Very limited SFZ support.

[Renoise (Redux)](https://www.renoise.com/)

Commercial

✓

✓

✓

[Serum 2](https://xferrecords.com/products/serum-2)

Commercial

X

✓

✓

a wavetable synthesizer with multiple oscillator types. Multisample Oscillator gives you the option to use xfer factory .sfz library or import your own .sfz instruments.

[](#no-longer-available)No longer available
-------------------------------------------

*   Alchemy (Camel Audio was acquired by Apple, and the current incarnation of Alchemy no longer supports SFZ.)
*   Cakewalk [sfz](https://web.archive.org/web/20071011005744/http://www.rgcaudio.com/sfz.htm) (backup on web.archive.org)
*   Equator 2 (per [Equator 2 FAQ](https://support.roli.com/support/solutions/articles/36000255935-equator2-faqs#Can-I-import-my-own-samples-or-wavetable-files-into-Equator2?), "SFZ import is not currently supported")

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/software/players.md)

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