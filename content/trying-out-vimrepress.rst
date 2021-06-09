Trying out VimRepress
#####################
:date: 2012-02-09 16:48
:author: cpatti
:category: Geekery
:tags: blog, blogging, editors, vim
:slug: trying-out-vimrepress
:status: published

VimRePress
----------

| In an ongoing effort to immerse myself in Vim as much as possible, I'm trying out a plugin called `VimRepress <https://github.com/vim-scripts/VimRepress>`__ - a fork of the popular Vimpress plugin.
| 

Installing
~~~~~~~~~~

Unfortunately, getting it running with MacVim on MacOS X Lion is a bit of a bear, but thankfully Paulo Poiati wrote an excellent `article <https://blog.paulopoiati.com/2012/02/07/installing-vimrepress-in-macvim-osx-lion/>`__ on getting the job done.

Basically, if you're using Homebrew, you have to rebuild your MacVim to use the i386 architecture, otherwise you wind up with a Python interpreter that doesn't match the bitness of your editor, and when MacVim goes to invoke Python to run the blogging bits in the plugin, MacVim explodes.

Also unfortunately, you can't use the Homebrew built Python or Ruby interpreters when building MacVim either, and have to instead use the bundled ones from MacOS (both sorely out of date. Who uses Ruby 1.8 anymore? :).

So I had to uninstall my Homebrew based Python and Ruby, install python-markdown2 into the OSX default Python instance, and now everything seems to be working just fine.

Living the Vim Life
-------------------

VimRepress and Blogging
~~~~~~~~~~~~~~~~~~~~~~~

That said, there are still some creature comforts that I miss from the awesome Blogging bundle in TextMate - silly things like giving me a drop down list with the possible Categories for my post and the like. Hopefully over time we can get those implemented in Vim land :)

On the upside, and this counts for a lot, is that I can now write in `Markdown <https://daringfireball.net/projects/markdown/>`__ again <*contented sigh*> I've missed Markdown terribly ever since I transitioned the blog from Typo to Wordpress many moons ago. It's a joy to write in, and really lets me think about the writing, not about a properly formed HTML element, which is priceless.

Vim and Me In the Large
~~~~~~~~~~~~~~~~~~~~~~~

For what it's worth, thus far the minor pain of transitioning to Vim has been entirely worth it, I've definitely seen a noticeable productivity boost, and for work-a-day code and configuration editing, I'm actually finding Vim to be vastly more powerful than TextMate simply because my environment is everywhere I want to be rather than being chained to using my Mac desktop for editing and resorting to chicanery like remote mounted filesystems via sshfs.

For years I'd read `The Pragmatic Programmer <https://pragprog.com/the-pragmatic-programmer>`__ with its mantra of "Learn **one** editor, and learn it \*\ *well*" (paraphrase).

I always had mixed feelings about that. I'd taken pride through most of my career in being able to learn a multitude of different tools and adapt to whatever worked best in the local environment. That is in fact a really great skill to have, but there is definitely wisdom where editors are concerned to pick one and *live* in it 24/7.

`MacVim <https://code.google.com/p/macvim/>`__ has helped tremendously with that. With it you can have your cake and eat it to. You can use the very same config files and plugins you use on your UNIX servers on your desktop, only wrapped in a superbly crafted Aqua GUI.

It's a continuing process, but thus far the work I've put in has been totally worth it. I would encourage anyone who's on the fence to give it a try and be strict with yourself about it. Pick a time when you can afford to take the hit and spend the time to get facile enough that you won't miss your old environment. You won't regret it.
