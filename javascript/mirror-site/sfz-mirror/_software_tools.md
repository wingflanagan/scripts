    SFZ Creation Tools - SFZ Format                    Top

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

SFZ Creation Tools
==================

Although SFZ files can be created with any text editor, and some users have also created SFZ with spreadsheets, there are some dedicated tools which can make mapping large amounts of samples easier. As SFZ instruments can quickly grow to thousands of samples, efficiency in creating the mappings becomes important. One way of creating SFZ files is to use one of these tools to create the initial maps with keys, dynamic layers, round robins etc. defined, then add controls etc. using a text editor.

[](#automappers)Automappers
---------------------------

Name

License

Linux

macOS

Windows

Description

[SFZ Python Automapper](https://vis.versilstudios.com/sfzconverter.html#u13452-4)

Public Domain

✓

✓

✓

[Folder-to-SFZ converter](http://vis.versilstudios.net/sfzconverter.html)

Freeware

✓

✓

✓

[Bjoerns Sample Mapper](https://www.bjoernbojahr.de/bjoerns-sample-mapper.html)

Freeware

X

✓

✓

[soundmap](https://codeberg.org/KMIJPH/soundmap)

GPL-3.0

✓

✓

✓

Online automapper. Can create .sfz and .dspreset

[](#converters)Converters
-------------------------

Name

License

Linux

macOS

Windows

Description

[ConvertWithMoss (Java)](https://www.mossgrabers.de/Software/ConvertWithMoss/ConvertWithMoss.html)

LGPL-3.0-only

✓

✓

✓

Converts multisamples in a specific source format to a different destination format.

[exs2sfz (Python)](_assets_src_exs2sfz_py.md)

ISC

✓

✓

✓

EXS24 to SFZ sample library metadata converter.

[SFZ to HISE Converter](https://keypleezer.com/sfz-to-hise-converter/)

MIT

✓

✓

✓

Parses and translates/converts SFZ instruments to HISE samplemaps and extracts SFZ opcode data to a JS/JSON object. Runs in a web browser.

[EXS2SFZ](https://www.bjoernbojahr.de/exs2sfz.html)

Freeware

X

✓

✓

Imports sample mapping information from EXS24 instruments and generates SFZ files from it.

[TX2SFZ](https://www.kvraudio.com/product/tx2sfz-by-derknott)

Freeware

X

X

✓

Converts sample mapping information from TX16WX sampler to SFZ.

[Awave Studio](https://www.fmjsoft.com/awavestudio.html#main)

Commercial

X

X

✓

Multi-purpose audio tool that reads a veritable host of audio carrying file formats from different platforms, synthesizers, trackers, mobile phones. It can be used in a variety of ways; as a file format converter, as an audio editor, or as a synth instrument editor.

[Chicken Systems Translator](https://www.chickensys.com/products2/translator/index.html)

Commercial

X

✓

✓

[Extreme Sample Converter](https://extranslator.com/index.php?page=exsc)

Commercial

X

X

✓

[sfz-tools-cli](https://github.com/kmturley/sfz-tools-cli)

CC0-1.0

✓

✓

✓

Command line interface comprised of several tools to read, convert and parse SFZ and audio files.

[](#editors)Editors
-------------------

Name

License

Linux

macOS

Windows

Description

[Polyphone](https://www.polyphone-soundfonts.com/en/)

GPL-3.0

✓

✓

✓

An open-source soundfont editor for creating musical instruments. Note: being a soundfont editor (sf2) it has limited sfz support when exporting.

[sfZed](https://github.com/sfz/bin/releases/download/utilities/sfZed09.zip)

Freeware

X

X

✓

An editor for the SFZ format used by certain VST instruments. It will also convert Soundfont SF2 to SFZ and works with a midi keyboard to allow you to play and set values, including mapping drum samples.

[](#loop-editors)Loop Editors
-----------------------------

Name

License

Linux

macOS

Windows

Description

[LoopAuditioneer](https://loopauditioneer.sourceforge.io/)

GPL-3.0-or-later

✓

X

✓

Software for evaluating, creating and manipulating loops and cues and other properties of wav file metadata.

[Edison](https://www.image-line.com/fl-studio-learning/fl-studio-online-manual/html/plugins/Edison.htm)

Commercial

X

✓

✓

Fully integrated audio editing and recording tool in FL Studio.

[Endless WAV](https://www.bjoernbojahr.de/endlesswav.html)

Freeware

X

✓

✓

Software to create sustain loops in WAV files (8, 16 and 24 bit) with loop mix, auto loop, realtime crossfade, fade and cut functions.

[Wavosaur](https://www.wavosaur.com/)

Freeware

X

X

✓

Software for editing, processing and recording sounds, wav and mp3 files. Wavosaur has all the features to edit audio (cut, copy, paste, etc.) produce music loops, analyze, record, batch convert. Supports VST plugins, ASIO driver, multichannel wav files, real time effect processing.

[](#misc)Misc
-------------

Name

License

Linux

macOS

Windows

Description

[Freepats-tools](https://github.com/freepats/freepats-tools)

GPL-3.0

✓

✓

✓

Tools to manage, create and convert sound fonts, collections of sampled musical instruments and sound banks. Originally created for the [FreePats project](http://freepats.zenvoid.org/).

[sfzlint](https://github.com/jisaacstone/sfzlint/)

MIT

✓

✓

✓

Linter and parser for .sfz files.

[sfz-tools-core](https://github.com/kmturley/sfz-tools-core)

CC0-1.0

✓

✓

✓

TypeScript/JavaScript library to read, convert and parse SFZ and audio files.

[](#syntax-highlighting)Syntax Highlighting
-------------------------------------------

Name

License

Linux

macOS

Windows

Description

[CudaText Editor](http://uvviewsoft.com/cudatext/)

MPL-2.0

✓

✓

✓

[SFZ major mode for GNU Emacs](https://github.com/sfztools/emacs-sfz-mode)

MIT

✓

✓

✓

[for Geany](https://github.com/sfztools/syntax-highlighting-geany)

FOSS

✓

✓

✓

[for gedit](https://github.com/sfztools/syntax-highlighting-gedit)

FOSS

✓

✓

✓

[for Kate](https://www.pling.com/p/1840691/)

MIT

✓

✓

✓

[for Sublime Text](https://github.com/sfztools/syntax-highlighting-sublime-text)

FOSS

✓

✓

✓

[for VSCode](https://github.com/jokela/vscode-sfz)

MIT

✓

✓

✓

[for Notepad++](https://github.com/sfztools/syntax-highlighting-notepad-plus-plus)

FOSS

X

X

✓

[for Notepad++](http://www.drealm.info/sfz/sfz-udl.xml)

FOSS

X

X

✓

[SFZ Tools for UltraEdit](https://noisesculpture.com/sfz-tools/)

FOSS

✓

✓

✓

Some Windows only software can be used under other Unix based operating systems using [Wine](https://www.winehq.org/) / [CrossOver](https://www.codeweavers.com/) or in a virtual machine software like [VirtualBox](https://www.virtualbox.org/).

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/software/tools.md)

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