    Modular SFZ Instruments - SFZ Format                    Top

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

Modular SFZ Instruments
=======================

[](#the-include-statement)The Include Statement
-----------------------------------------------

SFZ is not a programming language, and has a structure based on a hierarchy of headers. There are no procedure or function calls which would allow the same block of code to be called from various places in an SFZ file. This can lead to a lot of repetition in large SFZ instruments. As a simple example, here's a polyphony switch in an instrument causing duplication of the sample map.

```
<group>
hicc100=63
<region>key=48 sample=c4.wav
<region>key=49 sample=db4.wav
<region>key=50 sample=d4.wav
<region>key=51 sample=eb4.wav
<region>key=52 sample=e4.wav
<region>key=53 sample=f4.wav
<region>key=54 sample=gb4.wav
<region>key=55 sample=g4.wav
<region>key=56 sample=ab4.wav
<region>key=57 sample=a4.wav
<region>key=58 sample=bb4.wav
<region>key=59 sample=b4.wav
<region>key=60 sample=c5.wav

<group>
locc100=64
group=1
off_by=1
<region>key=48 sample=c4.wav
<region>key=49 sample=db4.wav
<region>key=50 sample=d4.wav
<region>key=51 sample=eb4.wav
<region>key=52 sample=e4.wav
<region>key=53 sample=f4.wav
<region>key=54 sample=gb4.wav
<region>key=55 sample=g4.wav
<region>key=56 sample=ab4.wav
<region>key=57 sample=a4.wav
<region>key=58 sample=bb4.wav
<region>key=59 sample=b4.wav
<region>key=60 sample=c5.wav

```

If we create an SFZ file called sample\_map.sfz with the following content:

```
<region>key=48 sample=c4.wav
<region>key=49 sample=db4.wav
<region>key=50 sample=d4.wav
<region>key=51 sample=eb4.wav
<region>key=52 sample=e4.wav
<region>key=53 sample=f4.wav
<region>key=54 sample=gb4.wav
<region>key=55 sample=g4.wav
<region>key=56 sample=ab4.wav
<region>key=57 sample=a4.wav
<region>key=58 sample=bb4.wav
<region>key=59 sample=b4.wav
<region>key=60 sample=c5.wav

```

Then the sample map becomes a reusable module which can be "called" using an [#include](../../opcodes/include/) statement. The instrument can be decluttered to this:

```
<group>
hicc100=63
#include "sample_map.sfz"

<group>
locc100=64
group=1
off_by=1
#include "sample_map.sfz"

```

[](#include-and-file-paths)Include And File Paths
-------------------------------------------------

With large instruments which would be broken down into many files, the included files can be placed in a different folder or in a subfolder of the folder containing the instruments. Regardless of which file folder the included files are in, the sample file paths and include file paths will be calculated starting with the folder which contains the instrument file.

So, if our above example instrument has the main SFZ file, called main.sfz, in a Programs folder under the instrument root, samples in a Samples folder under that, and the sample\_map.sfz is in Programs/mappings, then main.sfz should contain:

```
<group>
hicc100=63
#include "mappings/sample_map.sfz"

<group>
locc100=64
group=1
off_by=1
#include "mappings/sample_map.sfz"

```

The sample\_map.sfz file in mappings should have the following contents:

```
<region>key=48 sample=../Samples/c4.wav
<region>key=49 sample=../Samples/db4.wav
<region>key=50 sample=../Samples/d4.wav
<region>key=51 sample=../Samples/eb4.wav
<region>key=52 sample=../Samples/e4.wav
<region>key=53 sample=../Samples/f4.wav
<region>key=54 sample=../Samples/gb4.wav
<region>key=55 sample=../Samples/g4.wav
<region>key=56 sample=../Samples/ab4.wav
<region>key=57 sample=../Samples/a4.wav
<region>key=58 sample=../Samples/bb4.wav
<region>key=59 sample=../Samples/b4.wav
<region>key=60 sample=../Samples/c5.wav

```

This means that opening the main.sfz file will work, but trying to open sample\_map.sfz directly would not, as it would try to locate the samples in a relative path of ../Samples, which exists when starting from Programs, but does not exist when starting from Programs/modules. This can make testing sample maps somewhat messy, as they need to be moved out of their "proper" folder if the map needs to be tested by itself, without the rest of the SFZ.

[](#include-and-nesting)Include And Nesting
-------------------------------------------

Included files can, themselves, include files. This is not a problem, just avoid circular recursion.

[](#other-use-cases-for-include)Other Use Cases For Include
-----------------------------------------------------------

In addition to sample maps, modulations can also be reused. For example, a common set of vibrato controls can be included for violin samples which need them, but left out for samples which don't, such as harmonics, percussive noises and legato transitions. Different dynamics controls for long vs. short bowed articulations are also candidates for such treatment.

```
<master>
sw_last=34
sw_label=Sustain
#include "modules/vibrato.sfz"
#include "modules/long_dynamics.sfz"
#include "mappings/sustain.sfz"

<master>
sw_last=33
sw_label=Staccato
#include "modules/vibrato.sfz"
#include "modules/short_dynamics.sfz"
#include "mappings/staccato.sfz"

<master>
sw_last=32
sw_label=Natural harmonics
#include "modules/long_dynamics.sfz"
#include "mappings/harmonics.sfz"

<master>
sw_last=31
sw_label=Percussive noises
#include "modules/short_dynamics.sfz"
#include "mappings/noises.sfz"

```

The same file can also be included in multiple instruments, for example a violin spiccato articulation map can be used in both a spiccato-only instrument and in a keyswitch instrument which contains other articulations as well.

Putting each set of round robins inside its own file without defining [seq\_position](../../opcodes/seq_position/) inside that file can also be useful for emulating double-tracking. If the basic non-doubletracked instrument is set up like this:

```
<global>
seq_length=4

<group>
seq_position=1
#include "mappings/palm_mute_rr1_map.sfz"
<group>
seq_position=2
#include "mappings/palm_mute_rr2_map.sfz"
<group>
seq_position=3
#include "mappings/palm_mute_rr3_map.sfz"
<group>
seq_position=4
#include "mappings/palm_mute_rr4_map.sfz"

```

It then becomes very simple to make a doubletracked instrument which uses differnt round robins in the left and right channels:

```
<global>
seq_length=4

<group>
pan=100
seq_position=1
#include "mappings/palm_mute_rr1_map.sfz"
<group>
pan=100
seq_position=2
#include "mappings/palm_mute_rr2_map.sfz"
<group>
pan=100
seq_position=3
#include "mappings/palm_mute_rr3_map.sfz"
<group>
pan=100
seq_position=4
#include "mappings/palm_mute_rr4_map.sfz"

<group>
pan=-100
seq_position=1
#include "mappings/palm_mute_rr2_map.sfz"
<group>
pan=-100
seq_position=2
#include "mappings/palm_mute_rr3_map.sfz"
<group>
pan=-100
seq_position=3
#include "mappings/palm_mute_rr4_map.sfz"
<group>
pan=-100
seq_position=4
#include "mappings/palm_mute_rr1_map.sfz"

```

[](#include-and-headers)Include And Headers
-------------------------------------------

When including files, it's common to put lower levels of [header](../../headers/) organization, such as region and group in the included file, and put higher levels in the main file. However, this is not necessary, and any levels of headers can be included. It is important to keep in mind that included files are essentially just concatenated to make the SFZ file which the SFZ instrument actually parses. Although an included file is a little like a procedure in a programming language, it isn't really one, and the end of the included file is not meaningful when

SFZ opcodes set under headers within an included file will be in effect until encountering another header of the same or higher level. For example, let's say a snare drum sample map contains one-shot samples under `<region>` headers and also multisampled hits under a `<group>` header later in the file, and this file is called snare\_map.sfz.

```
<region>
key=37
sample=Sidestick.wav
<region>
key=39
sample=Off_center.wav
<region>
key=40
sample=Rimshot.wav
<group>
key=38
seq_length=4
<region>
seq_position=1
sample=Center_rr1.wav
<region>
seq_position=2
sample=Center_rr2.wav
<region>
seq_position=3
sample=Center_rr3.wav
<region>
seq_position=4
sample=Center_rr4.wav

```

If we want to put snare controls which apply to all those, this would work:

```
<master>
amplitude_oncc100=100
tune_oncc101=1200
tune_curvecc101=1
#include "snare_map.sfz"

```

This, however, would make the controls affect the sidesticks, off-center hits and rimshot, but not the center hits:

```
<group>
amplitude_oncc100=100
tune_oncc101=1200
tune_curvecc101=1
#include "snare_map.sfz"

```

That is because the opcodes set under the `<group>` header would only be active until the `<group>` header for the center hits is reached. If a `<master>` header is used, they remain in force until another `<master>` header is encountered. When the headers are not immediately visible because they're in an included file, it is easy to fall into this kind of trap.

[](#the-define-statement)The Define Statement
---------------------------------------------

In addition to include, [#define](../../opcodes/define/) is the other statement which is very useful in making instruments more modular.

Define and include can be used together. For example, user-editable parameters, such as MIDI note assignments for drum kits and CC ranges, can also be placed in a separate file such as the below.

```
#define $KICKKEY 36
#define $SIDESTICKKEY 37
#define $SNAREKEY 38

```

The defined variables can then be used throughout the instrument, and an end user who wants to change the keymap can edit the file containing the defined numbers without having to search through the entire instrument. In the specific implementation of ARIA, anything which uses the defined variables also needs to be placed in the main SFZ file using include, because of the way ARIA parses SFZ files, described in more detail under the opcode page.

Using define as a constant with a single value thorughout an instrument works easily. Defining the same variable to have multiple values at different points in the same instrument, however, requires care. Using #define to set the same variable to different values at one point in the same SFZ file does not work well at least in ARIA/Sforzando when loading an instrument. However, a workaround there is to use include to put each set of define statements with different values in a separate file. In simple tests, that has been successful.

Sometimes copying large chunks of SFZ code and performing search-replace within them is easier than redefining variables comes into play. There's a balance of when to use include statements and when to just copy some files and use search-replace.

Multiple defined variables can be used in the same line.

```
#define $MIC_NAME Room
#define $MIC_MIX_CC 32
<control>
label_cc$MIC_MIX_CC=$MIC_NAME

```

One thing to keep in mind is that each variable name should be unique. This is good:

```
#define $SNARE_KEY 38
#define $SNARE_RIMSHOT_KEY 40

```

This will fail in at least some SFZ players, because the complete name of one variable is also the start of another variable's name:

```
#define $SNARE 38
#define $SNARE_RIMSHOT 40

```

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/modular_instruments.md)

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