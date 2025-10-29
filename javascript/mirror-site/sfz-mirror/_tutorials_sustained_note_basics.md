    Sustained note basics - SFZ Format                    Top

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

Sustained note basics
=====================

We've covered the basic opcodes required to map simple drum instruments on [another page](../drum_basics/), and here we are going to apply that knowledge to pitched instruments, plus add more opcodes. Let's say we want to sample a folk flute whose lowest note is a D. If the lowest five notes are D, E, F#, G and A, and there is one sample available for each note, they could be mapped like this:

```
<region>key=50 sample=d4.wav
<region>key=52 sample=e4.wav
<region>key=54 sample=f#4.wav
<region>key=55 sample=g4.wav
<region>key=57 sample=a4.wav

```

This would work well enough to make a sound when a MIDI note corresponding to one of the sampled pitches is played. However, playing notes inbetween the D and E, or E and F#, would mean no sound. We can "stretch" one of the neighboring notes to cover that D# and that F using the [lokey / hikey](../../opcodes/lokey/) and [pitch\_keycenter](../../opcodes/pitch_keycenter/) opcodes instead of key. If a sample does not need to cover multiple notes, it can still use key. Whether to use the D or E sample to cover the D# in our example is a judgment call - which sounds better?

```
<region>lokey=50 hikey=51 pitch_keycenter=50 sample=d4.wav
<region>lokey=52 hikey=53 pitch_keycenter=52 sample=e4.wav
<region>key=54 sample=f#4.wav
<region>lokey=55 hikey=55 pitch_keycenter=56 sample=g4.wav
<region>key=57 sample=a4.wav

```

The samples will play as long as a note is held, but when the note is released, they will end suddenly, which is probably not realistic for a flute sound, or indeed most other instruments. We'll need to apply a volume envelope with a release time set, which can be applied to all regions. The [ampeg\_release](../../opcodes/ampeg_release/) opcode accomplishes this.

```
<global>ampeg_release=0.3

<region>lokey=50 hikey=51 pitch_keycenter=50 sample=d4.wav
<region>lokey=52 hikey=53 pitch_keycenter=52 sample=e4.wav
<region>key=54 sample=f#4.wav
<region>key=55 sample=g4.wav

```

If we have samples at various dynamics, such as quiet and loud, we could use note velocity to choose which sample is played - however, while this makes perfect sense for drum hits or piano notes, with instruments such as flute or violin, it's possible for the player to vary the dynamic level while a note is being sustained. This can be simulated with the [xfin\_loccN / xfin\_hiccN](../../opcodes/xfin_loccN/) and [xfout\_loccN / xfout\_hiccN](../../opcodes/xfout_loccN/) opcodes. Using only the D4 and E4 samples as an example, and controlling the dynamics with CC1 (mod wheel). The [amp\_veltrack](../../opcodes/amp_veltrack/) opcode is set to 0, so that velocity does not affect volume.

```
<global>ampeg_release=0.3 amp_veltrack=0

<group>lokey=50 hikey=51 pitch_keycenter=50
<region>sample=d4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=d4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=d4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52
<region>sample=e4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=e4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=e4_f.wav xfin_locc1=86 xfin_hicc1=127

```

Now, CC1 would first fade in the quiet sample when it was between 0 and 42. From 43 to 85, the quiet sample is faded out and the medium sample faded in. From 86 to the max value of 127, the medium sample is faded out while the loud sample fades in. If we have multiple techniques or articulation sampled, for example regular sustains and fluttertongue sustains, we need a way to switch between them. Each could be its own independent and complete SFZ file, and we could just load the desired file into the player, but for convenience, especially in live performance, it's good to load both at once and have a way of switching between them. One way is [loccN / hiccN](../../opcodes/loccN/) where which sample is triggered for a particular note depends on the value of a MIDI CC - let's use MIDI CC 11. Notice that the fluttertongue samples in this example have fewer dynamic layers than the main sustain samples - it's common for the "core" articulations of an instrument to be sampled in more detail, and the SFZ format is flexible enough to allow this, or even allow different amounts of dynamic layers or round robins for different notes within the same articulation.

```
<global>ampeg_release=0.3 amp_veltrack=0

<group>lokey=50 hikey=51 pitch_keycenter=50 hicc11=63
<region>sample=d4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=d4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=d4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 hicc11=63
<region>sample=e4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=e4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=e4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=50 hikey=51 pitch_keycenter=50 locc11=64
<region>sample=d4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=d4_ft_f.wav xfin_locc1=64 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 locc11=64
<region>sample=e4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=e4_ft_f.wav xfin_locc1=64 xfin_hicc1=127

```

