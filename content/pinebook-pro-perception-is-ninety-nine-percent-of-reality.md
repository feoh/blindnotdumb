Title: The Pinebook Pro - Perception is 99% of Reality
Date: 2020-10-28 
Category: Geekery
Status: published
Tags: hardware, software, arm, floss, laptop
Authors: Chris Patti

![Pinebook Pro Picture]({static}/images/pinebook_pro_smol.jpg)

# Intro

Since I received my Pinebook Pro a bit less than 3 months ago I've gotten a ton of
questions from interested people wondering what my impressions and experiences with
the device.

To be honest, I don't think initial impressions are all that useful, and besides, there are umpteen
"Pinebook Pro - First Impressions" blog posts and Youtube videos.

What I'd want to know if I were one of the folks asking is: Does the Pinebook Pro meet my expectations
and needs?

The answer is a qualified yes. To understand why I say it's qualified, I'll need to go into a bit more detail. Hopefully you'll find it useful.

When I did my research on the Pinebook Pro, I got the impression that it's a low power usage ARM based laptop that's light but has incredible battery life. I knew that the software support would not be nearly the same as what I'm used to on X86 based laptops, and being an old UNIX hand (I still have nightmares of my early job porting the BSD lp suite to SVR3.2 - Printer lp0 is enabled and printinginginginging...)
I figured I might even enjoy the opportunity to bring some well loved skills to bear and make some small contribution to the Linux open source community, and maybe even empower someone in a less privileged position than I to do something cool or get excited about computing and open source.

It has succeeded in those goals and expectations admirably. Thus far I've managed to get TIC-80 building and
running flawlessly, and am taking the opportunity to learn about CMake so I can contribute that fix back.

All that is indeed pretty awesome, but why am I only giving a qualified yes? Because, in essence, in my opinion anyway, the Pinebook Pro is currently not a polished commercial grade laptop. It's a really great open source project currently undergoing development. It's definitely made a TON of progress, and I am in fact using it as my daily driver laptop for personal/home use, but there are some aspects of the experienced that are still quite raw, and you should be aware of those before you buy. 

# The Dirt

I should say that I think PINE64 is an awesome company, and they've been very clear that they're making these laptops at cost as a service to the community,

So, let's get to the real-talk portion of this discussion:

* There are serious QC problems in manufacturing, and those are even worse during the pandemic.
  * My laptop and every unit in the batch I ordered from have an improperly positioned lid magnet. [the procedure](https://wiki.pine64.org/index.php?ngtitle=Pinebook_Pro_Troubleshooting_Guide#Lid_Magnet_Repositioning_Step-by-Step) for fixing this is incredibly daunting and while my wife and I attempted it (I'm partially blind and she's fully coordinated and totally non technical but super sweet!) but ultimately decided that we had exactly zero confidence that we would be able to rebuild the machine after tearing its throbbing innards out as prescribed. Humor aside, I think it's totally unreasonable for PINE64 to view this as a user serviceable repair. I'd be happy to ship my laptop back at cost and have them fix it for a fee even, but for now I'm just dealing with the malfunction, which leads me to the next bullet.
* Sleep doesn't work. At all.
  * There is apparently a serious firmware bug in the Trusted Firmware Alliance) boot loader that most PBPro distros use, so even if you do fix your lid magnet, the laptop will still drain its battery overnight if you close the lid and walk away. Not amazing.
  * Apparently if you run the older Debian OS that was initially shipped with the PBPro before they switched to Manjaro, and you have a working lid magnet, some folks say sleep works. Can't verify this, no working lid magnet :)
* The company doesn't have time/bandwidth to respond to much
  * This is understandable, and I hesitate to list it here, but you should know that buying a Pinebook Pro isn't like buying a Dell or a Lenovo. See bullet above about this being a FLOSS project in development. 
* There are multiple ways to arrive at a state when your Pinebook Pro won't boot, and you'll need more hardware to fix it.
  * So as it turns out, the Manjaro Linux shipped with the Pinebook Pro plays fast and loose with the rules around booting off an SD card. Specifically, distros booted from the SD card SHOULD NOT TOUCH the internal hard disk analog, the emcc memory chip. Manjaro does, so if you botch you could easily be in a situation like I was where you need to either:
    * Take out your emmc and re-flash it using the USB emmc adapter that PINE sells at their store or
    * Replace it with a different emmc (This is what I did. I upgraded to the 128GB version)
* Without the firmware debug cable, you can easily get into a mode where your Pinebook isn't booting and you have no way to debug it.
  * This isn't X86 where you can simply flip to a different VT and watch the boot messages go by. You'll need to buy the firmware debug cable from the PINE64 store, pry your case open, flip a switch and plug it in.
* Don't assume that if you have source, getting it to run will be a trivial lift
  * There are a surprising number of lower level dependencies that won't compile or just aren't supported on AARCH64 yet. Expect getting an unsupported piece of software to run to be a hacking project of indeterminate size.
* Don't assume that just because your favorite flavor/distro exists that it'll be at all usable or run well
  * Rolling an SD boot image for the Pinebook Pro isn't particularly hard, which means a LOT of people have tried their hand at it with mixed results. The Pinebook Pro's unique big/little ARM CPU arrangement requires some fairly specific kernel tuning to perform well, so I'd strongly recommend running one of the stock distros (Currently Debian or Manjaro) unless you're into that kind of super low level hackery :)

