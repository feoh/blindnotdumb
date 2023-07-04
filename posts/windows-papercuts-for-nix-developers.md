<!--
.. title: Windows Papercuts for *NIX Developers
.. slug: windows-papercuts-for-nix-developers
.. date: 2023-07-04 13:42:31 UTC-04:00
.. tags: Windows, python, neovim, compiler, powershell
.. category: geekery
.. link: 
.. description: Every Platform or Operating System Has Paper Cuts
.. type: text
-->

## Introduction

If you're used to developing on *NIX systems, coming to Windows can be a bit of
a shock.

My goal in writing this article is to point out some of the pain points and,
where I know they exist, some work-arounds.

Note that I'm talking about *native* Windows here. If WSL meets your needs and
your environment allows it (not everyone's does. Many IT orgs turn it off) then
bully for you but this article isn't about that :) I think WSL is both an
incredible tool for developers and an awesome feat of engineering. I wish more
Linux folks appreciated this. Anyway :)

So let's get started!

## The Paper Cuts

### The C Compiler

For most of us, having a standard raft of development tools on hand is par for
the course. We just expect gcc and make to be there at our beck and call, and
the fact that they're not can cause some tools to fail spectacularly.

For instance, whenever I start my editor of choice (Neovim) I'm greeted with:

![Neovim C Compiler Error on Windows](/images/windows_nvim_c_boom.png)

Having spoken to some experts, apparently it's considered *really* bad form to
leave your C compiler on the PATH on Windows. I suspect this is because malware
on Windows is such an incredibly pervasive problem.

I get that, but then we should probably either modify our tool-chains to not
expect that as a default or maybe create documentation to help people understand
the happy path.

As near as I can tell, the 'standard' set of c/c++ tools on Windows is Microsoft
Visual Studio. The free "Community" version works just fine though the installer
is a bit of a jank-fest.

That thing provides a prompt shortcut called "Powershell for VS XXXX" and you
can use that to get a shell that has the usual build tools available.

Not a great solution though, since the experts say not to run that way as a
default, but having your editor blow up on start just-up isn't a great feel.

### The Shell

While you certainly *can* run tools like bash or zsh on Windows, unless you
*really* know what you're doing, this is not the happy path. You're in Rome. Do
what the Romans do and you won't regret it :)

The good news here is that the native tools are now really quite good. Gone are
the days when CMD.EXE was your only choice. You now have Powershell and it's
really quite awesome.

Here are a couple of tips to make your Powershell experience awesome and help
you appreciate what this environment has to offer.

#### Oh My Posh

This one's gotten a lot of press and let me tell you it's incredibly well
deserved. It's like the oh my zsh of Windows shell prompts :)

Mine shows me git status and whether my last command's exit code indicates
success or failure, as well as what Git branch I'm on. Here's what it looks
like:

![What My Oh My Posh Prompt Looks Like](/images/OhMyPoshScreenshot.png)

I wrote some about Oh My Posh in my [previous article on Windows for Python
Developers](https://www.feoh.org/posts/getting_started_with_python_on_windows_2021_edition_push_the_easy_button.html).

#### PSFzf

One of the biggest productivity boost for me in recent memory was when I
integrated [fzf](https://github.com/junegunn/fzf) the fuzzy finder into my
workflow.

With a single keystroke I can find any file or directory on my system.
Navigation becomes effortless and the endless sequence of `cd` and `pwd` commands
melt away in a burst of productivity goodness :)

Thankfully, Powershell offers all these benefits as well via
[PSFzf](https://github.com/kelleyma49/PSFzf).

Here's what it looks like. In this case I wanted to edit my Neovim main
configuration file `init.lua`:

![Edit my init.lua file](/images/psfzf.png)

### The Console / Terminal

For long time *NIX users, one of the biggest bones of contention for a
long time was the Windows console. To put it kindly, it was god awful, mostly
because it maintained compatibility with the Antideluvian DOS console.

Happily, we now have a fairly decent solution [Windows
Terminal](https://github.com/microsoft/terminal). I say fairly decent because
it's still not quite up to par with your favorite *NIX terminal, but the fine
folks behind this open source project are working *really* hard to change that,
and the progress they've made here has been nothing short of miraculous. Mad
props to these folks for fixing by far the biggest deal breaker for many around
working in Windows!

They've even recently added an easier UI for editing settings, but you can also
still go edit the JSON yourself if that's your jam :)

It's not perfect, but this is an incredibly flexible tool with a ton of depth
and it's been exciting to watch it evolve.

### The Windows Desktop/GUI

I'm sure there will be folks who aren't happy with this one but my take? Just
ignore it.

Windows is pretty good about making EVERYTHING accessible from the keyboard, and
many things are also accessible from the command line. If you just avoid
graphical interfaces wherever possible, and if you're anything like me, you'll
see your productivity levels soar and your frustration levels plummet.

### Where Do I Put?

One of the things I continue to struggle with is the simple expedient of "Where
do I PUT things?". On UNIX based systems, pretty much everything user or
configuration related lives in $HOME. Not so on Windows.

As just an example, my Neovim configuration lives in something like
`$HOME\AppData\Local\nvim.`

In some respects, I get it. Keeping application configuration separate is a good
thing, but navigating where to put what can feel like a bit of a morass for the
uninitiated.

Maybe once I get a better understanding of the lay of the land, I can create a
cheat sheet for UNIX users.

## Fin

That's all I have for now, but I may update this post as time permits or if
various situations I detail here improve. Thanks for reading!