Another, probably more common, way is to use keyswitches. If we define the keyswitch range as the C and C# below our lowest D using [sw\_lokey / sw\_hikey](../../opcodes/sw_lokey/), we can then use [sw\_last](../../opcodes/sw_last/) to select articulations.

```
<global>ampeg_release=0.3 amp_veltrack=0 sw_lokey=48 sw_hikey=49

<group>lokey=50 hikey=51 pitch_keycenter=50 sw_last=48
<region>sample=d4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=d4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=d4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 sw_last=48
<region>sample=e4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=e4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=e4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=50 hikey=51 pitch_keycenter=50 sw_last=49
<region>sample=d4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=d4_ft_f.wav xfin_locc1=64 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 sw_last=49
<region>sample=e4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=e4_ft_f.wav xfin_locc1=64 xfin_hicc1=127

```

There are other possibilities - for example, since velocity is not needed to control dynamics, we could use that to select articulations using [lovel / hivel](../../opcodes/lovel/), for example. However, it' is quite common, especially with string instruments, to use a MIDI CC to control the dynamics of sustained articulations, and velocity to control the dynamics of short articulations such as staccato. In those cases, the short articulations could use amp\_veltrack set to 100 instead of 0, and generally be mapped in the same way as [the drums we've discussed before](../drum_basics/). The flute is a monophonic instrument in reality - you can't play chords on it, while you can using our SFZ here. For more realism, playing a note on this flute should mute any previously playing notes. To make an instrument which can only play one note at a time, the [group](../../opcodes/group/) and [off\_by](../../opcodes/off_by/) opcodes can be used. Although these can be used in more complex scenarios, for a monophonic instrument with no multiple microphone positions sampled, it's enough to put all samples in the same group, and have that group muted whenever a new note from that group is played.

```
<global>ampeg_release=0.3 amp_veltrack=0 sw_lokey=48 sw_hikey=49 group=1 off_by=1

<group>lokey=50 hikey=51 pitch_keycenter=50 sw_last=48
<region>sample=d4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=d4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=d4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 sw_last=48
<region>sample=e4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=e4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=e4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=50 hikey=51 pitch_keycenter=50 sw_last=49
<region>sample=d4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=d4_ft_f.wav xfin_locc1=64 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 sw_last=49
<region>sample=e4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=e4_ft_f.wav xfin_locc1=64 xfin_hicc1=127

```

However, this cuts off the note suddenly, creating a gap before the next note can reach full volume. That problem can be fixed by setting [off\_mode](../../opcodes/off_mode/) to normal, which will make the notes being muted fade out gradually over the duration previously specified with the ampeg\_release opcode.

```
<global>ampeg_release=0.3 amp_veltrack=0 sw_lokey=48 sw_hikey=49

group=1 off_by=1 off_mode=normal
<group>lokey=50 hikey=51 pitch_keycenter=50 sw_last=48
<region>sample=d4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=d4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=d4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 sw_last=48
<region>sample=e4_p.wav xfin_locc1=0 xfin_hicc1=42 xfout_locc1=43 xfout_hicc1=85
<region>sample=e4_mf.wav xfin_locc1=43 xfin_hicc1=85 xfout_locc1=86 xfout_hicc1=127
<region>sample=e4_f.wav xfin_locc1=86 xfin_hicc1=127
<group>lokey=50 hikey=51 pitch_keycenter=50 sw_last=49
<region>sample=d4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=d4_ft_f.wav xfin_locc1=64 xfin_hicc1=127
<group>lokey=52 hikey=53 pitch_keycenter=52 sw_last=49
<region>sample=e4_ft_p.wav xfin_locc1=0 xfin_hicc1=63 xfout_locc1=64 xfout_hicc1=127
<region>sample=e4_ft_f.wav xfin_locc1=64 xfin_hicc1=127

```

This is enough to make a basic monophonic wind instrument, vocal, or other monophonic instrument. There are more possibilities - better legato, vibrato emulation, multiple microphone positions etc. - which we'll describe later in another part of this guide. Together with the information covered in [drum basics](../drum_basics/) earlier, this should also be enough to make a basic sampled piano or guitar.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/sustained_note_basics.md)

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