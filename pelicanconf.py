#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Chris Patti'
SITENAME = 'Blind Not Dumb'
SITEURL = 'https://www.feoh.org'


PATH = 'content'

TIMEZONE = 'America/New_York'

DEFAULT_LANG = 'en'

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

# Set newly pushed posts as draft.
#DEFAULT_METADATA = {
#    'status': 'draft',
#}

DISQUS_SITENAME='blindnotdumb'

# Blogroll
LINKS = (('Podcast.__init__', 'http://www.podcastinit.com/'),
         ('Empiricism Ops', 'https://danslimmon.wordpress.com/'),
         ('AJS Essays', 'http://essays.ajs.com/'),)

# Social widget
SOCIAL = (('Me @ Everywhere :)', 'http://about.me/feoh'),)


# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

# Yay typography enhancements. Requires the python Typography module be installed.
TYPOGRIFY = True


TWITTER_ADDRESS='feoh'
EMAIL_ADDRESS='feoh@feoh.org'
