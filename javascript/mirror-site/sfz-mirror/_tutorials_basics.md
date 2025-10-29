    Intro to SFZ - SFZ Format                    Top

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

Intro to SFZ
============

A SFZ file is a set of plain text, computer-readable instructions, which accompany a sample set and define how the sampler should load and work with those samples. If the samples are the strings of a piano or pipes of an organ, the SFZ file is the mechanism that connects the key to the hammer which strikes the strings or the air and signals to the pipes of the organ.

SFZ files can be opened, edited, and created in any text editor application, even the default 'Notepad' in Windows. No external software is necessary to create or modify a SFZ file, though there are some pieces of software or scripts out there which greatly ease the creation or editing process. An example of this is an automapper, which is a script or application that takes a sample set and uses the names of the samples or actual audio content to determine how to map those samples.

The SFZ file's role is a simple, two-part operation: 1. Explain how to **filter** or **sort** the incoming MIDI data and determine which sample(s), if any, should sound in response. 2. Instruct the Sampler how to **modulate**, or _adapt_, those samples, such as make them quieter or apply a filter.

```
#mermaid-1750991481814{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;fill:#333;}#mermaid-1750991481814 .error-icon{fill:#552222;}#mermaid-1750991481814 .error-text{fill:#552222;stroke:#552222;}#mermaid-1750991481814 .edge-thickness-normal{stroke-width:2px;}#mermaid-1750991481814 .edge-thickness-thick{stroke-width:3.5px;}#mermaid-1750991481814 .edge-pattern-solid{stroke-dasharray:0;}#mermaid-1750991481814 .edge-pattern-dashed{stroke-dasharray:3;}#mermaid-1750991481814 .edge-pattern-dotted{stroke-dasharray:2;}#mermaid-1750991481814 .marker{fill:#333333;stroke:#333333;}#mermaid-1750991481814 .marker.cross{stroke:#333333;}#mermaid-1750991481814 svg{font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:16px;}#mermaid-1750991481814 .label{font-family:"trebuchet ms",verdana,arial,sans-serif;color:#333;}#mermaid-1750991481814 .cluster-label text{fill:#333;}#mermaid-1750991481814 .cluster-label span,#mermaid-1750991481814 p{color:#333;}#mermaid-1750991481814 .label text,#mermaid-1750991481814 span,#mermaid-1750991481814 p{fill:#333;color:#333;}#mermaid-1750991481814 .node rect,#mermaid-1750991481814 .node circle,#mermaid-1750991481814 .node ellipse,#mermaid-1750991481814 .node polygon,#mermaid-1750991481814 .node path{fill:#ECECFF;stroke:#9370DB;stroke-width:1px;}#mermaid-1750991481814 .flowchart-label text{text-anchor:middle;}#mermaid-1750991481814 .node .label{text-align:center;}#mermaid-1750991481814 .node.clickable{cursor:pointer;}#mermaid-1750991481814 .arrowheadPath{fill:#333333;}#mermaid-1750991481814 .edgePath .path{stroke:#333333;stroke-width:2.0px;}#mermaid-1750991481814 .flowchart-link{stroke:#333333;fill:none;}#mermaid-1750991481814 .edgeLabel{background-color:#e8e8e8;text-align:center;}#mermaid-1750991481814 .edgeLabel rect{opacity:0.5;background-color:#e8e8e8;fill:#e8e8e8;}#mermaid-1750991481814 .labelBkg{background-color:rgba(232, 232, 232, 0.5);}#mermaid-1750991481814 .cluster rect{fill:#ffffde;stroke:#aaaa33;stroke-width:1px;}#mermaid-1750991481814 .cluster text{fill:#333;}#mermaid-1750991481814 .cluster span,#mermaid-1750991481814 p{color:#333;}#mermaid-1750991481814 div.mermaidTooltip{position:absolute;text-align:center;max-width:200px;padding:2px;font-family:"trebuchet ms",verdana,arial,sans-serif;font-size:12px;background:hsl(80, 100%, 96.2745098039%);border:1px solid #aaaa33;border-radius:2px;pointer-events:none;z-index:100;}#mermaid-1750991481814 .flowchartTitleText{text-anchor:middle;font-size:18px;fill:#333;}#mermaid-1750991481814 :root{--mermaid-font-family:"trebuchet ms",verdana,arial,sans-serif;}

Incoming MIDI Data

Sampler

Audio Output

SFZ File

Sample1.wav

Sample2.wav

Sample3.wav

Modulation


```

