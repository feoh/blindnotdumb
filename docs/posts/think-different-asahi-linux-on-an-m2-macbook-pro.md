---
title: 'Think Different: Asahi Linux On An M2 MacBook Pro'
slug: think-different-asahi-linux-on-an-m2-macbook-pro
date: 2025-12-11 18:57:35 UTC-05:00
tags:
- mac
- macos
- linux
- asahi
- m2
- macbook
---

# Fair Warning

I am a pragmatist. If the idea of someone using Snap to install software fills you with inchoate rage, shop elsewhere
and, forgive me, but maybe reconsider your life choices :)

Also, Asahi is still a diamond in the rough. Please do read the [Supported
Features](https://asahilinux.org/docs/platform/feature-support/overview/) for your particular hardware **very**
carefully to ensure that Asahi will meet your needs.

# It's Not Me, Mac, It's You.

Over the last few years it has become ever more increasingly clear to me that, to put it simply and as objectively as I
can, Apple's target customer's needs and my needs are drifting further and further apart.

The Mac has always been a bit of a rainbow farting unicorn. It is a computer that people who **love** computers also
love to use, but it's also a computer you can confidently give to grandma and grandpa and know that they'll be just fine
(either through their own cleverness or the fact that AppleCare is never more than a phone call away).

I don't in any way blame Apple for this. The computer market is dwindling at an alarming rate. More and more people can
do everything they need on their tablets or even their phones, so companies that want to stay in the game are being
forced to make some hard decisions.

The last straw for me was their recent "glass" redesign. I'm partially blind and low vision, and making everything *even
more translucent and harder to see** has convinced me utterly that accessibility is no longer a priority for them.

Evasive action is called for.

I don't currently own a laptop of my own, but 3 years ago, lured by the siren song of its incredible battery life, when
I started work at MIT I chose a 16" M2 Macbook Pro.

Since I recently adopted Linux with KDE on my primary workhorse desktop computer at home, I was chuffed to learn that
the [Asahi Linux Project](https://asahilinux.org) has, after moving through a few other Linux flavors, settled upon the
amazing [KDE Desktop](https://kde.org) running on top of [Fedora Linux](https://www.fedoraproject.org).

I'll be writing a separate post about how much I'm enjoying KDE. There's SO much to explore there, and for someone like
me who enjoys hyper-optimizing their workflow and environment? It's a gold mine!

But today, I want to talk about finding ways to leverage Asahi. It's still very much a work in progress, and one might
even say a labor of love created by a truly amazing group of brilliant engineers and open source contributors.

There's no doubt that there are a few rough edges, but even so I have taken a machine that had become a regular source
of frustration and turned it into the amazing intellectual spring board it had the potential to become!

So let's get started!

# Installing

While you definitely don't want to ask Grandpa to install Asahi Linux on his Mac without a more technically savvy friend
standing by, the actual process is very straightforward if you pay careful attention and follow directions.

## Choices

The first real choice you'll be confronted with is how much disk space to allocate to Asahi. Of course, this is up to
you, but as my lovely wife is fond of saying, I am all about the extremes. Everything or nothing, winning or losing,
BRING IT! :)

So I chose the 'min' option to leave the minimal amount of space required for MacOS behind and use the rest to dive into
the brave new world of Asahi.

Pay **very** careful attention to the section of the installation instructions where it tells you what to do after
reboot. This is where most new folks stumble so it pays to print the instructions out or have them handy on a tablet for
a careful re-read as you go.

Once you're booted into Fedora, it's smooth sailing and you're in Linux just like you would be on an Intel machine!

# Moving In's Easy. Unpacking? Not So Much!

I won't bore you with the details of the process I use to set up a new computer. I'll probably write that up as a
separate article as well, but the bottom line is I use the IMO excellent strategy of making my Linux home directory into
a Git repository, so managing my dot files works just like any other work with Github I do every day, and setting up a
new machine is as easy as running a tiny [shell script](https://gist.github.com/feoh/3bcde14af243d1bc626aad0f652fe49c)
shell script I have on a Github Gist.

I stole this strategy from an [Atlassian blog post](https://www.atlassian.com/git/tutorials/dotfiles) and it's been a
life changer. No more struggling with whether a given dot file is up to date, or remembering whether I made changes over
there and forgot to copy them. It's all in Git. Done and dusted!

# The Devil's In The Details - Software!

While many of the tools I use day to day are handily contained in Fedora's standard repositories and are either a trip
to KDE Discovery or a 'dnf install' away, there are a number of problem children that proved harder to get going. These
tools are core to my day to day work so getting them right is important. I wanted to share my experiences here in the
hope that I can save you some work, and maybe even invite you to tell me how I can do it better!

## Obsidian Note Taking

The only way I was able to make this work is by downloading the AppImage. Head on over to [The Obsidian
Website](https://obsidian.md) and Click the "Get Obsidian for Linux (AppImage)" link. Be sure to down download  the ARM64
version or you will be sad :)

On Intel systems, I normally integrate AppImages with my desktop using the excellent
[AppImageLauncher](https://github.com/TheAssassin/AppImageLauncher) but I haven't been able to get it to work on Asahi.
I can install it but it does nothing when I double click the AppImage from Dolphin. On Intel it pops up a dialog and
offers to register your new app with KDE.

I seem to have managed to get it registered in KDE using the [Pin It!](https://github.com/ryonakano/pinit) utility
installed from Discover, but I'm not quite sure what I did so you may need to fiddle a bit (Sorry, awfully vague I
know!).

## Vivaldi Browser

This one was a bit tricky, I tried the various RPMs with zero success, but ultimately decided to give the Snap from the
snap store a try, and it worked like a champ! Just run `snap install vivaldi` and you're good to go!

## Zoom Teleconferencing

What I thought was going to end in a trail of turns actually turned out alright!

I could not for love or money get the Zoom Workspace app to run properly or join a meeting, but in the end analysis,
installing the Chrome extension in Vivaldi and just joining meetings with the web version works great! I can even share
my entire screen!

## Slack

This is IMO the one truly sad story in my personal Asahi journey. Slack does not as of yet ship *any* ARM binaries at
all. It's Intel or GTFO in Slack's book. Jerks.

I realize that it's a matter of getting funded for a niche platform, but then be more friendly to third party developers
who would be **happy** to build clients if you'd only let them in!

Ultimately, I ended up using Vivalidi's PWA (Persistent Web Application) feature to just make the web version of Slack
into its own "app".  This isn't great in any number of ways, but it's the best I've got at the moment.

People have recommended [Slacky](https://github.com/andirsun/Slacky) but all I could get out of that was that Slack was
unable to load. Grump :)

I'll keep updating this as I go with any learning I can share. Please get in touch on the Fediverse if you have
questions or are thinking of trying this yourself. I'd love to hear from you! I'm [@feoh@oldbytes.space there](https://oldbytes.space/@feoh).

I hope you have as much fun as I did transforming your Mac into a lean, mean KDE Linux machine!
