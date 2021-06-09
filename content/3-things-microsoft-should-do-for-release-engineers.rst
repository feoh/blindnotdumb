3 Things Microsoft Should Do for Release Engineers
##################################################
:date: 2010-01-28 13:39
:author: cpatti
:category: Geekery
:tags: infrastructure, Installers, installshield, microsoft, msbuild, powershell, release, releng, scripting, tfs, Windows
:slug: 3-things-microsoft-should-do-for-release-engineers
:status: published

For the last year or so I've been working at a 100% Windows based enterprise development shop.   They ship a fairly large and complex application for health insurance providers, which draws on many of the core technologies in the Microsoft enterprise stable.

| 
| This post highlights a few things that make working in this environment a whole lot more onerous than it needs to be in my opinion, so let's get started.

1. Installers
-------------

The Windows installation landscape has been a bleak one indeed for a very long time.  Tools like Installshield with their own proprietary languages like InstallScript make installer development unnecessarily painful and baroque.  Is there **really** any reason I should be programming in a language with no real data structures to speak of in 2010?  Even flow of control is handled in a way I can only describe as baroque.  There are methods/functions, but the main body of your installer's code has to jump around everywhere using goto.  What a mess.

There is hope on this front, in the form of `WiX <https://wix.sourceforge.net/>`__, the Windows Installer XML toolkit, which allows developers to iteratively build and design their installer along with the regular development process.  Right now however the learning curve seems incredibly steep.  Perhaps Visual Studio could generate a template WiX project to get people started?

I'd also love to see some thought given to simplifying the deployment model for things like `COM+ <https://msdn.microsoft.com/en-us/library/ms685978%28VS.85%29.aspx>`__ - which feels to me like a magic black box with myriad buttons and levers, all of which are a bear to get right at install time.

2. Builds/SCM
-------------

MSBuild needs to have **dramatically** better documentation, and to a lesser extent so does TFS  - they get the broad bits right - everything you could want to do through the UI is covered, but process automation using scripting / command line tools gets substantially murkier.

In the 'credit where credit is due' department, the TFS team has been incredibly responsive on their forums, and that's what's helped us get by so far, but there's no substitute for first rate docs.

3. Infrastructure Scripting
---------------------------

As of right now, there are a thousand different interfaces to accomplish the same thing, and for complex configuration tasks like configuring IIS at install time, the possibilities can be dizzying.  I would like to see Microsoft choose **one** mechanism for run-time system/software configuration and document the heck out of it.

Kudos to the `PowerShell <https://blogs.msdn.com/powershell/>`__ team and `The Scripting Guys <https://technet.microsoft.com/en-us/scriptcenter/dd901334.aspx>`__ for making great strides in this area.  PowerShell is a really nice environment for all kinds of scripting, and I look forward to the day when we can eliminate VBScript from our installers entirely in its favor, but we're not there yet sadly.  The object pipeline is one of the more powerful concepts in the modern scripting milieu, and I think Apple and the UNIX world could take a page from PowerShell's book in this regard.

Being a release engineer in a Windows world presents some very interesting and different challenges for someone coming from a UNIX background like myself, and with a little bit of emphasis and effort on Microsoft's part, surmounting them could be a whole lot less painful.
