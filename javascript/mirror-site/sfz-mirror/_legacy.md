The SFZ Format

 

  
The _sfz_ Format: Basics 

* * *

> What's The _sfz_ Format?  
> **The _sfz_ format** is a file format to define how a collection of samples are arranged for performance.  
>   
> The goal behind **the _sfz_ format** is to provide a free, simple, minimalistic and expandable format to arrange, distribute and use audio samples with the highest possible quality and the highest possible performance flexibility.
> 
> A _sfz_ format file can be played in our freeware _**sfz**_ player.  
>   
> Soundware, software and hardware developers can create, use and distribute **the _sfz_ format** files for free, for either free or commercial applications.
> 
> Some of the features of **the _sfz_ format** are:
> 
> \- Samples of any bit depth (8/16/24/32-bit) support, mono or stereo.  
> \- Samples taken at any samplerate (i.e. 44.1k, 48k, 88.2k, 96k, 176.4k, 192k, 384k).  
> \- Compressed samples. Compressed and uncompressed can be combined.  
> \- Looped samples.  
> \- Unlimited keyboard splits and layers.  
> \- Unlimited velocity splits and layers.  
> \- Unlimited regions of sample playback based on MIDI controllers (continuous controllers, pitch bend, channel and polyphonic aftertouch, keyboard switches) and internal generators (random, sequence counters).  
> \- Sample playback on MIDI control events.  
> \- Unlimited unidirectional and bidirectional exclusive regions (mute groups).  
> \- Unlimited release trigger regions with release trigger attenuation control.  
> \- Unlimited crossfade controls.  
> \- Trigger on first-note and legato notes.  
> \- Sample playback synchronized to host tempo.  
> \- Dedicated Envelope Generators for pitch, filter and amplifier.  
> \- Dedicated LFO for pitch, filter and amplifier.  
> 
>   
> How the _sfz_ format is structured?  
> The _sfz_ format is a collection of sample files plus one or multiple .sfz definition files. This structure, containing multiple files instead of a single file is defined as non-monolithic.  
>   
> Two kinds of sample files were selected to be included in the _sfz_ format: a basic PCM uncompressed format (standard Windows wave files) and a basic, adjustable-quality, royalty free compressed format (ogg-vorbis encoded files).  
>   
> The inclusion of a compressed format allows sample developers and soundware creators to easily create preview or demonstration files in a small package so they can be transferred with minimum bandwidth, while retaining complete performance functionality.
> 
> Both formats are 100% royalty-free, so players can be created to reproduce them without fixed or per-copy fees. They can also be freely distributed on the web (provided that the contents of the files are copyright cleared).  
>   
> Each .sfz definition file represents one or a collection of **instruments**. An instrument is defined as a collection of **regions**. Regions include the definition for the input controls, the samples (the wav/ogg files) and the performance parameters to play those samples.
> 
> How the .sfz definition file is created?  
> A .sfz definition file is just a text file. Consequently, it can be created by using any text editor (i.e. Notepad).
> 
> Why non-monolithic?  
> While both monolithic and non-monolithic formats have advantages and disadvantages, there are several reasons which moved us to adopt a non-monolithic sample format. Technological and conceptual reasons can hardly be separated, so here's a basic explanation.
> 
> The most important reason is the file size limitation of a non-monolitic file on FAT32 partitions. Samples are getting really big nowadays, with thousands of individual samples collected in single instruments, and triggered according to many input control combinations.
> 
> Samples with high bit resolution (i.e. 24-bit samples) and high samplerate settings (96kHz, 192kHz) make the collection size even bigger. In the case of a non-monolithic format, the limitation still applies, but it applies to each sample instead of to the sum of all samples, making the limit virtually unreachable.  
>   
> While this limitation doesn't apply to NTFS, NTFS partitions are less efficient than FAT32 disks in terms of raw disk performance for streaming applications.  
>   
> Additionally, editing a single sample in a monolithic file implies loading the whole file, and after edit, saving the whole file again to disk. When collection size is big, the loading and saving operation is very time-consuming.  
>   
> However, we have not discharged the possibility of incorporating a monolithic format for the _sfz_ format, as soon as the format structure is completely implemented. Small sound sets (or NTFS users) could chose between the two options appropriately.
> 
> Why not XML?  
> XML was actually the first choice for the .sfz definition file, mainly due the simplicity from the development point of view as the XML parser and transaction code is already available.
> 
> However, XML was designed to exchange data over the web. Musicians, players, composers, soundware developers and audio technicians generally do not know about XML at all.
> 
> In addition, as a universal information exchange format designed for general-purpose applications, XML is inefficient (in terms of information over total data terms), and editing a XML file requires the use of a XML editor instead of a text editor.
> 
> A .sfz file is extremely self-explanatory. Most of the functionality of an instrument can be easily discovered by reading the file.
> 
> Is there a .sfz dedicated editor?  
> From **rgc:audio**, not yet... and not anytime soon.  
> However, we're working with several developers in the industry, creators of sample-conversion software to implement the .sfz format in their converters and editors.
> 
> The nature of the format allows creating instruments using other general-purpose software, like spreadsheets, wordprocessors, simple-scripting languages and other custom tailored software applications.

  
Implementation

* * *

> How an instrument is defined?  
> The basic component of an instrument is a **region**. An instrument then, is defined by one or more regions. Multiple regions can be arranged in a **group**. Groups allow entering common parameters for multiple regions.  
>   
> A region can include three main components: the definition for a **sample**, a set of **input controls** and a set of **performance parameters**.  
> 
> Sample  
> The sample opcode defines which sample file will be played when the region is defined to play.  
> If a **sample** opcode is not present in the region, the region will play the sample defined in the last **<group>**. If there's no previous group defined, or if the previous group doesn't specify a **sample** opcode, the region will be ignored.
> 
>   
> Input Controls  
> Input controls define **when** the sample defined in a region will play, based in real-world controller values and/or internally calculated values.  
>   
> Real-world controllers are the elements that players, musicians or composers actually use to play music. Internal values are calculated by the player, like sequence counters and random generators.  
>   
> The _sfz_ format relies in the standard Musical Instruments Digital Interface (MIDI) specification for all input controls. Most available performance controllers implement MIDI, and it's still the dominating specification for software audio sequencers in all platforms.
> 
> Keyboard controllers are the most significant example of an Input Controls generator. Other generators could be MIDI guitars and string instruments, wind controllers, drum and percussion controllers. With individual differences, they all generate a common set of messages defined in the MIDI specification.  
>   
> A set of input controls then, are the combination of a played MIDI note with its velocity, continuous controllers, pitch bend, channel and polyphonic aftertouch, etc.  
>   
> When a particular set of input controls matches the definition for a region, the sample specified in that region plays, using a particular set of performance parameters also specified in the region.
> 
> Inside the definition file, a region starts with the **<region>** header. A region is defined between two **<region>** headers, or between a **<region>** header and a **<group>** header, or between a **<region>** header and the end of the file,.
> 
> Following the **<region>** header one or more opcodes can be defined. The opcodes are special keywords which instruct the player on what, when and how to play a sample.
> 
> Opcodes within a region can appear in any order, and they have to be separated by one or more spaces or tabulation controls. Opcodes can appear in separated lines within a region.
> 
> Opcodes and assigned opcode values are separated by the equal to sign (**\=**), without spaces between the opcode and the sign. For instance:
> 
> sample=trombone\_a4\_ff.wav  
> sample=cello\_a5\_pp first take.wav  
>   
> are valid examples, while:  
>   
> sample = cello\_a4\_pp.wav  
>   
> Is not (note the spaces at the sides of the = sign).  
> Input Controls and Performance Parameters opcodes are optional, so they might not be present in the definition file. An 'expectable' default value for each parameter is pre-defined, and will be used if there's no definition.
> 
> Example region definitions:
> 
> <region> sample=440.wav  
>   
> This region definition instructs the player to play the sample file '440.wav' for the whole keyboard range.
> 
> <region> lokey=64 hikey=67 sample=440.wav  
>   
> This region features a very basic set of input parameters (lokey and hikey, which represent the low and high MIDI notes in the keyboard), and the sample definition.  
> This instructs the player to play the sample '440.wav', if a key in the 64-67 range is played.
> 
> It is very important to note that all Input Controls defined in a region act using the AND boolean operator. Consequently, all conditions must be matched for the region to play. For instance:
> 
> <region> lokey=64 hikey=67 lovel=0 hivel=34 locc1=0 hicc1=40 sample=440.wav
> 
> This region definition instructs the player to play the sample '440.wav' if there is an incoming note event in the 64-67 range AND the note has a velocity in the 0~34 range AND last modulation wheel (cc1) message was in the 0~40 range.
> 
>   
> Performance parameters  
> The Performance Parameters define **how** the sample specified will play, once the region is defined to play.  
> A simple example of a Performance Parameter is **volume**. It defines how loud the sample will be played when the region plays.  
>   
>   
> Groups  
> As previously stated, groups allow entering common parameters for multiple regions. A group is defined with the **<group>** opcode, and the parameters enumerated on it last till the next group opcode, or till the end of the file.
> 
> <group>  
> ampeg\_attack=0.04 ampeg\_release=0.45  
>   
> <region> sample=trumpet\_pp\_c4.wav key=c4  
> <region> sample=trumpet\_pp\_c#4.wav key=c#4  
> <region> sample=trumpet\_pp\_d4.wav key=d4<region> sample=trumpet\_pp\_d#4.wav key=d#4
> 
> <group>  
> <region> sample=trumpet\_pp\_e4.wav key=e4 // previous group parameters reset  
> 
> Comments  
> Comment lines can be inserted anywhere inside the file. A comment line starts with the slash character ('/'), and it extends till the end of the line.
> 
> <region>  
> sample=trumpet\_pp\_c4.wav  
> // middle C in the keyboard  
> lokey=60  
> // pianissimo layer  
> lovel=0 hivel=20 // another comment
> 
>   
> Where the sample files have to be stored?  
> Sample files can be stored either in the same folder where the .sfz definition file resides, or in any alternative route, specified relatively to the location of the definition file. Consequently:  
>   
> sample=trumpet\_pp\_c3.wav  
> sample=samples\\trumpet\_pp\_c3.wav  
> sample=..\\trumpet\_pp\_c3.wav  
>   
> Are all valid sample names.  
>   
> Alternatively, the player might specify one or several 'user folders', where it will search for samples if it doesn't find them in the same folder as the definition file.
> 
>   
> What the _sfz_ format can do?  
> The sfz format is aimed to allow the arrange of a sample collection in a flexible and expandable way. It's up to the player to decide which functionality it wants to implement.  
> 
> Units  
> All units in the sfz format are in real-world values. Frequencies are expressed in Hertz, pitches in cents, amplitudes in percentage and volumes in decibels.  
> Notes are expressed in MIDI Note Numbers, or in note names according to the International Pitch Notation (IPN) convention. According to this rules, middle C in the keyboard is C4 and the MIDI note number 60.

