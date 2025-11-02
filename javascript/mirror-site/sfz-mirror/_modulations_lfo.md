    LFO - SFZ Format                    Top

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

LFO
===

LFO (Low Frequency Oscillator) opcodes are part of the [Modulation](../../misc/categories/#modulation) category of opcodes. They are used to create effects such as pitch vibrato (when modulating pitch), tremolo (when modulating volume) and filter wobble (when modulating filter cutoff)

LFOs are triggered by note-on events for the specified region, which means there are no free-running LFOs in the SFZ spec. If a free-running LFO is needed, for example to apply one slow pitch vibrato wave to a series of rapidly plucked oud notes, that will need to use an external modulation source outside the SFZ player - in other words, perhaps in a DAW that the SFZ player is being used in as a plugin.

#### [](#sfz-1-lfos)SFZ 1 LFOs

3 LFO destinations in SFZ 1 standard:

*   amplfo (amplitude)
*   fillfo (filter)
*   pitchlfo (pitch)

[Here's a very simple example of a pitch LFO integration](../../tutorials/lfo/)

*   [(lfo type)\_delay](../../opcodes/amplfo_delay/)
*   [(lfo type)\_fade](../../opcodes/amplfo_fade/)
*   [(lfo type)\_freq](../../opcodes/amplfo_freq/)
*   [(lfo type)\_freqccX](../../opcodes/amplfo_freq/)
*   [(lfo type)\_depth](../../opcodes/amplfo_depth/)
*   [(lfo type)\_depthccX](../../opcodes/amplfo_depth/)
*   [(lfo type)\_depthchanaft](../../opcodes/amplfo_depthchanaft/)
*   [(lfo type)\_depthpolyaft](../../opcodes/amplfo_depthpolyaft/)
*   [(lfo type)\_freqchanaft](../../opcodes/amplfo_freqchanaft/)
*   [(lfo type)\_freqpolyaft](../../opcodes/amplfo_freqpolyaft/)

#### [](#assignable-lfos-sfz-2)Assignable LFOs (SFZ 2)

Much like the Flex EG, these newer LFO can target almost any tone-defining parameter:

[Here's a very simple example of an sfz 2 lfo integration, targeted to pitch](../../tutorials/lfo/)

*   [lfoN\_wave](../../opcodes/lfoN_wave/)
*   [lfoN\_freq](../../opcodes/lfoN_freq/)
*   [lfoN\_freq\_onccX](../../opcodes/lfoN_freq/)
*   [lfoN\_freq\_smoothccX](../../opcodes/lfoN_freq_smoothccX/)
*   [lfoN\_freq\_stepccX](../../opcodes/lfoN_freq_stepccX/)
*   [lfoN\_delay](../../opcodes/lfoN_delay/)
*   [lfoN\_delay\_onccX](../../opcodes/lfoN_delay/)
*   [lfoN\_fade](../../opcodes/lfoN_fade/)
*   [lfoN\_fade\_onccX](../../opcodes/lfoN_fade/)
*   [lfoN\_phase](../../opcodes/lfoN_phase/)
*   [lfoN\_phase\_onccX](../../opcodes/lfoN_phase/)
*   [lfoN\_count](../../opcodes/lfoN_count/)

#### [](#assignable-lfo-destinations)Assignable LFO Destinations

These destinations are added as a suffix to 'lfoN\_'. For example, lfo01\_pitch=100 makes LFO 01 affect pitch with a max depth of 100 cents, and lfo03\_freq\_lfo01=1.3 would make LFO 03 add up to 1.3 Hertz to the frequency of LFO 01. Note that it's possible to create modulation feedback loops this way, for example LFO 01 modulating LFO 02 while LFO 02 modulates LFO 01.

In addition to the below, in ARIA it's possible to control the amount of freq\_lfo with MIDI CC, so lfo03\_freq\_lfo01\_oncc117=1.3 would make LFO 03 add up to 1.3 Hertz to the frequency of LFO 01, with the amount modulated by MIDI CC 117. So, freq\_lfo\_oncc would be added to the below list for ARIA, though depth\_lfo\_oncc and depthadd\_lfo\_oncc do not appear to be available.

*   freq\_lfoX
*   depth\_lfoX
*   depthadd\_lfoX
*   pitch
*   pitch\_oncc
*   pitch\_smoothcc
*   pitch\_stepcc
*   decim
*   decim\_oncc
*   decim\_smoothcc
*   decim\_stepcc
*   bitred
*   bitred\_oncc
*   bitred\_smoothcc
*   bitred\_stepcc
*   cutoff
*   cutoff\_oncc
*   cutoff\_smoothcc
*   cutoff\_stepcc
*   resonance
*   resonance\_oncc
*   resonance\_smoothcc
*   resonance\_stepcc
*   cutoff2
*   cutoff2\_oncc
*   cutoff2\_smoothcc
*   cutoff2\_stepcc
*   resonance2
*   resonance2\_oncc
*   resonance2\_smoothcc
*   resonance2\_stepcc
*   eqNfreq
*   eqNfreq\_oncc
*   eqNfreq\_smoothcc
*   eqNfreq\_stepcc
*   eqNbw
*   eqNbw\_oncc
*   eqNbw\_smoothcc
*   eqNbw\_stepcc
*   eqNgain
*   eqNgain\_oncc
*   eqNgain\_smoothcc
*   eqNgain\_stepcc
*   volume
*   volume\_oncc
*   volume\_smoothcc
*   volume\_stepcc
*   amplitude
*   amplitude\_oncc
*   amplitude\_smoothcc
*   amplitude\_stepcc
*   pan
*   pan\_oncc
*   pan\_smoothcc
*   pan\_stepcc
*   width
*   width\_oncc
*   width\_smoothcc
*   width\_stepcc

[](#practical-considerations)Practical Considerations
-----------------------------------------------------

SFZ allows LFOs to modulate the frequency of other LFOs, including feedback (LFO number M modulating LFO number N, and vice versa). Mathematically, this can cause very chaotic results. However, in the Cakewalk products (and possibly also in ARIA, though this is not checked) this is simplified. If the number of the modulating LFO is lower than the LFO being modulated (for example, LFO1 modulates LFO2), the modulation is applied when it is calculated. However, if the number of the modulating LFO is higher than the LFO being modulated (for example, LFO4 modulating LFO2), the modulation is not applied until the next LFO frequency update cycle.

This both keeps LFO feedback controlled, and reduces the CPU needed to calculate LFO modulations.

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/modulations/lfo.md)

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