[](#opcodes)Opcodes
-------------------

The primary component of any SFZ file is the opcode. Opcodes essentially define 'thing=value'. For example, the opcode 'volume=6' defines the volume of the sample as +6 decibels relative to normal.

Opcodes functionally perform two different roles: (1) _defining performance parameters_, or (2) _restricting the conditions under which that sound may be used_. For example, `volume=6` defines a performance property: the sample will sound 6 decibels louder. On the other hand, `lokey=36 hikey=38` limits what condition the sound may play: the key to trigger the sound must be in the range 36 through 38.

You can think of your SFZ file as a giant conditional filter, which systematically takes a MIDI message and attempts to perform a specific action in response. At the most basic level, if you simply type

```
<region>
sample=piano.wav

```

Then that sample will be mapped to MIDI key 60 (middle C), and be available at ALL velocity ranges, ALL key ranges, and under ALL continuous controller values (i.e. regardless of if sustain pedal is held down or not, for example).

If we add `lokey=58 hikey=62 pitch_keycenter=60` to the region, then our piano note will ONLY respond if a key within the range 58-62 (Bb to D on either side of middle C) is played. We are restricting the conditions under which that specific sample will be played.

We can restrict whether or not a specific sample will play by a very wide range of parameters, including which keys are pressed, at what velocity, and what MIDI continuous controller (CC) values are currently present. For example, we can have a piano sample for when the sustain pedal is down AND velocity is less than 20 AND the key pressed is between 58 and 62 as follows:

```
<region>
sample=piano.wav

pitch_keycenter=60 //here we define the real "concert" pitch of the sample, MIDI note 60 or middle C
lokey=58 //here we set the range of pitches the region will play on
hikey=62

lovel=1 //here we set the range of key velocities that the region will play on
hivel=20

locc64=64 //here we set that the sustain pedal, cc64, must be on for the region to play
hicc64=127

```

If for any reason the MIDI signal DOES NOT meet ALL of the conditions, that sample will not play. That is the basic underlying framework on how SFZ files are organized.

[](#headers)Headers
-------------------

Headers serve to organize and separate opcodes, and are marked with `<` `>` on either side. There are three primary headers: `<region>`, `<group>`, and `<global>`, from most to least restrictive. A region, for example, may only contain a single sample. A group is comprised of a series of regions, each containing a single sample. A global is comprised of a series of groups, each containing a series of regions, etc.

`<control>` is a special purpose header used for a few special opcodes such as `default_path`.

Generally SFZ instruments are not indented, but if they were, they would appear as such:

```
<control>
<global>
    <group>
        <region>
            sample=
        <region>
            sample=
    <group>
        <region>
            sample=
        <region>
            sample=

```

### [](#inheriting)Inheriting

Note that if you entered an opcode between a `<group>` and its first `<region>`, that opcode would be inherited by the `<region>`s within the group. The same can be done for `<global>` as well, with `<global>` affecting all of the `<group>`s within it, and that being passed down to each of the `<region>`s within those groups as welll, allowing the parameters of dozens, hundreds, or thousands of samples to be altered with a single line. This massively cuts down on file size, as you do not need to repeat the same text in each item.

```
<group>
lovel=64 // enter stuff here if you want to apply it to all regions
hivel=127

<region>
sample=Trumpet_C4_v2.wav
key=60

<region>
sample=Trumpet_C#4_v2.wav
key=61

<region>
sample=Trumpet_D4_v2.wav
key=62

```

is the same as:

```
<region>
sample=Trumpet_C4_v2.wav
key=60
lovel=64
hivel=127

<region>
sample=Trumpet_C#4_v2.wav
key=61
lovel=64
hivel=127

<region>
sample=Trumpet_D4_v2.wav
key=62
lovel=64
hivel=127

```

This behavior can be overriden if that same opcode is specified within the lesser header with a different value. For example:

```
<global>
    volume=6 //this value will be inherited by everything, unless overriden below

    <group> //Group A
        volume=5

        <region> //Region 1
            volume=4

        <region> //Region 2

    <group> //Group B

        <region> //Region 3
            volume=2

        <region> //Region 4

```

(indented for clarity; SFZ is not usually indented)

Here's what's going on here:

*   Region 1's volume is 4, as it has volume defined.
*   Region 2's volume is 5, as it doesn't have volume defined, so it inherits from Group A, as Group A has volume defined.
*   Region 3's volume is 2, as it has volume defined.
*   Region 4's volume is 6 as it doesn't have volume defined, nor does Group B, so it inherits from the Global volume setting which is 6.

Always look for opportunities to use inheriting to keep your scripts tidy by removing duplicate code.

### [](#header-nesting)Header Nesting

Unlike many popular scripting or programming languages or markup languages like HTML, XML, JSON, etc. there is no such concept as _nesting_ in SFZ. _Nesting_ is when a header of the same type can exist within another header of the same type. Nesting is very useful, but it can add a lot of complexity and layers to a language, and is a common source of bugs or mistakes as well as a slight impediment of speed. The downside to the lack of nesting is that the number of layers is restricted severely rather than infinite. That is why there is both `<group>` and `<global>`, and the ARIA Player/Sforzando will also use an intermediate between the two, `<master>` to provide one more layer.

In SFZ format, a header ends when the next header of that type is started. For example, if I put a `<region>` after another `<region>`, it will end the first region automatically at the start of declaring the next.

Keep in mind that group, global, and master are merely macros to reduce duplicate code. When compiled (in most SFZ players), the SFZ file will run as if everything is inside the regions themselves.

[](#organization-of-opcodes-within-headers)Organization of Opcodes within Headers
---------------------------------------------------------------------------------

Opcodes may be listed in a row OR one per line, unofficially known as 'condensed' and 'expanded' view:

```
<region>
sample=piano_D4_vl1.wav
lokey=62
hikey=63
pitch_keycenter=62
lovel=1
hivel=50

```

is equal to:

```
<region> sample=piano_D4_vl1.wav lokey=62 hikey=63 pitch_keycenter=62 lovel=1 hivel=50

```

You can see how much space is saved in the latter case, and it allows bulk adjustments to be done easier and makes debugging slightly easier, e.g.:

```
<region> sample=piano_D4_vl1.wav lokey=62 hikey=63 pitch_keycenter=62 lovel=1 hivel=50
<region> sample=piano_E4_vl1.wav lokey=64 hikey=65 pitch_keycenter=64 lovel=1 hivel=50
<region> sample=piano_F#4_vl1.wav lokey=66 hikey=67 pitch_keycenter=66 lovel=11 hivel=50
<region> sample=piano_G#4_vl1.wav lokey=68 hikey=69 pitch_keycenter=68 lovel=1 hivel=50

```

You can see there is something wrong with the third region, a typo of `lovel=11` instaed of `lovel=1`.

These four lines would replace over 20 lines, making files much more manageable. It is possible to swap between the two by using a find-and-replace operation in your text editor (e.g. Notepad++ or equivalent) to replace new line character with a space (this can be done by selecting a blank line by clicking and dragging down on a blank so that one line is highlighted, _THEN_ open the find/replace dialog and it will be auto-filled in the 'find' field; put a single space in the 'replace with' field. Try executing and see if it works; see the video below for a visual representation of the process).

[](#pitch)Pitch
---------------

If using a pitch based instrument, you will most likely be working heavily with three opcodes: `lokey`, `hikey`, and `pitch_keycenter`. These opcodes define the range of MIDI note numbers or note names that will allow the note to play. It is highly recommended that you use MIDI note numbers, as pitch naming conventions are poorly standardized at best.

You can remember the MIDI note numbers for the C's as follows, using _International Pitch Notation_, which states C4=MIDI note number 60:

```
C1:24
C2: 36 (this is the C below bass clef)
C3: 48 (this is the C in bass clef)
C4: 60 (this is Middle C)
C5: 72 (this is the C in treble clef)
C6: 84 (this is the C above treble clef)
C7: 96

```

(note that many, many samplers use a different standard of C3=60, in which case all numbers are shifted down one; in fact, this is probably much more commonly found)

You'll notice each value is exactly 12 notes apart from the others. It's not too difficult to calculate notes between the C's, or keep a chart on your wall or desk with the note names and MIDI numbers listed out. Many hours have been saved debugging and mapping for me in this way.

[](#velocity-layers)Velocity Layers
-----------------------------------

For most instruments, it is possible to perform notes of varying intensity. For classically trained musicians, this might be called _dynamics_ (such as _piano, forte, mezzo-forte,_ etc.). For a piano, when a key is struck with minimal force versus a great deal of force, a rather different tone is emitted, with harder strikes having more higher frequency content present.

In the MIDI world, we refer to this as _Velocity_, borrowing the term from the world of physics. In the original MIDI spec, velocity has a range of 1-127 (aside: a velocity value of '0' is actually an alias of 'note off' signal, so the actual range is 1-127, not 0-127).

So, to make a realistic piano (or really most any instrument), it is necessary to sample the tone of the instrument at several different dynamic levels or velocities. We collectively refer to these sets of levels as _Velocity Layers_ or _Dynamic Layers_.

For example, let us say we record a piano with three such velocity layers. The softest layer might be what a classically trained pianist might call _piano_ or _pianissimo (p or pp_ marking). The moderate layer might be _mezzo-forte (mf)_, and the hardest layer _fortissimo (ff)_.

In SFZ, we would assign each layer to a velocity range from the 1-127 range. For example, the lowest layer might get the range of 1-50, the medium from 51-100, and the loudest from 101-127.

We express this in SFZ using lovel and hivel, for example:

```
<region>
sample=piano_C4_vl1.wav
lovel=1
hivel=50

<region>
sample=piano_C4_vl2.wav
lovel=51
hivel=100

<region>
sample=piano_C4_vl3.wav
lovel=101
hivel=127

```

We would of course also add our `lokey`, `hikey`, and `pitch_keycenter` to these as well if we recorded multiple tones on the instrument.

### [](#using-velocity-with-groups-inheriting)Using Velocity with Groups & Inheriting

To simplify our lives and keep our SFZ files from being huge, we can also use the `<group>` header to organize our velocity layers, for example.

Any `<region>` within a `<group>` will of course inherit whatever is listed in that `<group>`, so if we group our samples as shown below, we can significantly cut down on the amount of space needed in the file:

```
<group> //velocity layer 1 (pp)
lovel=1
hivel=50

<region> //C4
sample=piano_C4_vl1.wav
lokey=60
hikey=61
pitch_keycenter=60

<region> //D4
sample=piano_D4_vl1.wav
lokey=62
hikey=63
pitch_keycenter=62

<region> //E4
sample=piano_E4_vl1.wav
lokey=64
hikey=64
pitch_keycenter=64

<region> //F4
sample=piano_F4_vl1.wav
lokey=65
hikey=66
pitch_keycenter=65

<group> //velocity layer 2 (mf)
lovel=51
hivel=100

<region> //C4
sample=piano_C4_vl2.wav
lokey=60
hikey=61
pitch_keycenter=60

<region> //D4
sample=piano_D4_vl2.wav
lokey=62
hikey=63
pitch_keycenter=62

<region> //E4
sample=piano_E4_vl2.wav
lokey=64
hikey=64
pitch_keycenter=64

<region> //F4
sample=piano_F4_vl2.wav
lokey=65
hikey=66
pitch_keycenter=65

<group> //velocity layer 3 (ff)
lovel=101
hivel=127

<region> //C4
sample=piano_C4_vl3.wav
lokey=60
hikey=61
pitch_keycenter=60

<region> //D4
sample=piano_D4_vl3.wav
lokey=62
hikey=63
pitch_keycenter=62

<region> //E4
sample=piano_E4_vl3.wav
lokey=64
hikey=64
pitch_keycenter=64

<region> //F4
sample=piano_F4_vl3.wav
lokey=65
hikey=66
pitch_keycenter=65

```

Keep in mind of course that we can always override the inheriting behavior here, such as in the case of a sample for which only two velocity layers were recorded. This might happen in the case of a mistake, or in the case where time was running short in the session, or in some cases where the instrument physically has less distinction between its quietest and loudest sounds and it was desirable to save some time.

You can also use group, master, and global to organize other things than velocity layers, such as keys, sustain pedal state, round robins, mic positions, and more. Just be careful as in some cases you might run out of headers to use if the file gets too complex, such as if you are using multiple mic positions, round robins, and grouping your velocity layers as well.

[](#includes)Includes
---------------------

One final more advanced topic to discuss is Includes. Perhaps the dark magic of SFZ, `#include` allows you to take the contents of one SFZ file and import them into your current file. This allows another layer of organiziation to take place, with, for example, all of the samples for each drum in a drum kit to exist in a separate .sfz file without an assigned key range, and a single master .sfz file to inherit each of those into a `<group>` where their key range is assigned (see Virtuosity Drums as a good example of this process). This might also be useful for an acoustic instrument to organize by mic position or articulation.

This allows you to keep an extremely tidy workflow, creating easily-managed main files where you can rapidly change key ranges and other control values to get the controls you need.

.videoWrapper { position: relative; padding-bottom: 56.333%; height: 0; background: black; } .videoWrapper iframe { position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0; } function get\_youtube\_id(url) { var p = /^(?:https?:\\/\\/)?(?:www\\.)?(?:youtu\\.be\\/|youtube\\.com\\/(?:embed\\/|v\\/|watch\\?v=|watch\\?.+&v=)|youtube-nocookie\\.com\\/(?:embed\\/|v\\/|watch\\?v=|watch\\?.+&v=))((\\w|-){11})(?:\\S+)?$/; return (url.match(p)) ? RegExp.$1 : false; } function vimeo\_embed(url,el) { var id = false; $.ajax({ url: 'https://vimeo.com/api/oembed.json?url='+url, async: true, success: function(response) { if(response.video\_id) { id = response.video\_id; if(url.indexOf('autoplay=1') !== -1) var autoplay=1; else var autoplay=0; if(url.indexOf('loop=1') !== -1) var loop=1; else var loop=0; var theInnerHTML = '<div class="videoWrapper"><iframe src="https://player.vimeo.com/video/'+id+'/?byline=0&title=0&portrait=0'; if(autoplay==1) theInnerHTML += '&autoplay=1'; if(loop==1) theInnerHTML += '&loop=1'; theInnerHTML += '" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe></div>'; el.innerHTML = theInnerHTML; } } }); } function video\_embed() { var p = document.getElementsByTagName('p'); for(var i = 0; i < p.length; i++) { //check if this is an external url (that starts with https:// or http:// if (p\[i\].innerHTML.indexOf("http://") == 0 || p\[i\].innerHTML.indexOf("https://") == 0) { var youtube\_id = get\_youtube\_id(p\[i\].innerHTML); if(youtube\_id) { if(p\[i\].innerHTML.indexOf('autoplay=1') !== -1) var autoplay=1; else var autoplay=0; if(p\[i\].innerHTML.indexOf('loop=1') !== -1) var loop=1; else var loop=0; var theInnerHTML = '<div class="videoWrapper"><iframe width="720" height="420" src="https://www.youtube-nocookie.com/embed/' + youtube\_id + '?rel=0&showinfo=0'; if(autoplay==1) theInnerHTML += '&autoplay=1'; if(loop==1) theInnerHTML += '&loop=1&playlist='+youtube\_id+'&version=3'; if(p\[i\].innerHTML.indexOf('start=') !== -1) theInnerHTML += '&start='+p\[i\].innerHTML.substring(p\[i\].innerHTML.indexOf('start=')+6); theInnerHTML += '" frameborder="0" allowfullscreen></iframe></div>'; p\[i\].innerHTML = theInnerHTML; } if(p\[i\].innerHTML.indexOf('vimeo.com') !== -1) { //ask vimeo for the id and place the embed vimeo\_embed(p\[i\].innerHTML,p\[i\]); } } } } video\_embed(); function mp3\_embed() { var p = document.getElementsByTagName('p'); for(var i = 0; i < p.length; i++) { if(p\[i\].innerHTML.indexOf('.mp3') !== -1) { var str = p\[i\].innerHTML.split('?'); if(str.length == 1) str\[1\] = ''; var str1 = str\[1\]; str1 = str1.replace('&','').replace('&',''); str1 = str1.replace('autoplay=1','').replace('autoplay=0',''); str1 = str1.replace('loop=1','').replace('loop=0',''); str1 = str1.replace('controls=0','').replace('controls=1',''); if (str\[0\].lastIndexOf('.mp3', str\[0\].length - 4) === str\[0\].length - 4 && str1.length == 0) { if(str\[1\].indexOf('autoplay=1') !== -1) var autoplay=1; else var autoplay=0; if(str\[1\].indexOf('loop=1') !== -1) var loop=1; else var loop=0; if(str\[1\].indexOf('controls=0') !== -1) var controls=0; else var controls=1; var newInnerHTML = '<audio'; if(autoplay==1) newInnerHTML += ' autoplay'; if(loop==1) newInnerHTML += ' loop'; if(controls==1) newInnerHTML += ' controls'; newInnerHTML += '><source src="'+str\[0\]+'" type="audio/mpeg">Your browser does not support the audio element.</audio>'; p\[i\].innerHTML = newInnerHTML; } } } } mp3\_embed();

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/tutorials/basics.md)

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