Opcode list

* * *

> The following is a description of all valid opcodes for the _sfz_ format version 1.0:  
>   
> 
> Opcode
> 
> Description
> 
> Type
> 
> Default
> 
> Range
> 
> Sample Definition
> 
> **sample**
> 
> This opcode defines which sample file the region will play.  
> The value of this opcode is the filename of the sample file, including the extension. The filename must be stored in the same folder where the definition file is, or specified relatively to it.  
> If the sample file is not found, the player will ignore the whole region contents.  
> Long names and names with blank spaces and other special characters (excepting the = character) are allowed in the sample definition.  
>   
> The sample will play unchanged when a note equal to the **pitch\_keycenter** opcode value is played. If **pitch\_keycenter** is not defined for the region, sample will play unchanged on note 60 (middle C).
> 
> Examples:  
> sample=guitar\_c4\_ff.wav  
> sample=dog kick.ogg  
> sample=out of tune trombone (redundant).wav  
> sample=staccatto\_snare.ogg  
> 
> string  
> (filename)
> 
> n/a
> 
> n/a
> 
> Input Controls
> 
> **lochan  
> hichan**
> 
> If incoming notes have a MIDI channel between **lochan** and **hichan**, the region will play.
> 
> Examples:  
> lochan=1 hichan=5
> 
> integer
> 
> lochan=1  
> hichan=16
> 
> 1 to 16
> 
> **lokey  
> hikey  
> key**
> 
> If a note equal to or higher than **lokey** AND equal to or lower than **hikey** is played, the region will play.  
>   
> **lokey** and **hikey** can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)  
>   
> The **key** opcode sets **lokey, hikey** and **pitch\_keycenter** to the same note.  
>   
> Examples:  
> lokey=60 // middle C  
> hikey=63 // middle D#  
> lokey=c4 // middle C  
> hikey=d#4 // middle D#  
> hikey=eb4 // middle Eb (D#)  
>   
> 
> integer
> 
> lokey=0, hikey=127
> 
> 0 to 127  
> C-1 to G9
> 
> **lovel  
> hivel**
> 
> If a note with velocity value equal to or higher than **lovel** AND equal to or lower than **hivel** is played, the region will play.
> 
> integer
> 
> lovel=0,  
> hivel=127
> 
> 0 to 127
> 
> **loccN  
> hiccN**
> 
> Defines the range of the last MIDI controller N required for the region to play.  
>   
> Examples:  
> locc74=30 hicc74=100
> 
> The region will play only if last MIDI controller 74 received was in the 30~100 range.  
>   
> 
> integer
> 
> locc=0, hicc=127  
>   
> for all controllers
> 
> 0 to 127
> 
> **lobend  
> hibend**
> 
> Defines the range of the last Pitch Bend message required for the region to play.  
>   
> Examples:  
> lobend=0 hibend=4000
> 
> The region will play only if last Pitch Bend message received was in the 0~4000 range.  
>   
> 
> integer
> 
> lobend=-8192, hibend=8192  
> 
> \-8192 to 8192
> 
> **lochanaft  
> hichanaft**
> 
> Defines the range of last Channel Aftertouch message required for the region to play.  
>   
> Examples:  
> lochanaft=30 hichanaft=100
> 
> The region will play only if last Channel Aftertouch message received was in the 30~100 range.  
>   
> 
> integer
> 
> lochanaft=0, hichanaft=127  
> 
> 0 to 127
> 
> **lopolyaft  
> hipolyaft**
> 
> Defines the range of last Polyphonic Aftertouch message required for the region to play.  
>   
> The incoming **note** information in the Polyphonic Aftertouch message is not relevant.  
>   
> Examples:  
> lopolyaft=30 hipolyaft=100
> 
> The region will play only if last Polyphonic Aftertouch message received was in the 30~100 range.  
>   
> 
> integer
> 
> lopolyaft=0, hipolyaft=127  
> 
> 0 to 127
> 
> **lorand  
> hirand**
> 
> Random values. The player will generate a new random number on every note-on event, in the range 0~1.  
>   
> The region will play if the random number is equal to or higher than **lorand**, and lower than **hirand**.
> 
> Examples:  
> lorand=0.2 hirand=0.4  
> lorand=0.4 hirand=1  
>   
> 
> floating point
> 
> lorand = 0  
> hirand = 1
> 
> 0 to 1
> 
> **lobpm  
> hibpm**
> 
> Host tempo value. The region will play if the host tempo is equal to or higher than **lobpm**, and lower than **hibpm**.
> 
> Examples:  
> lobpm=0 hibpm=100  
> lobpm=100 hibpm=200.5  
> 
> floating point
> 
> lobpm = 0  
> hibpm = 500
> 
> 0 to 500 bpm
> 
> **seq\_length**
> 
> Sequence length. The player will keep an internal counter creating a consecutive note-on sequence for each region, starting at 1 and resetting at **seq\_length.**
> 
> Examples:  
> seq\_length=3  
> 
> integer
> 
> 1
> 
> 1 to 100
> 
> **seq\_position**
> 
> Sequence position. The region will play if the internal sequence counter is equal to **seq\_position**.
> 
> Examples:  
> seq\_length=4 seq\_position=2  
>   
> In above example, the region will play on the second note every four notes.  
> 
> integer
> 
> 1
> 
> 1 to 100
> 
> **sw\_lokey  
> sw\_hikey**
> 
> Defines the range of the keyboard to be used as trigger selectors for the **sw\_last** opcode.  
>   
> **sw\_lokey** and **sw\_hikey** can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)  
>   
> Examples:  
> sw\_lokey=48 sw\_hikey=53  
>   
> 
> integer
> 
> sw\_lokey=0, sw\_hikey=127  
> 
> 0 to 127  
> C-1 to G9
> 
> **sw\_last**
> 
> Enables the region to play if the last key pressed in the range specified by **sw\_lokey** and **sw\_hikey** is equal to the **sw\_last** value.  
>   
> **sw\_last** can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)  
>   
> Examples:  
> sw\_last=49  
>   
> 
> integer
> 
> 0  
> 
> 0 to 127  
> C-1 to G9
> 
> **sw\_down**
> 
> Enables the region to play if the key equal to **sw\_down** value is depressed.  
> Key has to be in the range specified by **sw\_lokey** and **sw\_hikey**.  
>   
> **sw\_down** can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)  
>   
> Examples:  
> sw\_down=Cb3  
>   
> 
> integer
> 
> 0  
> 
> 0 to 127  
> C-1 to G9
> 
> **sw\_up**
> 
> Enables the region to play if the key equal to **sw\_up** value is not depressed.  
> Key has to be in the range specified by **sw\_lokey** and **sw\_hikey**.  
>   
> **sw\_up** can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)  
>   
> Examples:  
> sw\_up=49  
>   
> 
> integer
> 
> 0  
> 
> 0 to 127  
> C-1 to G9
> 
> **sw\_previous**
> 
> Previous note value. The region will play if last note-on message was equal to **sw\_previous** value.  
>   
> **sw\_previous** can be entered in either MIDI note numbers (0 to 127) or in MIDI note names (C-1 to G9)
> 
> Examples:  
> sw\_previous=60  
>   
> 
> integer
> 
> none
> 
> 0 to 127  
> C-1 to G9
> 
> **sw\_vel**
> 
> This opcode allows overriding the velocity for the region with the velocity of the previous note. Values can be:
> 
> **current**: Region uses the velocity of current note.  
>   
> **previous**: Region uses the velocity of the previous note.  
>   
> Examples:  
> sw\_vel=previous  
>   
> 
> text
> 
> current
> 
> current, previous
> 
> **trigger  
> **
> 
> Sets the trigger which will be used for the sample to play. Values can be:  
>   
> **attack** (default): Region will play on note-on.  
> **release:** Region will play on note-off. The velocity used to play the note-off sample is the velocity value of the corresponding (previous) note-on message.  
> **first:** Region will play on note-on, but if there's no other note going on (staccato, or first note in a legato phrase).  
> **legato:** Region will play on note-on, but only if there's a note going on (notes after first note in a legato phrase).
> 
> Examples:  
> trigger=release
> 
> integer
> 
> attack
> 
> attack,  
> release, first, legato
> 
> **group**
> 
> Exclusive group number for this region.  
> 
> Examples:  
> group=3  
> group=334  
>   
> 
> integer
> 
> 0
> 
> 0 to 4Gb (4294967296)
> 
> **off**\_**by**
> 
> Region off group. When a new region with a group number equal to **off\_by** plays, this region will be turned off.  
> 
> Examples:  
> off\_by=3  
> off\_by=334  
>   
> 
> integer
> 
> 0
> 
> 0 to 4Gb (4294967296)
> 
> **off**\_**mode**
> 
> Region off mode. This opcode will determinate how a region is turned off by an **off\_by** opcode. Values can be:
> 
> **fast** (default): The voice will be turned off immediately. Release settings will not have any effect.  
>   
> **normal**: The region will be set into release stage. All envelope generators will enter in release stage, and region will expire when the amplifier envelope generator expired.  
> 
> Examples:  
> off\_mode=fast  
> off\_mode=normal  
>   
> 
> text
> 
> fast
> 
> fast, normal
> 
> **on\_loccN  
> on\_hiccN**
> 
> Sample trigger on MIDI continuous control N. If a MIDI control message with a value between **on\_loccN** and **on\_hiccN** is received, the region will play.  
> 
> Examples:  
> on\_locc1=0 on\_hicc1=0  
>   
> Region will play when a MIDI CC1 (modulation wheel) message with zero value is received.
> 
> integer
> 
> \-1 (unassigned)
> 
> 0 to 127
> 
> Performance Parameters
> 
> Sample Player
> 
> **delay**
> 
> Region delay time, in seconds.  
> If a **delay** value is specified, the region playback will be postponed for the specified time.  
> If the region receives a note-off message before delay time, the region won't play.  
>   
> All envelope generators delay stage will start counting after region delay time.
> 
> Examples:  
> delay\=1  
> delay=0.2  
>   
> 
> floating point
> 
> 0
> 
> 0 to 100 seconds
> 
> **delay\_random**
> 
> Region random delay time, in seconds.  
> If the region receives a note-off message before delay time, the region won't play.  
>   
> Examples:  
> delay\_random=1  
> delay\_random=0.2  
>   
> 
> floating point
> 
> 0
> 
> 0 to 100 seconds
> 
> **delay\_ccN**
> 
> Region delay time after MIDI continuous controller N messages are received, in seconds.  
> If the region receives a note-off message before delay time, the region won't play.  
>   
> Examples:  
> delay\_cc1=1  
> delay\_cc2=.5  
>   
> 
> floating point
> 
> 0
> 
> 0 to 100 seconds
> 
> **offset**
> 
> The offset used to play the sample, in sample units.  
> The player will reproduce samples starting with the very first sample in the file, unless **offset** is specified. It will start playing the file at the **offset** sample in this case.  
> 
> Examples:  
> offset=3000  
> offset=32425  
>   
> 
> integer
> 
> 0
> 
> 0 to 4 Gb (4294967296)
> 
> **offset\_random**
> 
> Random offset added to the region offset, in sample units.  
> 
> Examples:  
> offset\_random=300  
> offset\_random=100  
>   
> 
> integer
> 
> 0
> 
> 0 to 4 Gb (4294967296)
> 
> **offset\_ccN**
> 
> The offset used to play the sample according to last position of MIDI continuous controller N, in sample units.  
>   
> This opcode is useful to specify an alternate sample start point based on MIDI controllers.  
> 
> Examples:  
> offset\_cc1=3000  
> offset\_cc64=1388  
>   
> 
> integer
> 
> 0
> 
> 0 to 4 Gb (4294967296)
> 
> **end**
> 
> The endpoint of the sample, in sample units.  
> The player will reproduce the whole sample if **end** is not specified.  
>   
> If end value is -1, the sample will not play. Marking a region end with -1 can be used to use a silent region to turn off other regions by using the **group** and **off\_by** opcodes.
> 
> Examples:  
> end\=133000  
> end=4432425  
>   
> 
> integer
> 
> 0
> 
> \-1 to 4 Gb (4294967296)
> 
> **count**
> 
> The number of times the sample will be played. If this opcode is specified, the sample will restart as many times as defined. Envelope generators will not be retriggered on sample restart.  
> When this opcode is defined, loopmode is automatically set to **one\_shot**.
> 
> Examples:  
> count=3  
> count=2  
>   
> 
> integer
> 
> 0
> 
> 0 to 4 Gb (4294967296)
> 
> **loop**\_**mode**
> 
> If **loop**\_**mode** is not specified, each sample will play according to its predefined loop mode. That is, the player will play the sample looped using the first defined loop, if available. If no loops are defined, the wave will play unlooped.  
>   
> The **loop\_mode** opcode allows playing samples with loops defined in the unlooped mode. The possible values are:
> 
> **_no\_loop_:** no looping will be performed. Sample will play straight from start to end, or until note off, whatever reaches first.  
> **_one\_shot_:** sample will play from start to end, ignoring note off.  
> This mode is engaged automatically if the **count** opcode is defined.  
> **_loop\_continuous_:** once the player reaches sample loop point, the loop will play until note expiration.  
> **_loop\_sustain_:** the player will play the loop while the note is held, by keeping it depressed or by using the sustain pedal (CC64). The rest of the sample will play after note release.  
>   
> Examples:  
> loop\_mode=no\_loop  
> loop\_mode=loop\_continuous  
>   
> 
> text
> 
> **no\_loop** for samples without a loop defined,  
> **loop\_continuous** for samples with defined loop(s).  
> 
> n/a
> 
> **loop**\_**start**
> 
> The loop start point, in samples.  
>   
> If **loop**\_**start** is not specified and the sample has a loop defined, the sample start point will be used.  
>   
> If **loop**\_**start** is specified, it will overwrite the loop start point defined in the sample.
> 
> This opcode will not have any effect if loopmode is set to **no\_loop**.
> 
> Examples:  
> loop\_start=4503  
> loop\_start\=12445  
>   
> 
> integer
> 
> 0
> 
> 0 to 4 Gb (4294967296)
> 
> **loop**\_**end**
> 
> The loop end point, in samples. This opcode will not have any effect if loopmode is set to **no\_loop**.
> 
> If **loop**\_**end** is not specified and the sample have a loop defined, the sample loop end point will be used.  
>   
> If **loop**\_**end** is specified, it will overwrite the loop end point defined in the sample.
> 
> Examples:  
> loop\_end\=34503  
> loop\_end=212445  
>   
> 
> integer
> 
> 0
> 
> 0 to 4 Gb (4294967296)
> 
> **sync\_beats**
> 
> Region playing synchronization to host position.  
>   
> When **sync\_beats** is specified and after input controls instruct the region to play, the playback will be postponed until the next multiple of the specified value is crossed.  
>   
> Examples:  
> sync\_beats=4  
>   
> In this example, if note is pressed in beat 2 of current track, note won't be played until beat 4 reaches.  
>   
> This opcode will only work in hosts featuring song position information (vstTimeInfo ppqPos).  
>   
> 
> floating point
> 
> 0
> 
> 0 to 32 beats
> 
> **sync\_offset**
> 
> Region playing synchronization to host position offset.  
>   
> When **sync\_beats** is specified and after input controls instruct the region to play, the playback will be postponed until the next multiple of the specified value plus the **sync\_offset** value is crossed.  
>   
> Examples:  
> sync\_beats=4 sync\_offset=1  
>   
> In this example, if note is pressed in beat 2 of current track, note won't be played until beat 5 reaches.  
>   
> This opcode will only work in hosts featuring song position information (vstTimeInfo ppqPos).  
>   
> 
> floating point
> 
> 0
> 
> 0 to 32 beats
> 
> Pitch
> 
> **transpose**
> 
> The transposition value for this region which will be applied to the sample.  
>   
> Examples:  
> transpose=3  
> transpose=-4  
>   
> 
> integer
> 
> 0
> 
> \-127 to 127
> 
> **tune**
> 
> The fine tuning for the sample, in cents. Range is �1 semitone, from -100 to 100. Only negative values must be prefixed with sign.  
>   
> Examples:  
> tune=33  
> tune=-30  
> tune=94  
>   
> 
> integer
> 
> 0
> 
> \-100 to 100
> 
> **pitch\_keycenter**
> 
> Root key for the sample.  
>   
> Examples:  
> pitch\_keycenter=56  
> pitch\_keycenter\=c#2  
>   
> 
> integer
> 
> 60 (C4)
> 
> \-127 to 127  
> C-1 to G9
> 
> **pitch\_keytrack**
> 
> Within the region, this value defines how much the pitch changes with every note. Default value is 100, which means pitch will change one hundred cents (one semitone) per played note.  
> Setting this value to zero means that all notes in the region will play the same pitch, particularly useful when mapping drum sounds.  
>   
> Examples:  
> pitch\_keytrack=20  
> pitch\_keytrack\=0  
>   
> 
> integer
> 
> 100
> 
> \-1200 to 1200
> 
> **pitch\_veltrack**
> 
> Pitch velocity tracking, represents how much the pitch changes with incoming note velocity, in cents.  
>   
> Examples:  
> pitch\_veltrack=0  
> pitch\_veltrack=1200  
>   
> 
> integer
> 
> 0
> 
> \-9600 to 9600 cents
> 
> **pitch\_random**
> 
> Random tuning for the region, in cents. Random pitch will be centered, with positive and negative values.  
>   
> Examples:  
> pitch\_random=100  
> pitch\_random=400  
>   
> 
> integer
> 
> 0
> 
> 0 to 9600 cents
> 
> **bend\_up**
> 
> Pitch bend range when Bend Wheel or Joystick is moved up, in cents.  
>   
> Examples:  
> bend\_up=1200  
> bend\_up=100  
>   
> 
> integer
> 
> 200
> 
> \-9600 to 9600
> 
> **bend**\_**down**
> 
> Pitch bend range when Bend Wheel or Joystick is moved down, in cents.  
>   
> Examples:  
> bend\_down=1200  
> bend\_down=100  
>   
> 
> integer
> 
> \-200
> 
> \-9600 to 9600
> 
> **bend**\_**step**
> 
> Pitch bend step, in cents.  
>   
> Examples:  
> bend\_step=100 // glissando in semitones  
> bend\_step=200 // glissando in whole tones  
> 
> integer
> 
> 1
> 
> 1 to 1200
> 
> Pitch EG
> 
> **pitcheg\_delay**
> 
> Pitch EG delay time, in seconds. This is the time elapsed from note on to the start of the Attack stage.  
>   
> Examples:  
> pitcheg\_delay=1.5  
> pitcheg\_delay=0  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitcheg\_start**
> 
> Pitch EG start level, in percentage.  
>   
> Examples:  
> pitcheg\_start=20  
> pitcheg\_start=100  
>   
>   
> 
> floating point
> 
> 0 %
> 
> 0 to 100 %
> 
> **pitcheg\_attack**
> 
> Pitch EG attack time, in seconds.  
>   
> Examples:  
> pitcheg\_attack=1.2  
> pitcheg\_attack=0.1  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitcheg\_hold**
> 
> Pitch EG hold time, in seconds. During the hold stage, EG output will remain at its maximum value.  
>   
> Examples:  
> pitcheg\_hold=1.5  
> pitcheg\_hold=0.1  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitcheg\_decay**
> 
> Pitch EG decay time, in seconds.
> 
>   
> Examples:  
> pitcheg\_decay=1.5  
> pitcheg\_decay=3  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitcheg\_sustain**
> 
> Pitch EG sustain level, in percentage.  
>   
> Examples:  
> pitcheg\_sustain=40.34  
> pitcheg\_sustain=10  
>   
>   
> 
> floating point
> 
> 100 %
> 
> 0 to 100 %
> 
> **pitcheg\_release**
> 
> Pitch EG release time (after note release), in seconds.  
>   
> Examples:  
> pitcheg\_release=1.34  
> pitcheg\_release=2  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitcheg\_depth**
> 
> Depth for the pitch EG, in cents.  
>   
> Examples:  
> pitcheg\_depth=1200  
> pitcheg\_depth\=-100  
>   
>   
> 
> integer
> 
> 0
> 
> \-12000 to 12000
> 
> **pitcheg\_vel2delay**
> 
> Velocity effect on pitch EG delay time, in seconds.  
>   
> Examples:  
> pitcheg\_vel2delay=1.2  
> pitcheg\_vel2delay\=0.1  
>   
> Delay time will be calculated as**  
>   
> delay time = pitcheg\_delay** **\+ pitcheg\_vel2delay \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **pitcheg\_vel2attack**
> 
> Velocity effect on pitch EG attack time, in seconds.  
>   
> Examples:  
> pitcheg\_vel2attack=1.2  
> pitcheg\_vel2attack=0.1  
>   
> Attack time will be calculated as**  
>   
> attack time = pitcheg\_attack** **\+ pitcheg\_vel2attack \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **pitcheg\_vel2hold**
> 
> Velocity effect on pitch EG hold time, in seconds.  
>   
> Examples:  
> pitcheg\_vel2hold=1.2  
> pitcheg\_vel2hold=0.1  
>   
> Hold time will be calculated as**  
>   
> hold time = pitcheg\_hold** **\+ pitcheg\_vel2hold \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **pitcheg\_vel2decay**
> 
> Velocity effect on pitch EG decay time, in seconds.  
>   
> Examples:  
> pitcheg\_vel2decay=1.2  
> pitcheg\_vel2decay=0.1  
>   
> Decay time will be calculated as**  
>   
> decay time = pitcheg\_decay** **\+ pitcheg\_vel2decay \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **pitcheg\_vel2sustain**
> 
> Velocity effect on pitch EG sustain level, in percentage.  
>   
> Examples:  
> pitcheg\_vel2sustain=30  
> pitcheg\_vel2sustain=20  
>   
> Sustain level will be calculated as**  
>   
> sustain level = pitcheg\_sustain** **\+ pitcheg\_vel2sustain  
> **  
> 
> floating point
> 
> 0 %
> 
> \-100 % to 100 %
> 
> **pitcheg\_vel2release**
> 
> Velocity effect on pitch EG release time, in seconds.  
>   
> Examples:  
> pitcheg\_vel2release=1.2  
> pitcheg\_vel2release=0.1  
>   
> Release time will be calculated as**  
>   
> release time = pitcheg\_release** **\+ pitcheg\_vel2release \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **pitcheg\_vel2depth**
> 
> Velocity effect on pitch EG depth, in cents.  
>   
> Examples:  
> pitcheg\_vel2depth=100  
> pitcheg\_vel2depth=-1200  
> 
> integer
> 
> 0 cents
> 
> \-12000 to 12000 cents
> 
> Pitch LFO
> 
> **pitchlfo\_delay**
> 
> The time before the Pitch LFO starts oscillating, in seconds.  
>   
> Examples:  
> pitchlfo\_delay=1  
> pitchlfo\_delay=0.4  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitchlfo\_fade**
> 
> Pitch LFO fade-in effect time.  
>   
> Examples:  
> pitchlfo\_fade=1  
> pitchlfo\_fade=0.4  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **pitchlfo\_freq**
> 
> Pitch LFO frequency, in hertz.  
>   
> Examples:  
> pitchlfo\_freq=0.4  
> pitchlfo\_freq=1.3  
>   
> 
> floating point
> 
> 0 Hertz
> 
> 0 to 20 hertz
> 
> **pitchlfo\_depth**
> 
> Pitch LFO depth, in cents.  
>   
> Examples:  
> pitchlfo\_depth=1  
> pitchlfo\_depth=4  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **pitchlfo\_depthccN**
> 
> Pitch LFO depth when MIDI continuous controller N is received, in cents.  
>   
> Examples:  
> pitchlfo\_depthcc1=100  
> pitchlfo\_depthcc32=400  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **pitchlfo\_depthchanaft**
> 
> Pitch LFO depth when channel aftertouch MIDI messages are received, in cents.  
>   
> Examples:  
> pitchlfo\_depthchanaft=100  
> pitchlfo\_depthchanaft=400  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **pitchlfo\_depthpolyaft**
> 
> Pitch LFO depth when polyphonic aftertouch MIDI messages are received, in cents.  
>   
> Examples:  
> pitchlfo\_depthpolyaft\=100  
> pitchlfo\_depthpolyaft\=400  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **pitchlfo\_freqccN**
> 
> Pitch LFO frequency change when MIDI continuous controller N is received, in hertz.  
>   
> Examples:  
> pitchlfo\_freqcc1=5  
> pitchlfo\_freqcc1\=-12  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> **pitchlfo\_freqchanaft**
> 
> Pitch LFO frequency change when channel aftertouch MIDI messages are received, in hertz.  
>   
> Examples:  
> pitchlfo\_freqchanaft=10  
> pitchlfo\_freqchanaft=-40  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> **pitchlfo\_freqpolyaft**
> 
> Pitch LFO frequency change when polyphonic aftertouch MIDI messages are received, in hertz.  
>   
> Examples:  
> pitchlfo\_freqpolyaft\=10  
> pitchlfo\_freqpolyaft\=-4  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> Filter
> 
> **fil**\_**type**
> 
> Filter type. Avaliable types are:
> 
> **lpf\_1p**: one-pole low pass filter (6dB/octave).  
> **hpf\_1p**: one-pole high pass filter (6dB/octave).  
> **lpf\_2p**: two-pole low pass filter (12dB/octave).  
> **hpf\_2p**: two-pole high pass filter (12dB/octave).  
> **bpf\_2p**: two-pole band pass filter (12dB/octave).  
> **brf\_2p**: two-pole band rejection filter (12dB/octave).  
>   
> Examples:  
> fil\_type=lpf\_2p  
> fil\_type=hpf\_1p  
>   
> 
> text
> 
> lpf\_2p
> 
> lpf\_1p, hpf\_1p, lpf\_2p, hpf\_2p, bpf\_2p, brf\_2p
> 
> **cutoff**
> 
> The filter cutoff frequency, in Hertz.  
>   
> If the cutoff is not specified, the filter will be disabled, with the consequent CPU drop in the player.
> 
> Examples:  
> cutoff=343  
> cutoff=4333  
>   
> 
> floating point
> 
> filter disabled
> 
> 0 to  
> SampleRate / 2
> 
> **cutoff\_ccN**
> 
> The variation in the cutoff frequency when MIDI continuous controller N is received, in cents.  
>   
> Examples:  
> cutoff\_cc1=1200  
> cutoff\_cc2=-100  
>   
> 
> integer
> 
> 0
> 
> \-9600 to 9600 cents
> 
> **cutoff\_chanaft**
> 
> The variation in the cutoff frequency when MIDI channel aftertouch messages are received, in cents.  
>   
> Examples:  
> cutoff\_chanaft=1200  
> cutoff\_chanaft\=-100  
>   
> 
> integer
> 
> 0
> 
> \-9600 to 9600 cents
> 
> **cutoff\_polyaft**
> 
> The variation in the cutoff frequency when MIDI polyphonic aftertouch messages are received, in cents.  
>   
> Examples:  
> cutoff\_polyaft=1200  
> cutoff\_polyaft\=-100  
>   
> 
> integer
> 
> 0
> 
> \-9600 to 9600 cents
> 
> **resonance**
> 
> The filter cutoff resonance value, in decibels.  
>   
> Examples:  
> resonance=30  
>   
>   
> 
> floating point
> 
> 0 dB
> 
> 0 to 40 dB
> 
> **fil\_keytrack**
> 
> Filter keyboard tracking (change on cutoff for each key) in cents.  
>   
> Examples:  
> fil\_keytrack=100  
> fil\_keytrack=0  
>   
> 
> integer
> 
> 0 cents
> 
> 0 to 1200 cents
> 
> **fil\_keycenter**
> 
> Center key for filter keyboard tracking. In this key, the filter keyboard tracking will have no effect.  
>   
> Examples:  
> fil\_keycenter=60  
> fil\_keycenter=48  
>   
> 
> integer
> 
> 60
> 
> 0 to 127
> 
> **fil\_veltrack**
> 
> Filter velocity tracking, represents how much the cutoff changes with incoming note velocity.  
>   
> Examples:  
> fil\_veltrack=0  
> fil\_veltrack=1200  
>   
> 
> integer
> 
> 0
> 
> \-9600 to 9600 cents
> 
> **fil\_random**
> 
> Random cutoff added to the region, in cents.  
>   
> Examples:  
> fil\_random=100  
> fil\_random=400  
>   
> 
> integer
> 
> 0
> 
> 0 to 9600 cents
> 
> Filter EG
> 
> **fileg\_delay**
> 
> Filter EG delay time, in seconds. This is the time elapsed from note on to the start of the Attack stage.  
>   
> Examples:  
> fileg\_delay=1.5  
> fileg\_delay=0  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fileg\_start**
> 
> Filter EG start level, in percentage.  
>   
> Examples:  
> fileg\_start=20  
> fileg\_start=100  
>   
>   
> 
> floating point
> 
> 0 %
> 
> 0 to 100 %
> 
> **fileg\_attack**
> 
> Filter EG attack time, in seconds.  
>   
> Examples:  
> fileg\_attack=1.2  
> fileg\_attack=0.1  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fileg\_hold**
> 
> Filter EG hold time, in seconds. During the hold stage, EG output will remain at its maximum value.  
>   
> Examples:  
> fileg\_hold=1.5  
> fileg\_hold=0.1  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fileg\_decay**
> 
> Filter EG decay time, in seconds.
> 
> Examples:  
> fileg\_decay=1.5  
> fileg\_decay=3  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fileg\_sustain**
> 
> Filter EG sustain level, in percentage.  
>   
> Examples:  
> fileg\_sustain=40.34  
> fileg\_sustain=10  
>   
> 
> floating point
> 
> 100 %
> 
> 0 to 100 %
> 
> **fileg\_release**
> 
> Filter EG release time (after note release), in seconds.  
>   
> Examples:  
> fileg\_release=1.34  
> fileg\_release=2  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fileg\_depth**
> 
> Depth for the filter EG, in cents.  
>   
> Examples:  
> fileg\_depth=1200  
> fileg\_depth\=-100  
>   
> 
> integer
> 
> 0
> 
> \-12000 to 12000
> 
> **fileg\_vel2delay**
> 
> Velocity effect on filter EG delay time, in seconds.  
>   
> Examples:  
> fileg\_vel2delay=1.2  
> fileg\_vel2delay\=0.1  
>   
> Delay time will be calculated as**  
>   
> delay time = fileg\_delay** **\+ fileg\_vel2delay \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **fileg\_vel2attack**
> 
> Velocity effect on filter EG attack time, in seconds.  
>   
> Examples:  
> fil\_vel2attack=1.2  
> fil\_vel2attack=0.1  
>   
> Attack time will be calculated as**  
>   
> attack time = fileg\_attack** **\+ fileg\_vel2attack \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **fileg\_vel2hold**
> 
> Velocity effect on filter EG hold time, in seconds.  
>   
> Examples:  
> fileg\_vel2hold=1.2  
> fileg\_vel2hold=0.1  
>   
> Hold time will be calculated as**  
>   
> hold time = fileg\_hold** **\+ fileg\_vel2hold \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **fileg\_vel2decay**
> 
> Velocity effect on filter EG decay time, in seconds.  
>   
> Examples:  
> fileg\_vel2decay=1.2  
> fileg\_vel2decay=0.1  
>   
> Decay time will be calculated as**  
>   
> decay time = fileg\_decay** **\+ fileg\_vel2decay \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **fileg\_vel2sustain**
> 
> Velocity effect on filter EG sustain level, in percentage.  
>   
> Examples:  
> fileg\_vel2sustain=30  
> fileg\_vel2sustain=-30  
>   
> Sustain level will be calculated as**  
>   
> sustain level = fileg\_sustain** **\+ fileg\_vel2sustain  
>   
> **Result will be clipped to 0~100%.  
> 
> floating point
> 
> 0 %
> 
> \-100 % to 100 %
> 
> **fileg\_vel2release**
> 
> Velocity effect on filter EG release time, in seconds.  
>   
> Examples:  
> fileg\_vel2release=1.2  
> fileg\_vel2release=0.1  
>   
> Release time will be calculated as**  
>   
> release time = fileg\_release** **\+ fileg\_vel2release \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **fileg\_vel2depth**
> 
> Velocity effect on filter EG depth, in cents.  
>   
> Examples:  
> fileg\_vel2depth=100  
> fileg\_vel2depth=-1200  
> 
> integer
> 
> 0 cents
> 
> \-12000 to 12000 cents
> 
> Filter LFO
> 
> **fillfo\_delay**
> 
> The time before the filter LFO starts oscillating, in seconds.  
>   
> Examples:  
> fillfo\_delay=1  
> fillfo\_delay=0.4  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fillfo\_fade**
> 
> Filter LFO fade-in effect time.  
>   
> Examples:  
> fillfo\_fade=1  
> fillfo\_fade=0.4  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **fillfo\_freq**
> 
> Filter LFO frequency, in hertz.  
>   
> Examples:  
> fillfo\_freq=0.4  
> fillfo\_freq=1.3  
>   
> 
> floating point
> 
> 0 Hertz
> 
> 0 to 20 hertz
> 
> **fillfo\_depth**
> 
> Filter LFO depth, in cents.  
>   
> Examples:  
> fillfo\_depth=1  
> fillfo\_depth=4  
>   
> 
> floating point
> 
> 0 dB
> 
> \-1200 to 1200 cents
> 
> **fillfo\_depthccN**
> 
> Filter LFO depth when MIDI continuous controller N is received, in cents.  
>   
> Examples:  
> fillfo\_depthcc1=100  
> fillfo\_depthcc32=400  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **fillfo\_depthchanaft**
> 
> Filter LFO depth when channel aftertouch MIDI messages are received, in cents.  
>   
> Examples:  
> fillfo\_depthchanaft=100  
> fillfo\_depthchanaft=400  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **fillfo\_depthpolyaft**
> 
> Filter LFO depth when polyphonic aftertouch MIDI messages are received, in cents.  
>   
> Examples:  
> fillfo\_depthpolyaft\=100  
> fillfo\_depthpolyaft\=400  
>   
> 
> integer
> 
> 0 cent
> 
> \-1200 to 1200 cents
> 
> **fillfo\_freqccN**
> 
> Filter LFO frequency change when MIDI continuous controller N is received, in hertz.  
>   
> Examples:  
> fillfo\_freqcc1=5  
> fillfo\_freqcc1\=-12  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> **fillfo\_freqchanaft**
> 
> Filter LFO frequency change when channel aftertouch MIDI messages are received, in hertz.  
>   
> Examples:  
> fillfo\_freqchanaft=10  
> fillfo\_freqchanaft=-40  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> **fillfo\_freqpolyaft**
> 
> Filter LFO frequency change when polyphonic aftertouch MIDI messages are received, in hertz.  
>   
> Examples:  
> fillfo\_freqpolyaft\=10  
> fillfo\_freqpolyaft\=-4  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> Amplifier
> 
> **volume**
> 
> The volume for the region, in decibels.  
>   
> Examples:  
> volume=-24  
> volume=0  
> volume=3.5  
>   
> 
> floating point
> 
> 0.0
> 
> \-144 to 6 dB
> 
> **pan**
> 
> The panoramic position for the region.  
>   
> If a mono sample is used, **pan** value defines the position in the stereo image where the sample will be placed.  
> When a stereo sample is used, the pan value the relative amplitude of one channel respect the other.  
>   
> A value of zero means centered, negative values move the panoramic to the left, positive to the right.  
>   
> Examples:  
> pan=-30.5  
> pan=0  
> pan=43  
>   
> 
> floating point
> 
> 0.0
> 
> \-100 to 100
> 
> **width**
> 
> Only operational for stereo samples, **width** defines the amount of channel mixing applied to play the sample.  
> 
> A **width** value of 0 makes a stereo sample play as if it were mono (adding both channels and compensating for the resulting volume change). A value of 100 will make the stereo sample play as original.  
>   
> Any value in between will mix left and right channels with a part of the other, resulting in a narrower stereo field image.  
>   
> Negative **width** values will reverse left and right channels.
> 
> Examples:  
> width=100 // stereo  
> width=0 // play this stereo sample as mono  
> width=50 // mix 50% of one channel with the other  
> 
> floating point
> 
> 0.0
> 
> \-100 to 100 %
> 
> **position**
> 
> Only operational for stereo samples, **position** defines the position in the stereo field of a stereo signal, after channel mixing as defined in the **width** opcode.
> 
>   
> A value of zero means centered, negative values move the panoramic to the left, positive to the right.
> 
>   
> Examples:  
> // mix both channels and play the result at left  
> width=0 position=-100  
>   
> // make the stereo image narrower and play it  
> // slightly right  
> width=50 position=30
> 
> floating point
> 
> 0.0
> 
> \-100 to 100 %
> 
> **amp\_keytrack**
> 
> Amplifier keyboard tracking (change in amplitude per key) in dB.  
>   
> Examples:  
> amp\_keytrack=-1.4  
> amp\_keytrack=3  
>   
> 
> floating point
> 
> 0 dB
> 
> \-96 to 12 dB
> 
> **amp\_keycenter**
> 
> Center key for amplifier keyboard tracking. In this key, the amplifier keyboard tracking will have no effect.  
>   
> Examples:  
> amp\_keycenter=60  
> amp\_keycenter=48  
>   
> 
> integer
> 
> 60
> 
> 0 to 127
> 
> **amp\_veltrack**
> 
> Amplifier velocity tracking, represents how much the amplitude changes with incoming note velocity.  
>   
> Volume changes with incoming velocity in a concave shape according to the following expression:
> 
> Amplitude(dB) = 20 log (127^2 / Velocity^2)  
>   
> The **amp\_velcurve\_N** opcodes allow overriding the default velocity curve.  
>   
> Examples:  
> amp\_veltrack=0  
> amp\_veltrack=100  
>   
> 
> floating point
> 
> 100 %
> 
> \-100 to 100 %
> 
> **amp\_velcurve\_1  
> amp\_velcurve\_127**
> 
> User-defined amplifier velocity curve. This opcode range allows defining a specific curve for the amplifier velocity. The value of the opcode indicates the normalized amplitude (0 to 1) for the specified velocity.
> 
> The player will interpolate lineraly between specified opcodes for unspecified ones:  
>   
> amp\_velcurve\_1=0.2 amp\_velcurve\_3=0.3  
> // amp\_velcurve\_2 is calculated to 0.25  
>   
> If **amp\_velcurve\_127** is not specified, the player will assign it the value of 1.  
>   
> Examples:  
> // linear, compressed dynamic range  
> // amplitude changes from 0.5 to 1  
> amp\_velcurve\_1=0.5  
>   
> 
> floating point
> 
> standard curve (see **amp\_veltrack**)
> 
> 0 to 1
> 
> **amp\_random**
> 
> Random volume for the region, in decibels.  
>   
> Examples:  
> amp\_random=10  
> amp\_random=3  
>   
> 
> floating point
> 
> 0
> 
> 0 to 24 dB
> 
> **rt**\_**decay**
> 
> The volume decay amount when the region is set to play in **release** trigger mode, in decibels per second since note-on message.  
>   
> Examples:  
> rt\_decay=6.5  
>   
>   
> 
> floating point
> 
> 0 dB
> 
> 0 to 200 dB
> 
> **output**
> 
> The stereo output number for this region.  
> If the player doesn't feature multiple outputs, this opcode is ignored.  
>   
> Examples:  
> output=0  
> output=4  
>   
> 
> integer
> 
> 0
> 
> 0 to 1024
> 
> **gain\_ccN**
> 
> Gain applied on MIDI control N, in decibels.
> 
> Examples:  
> gain\_cc1=12  
>   
> 
> floating point
> 
> 0
> 
> \-144 to 48 dB
> 
> **xfin\_lokey  
> xfin\_hikey**
> 
> Fade in control.  
>   
> **xfin\_lokey** and **xfin\_hikey** define the fade-in keyboard zone for the region.  
>   
> The volume of the region will be zero for keys lower than or equal to **xfin\_lokey**, and maximum (as defined by the **volume** opcode) for keys greater than or equal to **xfin\_hikey.**  
> 
> Examples:  
> xfin\_lokey=c3 xfin\_hikey=c4  
>   
> 
> integer
> 
> xfin\_lokey=0  
> xfin\_hikey=0
> 
> 0 to 127  
> C-1 to G9
> 
> **xfout\_lokey  
> xfout\_hikey**
> 
> Fade out control.  
>   
> **xfout\_lokey** and **xfout\_hikey** define the fade-out keyboard zone for the region.  
>   
> The volume of the region will be maximum (as defined by the **volume** opcode) for keys lower than or equal to **xfout\_lokey**, and zero for keys greater than or equal to **xfout\_hikey.**  
> 
> Examples:  
> xfout\_lokey=c5 xfout\_hikey=c6  
>   
>   
> 
> integer
> 
> xfout\_lokey=127  
> xfout\_hikey=127
> 
> 0 to 127  
> C-1 to G9
> 
> **xf\_keycurve**
> 
> Keyboard crossfade curve for the region. Values can be:
> 
> **gain:** Linear gain crossfade. This setting is best when crossfading phase-aligned material. Linear gain crossfades keep constant amplitude during the crossfade, preventing clipping.
> 
> **power:** Equal-power RMS crossfade. This setting works better to mix very different material, as a constant power level is kept during the crossfade.  
>   
> 
> text
> 
> power
> 
> gain, power
> 
> **xfin\_lovel  
> xfin\_hivel**
> 
> Fade in control.  
>   
> **xfin\_lovel** and **xfin\_hivel** define the fade-in velocity range for the region.  
>   
> The volume of the region will be zero for velocities lower than or equal to **xfin\_lovel**, and maximum (as defined by the **volume** opcode) for velocities greater than or equal to **xfin\_hivel.**  
> 
> Examples:  
> xfin\_lovel=0 xfin\_hivel=127  
>   
> 
> integer
> 
> xfin\_lovel=0  
> xfin\_hivel=0
> 
> 0 to 127
> 
> **xfout\_lovel  
> xfout\_hivel**
> 
> Fade out control.  
>   
> **xfout\_lokey** and **xfout\_hikey** define the fade-out velocity range for the region.  
>   
> The volume of the region will be maximum (as defined by the **volume** opcode) for velocities lower than or equal to **xfout\_lovel**, and zero for velocities greater than or equal to **xfout\_hivel.**  
> 
> Examples:  
> xfout\_lovel=0 xfout\_hivel=127  
>   
>   
> 
> integer
> 
> xfout\_lokey=127  
> xfout\_hikey=127
> 
> 0 to 127
> 
> **xf\_velcurve**
> 
> Velocity crossfade curve for the region. Values can be:
> 
> **gain:** Linear gain crossfade. This setting is best when crossfading phase-aligned material. Linear gain crossfades keep constant amplitude during the crossfade, preventing clipping.
> 
> **power:** Equal-power RMS crossfade. This setting works better to mix very different material, as a constant power level is kept during the crossfade.  
>   
> 
> text
> 
> power
> 
> gain, power
> 
> **xfin\_loccN  
> xfin\_hiccN**
> 
> Fade in control.  
>   
> **xfin\_loccN** and **xfin\_hiccN** set the range of values in the MIDI continuous controller N which will perform a fade-in in the region.  
>   
> The volume of the region will be zero for values of the MIDI continuous controller N lower than or equal to **xfin\_loccN**, and maximum (as defined by the **volume** opcode) for values greater than or equal to **xfin\_hiccN.**  
> 
> Examples:  
> xfin\_locc1=64 xfin\_hicc1=127  
>   
>   
> 
> integer
> 
> 0
> 
> 0 to 127
> 
> **xfout\_loccN  
> xfout\_hiccN**
> 
> Fade out control.  
>   
> **xfout\_loccN** and **xfout\_hiccN** set the range of values in the MIDI continuous controller N which will perform a fade-out in the region.  
>   
> The volume of the region will be maximum (as defined by the **volume** opcode) for values of the MIDI continuous controller N lower than or equal to **xfout\_loccN**, and zero for values greater than or equal to **xfout\_hiccN.**  
> 
> Examples:  
> xfout\_locc1=64 xfout\_hicc1=127  
>   
>   
> 
> integer
> 
> 0
> 
> 0 to 127
> 
> **xf\_cccurve**
> 
> MIDI controllers crossfade curve for the region. Values can be:
> 
> **gain:** Linear gain crossfade. This setting is best when crossfading phase-aligned material. Linear gain crossfades keep constant amplitude during the crossfade, preventing clipping.
> 
> **power:** Equal-power RMS crossfade. This setting works better to mix very different material, as a constant power level is kept during the crossfade.  
>   
> 
> text
> 
> power
> 
> gain, power
> 
> Amplifier EG
> 
> **ampeg\_delay**
> 
> Amplifier EG delay time, in seconds. This is the time elapsed from note on to the start of the Attack stage.  
>   
> Examples:  
> ampeg\_delay=1.5  
> ampeg\_delay=0  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **ampeg\_start**
> 
> Amplifier EG start level, in percentage.  
>   
> Examples:  
> ampeg\_start=20  
> ampeg\_start=100  
>   
>   
> 
> floating point
> 
> 0 %
> 
> 0 to 100 %
> 
> **ampeg\_attack**
> 
> Amplifier EG attack time, in seconds.  
>   
> Examples:  
> ampeg\_attack=1.2  
> ampeg\_attack=0.1  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **ampeg\_hold**
> 
> Amplifier EG hold time, in seconds. During the hold stage, EG output will remain at its maximum value.  
>   
> Examples:  
> ampeg\_hold=1.5  
> ampeg\_hold=0.1  
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **ampeg\_decay**
> 
> Amplifier EG decay time, in seconds.
> 
>   
> Examples:  
> ampeg\_decay=1.5  
> ampeg\_decay=3  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **ampeg\_sustain**
> 
> Amplifier EG sustain level, in percentage.  
>   
> Examples:  
> ampeg\_sustain=40.34  
> ampeg\_sustain=10  
>   
>   
> 
> floating point
> 
> 100 %
> 
> 0 to 100 %
> 
> **ampeg\_release**
> 
> Amplifier EG release time (after note release), in seconds.  
>   
> Examples:  
> ampeg\_release=1.34  
> ampeg\_release=2  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **ampeg\_vel2delay**
> 
> Velocity effect on amplifier EG delay time, in seconds.  
>   
> Examples:  
> ampeg\_vel2delay=1.2  
> ampeg\_vel2delay\=0.1  
>   
> Delay time will be calculated as**  
>   
> delay time = ampeg\_delay** **\+ ampeg\_vel2delay \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_vel2attack**
> 
> Velocity effect on amplifier EG attack time, in seconds.  
>   
> Examples:  
> ampeg\_vel2attack=1.2  
> ampeg\_vel2attack=0.1  
>   
> Attack time will be calculated as**  
>   
> attack time = ampeg\_attack** **\+ ampeg\_vel2attack \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_vel2hold**
> 
> Velocity effect on amplifier EG hold time, in seconds.  
>   
> Examples:  
> ampeg\_vel2hold=1.2  
> ampeg\_vel2hold=0.1  
>   
> Hold time will be calculated as**  
>   
> hold time = ampeg\_hold** **\+ ampeg\_vel2hold \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_vel2decay**
> 
> Velocity effect on amplifier EG decay time, in seconds.  
>   
> Examples:  
> ampeg\_vel2decay=1.2  
> ampeg\_vel2decay=0.1  
>   
> Decay time will be calculated as**  
>   
> decay time = ampeg\_decay** **\+ ampeg\_vel2decay \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_vel2sustain**
> 
> Velocity effect on amplifier EG sustain level, in percentage.  
>   
> Examples:  
> ampeg\_vel2sustain=30  
> ampeg\_vel2sustain=-30  
>   
> Sustain level will be calculated as**  
>   
> sustain level= ampeg\_sustain** **\+ ampeg\_vel2sustain  
>   
> **The result will be clipped to 0~100%**.  
> **  
> 
> floating point
> 
> 0%
> 
> \-100 % to 100 %
> 
> **ampeg\_vel2release**
> 
> Velocity effect on amplifier EG release time, in seconds.  
>   
> Examples:  
> ampeg\_vel2release=1.2  
> ampeg\_vel2release=0.1  
>   
> Release time will be calculated as**  
>   
> release time = ampeg\_release** **\+ ampeg\_vel2release \* velocity / 127  
> **  
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_delayccN**
> 
> Amplifier EG delay time added on MIDI control N, in seconds.  
>   
> Examples:  
> ampeg\_delaycc20=1.5  
> ampeg\_delaycc1\=0  
>   
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_startccN**
> 
> Amplifier EG start level added on MIDI control N, in percentage.  
>   
> Examples:  
> ampeg\_startcc20\=20  
> ampeg\_startcc1\=100  
>   
> 
> floating point
> 
> 0 %
> 
> \-100 to 100 %
> 
> **ampeg\_attackccN**
> 
> Amplifier EG attack time added on MIDI control N, in seconds.  
>   
> Examples:  
> ampeg\_attackcc20\=1.2  
> ampeg\_attackcc1\=0.1  
>   
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_holdccN**
> 
> Amplifier EG hold time added on MIDI control N, in seconds.  
>   
> Examples:  
> ampeg\_holdcc20\=1.5  
> ampeg\_holdcc1\=0.1  
>   
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_decayccN**
> 
> Amplifier EG decay time added on MIDI control N, in seconds.
> 
>   
> Examples:  
> ampeg\_decaycc20\=1.5  
> ampeg\_decaycc1\=3  
>   
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> **ampeg\_sustainccN**
> 
> Amplifier EG sustain level added on MIDI control N, in percentage.  
>   
> Examples:  
> ampeg\_sustaincc20\=40.34  
> ampeg\_sustaincc1\=10  
>   
> 
> floating point
> 
> 100 %
> 
> \-100 to 100 %
> 
> **ampeg\_releaseccN**
> 
> Amplifier EG release time added on MIDI control N, in seconds.  
>   
> Examples:  
> ampeg\_releasecc20\=1.34  
> ampeg\_releasecc1\=2  
>   
> 
> floating point
> 
> 0 seconds
> 
> \-100 to 100 seconds
> 
> Amplifier LFO
> 
> **amplfo\_delay**
> 
> The time before the Amplifier LFO starts oscillating, in seconds.  
>   
> Examples:  
> amplfo\_delay=1  
> amplfo\_delay=0.4  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **amplfo\_fade**
> 
> Amplifier LFO fade-in effect time.  
>   
> Examples:  
> amplfo\_fade=1  
> amplfo\_fade=0.4  
>   
>   
> 
> floating point
> 
> 0 seconds
> 
> 0 to 100 seconds
> 
> **amplfo\_freq**
> 
> Amplifier LFO frequency, in hertz.  
>   
> Examples:  
> amplfo\_freq=0.4  
> amplfo\_freq=1.3  
>   
> 
> floating point
> 
> 0 Hertz
> 
> 0 to 20 hertz
> 
> **amplfo\_depth**
> 
> Amplifier LFO depth, in decibels.  
>   
> Examples:  
> amplfo\_depth=1  
> amplfo\_depth=4  
>   
> 
> floating point
> 
> 0 dB
> 
> \-10 to 10 dB
> 
> **amplfo\_depthccN**
> 
> Amplifier LFO depth when MIDI continuous controller N is received, in decibels.  
>   
> Examples:  
> amplfo\_depthcc1=100  
> amplfo\_depthcc32=400  
>   
> 
> floating point
> 
> 0 dB
> 
> \-10 to 10 dB
> 
> **amplfo\_depthchanaft**
> 
> Amplifier LFO depth when channel aftertouch MIDI messages are received, in cents.  
>   
> Examples:  
> amplfo\_depthchanaft=100  
> amplfo\_depthchanaft=400  
>   
> 
> floating point
> 
> 0 dB
> 
> \-10 to 10 dB
> 
> **amplfo\_depthpolyaft**
> 
> Amplifier LFO depth when polyphonic aftertouch MIDI messages are received, in cents.  
>   
> Examples:  
> amplfo\_depthpolyaft\=100  
> amplfo\_depthpolyaft\=400  
>   
> 
> floating point
> 
> 0 dB
> 
> \-10 to 10 dB
> 
> **amplfo\_freqccN**
> 
> Amplifier LFO frequency change when MIDI continuous controller N is received, in hertz.  
>   
> Examples:  
> amplfo\_freqcc1=5  
> amplfo\_freqcc1\=-12  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> **amplfo\_freqchanaft**
> 
> Amplifier LFO frequency change when channel aftertouch MIDI messages are received, in hertz.  
>   
> Examples:  
> amplfo\_freqchanaft=10  
> amplfo\_freqchanaft=-40  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> **amplfo\_freqpolyaft**
> 
> Amplifier LFO frequency change when polyphonic aftertouch MIDI messages are received, in hertz.  
>   
> Examples:  
> amplfo\_freqpolyaft\=10  
> amplfo\_freqpolyaft\=-4  
>   
> 
> floating point
> 
> 0 hertz
> 
> \-200 to 200 hertz
> 
> Equalizer
> 
> **eq1\_freq  
> eq2\_freq  
> eq3\_freq**
> 
> Frequency of the equalizer band, in Hertz.  
>   
> Examples:  
> eq1\_freq=80 eq2\_freq=1000 eq3\_freq=4500  
>   
>   
> 
> floating point
> 
> eq1\_freq=50  
> eq2\_freq=500  
> eq3\_freq=5000
> 
> 0 to 30000 Hz
> 
> **eq1\_freqccN  
> eq2\_freqccN  
> eq3\_freqccN**
> 
> Frequency change of the equalizer band when MIDI continuous control N messages are received, in Hertz.  
>   
> Examples:  
> eq1\_freqcc1=80  
> 
> floating point
> 
> 0
> 
> \-30000 to 30000 Hz
> 
> **eq1\_vel2freq  
> eq2\_vel2freq  
> eq3\_vel2freq**
> 
> Frequency change of the equalizer band with MIDI velocity, in Hertz.  
>   
> Examples:  
> eq1\_vel2freq=1000  
> 
> floating point
> 
> 0
> 
> \-30000 to 30000 Hz
> 
> **eq1\_bw  
> eq2\_bw  
> eq3\_bw  
> **
> 
> Bandwidth of the equalizer band, in octaves.  
>   
> Examples:  
> eq1\_bw=1 eq2\_bw=0.4 eq3\_bw=1.4  
>   
>   
> 
> floating point
> 
> 1 octave
> 
> 0.001 to 4 octaves
> 
> **eq1\_bwccN  
> eq2\_bwccN  
> eq3\_bwccN  
> **
> 
> Bandwidth change of the equalizer band when MIDI continuous control N messages are received, in octaves.  
>   
> Examples:  
> eq1\_bwcc29=1.3  
>   
>   
> 
> floating point
> 
> 0
> 
> \-4 to 4 octaves
> 
> **eq1\_gain  
> eq2\_gain  
> eq3\_gain  
> **
> 
> Gain of the equalizer band, in decibels.  
>   
> Examples:  
> eq1\_gain=-3 eq2\_gain=6 eq3\_gain=-6  
>   
>   
> 
> floating point
> 
> 0 dB
> 
> \-96 to 24 dB
> 
> **eq1\_gainccN  
> eq2\_gainccN  
> eq3\_gainccN  
> **
> 
> Gain change of the equalizer band when MIDI continuous control N messages are received, in decibels.  
>   
> Examples:  
> eq1\_gaincc23=-12  
>   
>   
> 
> floating point
> 
> 0 dB
> 
> \-96 to 24 dB
> 
> **eq1\_vel2gain  
> eq2\_vel2gain  
> eq3\_vel2gain**
> 
> Gain change of the equalizer band with MIDI velocity, in decibels.  
>   
> Examples:  
> eq1\_vel2gain=12  
> 
> floating point
> 
> 0
> 
> \-96 to 24 dB
> 
> Effects
> 
> **effect1**
> 
> Level of effect1 send, in percentage (reverb in sfz).  
>   
> Examples:  
> effect1=100  
>   
>   
> 
> floating point
> 
> 0
> 
> 0 to 100 %
> 
> **effect2**
> 
> Level of effect2 send, in percentage (chorus in sfz).  
>   
> Examples:  
> effect2=100  
>   
>   
> 
> floating point
> 
> 0
> 
> 0 to 100 %