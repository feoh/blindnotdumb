I love you Pelican, but I'm struggling.
#######################################
:date: 2017-01-23 00:00
:author: cpatti
:tags: blogging, infrastructure, pelican, publishing, wordpress
:slug: i-love-you-pelican-but-im-struggling
:status: published

Happy 2017 all!

| A little over two years ago, the Wordpress instance I had been "maintaining" to run my blog was hacked by a bunch
| of script kiddies.

| Not like I'm excusing them or anything, hacking someone's hobby domain feels rather like walking into someone's
| yard and, if you'll forgive me for being crass for a moment, smashing the garden statues and relieving yourself
| in the pool, just because you can. However, I was doing a really crappy job of securing my site.

| I had set it up several years before on a Linode. I wasn't a "Devops" professional at that point, so I really
| had no idea what I was doing, and I made every mistake in the book.2017

| Static blogging was becoming all the rage, and my Podcast.\ **init** co-host was using
| `Pelican <https://blog.getpelican.com/>`__ so that seemed like a good choice. It was very straight forward to set
| up, and I could run it on a much simpler set of infrastructure. No database, no complex interactions between
| web server and interpreter, just a simple instance running a webserver. That's all. Super easy to lock down.

| Being the major nerd that I am, I did automate the whole thing using Chef. You can find the recipes
| `on my github <https://github.com/feoh/pelican_blog>`__. I even had it set up so that chef would handle updating
| the site when I checked a new post into git.

And, from an infrastructure perspective, it runs like clockwork.

| More recently, i was able to even eliminate the instance and just serve my blog from
| `Amazon S3 <https://aws.amazon.com/s3/>`__.

| But there's more to any system than the infrastructure that runs it. It has to be usable in a way that fits the
| needs and workflow of its users.

Through no fault of its own, I am beginning to wonder if Pelican doesn't fit my needs.

It's a fantastic package for all the reasons I outlined above, but I'm just not posting like I used to. Why?

| When I thought about it, I realized that I used to do a ton of blogging in the "in between times". On the go, on
| vacation, or in bed at night while my wife read. Wordpress has some superlative tools for this. It has a really
| nice web based authoring interface, complete with draft capabilities, rich markup, and the ability to effortlessly
| integrate images and other media into my posts.

| I've tried doing this with Pelican. either using `Editorial <http://omz-software.com/editorial/>`__ - the incredie
| programmable editor for IOS (You can write Python scripts to do text processing in IOS from your editor, how
| cool is that? :) or using Panic's outstanding `Prompt <https://www.panic.com/prompt/>`__ SSH client to connect to my
| cloud based development box and do the editing and publishing from there.

And, it works. I have successfully done it. But I certainly wouldn't call it convenient.

| So, I'm looking into other options. At this point, I'm wondering if I've learned all I can from running my own
| blog, and if maybe I mightn't be better served moving to one of the hosted services like
| `Wordpress.com <https://wordpress.com/>`__.

| I'm certainly open to other ideas though, I do enjoy the simplicity of static blogging, but making it harder than
| it needs to be feels like shooting myself in the foot.

Does anyone have any thoughts or ideas? I'd love to hear from you if you do.
