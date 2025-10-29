    ‹sample› - SFZ Format                    Top

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

‹sample›
========

Allows to embed sample data directly in SFZ files (Rapture).

[](#example)Example
-------------------

```
<region> sample=mysample.wav
<sample> name=mysample.wav data=[encoded-content-of-mysample.wav]

```

The content encoding is an alphabet mapping of 256 entries that map to each byte. (in the encoding, a WAV file is immediately recognizable by having its four byte "RIFF" header encoded to "|spp")

[This C source file](../../assets/src/makesample.c) can be compiled to convert a wav file to an embedded sample.

[](#decoding)Decoding
---------------------

The decoding algorithm is as follows:

*   Loop while there is an input byte `b1`
*   if `b1` is the end marker $24, stop reading
*   if `b1` is '\\r' (\\(0D) or '\\n' (\\)0A), discard it
*   if `b1` is the escape character '=' ($3D),
    *   extract the next byte `b2`, and compute the next output byte as `(b2+$C0)%256`
*   otherwise, compute the next output byte as `(b2+$D6)%256`

[](#encoding)Encoding
---------------------

*   Loop while there is an input byte `b1`
*   if `(b1+$2A)%256` is one of the "forbidden characters" ($3D, $00, $09, $0A, $0D, $24)
    *   output the escape character $3D, and then output the byte `(b1+$40)%256`
*   otherwise, output `(b1+$2A)%256`
*   Output the end marker $24

[](#alphabet)Alphabet
---------------------

The alphabet used for the coding is as following:

$00

$10

$20

$30

$40

$50

$60

$70

$80

$90

$A0

$B0

$C0

$D0

$E0

$F0

**$00**

$2A

$3A

$4A

$5A

$6A

$7A

$8A

$9A

$AA

$BA

$CA

$DA

$EA

$FA

$3D20

$1A

**$01**

$2B

$3B

$4B

$5B

$6B

$7B

$8B

$9B

$AB

$BB

$CB

$DB

$EB

$FB

$0B

$1B

**$02**

$2C

$3C

$4C

$5C

$6C

$7C

$8C

$9C

$AC

$BC

$CC

$DC

$EC

$FC

$0C

$1C

**$03**

$2D

$3D53

$4D

$5D

$6D

$7D

$8D

$9D

$AD

$BD

$CD

$DD

$ED

$FD

$3D23

$1D

**$04**

$2E

$3E

$4E

$5E

$6E

$7E

$8E

$9E

$AE

$BE

$CE

$DE

$EE

$FE

$0E

$1E

**$05**

$2F

$3F

$4F

$5F

$6F

$7F

$8F

$9F

$AF

$BF

$CF

$DF

$EF

$FF

$0F

$1F

**$06**

$30

$40

$50

$60

$70

$80

$90

$A0

$B0

$C0

$D0

$E0

$F0

$3D16

$10

$20

**$07**

$31

$41

$51

$61

$71

$81

$91

$A1

$B1

$C1

$D1

$E1

$F1

$01

$11

$21

**$08**

$32

$42

$52

$62

$72

$82

$92

$A2

$B2

$C2

$D2

$E2

$F2

$02

$12

$22

**$09**

$33

$43

$53

$63

$73

$83

$93

$A3

$B3

$C3

$D3

$E3

$F3

$03

$13

$23

**$0A**

$34

$44

$54

$64

$74

$84

$94

$A4

$B4

$C4

$D4

$E4

$F4

$04

$14

$3D3A

**$0B**

$35

$45

$55

$65

$75

$85

$95

$A5

$B5

$C5

$D5

$E5

$F5

$05

$15

$25

**$0C**

$36

$46

$56

$66

$76

$86

$96

$A6

$B6

$C6

$D6

$E6

$F6

$06

$16

$26

**$0D**

$37

$47

$57

$67

$77

$87

$97

$A7

$B7

$C7

$D7

$E7

$F7

$07

$17

$27

**$0E**

$38

$48

$58

$68

$78

$88

$98

$A8

$B8

$C8

$D8

$E8

$F8

$08

$18

$28

**$0F**

$39

$49

$59

$69

$79

$89

$99

$A9

$B9

$C9

$D9

$E9

$F9

$3D1F

$19

$29

{: .table .table-sm .table-bordered .table-striped }

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/headers/sample.md)

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