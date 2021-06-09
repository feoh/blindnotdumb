Windows Scripting - a VBScript Survival Guide
#############################################
:date: 2010-03-31 15:18
:author: cpatti
:category: Geekery
:tags: deployment, Installers, microsoft, powershell, scripting, systems, vbscript, visual basic, Windows
:slug: windows-scripting-a-vbscript-survival-guide
:status: published

1. Introduction
---------------

If you're new to the world of Windows scripting as I am, the array of acronyms, technologies and access methodologies that you need to traverse in order to get anything done can range from bewildering on a good day to utterly derangement inducing on a bad one.

| 
| I've been doing installer and deployment development at a Windows enterprise software company for the last year or so, and after decades spent comfortably swaddled in the familiarity of the UNIX and Java world, I definitely found myself feeling shell shocked, disoriented, and frustrated at the lack of any sort of cohesive resources to aid me in my quest.

Microsoft has been doing its best to pretend VBScript doesn't exist - touting `Windows PowerShell <https://blogs.msdn.com/PowerShell/>`__ as the way and the light.  PowerShell is indeed an awesome tool, and I for one would happily consign VBScript to the briny deeps never to be thought of again were it not for one little problem - the vast majority of Windows systems running in the wild don't have PowerShell installed.   Until a new day dawns and PowerShell is on \*every single\* Windows box our company wants to install its software on, VBScript remains the lowest common denominator for system scripting and thus the only **real** game in town for install time scripting.

The goal of this article is not to teach you VBScript, sadly, there are essentially no books and precious few online resources dedicated to this topic online.  I will offer pointers to those that I have found most useful, and some collected wisdom on how to best make use of them, as well as some pitfalls I encountered which with any luck I can help you avoid.

That said, let's get started.

2. Learning VBScript
--------------------

This will mostly be a collection of pointers to resources with a smidgen of commentary on each to get you moving in the right direction.

A. Books
~~~~~~~~

-  `Windows XP Annoyances <https://www.amazon.com/Windows-XP-Annoyances-Geeks-2nd/dp/0596008767/ref=sr_1_1?ie=UTF8&s=books&qid=1270065442&sr=8-1>`__ - This book should really be titled "Windows For Geeks" :) it is the single most useful book I have ever encountered for someone trying to make the transition from another environment and isn't content to just grit their teeth and groan at all the annoying defaults Windows ships with.  In addition to an incredible amount of depth around the Windows registry and how you can wield it to suit your needs, this book also has one of the best simple introductions to system scripting with VBScript I've seen.  Two thumbs up. Note that this is the 1997 edition, and this book now comes in Windows Vista and Windows 7 flavors which I haven't read, but can only assume are equally awesome.
-  `visualbasicscript.com <https://www.visualbasicscript.com/>`__ - This is far and away the single best VBScript resources on the intertubes.  The folks in these forums are experts, and will help you solve your problem virtually every time.  I can't say enough about the incredible community here.  Nine out of ten times, if I go looking somewhere else first I end up coming back here and wishing I hadn't wasted my time elsewhere first :)
-  `Microsoft Script Center / The Scripting Guys <https://technet.microsoft.com/en-us/scriptcenter/default.aspx>`__ - The second most useful scripting site on the web.  The Scripts Repository and "Scripting Guys" MSDN blog are an incredible resource for system scripters.  While the emphasis has definitely shifted towards PowerShell these days (and rightfully so) most of the techniques discussed can be leveraged in VBScript once you get cozy with the syntactic differences between the two (very different) languages.
-  `MSDN Windows Scripting Technologies <https://msdn.microsoft.com/en-us/library/d1et7k7c%28v=VS.85%29.aspx>`__ - This page covers things like the Windows Scripting Host, the core technology that actually allows you to perform useful work in VBScript.  While somewhat more complete than the VBScript reference itself, it's no great shakes.  You'll find yourself learning much more from examples published elsewhere, but for the occasional API lookup or clarification it can be useful.
-  `MSDN VBscript Reference <https://msdn.microsoft.com/en-us/library/t0aew7h6%28VS.85%29.aspx>`__ - You'll note this site's position well down the list.  It's there for a reason.  The documentation provided here is very sketchy and frankly incredibly misleading in places.  The authors seem to have weaseled out of writing a more complete documentation set by making a vacuous assertion along the lines of "Well, it's just like regular Visual Basic, with a few minor differences".  This leaves people like myself who have never had the need to touch a fully fledged VB implementation out in the cold, feeling like second class citizens.  While these pages can be useful for occasional clarification on some obscure language feature, those seeking to understand how the language works in the large should definitely look elsewhere.
-  `Windows Script Debugging Microsoft KB Article <https://support.microsoft.com/kb/308364>`__ - This article will get you started interactively debugging your scripts using Visual Studio.  Don't bother with the Windows Script Debugger, Visual Studio Express is free and much better :)
-  `W3Schools VBScript Tutorial/Reference <https://www.w3schools.com/vbscript/default.asp>`__ - This page is definitely rather Web-centric, focusing on VBScript in classic ASP programming, however, the core language and some of the techniques are the same.  In many cases this is a better reference than the MSDN one, and the tutorial lets you work through the examples online in a web browser which is cool.

3. Debugging
------------

Who turned the lights out?
~~~~~~~~~~~~~~~~~~~~~~~~~~

If you find that some script you've inherited is not working, but you get exactly zero output or errors, look for the telltale ``On Error Goto 0`` or ``On Error Resume Next`` statements. These basically disable VBScript's inherent error handling functionality and cause your script to silently ignore errors. Helpful, eh?

Never run while blind folded.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Know how you're invoking your VBScript. If you're calling your script from an installer or some such executable, you're likely using Microsoft's ``cscript`` tool. which doesn't do a very good job of always displaying handy things like syntax or run time errors. Try running your script with ``wscript`` instead for debugging purposes. Heretofore mysterious behavior may become clear :)

That's all!
~~~~~~~~~~~

Hopefully this post will prove useful to some poor soul, manacled in place, suffering through their own personal Windows induced hell. Even if it isn't, these tidbits have been rattling around in my head since I escaped (I now work for `Blue State Digital <https://www.bluestatedigital.com>`__, we're a LAMPs shop (Linux, Apache, MySQL, PHP) and I hope to never be trapped in Windows enterprise limbo again!
