<!--
.. title: Git Submodules are awful but occasionally necessary.
.. slug: git-submodules-are-awful-but-occasionally-necessary
.. date: 2024-01-09 23:09:31 UTC-05:00
.. tags: git,scm,version,control,submodules,vcs,bestpractices,subtree
.. previewimage: /images/YoDawgDotFiles.jpg
.. category: 
.. link: 
.. description: 
.. type: text
-->

![Yo Dawg I Hear You Like Dotfiles In Your Dotfiles](/images/YoDawgDotFiles.jpg)

# Intro
One of the beautiful things about powerful tools is that they enable you to do
easy things easily but also more complicated things as well.

Git is the perfect example of this. It represents an incredible amount of
innovation in mainstream widely adopted version control systems, but it has some
of the worst UX of any software I've ever used, and that includes Nortel switch
administration consoles where all input was in the form of numeric codes :)

# Git Submodules
Git submodules are a fractal of bad UX, which is almost assuredly why they
generate such incredibly strong feelings among the Git using community. Mention
that you use submodules in various technical communities chat rooms and you
might as well have lobbed a hand grenade into their midst without having had the
decency to shout "FIRE IN THE HOLE!" first.

However, I encountered a very particular use case that to mind virtually
necessitated their use. I would welcome any alternatives people may come up with
other than "Don't do that".

Let me explain.

# The Plot Thickens
I manage my dot files using Github, and in particular I utilize a variation on
the method laid out
[here](https://www.ackama.com/what-we-think/the-best-way-to-store-your-dotfiles-a-bare-git-repository-explained/).

You can read the article for details, but the upshot is that my home directory
actually contains a [Git repository](https://github.com/feoh/git_dotfiles) that houses my dot files, so I can revise
them to my heart's content and enjoy all the benefits that managing source code
in Github brings to the table.

Now, here's where the need for submodules comes in.

I co-maintain a moderately popular Neovim project called
[kickstart.nvim](https://github.com/nvim-lua/kickstart.nvim). As such I need to
be able to check out the latest revisions and test them on my own system to see
how they integrate with my own customizations.

Given that, being able to simply `git pull` the latest is critical.

So we have a "Yo dawg, I hear you like dotfiles in your dotfiles!" situation
here. Git submodules to the rescue!

I won't go into the details around adding a submodule to your existing project,
that's covered elsewhere in way more detail than I have time for here, but you
can see the net result in the repo I linked above.

I have kickstart.nvim checked out as a submodule of my main git dotfiles
project, so I can always pull down the latest changes from the master repository
into my own personalized fork for testing.

# Traps for the Unwary
As I mention above, Git submodules represent a loaded footgun and they are
*extremely* easy to mis-use to the point where you wind up with a tangle of
wires shooting sparks in your git workspace trapped in an unendingly frustrating
purgatory of bad error messages, unclear working states and an utterly obtuse
route back to the "happy path".

How do I avoid this? I Keep It Simple, Stupid :)

# Simple Rules For My Simple Mind - Using Submodules Sanely
I follow a few simple rules that keep things understandable. The key is not
trying to do too much.

## Avoid them wherever possible
Seriously, unless you have a use case like mine, they *are* a faff. You're
better off avoiding them if you can, but if you can't or can't see a way to
avoid them, then read on!

## Treat your checked out submodules as read-only.
Make any changes in a separate workspace for that project where you can branch,
fork and modify to your heart's content.

It's really tempting to just ignore this rule and make changes in your
submodule. I can just HEAR you saying "But Chris, it's git. It SHOULD work!" and
the truth is - *in a perfect world, it does!*. But you and I both know the world
we live in is far from perfect, and if humans can be counted on for anything
it's an utter lack of consistency and discipline when the chips are down and
time is of the essence.

So save yourself the heartache, make your changes elsewhere, and then simply
run:

`git submodule update --remote` potentially adding --force if things don't seem
to be updating properly.

## Don't be afraid to nuke and pave!
Assuming you're following my rule above, you can always simply nuke your
submodule and start over. Remember if you go this route that you'll likely need
to delete the .gitmodules directory in your project as they contain important
state for your submodules.

Seriously, this can be a *huge* win when you find yourself thinking "OK what the
blue blazes is *going on*?" and chances are good that if you choose to use
submodules, this day *will* come!

# Unless you know better...

As I've mentioned several times, submodules are indeed a pain, but for my needs
as outlined here I can't think of a better way to implement this. Do you know of
one? Have you found a minimal faff way to implement this without manually
copying new revisions from one Github project into another?

If you do, I'm all ears! You can reach me on the Fediverse - 
@feoh@oldbytes.space or via email - feoh at feoh dot org. Or leave a comment
here if that works for you. In any case I look forward to hearing from you, even
if you think I'm full of malarkey :)

# Update: Someone knew better! Git subtree!

If you're a technical person in 2024 and you're not on the Fediverse, you're
missing out. It doesn't have the dank memes and crap posting Twitter does, but
some of us consider that a feature :)

When I wrote this post, I sent a copy there and asked "Does anyone know
better?". Thankfully I received an incredibly helpful
[response](https://cybersecurity.theater/@varx/111731694640751156).

It turns out there's a much better alternative to git submodules, and they're
called Git subtrees. They're awesome :)

You can find all about them
[here](https://www.atlassian.com/git/tutorials/git-subtree). Once you set a
subtree up, it checks out automatically with the rest of your repository.

I'm delighted thus far!
