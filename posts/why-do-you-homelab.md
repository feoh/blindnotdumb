<!--
.. title: Why do YOU Homelab?
.. slug: why-do-you-homelab
.. date: 2023-12-01 17:20:29 UTC-05:00
.. tags: homelab,selfhosting,infrastructure,philosophy,technology,nerdlife
.. category: 
.. link: 
.. description: 
.. type: text
.. author: Chris Patti
-->

![XKCD Comic About Self Hosting](https://imgs.xkcd.com/comics/hard_reboot.png)


# The Internet is a Dangerous Place These Days (Introduction)

In this day and age, you really are taking a risk if you're not running some
form of ad blocking. Heck, even [CISA is telling government agencies this](https://www.wired.com/story/security-roundup-even-cia-nsa-use-ad-blockers/).

So I mentioned on the Fediverse that I was thinking about going back to using
[Pi-hole](https://pi-hole.net/) for this. It's quick to set up, super
convenient, and all around does the job well.

At this, -dsr-, a long time online acquaintance whose opinions I respect, piped in with this:

<iframe src="https://tilde.zone/@dashdsrdash/111449235781879573/embed" width="400" allowfullscreen="allowfullscreen" sandbox="allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox allow-forms"></iframe>

Generally, when he speaks, I listen. His skill as a system administrator is formidable
and to say that he has helped me out from time to time would be an understatement.

So I started down the rabbit hole of doing what he suggested and installing BIND in a VM
and getting it set to use DNSRBL to perform the same kind of ad blocking Pi-hole does.

And then I realized something: This is absolutely positively the *wrong* tool for my use case.

Why? I'll answer that, but before I do, let's get down to the business of this post.

# Why *I* Homelab

Over the last few years, people interested in technology have enjoyed an incredibly bounty of
free and open source software. It's not just possible but *easy* to do things that would in
past eras have taken incredible amounts of effort and physical hardware with a few hours
of spare time, a relatively small amount of money, and maybe a smidgen of space on a desk somewhere.

There are all kinds of reasons one might wish to run various bits and bobs of infrastructure at home,
and sometimes trying to figure out which rabbit hole to go down can be dizzying and maybe even a bit
intimidating, and answering the Why question may be able to help you as it did me.

I run a bunch of my infrastructure at home myself rather than relying on cloud vendors because ultimately
I want to enhance my privacy and, more importantly to me, take control of my technology life in a day and
age when books can vanish from your Kindle in the dead of night, never to return, music you love can
sink beneath the waves when your streaming service and a record company get into a tiff, and software you
purchased with actual money can evaporate into a puff of bits because some company somewhere decided it 
wasn't profitable enough.

I'm not primarily doing it as a way to build skills for my career. I do feel like any time I flex my
technical muscle I'm improving myself career wise though.

# Why Others Might Homelab

There are all kinds of great reasons to run your own server hardware and software at home that don't 
match those I cited above. I want to cover a couple of them here.

## Building Your Systems / Network Administration Skills

Depending on what you do for work, it can be incredibly hard to constantly evolve all the skills the
job market is looking for in new hires. Whether you're currently working or looking for work, being
able to honestly claim "Oh yeah, I've done that. I set it up in my Homelab" is a fabulous answer to
have during an interview, and you can certainly add these new found skills to your resume so long as
you're VERY honest with yourself about your *actual* level of mastery. Don't fall prey to the 
[Dunning Kreuger Effect](https://en.wikipedia.org/wiki/Dunning%E2%80%93Kruger_effect)!

For example during my last job search I was finding employers REALLY wanted
Kubernetes experience, so I set up Rancher in some VMs running on one of the ProxMox servers I have here. It was great and I 
learned a tun.

This is where -dsr-'s toot above really comes in. He's absolutely right, setting up BIND instead of
a Pi-hole is most decidedly *not* hard for anyone with a reasonable degree of comfort with UNIX
systems and infrastructure, and you win familiarity with one of the most important pieces of 
infrastructure software in the world - bind.

## The Chance To Experiment With Zero Consequences

I don't know about you, but after 30 years working in the technology sector, I've lost count of the
number of times I was asked to build some really *truly* complex piece of software or infrastructure,
live, without a net. No test environments, no dry runs.

You'd better be good at running downhill while juggling chainsaws, because that's what you'll be asked
to do. Over and over and *OVER*.

With a homelab, you can play, blow stuff up, shrug your shoulders and enjoy the satisfaction of knowing
that you learned something from your failure and will know what to do next time.

This is what life as a technology professional *should* be like everywhere, but
all too frequently isn't.

# Why I Ultimately Chose Pi-hole

The answer is very simple: My lovely wife :)

In order to be an effective solution for us, she needs to be able to control the ad blocker we use.

The most critical thing is that she herself be able to add exceptions to the block list. With Pi-hole,
that's as easy as surfing to the web address of Pi-hole's admin and entering a value.

There is absolutely positively *zero* chance of her learning a UNIX editor, much less BIND's configuration file format.

It's not that she couldn't do it if she wanted to, but she REALLY doesn't want to! Computers are appliances to her.

So, for my purposes, any desire to hone my sysadmin skills is irrelevant, at least for the purposes of this particular
decision.


So, why do *you* homelab?
