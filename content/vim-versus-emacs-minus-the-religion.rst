Vim Versus Emacs - Minus the Religion
#####################################
:date: 2015-07-15 00:00
:author: cpatti
:category: Geekery
:tags: editors, emacs, programming, technology, text, vim
:slug: vim-versus-emacs-minus-the-religion
:status: published

Vim Versus Emacs - Minus the Religion
=====================================

**[Note: I originally wrote this for**\ `Quora <http://www.quora.com/Text-Editors/Which-is-better-Vim-or-Emacs-Why/answer/Christopher-Patti>`__\ **but am reposting it here with slight embelishment.**

Introduction
------------

| In hard core technical circles, discussing the relative merits of
| these two editors is pretty much verboten. In the past, debates around
| this issue have actually become vicious (which is ludicrous when you
| think about it) and raged on for literally years. Devotees on either
| side would rarely listen to reason, and mostly everyone seemed to
| think it was an either/or situation. To be honest, I think that stance
| is utter rubbish.

| I feel as if I'm uniquely placed to answer this one because I've been
| using both for about 25 years now. (15 with almost full time Vim and
| 10 emacs).

| First off, I want to slightly challenge your question. It's too
| simplistic and there can be no answer to it the way you asked it.
| Emacs and vi are both superlative editors for certain types of
| things - their strengths give them super powers in very different ways
| that lend them to solving some problems more easily than others.

Vi/Vim
~~~~~~

| To my mind, if your goal is simply to edit text, Vim might be better
| suited to the task. Its modal editing lends itself to lightning fast
| text entry, and there is a nearly infinite potential growth curve for
| how its various commands and shortcuts can be efficiently brought to
| bear in navigating and moving text around.

| Through the years, various extension technologies have been added to
| Vi (a-la Vim) that enable it to be extended in various ways, but in my
| personal hard wrought experience, there are limits as to how far you
| can push that extension before the both the editing paradigm and the
| mechanics begin to creak and groan under the weight of what you're
| trying to accomplish.

| For instance, the straw that broke the camel's back for me was trying
| to get IDE like method and member auto-completion and refactoring into
| the editor. There are various solutions for this in Vim, but they
| either just plain didn't work, or if they did de-stabilized my Vim
| installation because they required the installation of C shared
| libraries that were a pain to build and install. There's nothing quite
| like having your editor dump core in the middle of a critical editing
| session to make you reconsider your choice of tools.

| Note that the above scenario has virtually nothing to do, strictly
| speaking, with editing text. It's the result of trying to make Vim
| into an IDE, which it isn't.

| As others have mentioned Vi/Vim also has the advantage of ubiquity.
| It's bundled by default on just about every UNIX system on the planet,
| and that's definitely worth noting.

| A great resource for Vim users is `Vimcasts <http://www.vimcasts.com>`__
| and Drew Neil's excellent book `Practical Vim <https://pragprog.com/book/dnvim/practical-vim>`__.

Emacs
~~~~~

| I personally think of emacs less as a text editor and more as an
| incredibly powerful programming environment hyper optimized for
| working with text - the upshot being that it also has very capable
| text editing features.

| I know that sounds like I'm just playing with words but trust me I'm
| not. If you want to create the most incredibly powerful programming
| environment utterly customized to your every need, then Emacs is
| undoubtedly for you.

| It excels at subprocess control, so for instance if you're programming
| in Python, emacs will run a Python interpreter for you inside the
| editor. Why would you want this you might ask? Because then you can,
| while you're coding, try bits and bobs of code out and actually run it
| and see how it works. Emacs can even run the Python interpreter on a
| remote machine and hook it into your editing session.

| At the core of emacs is emacs lisp - elisp is at the heart of emacs's
| superpowers. It is the ONLY extension language available in emacs,
| but it can do just about anything. You can avoid learning elisp and
| still be very productive using emacs, but chances are if you're like
| most people you will get sucked in eventually as the lure of sanding
| the rough edges off of some mode or other becomes too great :)

| You can, if you so choose, use emacs as your entire working
| environment - edit, code, chat, manipulate source control (like Git) -
| pretty much anything.

| This is a common attack non emacs users make "It's not an editor. It's
| an operating system!" and I say they're right, but they're also
| missing the point :)

| Excellent starter resources for Emacs users are - `Pragmatic Emacs <http://pragmaticemacs.com/>`__ and
| the book / website (both stellar) `Mastering Emacs <https://www.masteringemacs.org/>`__.

Summary
-------

| I realize this is a long answer, but the question is nuanced and
| complex so hopefully the length is merited.

| If you are mostly editing plain old text, or doing very light coding
| or maybe editing static configurations, or if you need your editor
| to be there by default everywhere you go in UNIX-land, then Vim is
| almost undoubtedly your best bet.

| If your needs are more complex, and you find yourself pushing the
| envelope, asking IDE like things of your editor, or if you know off
| the bat that you're a hard core developer who dreams in code and
| demands the utmost in customization capabilities from your
| environment, then skip right to emacs.

| Ultimately, ignore all the rhetoric and religion and figure out which
| will make you more productive - or do what I do and use them both! I
| use vi for super quick edits on servers and emacs for heavier editing
| or when I'm editing on my desktop / laptop.

Tools are just tools, use what makes sense.

[ **Update 07/16/2015: My astute readers reminded me of**\ `evil-mode <http://www.emacswiki.org/emacs/Evil>`__\ **
which can be seen as letting you have your cake and eat it too :) It provides startlingly complete vim compatibility inside emacs. It works great, I used it initially when I was making the transition from vi to emacs and can recommend it heartily.** ]
