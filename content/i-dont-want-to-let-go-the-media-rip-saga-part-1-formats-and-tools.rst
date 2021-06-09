I don't WANT to let go! The Media Rip Saga - Part 1: Formats and Tools.
#######################################################################
:date: 2018-03-22 09:59
:author: cpatti
:category: geekery
:tags: FLAC, formats, Matroska, music, NAS, reference, rip, tools, video
:slug: i-dont-want-to-let-go-the-media-rip-saga-part-1-formats-and-tools
:status: published

[caption id="attachment_498" align="aligncenter" width="300"]\ |image1| A Musical Mind[/caption]

A coworker at my previous job once said in response to my whining a bit about having just lost 700 songs from my digital music library "Let go of your music collection!".  That got me thinking, long and hard.

Why?

Why **am** I lugging around this corpus of several thousand compact discs? Why **do** I have several shelves worth of DVDs? Why don't I simply let go of the whole idea of media ownership and just drink from the infinite fire-hose that is the internet?

Because, when push comes to shove, my media is **part of me.**  My CD collection represents innumerable fond memories of places, people and moments I've moved on from but that inhabit special places in my heart and mind.

You may have heard the theory that when one sense is diminished, the brain compensates by heightening another. I'm partially blind, so many if not most of my fond memories have a soundtrack. Being able to listen to that particular album and feel some semblance of that moment wash over me is like having a personal time machine.

Oh hey, there's that Autechre album, not available anymore anywhere as far as I can tell. That was one of the first times ever that I was **really** turned on by electronica. Music plays in my mind's eye - one of my best friends and I walking into a record shop on Newbury Street. And there's that Boiled In Lead CD I got the day after I was invited to an incredibly cool private concert at a farm in NH by a friend who's since passed away. Neither of these things is on Spotify near as I can tell. If I let go, I lose them, and an aspect of those fond memories along with them.

But I'm getting older - in fact I turn 50 in a few months. Having moved countless times I have begun to feel the weight of my possessions. I recognize that I am privileged in that I **can** make this choice. Not everyone is lucky enough to be able to buy a NAS (Network Attached Storage) and spend their leisure time converting their media collection into a giant bag of bits. I count myself lucky.

So, now that you've heard way more than you ever wanted to know about **why** I chose to embark upon this epic project, let's talk turkey in case you're thinking about doing this for yourself.

Preserving all your media in virtual form can create a veritable labyrinth of choices. As with all things, I suggest keeping it simple. I'll tell you what my choices were and maybe even offer another option or two along the way, but mostly I'll be guiding you through my process as it has evolved for my purposes.

First let's answer a basic question: What kind of media do you want to preserve? In my case the answer is simple. My collection consists entirely of CDs and DVDs, as well as a handful of Blu-ray discs.

The first big choice - to compress or not to compress? Compressing your media will save you disk space, but cost you in terms of fidelity. The movies you rip won't look exactly as they did on disc, and the music you rip won't be exactly as it was in its original form either.

I will not go down the rabbit hole of trying to convince you of any particular absolute truth, but my ultimate destination ended up being "I **never** want to have to do this again and I want no loss in quality".

So, on the video side, I don't use any compression at all. I rip my movies straight to `Matroska <https://www.matroska.org/>`__ video or ".mkv" files. This format is incredibly rich and versatile, and also has the advantage of being open source. Why do I care one might ask? See above - I **NEVER** want to do this again :) So I don't want to be beholden to some company or other deciding that the format I chose is changing, going away, or under license dispute. These are **my** bits embodying **my** legally purchased media. Full stop.

On the audio side, I was able to take advantage of an excellent format called `FLAC.  <https://xiph.org/flac/>`__\ It provides some compression so as to save space, but most important for me is the fact that it's lossless, so I lose no fidelity at all in my ripped copy. This format is also open source, and the author is a fellow Somervillian :)

Having made the important decisions about format, let's choose appropriate tools.

For the video side, I chose `MakeMKV <https://www.makemkv.com/>`__. It's cross-platform (Mac, Linux, Windows), has a very straight forward user interface, and is dirt cheap. You can download it for free, but to rip Blu-ray discs, you have to pay them $5 or $10 to unlock the decoder. Trust me, for the power this tool offers, give them their money. They've earned it. This was one of the only tools I could find that made ripping both Blu-ray and DVD discs easy while also giving me the flexibility I needed. A number of lesser tools I tried had nice user interfaces, but were rife with bugs. making it nearly impossible to extract the raw bits with no compression.

Another critical tool if you want to rip TV series from DVD is a little thing called `FileBot <https://www.filebot.net/>`__. It will rename the files to conform to what Plex requires.

For the rare case where multiple episodes in a TV show are glommed into one big file, I chose `MKVToolNix <https://mkvtoolnix.download/>`__ to split .mkv files into usable chunks  I'm unsure whether it's worth the effort, especially for series with lots of episodes.

On the audio side, I used `XLD <https://tmkk.undo.jp/xld/index_e.html>`__ for the Mac. It's on par with Xact Audio Copy for Windows, the most highly regarded audio ripper out there near as I can tell. It rips to FLAC effortlessly and the developer maintains a very high quality checksum database of every CD that's been ripped with the tool so you can be sure that your results are crystal clear and bit perfect. I've had Linux folks ask about something similar for them, and I haven't been able to find anything yet. Sorry about that. If someone finds something that does similar things and has a nice UI, do let me know.

You'll also need a place to put the resulting bits. A really safe place. This is a labor intensive effort, and you really don't want to lose all your countless hours of work due to a hard drive failure.

I chose a `Synology <https://www.synology.com/en-us>`__ DS216+ii for the task. It's a nice little box that holds two big hard drives that you can run as a RAID set. In addition to having hardware that meets my needs, I chose these folks because the software the NAS runs is easy to administer, incredibly flexible, and has a rich ecosystem. One great feature I've not seen elsewhere is with just a few clicks, you can back up your data to cloud services like `Glacier <https://aws.amazon.com/glacier/?sc_channel=PS&sc_campaign=acquisition_US&sc_publisher=google&sc_medium=glacier_b&sc_content=glacier_e&sc_detail=aws%20glacier&sc_category=glacier&sc_segment=86341125282&sc_matchtype=e&sc_country=US&s_kwcid=AL!4422!3!86341125282!e!!g!!aws%20glacier&ef_id=WrarjAAABQgBo0QZ:20180324194828:s>`__. Synology has a proprietary suite of software you can use to manage your media. I chose `Plex <https://aws.amazon.com/glacier/?sc_channel=PS&sc_campaign=acquisition_US&sc_publisher=google&sc_medium=glacier_b&sc_content=glacier_e&sc_detail=aws%20glacier&sc_category=glacier&sc_segment=86341125282&sc_matchtype=e&sc_country=US&s_kwcid=AL!4422!3!86341125282!e!!g!!aws%20glacier&ef_id=WrarjAAABQgBo0QZ:20180324194828:s>`__ because it's feature rich and for a lifetime fee will automatically transcode movies and music to work with any viewing or listening device.

In the next installment we'll start getting into the nitty-gritty of how to get the job done. The good, the bad, and the **ugly!**

.. |image1| image:: https://feohorg.files.wordpress.com/2018/03/14119218-music-brain-as-a-musical-mind-as-a-creative-genius-with-musical-notes-representing-the-craft-of-comp.jpg?w=300
   :class: size-medium wp-image-498
   :width: 300px
   :height: 300px
