    Legato - SFZ Format                    Top

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

Legato
======

[](#basic-monophony)Basic monophony
-----------------------------------

In the basic sustained instruments tutorial, we have the below example of a monophonic flute, which uses the [group](../../opcodes/group/) and [off\_by](../../opcodes/off_by/) opcodes to allow only one be played at a time, and the [off\_mode](../../opcodes/off_mode/) together with [ampeg\_release](../../opcodes/ampeg_release/) make the fadeout of the previous note a little smoother. This is a starting point for implementing legato.

If only group and off\_by are specified, the resulting sound will probably be quite bad, as this will use default values for off\_mode, ampeg\_attack and ampeg\_release. This means the note being muted will drop off extremely quickly, which will probably leave an audible drop in levels during the transition, unless the next note has an extremely fast attack. Therefore, at least ampeg\_release will need to be specified in most cases - though most instruments will need to specify that even if not using legato.

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

[](#legato-regions)Legato regions
---------------------------------

The above will allow only one note to sound at a time, with a quick crossfade between the old and new note. In many cases, though, it makes sense to treat the legato notes differently than the notes which start a phrase when no other note is playing. The [trigger](../../opcodes/trigger/) opcode is used to separate regions into initial and legato. For sustained sounds, it can make sense to use the [offset](../../opcodes/offset/) opcode to skip the start of the sample for legato regions. It's also probably a good idea to use offset\_attack in these cases, which both makes the transition sound smoother and avoids clicks and pops in cases where the offset does not fall on a zero crossing. Here are the relevant opcodes from the Hadziha choir.

An offset of 6000 samples is enough to skip the fraction of a second when the singers are starting the note, but not enough to skip the part of the sample when they're still settling on a common pitch, so it works well for this particular choir. The crossfade times with an off time of 1 second and legato note attack time of 0.4 seconds are probably much longer than would be needed for most solo instruments or voices, or ensembles intended for fast legato, but could be a good range for other types of ensembles playing slowly.

Note that the samples are not all in the same group - the initial note regions are in polyphony group 1, which is muted by group 2. The legato regions are in polyphony group 2, which mutes itself. Having everything in group 1 should also work, though. This was done this was to allow the use of additional syllable start samples, which would then be group 3 and also be muted by group 2. As with hi-hat muting, if there are multiple mic positions in separate files, each mic position will need its own polyphony groups.

```
<global>off_mode=time
off_time=1
amp_veltrack=0

<master>trigger=first
group=1
off_by=2
//Sample map goes here
#include "mappings/6_a_map.sfz"

<master>trigger=legato
offset=6000
ampeg_attack=0.4
group=2
off_by=2
//Sample map goes here
#include "mappings/6_a_map.sfz"

```

As this does not use velocity to control note volume, that frees up velocity for something else, so in this specific case velocity is repurposed to shorten the attack time on the legato notes, which makes the patch more intuitively playable.

```
<global>off_mode=time
off_time=1
amp_veltrack=0

<master>trigger=first
group=1
off_by=3
//Sample map goes here
#include "mappings/6_a_map.sfz"

<master>trigger=legato
offset=6000
ampeg_attack=1
ampeg_vel2attack=-0.8
group=3
off_by=3
//Sample map goes here
#include "mappings/6_a_map.sfz"

```

[](#portamento)Portamento
-------------------------

Another possibility is portamento, or having a pitch glide implemented on the legato regions. Here are the relevant opcodes from Karoryfer Samples Meatbass, which has both legato and portamento. The portamento is very obviously fake for slow glides across long intervals, but as long as the interval is no more than a third or fourth, it can be convincing. Of course, the narrower the interval and the shorter the time, the easier it is to sound convincing. With the portamento time at zero, this is effectively the same as non-portamento legato in the above example.

In the below setup, MIDI CC109 controls the glide time and an SFZ2 [envelope](../../modulations/envelope_generators/) is used to make the pitch change happen. CC140 is the ARIA extension CC for pitch delta, and being the difference in pitch between the previous note and the current note, it sets the depth of the glide envelope.

```
<global>eg06_sustain=1 //Pitch envelope setup for legato slides
eg06_level0=-1 //Envelope starts away from the note pitch
eg06_time0=0
eg06_pitch_oncc140=100 //This is the pitch depth
eg06_time1=0
eg06_level1=0 //At the end of the envelope, return to base pitch
//eg06_time1_oncc109 needs to be set for the legato regions - but we don't want
//it on for all regions so the default is 0
//At zero envelope duration the pitch goes to base pitch immediately so there
//is no glide

//Typical stuff for monophonic instruments
off_mode=normal
ampeg_release_oncc104=2

```

All the sample regions are then basically duplicated in non-legato and legato versions. Here's an example non-legato region with trigger set to first and no eg06\_time\_oncc109 set. The group and off\_by work just like in the above examples.

```
<group>
trigger=first
off_mode=normal
group=1
off_by=1

<region>
sample=..\Samples\arco_looped\c4_sustain.wav
pitch_keycenter=48

```

And the corresponding legato region with trigger set to legato, the eg06 glide envelope time control, and also an attack time, to let the note fade in more gradually, with this controlled by CC100 rather than velocity, as the example above. This is another option.

```
<group>
trigger=legato
off_mode=normal
group=1
off_by=1
eg06_time1_oncc109=0.3
ampeg_attack_oncc100=0.5

<region>
sample=..\Samples\arco_looped\c4_sustain.wav
pitch_keycenter=48

```

[](#true-sampled-legato)True sampled legato
-------------------------------------------

Here are examples from a simple flute test by MatFluor. The trigger=first regions work similarly as all the above examples, and the [sw\_previous](../../opcodes/sw_previous/) opcode can be used to choose which sample plays for the legato regions. If the samples would include both the legato transition and the complete sustain of the following note, things would be very simple:

```
<group>
// Legato transitions and the complete sustain of the next note both in the same sample
trigger=legato
group=2
off_by=2
ampeg_attack=0.05 ampeg_release=0.2
off_mode=normal

// Leg transitions up
<region> sample=legatovib_g4_a4.wav key=A4 sw_previous=G4
<region> sample=legatovib_g4_c5.wav key=C5 sw_previous=G4
<region> sample=legatovib_a4_c5.wav key=C5 sw_previous=A4
// Leg transitions down
<region> sample=legatovib_c5_a4.wav key=A4 sw_previous=C5
<region> sample=legatovib_c5_g4.wav key=G4 sw_previous=C5

```

Recording the full sustain after every transition adds greatly to the recording time, diskspace and RAM use, however. It may be necessary in some cases, such as solo vocals, but in other cases it's possible to use transition samples which are short, then fade in the regular sustain sample.

```
<group>
// Legato transition group
trigger=legato
group=2
off_by=2
offset=45000
ampeg_attack=0.05 ampeg_hold=0.25 ampeg_decay=0.2 ampeg_sustain=0 ampeg_release=0.2
ampeg_decay_shape=-1.4
off_mode=normal

// Leg transitions up
<region> sample=legatovib_g4_a4.wav key=A4 sw_previous=G4
<region> sample=legatovib_g4_c5.wav key=C5 sw_previous=G4
<region> sample=legatovib_a4_c5.wav key=C5 sw_previous=A4
// Leg transitions down
<region> sample=legatovib_c5_a4.wav key=A4 sw_previous=C5
<region> sample=legatovib_c5_g4.wav key=G4 sw_previous=C5
<region> sample=legatovib_a4_g4.wav key=G4 sw_previous=A4

<group>
// Sustain group crossfaded into after legato transition
trigger=legato
group=1
off_by=2
offset=5000
ampeg_attack=0.3 ampeg_release=0.2
ampeg_attack_shape=3.8 
off_mode=normal

// Leg sustains
<region> sample=sustainvib_c5.wav key=C5
<region> sample=sustainvib_a4.wav key=A4
<region> sample=sustainvib_g4.wav key=G4

```

Another consideration is that for instruments with a wide range, it may not be worthwhile to record every possible transition, and only record transitions of up to one octave, for example. The [extended CCs](../../extensions/midi_ccs/) do not always behave quite like other CCs, necessitating using hdcc in ARIA, but the below works for a legato vocal with a range of less than two octaves.

```
<global>
off_mode=time
off_time=0.4
ampeg_release=0.3

<group>
trigger=first
group=1
off_by=1
#include "modules/vowel_sustain_a.sfz"

<group>
trigger=legato
group=1
off_by=1
ampeg_attack=0.1
ampeg_hold=0.3
ampeg_decay=0.6
ampeg_sustain=0
hihdcc141=12.1
#include "modules/vowel_transition_a.sfz"

<group>
trigger=legato
group=2
off_by=1
delay=0.3
ampeg_attack=0.2
offset=40000
hihdcc141=12.1
#include "modules/vowel_sustain_a.sfz"

<group>
trigger=legato
group=1
off_by=1
ampeg_attack=0.1
lohdcc141=12.9
hihdcc141=24
offset=12000
#include "modules/vowel_sustain_a.sfz"

```

It is also possible to use CC 140 in a similar way in an instrument which, for example, has legato transitions recorded ascending but not descending.

[](#further-true-legato-possibilities)Further True Legato Possibilities
-----------------------------------------------------------------------

It's possible to make a legato instrument that's not sampled chromatically. In such cases, it's necessary to use the same tricks used when [extending](../range_extension/) range and transpose samples across a wider range. The important thing to remember is that when extending the range of a sample, lokey, hikey and sw\_previous all need to be changed by the same amount from the original. For example, if an instrument has transitions sampled from C and D but not from C#, like this:

```
<region> sample=legatovib_c5_a4.wav key=A4 sw_previous=C5
<region> sample=legatovib_c5_a#4.wav key=A#4 sw_previous=C5
<region> sample=legatovib_c5_b4.wav key=B4 sw_previous=C5
<region> sample=legatovib_d5_a4.wav key=A4 sw_previous=D5
<region> sample=legatovib_d5_a#4.wav key=A#4 sw_previous=D5
<region> sample=legatovib_d5_b4.wav key=B4 sw_previous=D5

```

Extending the transitions from C5 to be used as transitions from C#5 for those same three notes could look like this:

```
<region> sample=legatovib_c5_a4.wav key=A4 sw_previous=C5
<region> sample=legatovib_c5_a#4.wav key=A#4 sw_previous=C5
<region> sample=legatovib_c5_b4.wav key=B4 sw_previous=C5
<region> sample=legatovib_c5_g#4.wav lokey=A4 hikey=A4 pitch_keycenter=G#4 sw_previous=C#5
<region> sample=legatovib_c5_a4.wav lokey=A#4 hikey=A#4 pitch_keycenter=A4 sw_previous=C#5
<region> sample=legatovib_c5_a#4.wav lokey=B4 hikey=B4 pitch_keycenter=A#4 sw_previous=C#5
<region> sample=legatovib_d5_a4.wav key=A4 sw_previous=D5
<region> sample=legatovib_d5_a#4.wav key=A#4 sw_previous=D5
<region> sample=legatovib_d5_b4.wav key=B4 sw_previous=D5

```

In one real-world case where the notes from which the intervals were sampled was not completely consistent between different dynamic layers, the easiest way to deal with this was to copy the entire sample map, move the lokey, hikey and sw\_previous values by one in the copy, then manually delete the duplicates and values where either the key or sw\_previous falls outside the instrument's range.

An instrument which does not have all interval transitions sampled, however, would be more tricky. For example, a diatonic folk flute in C would not have a minor second from C to C#, and the nearest available minor second transition would be from E to F, which would be a pretty big transposition. One possible compromise in such cases would probably be to use the C to D transition transposed down a minor second, which would include a bit of B at the start of the transition, but if the transitions are quick enough this might be passable. A better but more laborious solution would be processing the recordings with pitch transposition software such as Melodyne or Zplane reTune to create the missing intervals.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/legato.md)

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