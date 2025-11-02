    Latest News - SFZ Format                    Top

[![Logo image](images/logo_svg)](..)

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

Latest News
===========

.md-typeset .blog-post:first-of-type h3 { margin-top: 0; } .md-typeset .blog-post-title { margin-bottom: 0; } .md-typeset .blog-post-extra { color: var(--md-default-fg-color--light); } .md-typeset .blog-center { text-align: center; } .md-typeset .blog-pagination { display: inline-block; margin-top: 20px; } .md-typeset .blog-pagination a { color: var(--md-typeset-color); float: left; padding: .25em 1em; text-decoration: none; border-radius: 1em; margin-left: .25em; margin-right: .25em; transition: all .15s ease-in-out; } .md-typeset .blog-pagination a.active { background-color: var(--md-typeset-a-color); color: white; font-weight: bold; } .md-typeset .blog-pagination a:hover:not(.active) { background-color: #dddddda1; } .md-typeset .blog-hidden { display: none; } .md-typeset .blogging-tags-grid { display: flex; flex-direction: row; flex-wrap: wrap; gap: 8px; margin-top: 5px; } .md-typeset .blogging-tag { color: var(--md-typeset-color); background-color: var(--md-typeset-code-color); white-space: nowrap; display: block; } .md-typeset .blogging-tag code { border-radius: 5px; }

### [](#bootstrap-5-3-0-with-color-modes)[Bootstrap 5.3.0 with color modes](https://sfz.github.io/news/posts/2023-06-03-bootstrap-530-with-color-modes/)

Published by redtide on 2023-06-03 11:43:28

Bootstrap updated to v5.3.0 which supports [color modes](https://getbootstrap.com/docs/5.3/customize/color-modes/), which means that if your system uses a dark color theme, it will adapt to your visual preferences on browsers that supports it. Highlight.js will adapt to the chosen theme, so the sfz examples will be shown with it.

### [](#opcodes-page-update)[Opcodes page update](https://sfz.github.io/news/posts/2020-10-16-opcodes-page-update/)

Published by redtide on 2020-10-16 19:59:58

For those who missed it we have some updates on the website, mainly regarding the opcodes page. Recently I've added a [javascript library](https://bootstrap-table.com) that permits tables column sorting, and now with an awesome contribution from @jpcima also a script to filter opcode names, versions and categories. Hope you'll find them handy!

### [](#new-tutorial-and-opcode-additions)[New tutorial and opcode additions](https://sfz.github.io/news/posts/2020-03-17-new-tutorial-and-opcode-additions/)

Published by redtide on 2020-03-17 00:00:00

A new tutorial about [subtractive synthesizers](https://sfzformat.com/tutorials/subtractive_synths) was shared by DSmolken's sample instruments experience applied in the [Caveman Cosmonaut](https://github.com/sfzinstruments/karoryfer.caveman-cosmonaut) sample library.  
Some fixes and additions were made in our opcode database and in software as well, like the Windows [OpenMPT](https://openmpt.org/) music tracker by sagamusix.  
New contributions was provided by other users like jisaacstone, and a big contribution from jpcima for the [effects](https://sfzformat.com/opcodes/type#cakewalk-implementation) section.  
Now we have also a new page for convenience that lists [all opcodes](https://sfzformat.com/misc/all_opcodes) present in our database.

### [](#new-year-new-work-in-progress)[New year, new work in progress](https://sfz.github.io/news/posts/2020-01-31-new-year-new-work-in-progress/)

Published by redtide on 2020-01-31 00:00:00

The most relevant additions on the website for this month were [Instruments](https://sfzinstruments.github.io) and [Modulations](../../../modulations/) sections, adding slowly one by one some sample instruments libraries created and freely distribuited over the net, and documenting in a generic way the various modulations used in SFZ. Some new opcodes were also added in our database, starting from some modulation aliases like amplitude\_ccN, pan\_ccN and tune\_ccN to the recent fil\_gain. I would like to thank some people who contributed to the site, like falkTX for adding our news feed on [Linuxaudio Planet](https://planet.linuxaudio.org/), jpcima, MatFluor, PaulFd and sfw. This website is an opensource non profit project, I hope to see more people involved in the future to help make it grow.

### [](#happy-new-year)[Happy new year!](https://sfz.github.io/news/posts/2019-12-29-happy-new-year/)

Published by RedTide on 2019-12-29 00:00:00

Here we are with the latest relevant updates, the last ones for this year:

*   Added `*_mod` and `*_dynamic` opcodes
*   Added [Cakewalk SFZv2 opcodes](../../../opcodes/?v=cakewalk) (work in progress) page
*   Added the SFZ test suite for sample instruments developers in homepage
*   Improved SFZ syntax highlighting in [Google Prettify](https://github.com/google/code-prettify) for all pages
*   Search now works correctly, though it is slow and needs some more improvements

Happy new year!

### [](#legato-tutorial)[Legato tutorial](https://sfz.github.io/news/posts/2019-11-21-legato-tutorial/)

Published by DSmolken on 2019-11-21 00:00:00

The legato tutorial has been expanded from one simple example to include simulated legato, simulated portamento, and true sampled legato.

### [](#new-players-and-tutorial)[New players and tutorial](https://sfz.github.io/news/posts/2019-11-16-new-players-and-tutorial/)

Published by RedTide on 2019-11-16 00:00:00

New applications were added to the players list recently: - [HISE](http://hise.audio/) - [sfizz](https://sfz.tools/sfizz/) - [liquidsfz](https://github.com/swesterfeld/liquidsfz)

and a new tutorial from [Sonoj 2019 Convention](https://www.sonoj.org/) on [how to recording samples using Ardour and LinuxSampler](https://media.ccc.de/v/sonoj2019-1904-recording-samples#t=1469) by [Christoph Kuhr](https://media.ccc.de/search?q=Christoph+Kuhr) to our [Video tutorials](https://sfzformat.com/tutorials/videos) section.

Thanks to [Stefan Westerfeld](https://github.com/swesterfeld) for our first GitHub pull request! And to Sonoj organization for the video tutorial contribuition.

Last but not least, for those like me who prefer [IRC](https://en.wikipedia.org/wiki/Internet_Relay_Chat) we have now also an [IRC channel](https://kiwiirc.com/nextclient/#irc://irc.freenode.net:+6697/#sfzformat) on [freenode](https://freenode.net/) server.

`/join` us!

### [](#sfz-page-on-italian-wikipedia)[SFZ page on Italian Wikipedia](https://sfz.github.io/news/posts/2019-09-16-sfz-page-on-italian-wikipedia/)

Published by RedTide on 2019-09-16 00:00:00

A new page about the SFZ format has been added to the [Italian Wikipedia](https://it.wikipedia.org/wiki/SFZ_\(formato_di_file\)). Let's grow!

### [](#modulations-explained)[Modulations Explained](https://sfz.github.io/news/posts/2019-08-01-modulation_explained/)

Published by DSmolken on 2019-08-01 00:00:00

We have two new articles explaining the modulations possible in [SFZ1](../../../tutorials/sfz1_modulations/) and [SFZ2](../../../tutorials/sfz2_modulations/). Hopefully it will now be much easier to understand what's possible under each spec level, and just what those complex SFZ2 LFOs and envelopes can and can't do.

### [](#new-tutorial)[New Tutorial](https://sfz.github.io/news/posts/2019-07-25-new-tutorial/)

Published by DSmolken on 2019-07-25 00:00:00

We've published a [new tutorial](../../../tutorials/brush_stirs/) explaining how to use samples to model brushed drum techniques which produce a continuous sound rather than a discrete hit. Admittedly, this is a rather niche technique not only in the samples world but also in real-world music, mainly used in jazz and some indie music. Next we plan to expand the [vibrato tutorial](../../../tutorials/vibrato/), which is currently only a simple code example.

Minor updates: + global\_label, master\_label, group\_label and region\_label opcodes added. + Added Carla and Bliss Sampler to SFZ players, updated TAL Sampler info.

### [](#new-website-launched)[New Website Launched](https://sfz.github.io/news/posts/2019-04-23-new-website-launched/)

Published by RedTide on 2019-04-23 00:00:00

We're proud to announce a new website!

*   Built on [Jekyll](http://jekyllrb.com/).
*   Most content is authored in [Markdown](http://daringfireball.net/projects/markdown/) format.
*   Utilizes [Bootstrap](http://getbootstrap.com/) and [SASS](https://sass-lang.com/) for easy skinning and responsive design, making the website available to mobile devices.
*   Utilizes [FontAwesome](http://fontawesome.io/) and [Favicon Generator](https://realfavicongenerator.net/) for content and website icons.

1 [2](#blog-p2) [3](#blog-p3)

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

This site is open source. [Improve this page](https://github.com/sfz/sfz.github.io/edit/source/docs/news/index.md)

var base\_url = "..", shortcuts = {"help": 191, "next": 78, "previous": 80, "search": 83}; hljs.highlightAll(); window.addEventListener("load", function (event) { if (anchors) { anchors.options.placement = 'left'; anchors.add(); } });

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

var currentPage = 0 const lastComponent = window.location.href.split("/").slice(-1).pop() if (lastComponent && lastComponent.slice(0, 7) == "#blog-p") { const page = parseInt(lastComponent.slice(7)) if (page) { currentPage = page - 1 } } function scrollToTop() { setTimeout(function () { window.scrollTo(0, 0); }, 100); } const onButtonClick = (ele) => { var current = pagination.getElementsByClassName("active"); if (current.length) { current\[0\].className = current\[0\].className.replace( " active", "" ); } ele.className += " active"; // Togglg visibility of pages const destPage = parseInt(ele.textContent) var pages = document.getElementsByClassName("page") if (destPage && pages.length) { for (var j = 0; j < pages.length; j++) { const pageId = parseInt(pages\[j\].id.replace("page", "")) if (pageId != destPage) { // This is not the destination page if (!pages\[j\].className.includes("blog-hidden")) { pages\[j\].className += " blog-hidden" } } else { // This is the destination page pages\[j\].className = pages\[j\].className.replace(" blog-hidden", "") } } scrollToTop(); } }; var pagination = document.getElementById("blog-pagination"); if (pagination) { var links = pagination.getElementsByClassName("page-number"); if (links.length) { for (var i = 0; i < links.length; i++) { // Toggle pagination highlight links\[i\].addEventListener("click", function () { onButtonClick(this); }); } links\[currentPage\].className += " active" onButtonClick(links\[currentPage\]); } }