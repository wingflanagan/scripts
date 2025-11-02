    Sympathetic Resonance - SFZ Format                    Top

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

Sympathetic Resonance
=====================

[](#basics)Basics
-----------------

Many instruments have elements which will resonate after a note is stopped. A piano with the sustain pedal down is an obvious example. In sampled instruments, this is usually dealt with by recording one set of pedal-up samples and one set of pedal-down samples. Some sampled pianos will also support half-pedaling, though this will have to be documented later.

The current version of this tutorial is based on an implementation of sympathetic resonance for a nyckelharpa, which is, more or less, a violin with a key mechanism and a set of 12 sympathetic strings. This was also reused for another instrument with a smaller number of diatonic sympathetic strings.

The basic concept is simple: when a sustained note ends, a sympathetic resonance sample is played as a release sample. In the case of the nyckelharpa, the resonance samples were created by using only the tails of short notes. There is a set of round robin samples for each pitch, and they are mapped to the keys as normal. The [trigger](../../opcodes/trigger/) opcode is key.

```
<master>
#include "modules/maps/strings/nh/nh_sus_f_map.sfz"

<master>
trigger=release
ampeg_attack=0.1
#include "modules/maps/strings/nh/nh_release_map.sfz"

```

Instead of creating a separate set of samples it's even possible to simply use the shorts samples with an [offset](../../opcodes/offset/), if the shorts are performed consistently enough.

```
<master>
#include "modules/maps/strings/nh/nh_sus_f_map.sfz"

<master>
trigger=release
ampeg_attack=0.1
offset=6600
#include "modules/maps/strings/nh/nh_short_map.sfz"

```

[](#controls)Controls
---------------------

We can add a simple volume control using [amplitude](../../opcodes/amplitude/) modulation and [locc](../../opcodes/hiccN/).

```
<master>
#include "modules/maps/strings/nh/nh_sus_f_map.sfz"

<master>
trigger=release
ampeg_attack=0.1
amplitude_oncc52=100
locc52=1
#include "modules/maps/strings/nh/nh_release_map.sfz"

```

To prevent the buildup of voices with fast playing, a polyphony [group](../../opcodes/group/) and the [note\_polyphony](../../opcodes/note_polyphony/) opcode can be used.

```
<master>
#include "modules/maps/strings/nh/nh_sus_f_map.sfz"

<master>
trigger=release
ampeg_attack=0.1
amplitude_oncc52=100
locc52=1
off_time=0.4
group=14
note_polyphony=1 
#include "modules/maps/strings/nh/nh_release_map.sfz"

```

[](#multiple-articulations)Multiple articulations
-------------------------------------------------

There could be a separate set of resonance samples captured for each technique, but in practice one set of samples cut from shorts works reasonably well for most. However, tremolo seemed to agitate all the strings more. In other words, playing an A didn't just make the A and a little E resonate, even the A# and G# strings resonated a bit, perhaps as a result of the whole instrument shaking a bit. So, tremolo got its own set of samples.

Shorts and pizzicato didn't use separate resonance samples, they were simply set to one-shot mode, so the entire sample played, resonance and all. This has its downsides, of course, but again it seems to work well enough in reality.

However, with the jete technique, the same set of samples was used with the addition of [rt\_decay](../../opcodes/rt_decay/). Keeping it simple, here is the polyphonic implementation:

```
<master>
#include "modules/maps/strings/nh/nh_jete_map.sfz"

<master>
trigger=release
off_time=0.4
rt_decay=12
ampeg_attack=0.1
#include "modules/maps/strings/nh/nh_release_map.sfz"

```

[](#multiple-voices)Multiple voices
-----------------------------------

When one key triggers multiple samples, whether they are crossfaded dynamic layers, mic posotions or unison voices, each sample playing is a voice which can trigger a release. In other words, with four mic positions having four sets of releases, sixteen release voices would be triggered for each note. This not only uses up unison voices but also is too loud and doesn't sound good. Fortunately this is easily fixed by creating a separate polyphony [group](../../opcodes/group/) for each voice's releases, and limiting its [note\_polyphony](../../opcodes/note_polyphony/).

This is not a consideration limited to sympathetic resonance, of course, but a general principle of using release triggers with multiple voices.

```
<master>
trigger=release
ampeg_attack=0.1
//To keep from over-triggering when unison is on
group=199
note_polyphony=1
#include "modules/maps/strings/nh/nh_release_map.sfz"

```

[](#legato)Legato
-----------------

The above works fine for polyphonic instruments, but with a mono instrument it's not enough to have a sample play on release; we also need to play a sample when a note is muted and a new note starts playing. At that point, we need to trigger the resonance based not on the incoming MIDI note but based on the previous pitch that was playing. This means creating a separate map. This implementation also uses [extended CCs](../../extensions/midi_ccs/), specifically CC 153, so the resonance sample is only triggered when one key is currently down.

```
//Mono mode

<master>
group=1
off_by=1
#include "modules/maps/strings/nh/nh_sus_f_map.sfz"

//Mono mode, keypress restrictions so only triggered on last note of phrase

<master>
trigger=release
amplitude_oncc52=200
locc52=1
off_time=0.4
ampeg_attack=0.1
group=14
note_polyphony=1 
//Trigger only when one key was down
lohdcc153=0
hihdcc153=1.1
//To keep from over-triggering when unison is on
group=199
note_polyphony=1
#include "modules/maps/strings/nh/nh_release_map.sfz"

//Mono mode, legato triggers
//Loop mode is one shot to keep these from dying when the next key is released

<master>
trigger=legato
amplitude_oncc52=200
locc52=1
locc105=64
off_time=0.4
ampeg_attack=0.1
loop_mode=one_shot
pitch_keytrack=0
#include "modules/maps/strings/nh/nh_release_swdown_map.sfz"

```

Inside the map will need to use [sw\_down](../../opcodes/sw_down/) to trigger the proper sample. [lokey/hikey](../../opcodes/lokey/) is not necessary for correct triggering, but it is used to determine which keys are shown as playable in ARIA, and leaving this out would make the entire keyboard appear as playable in the GUI.

Whether it's strictly necessary to avoid creating regions where sw\_down falls between lokey and hikey is not certian, but they are absent from the nyckelharpa on which this tutorial is based.

```
<region>
sample=../Samples/strings/nyckelharpa/stac/nyckelharpa_g3_stac.wav
lokey=44
hikey=86
sw_down=43

<region>
sample=../Samples/strings/nyckelharpa/stac/nyckelharpa_ab3_stac.wav
lokey=43
hikey=43
sw_down=44

<region>
sample=../Samples/strings/nyckelharpa/stac/nyckelharpa_ab3_stac.wav
lokey=45
hikey=86
sw_down=44

<region>
sample=../Samples/strings/nyckelharpa/stac/nyckelharpa_a3_stac.wav
lokey=43
hikey=44
sw_down=45

<region>
sample=../Samples/strings/nyckelharpa/stac/nyckelharpa_a3_stac.wav
lokey=45
hikey=86
sw_down=45

```

[](#other-methods)Other methods
-------------------------------

At least in theory, a better way to do this would be to capture an impulse response of the resonance, perhaps by giving the instrument a whack and letting the sympathetic strings ring. However, this would require an sfz player with convolution reverb implemented.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/sympathetic_resonance.md)

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