# The Good News (There's Plenty Of It!)

Somewhere around the moment when I couldn't get my laptop to boot at all even from SD and someone from the community told me I needed to open the case and flip a switch th disable the emmc entirely so SD boot would play nice, I had a bit of a revelation. This wasn't going to be the plug and play laptop I'd thought it would be. It's going to be something I'm going to need to hack on to get various bits to work from time to time, and you know what? When I figured that out and opened my mind to the idea I FOUND I'M ACTUALLY ENJOYING IT!

## A Different, Awesome Experience
Over the last 3 months I have learned an incredible amount about ARM System on a Chip architectures - how their firmware is laid out, how the boot process differs from X86 (TL;DR - A LOT!) and a host of other tidbits. It's not every day you get to explore an entirely new architecture, and that has been surprisingly edifying.

## Selling Points

Beyond that, as I say above, I currently use my Pinebook Pro as my daily driver at home. A few things I love about it off the top:

* The keyboard - The Pinebook Pro's keyboard is a pleasant surprise for its price point. I find it MUCH easier on my wrists and more pleasant to use, with much better tactile feedback, than the 2018 Macbook Pro work issued me.
- The screen - Its 14" display is surprisingly bright and clear with decent color reproduction and perfectly reasonable video playback.
- The battery life - Depending on what I'm doing, I can get between 8 and 12 hours out of this laptop between charges. That's HUGE! I used to long for a laptop that could just keep me going at a technical conference without needing to worry about plugging in partway through the day.
- The community - Can't say enough good things about the Pinebook Pro community. Every problem I faced I was able to get helpful advice and ultimately solutions from the Pinebook Pro Discord & Forum.

## Performance - Realistic Expectations Are Key

If you buy a Pinebook Pro expecting it to perform like your monster beast Skylake 4 core X86 CPU, you're going to be disappointed, but (and the answer may well be yes!) do you actually NEED that kind of perf for the kinds of day to day work you'll want to be doing on an ultra-portable laptop optimized for battery life?

Here are some things I run just about every day on my Pinebook Pro and find the performance to be good enough that I don't notice it getting in my way:

* Pycharm/IntelliJ IDEA
  * This one surprised me, but it turns out most Java/OpenJDK compatible apps run quite well as the OpenJDK for ARM has had a ton of optimization work put into it.
* Visual Studio Code
  * Microsoft just recently released ARM64 builds of this and they're fantastic. I'm typing this article with it now.
* Firefox / Chrome
  * Firefox is my daily driver, but I have tested Chrome and it works fine. Note that there is about a 2 second delay between clicking the icon or running the executable and Firefox coming up ready. But honestly, start it and forget it. Who cares? :)
  * I've tested it and found it to perform great with everything but the most demanding WebAssembly / media and compute heavy Javascript applications (And only some of those lag - I suspect it depends on usage patterns and APIs used)
* Older open source games and emulators
  * There are a surprising number of games that play great on the Pinebook Pro. You can find a thread with some examples [here](https://forum.pine64.org/showthread.php?tid=8665) on the forums.

## What PINE64 Should Consider Doing

Part of the overall perception problem I'm seeing is that IMO PINE64's messaging around the laptop doesn't make the performance expectations clear enough, and ESPECIALLY when they give 'freebie' laptops to members of the Linux community. I know in at least two cases I've heard Linux luminaries express disappointment at the Pinebook Pro's performance, and I suspect that part of that is an expectation setting problem.

## What Linux Community Influencers Should Do

Set expectations realistically. Don't expect this to be a drop-in for your monster Intel laptop, and recognize that it's a fundamentally different KIND of tool with very different functional goals. If you do I think you'll see there's some real value here for a lot of people, and possibly for the environmental health of the planet!
<!--  -->
# TL;DR (Too Long, DO read!)

The Pinebook Pro isn't a laptop, it's an adventure. You'll learn a ton and wind up with a tool that's incredibly versatile and useful in situations where your monster beast X86 laptop will have long since run out of gas. And on top of everything, I'd guess you're benefiting the environment by consuming a fraction of the energy your giant laptop would when you're just running a web browser or the like :)

If you go in eyes wide open and set your expectations realistically, you may end up loving this little device as much as I do mine.

And, if you do decide to buy, I have these quick tips that'll help you enjoy your purchase more and save yourself some heart-ache later:

* Buy the debug cable. It's $5. YOLO, and if you need it, you'll REALLY need it.
* Spring for the extra $50 128GB emmc. It's a trivial price increment to double your storage without all the footnotes and question marks around adding an NVME SSD (There are power drain and compatibility issues).
* Consider adding an extra set of screws for $1.00 - I guarantee you'll need to pop the case a few times, and the extras are super handy to have if you lose a screw.
* Participate in the community! Just post on the forums or come join the Discord/IRC/Matrix and hang out. It's an amazing group of folks and you'll be glad you did.

Do say hi on the forums or chat and let me know if I can answer questions or help get you started!
