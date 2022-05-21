<!--
.. title: Mis-Adventures In GatsbyJS
.. slug: mis-adventures-in-gatsbyjs
.. date: 2022-05-20 16:14:19 UTC-04:00
.. tags: JavaScript, development,framework,programming
.. category: geekery
.. link: 
.. description: 
.. preview: /images/Octopus.jpg
.. type: text
-->

![Key West Octopus by oe Parks is licensed under CC BY-NC 2.0](/images/Octopus-smol.jpeg)


Over the last few years I've been feeling like living exclusively in my Python programming happy place is something I can't afford to do.

<!-- TEASER_END -->

### Setting The Scene

It's almost impossible to ignore the rise of JavaScript in our industry. What started out as an extension project for Mozilla has grown into an ecosystem with more tentacles
than an H.P. Lovecraft novel.

So while there are aspects of the language that I find very uncomfortable to work with and that seem to be a bad fit for my brain, I feel compelled to give JavaScript a fair
shake and make a point of using it "in anger" in an actual project that I can ultimately get something out of beyond just learning and keep using and maintaining over time.

For the last few years I've been running my blog on [Pelican](https://blog.getpelican.com/) a beautiful Python based static site generator which has one of the most elegant and
easy to understand and modify code bases of any open source project I've ever used.

However, Pelican's minimalist DIY spirit was forcing me to come to terms with an ugly reality I was loathe to admit: I know absolutely nothing about modern web development!

Sure, I've been able to cobble together simple HTML pages for years. Nothing difficult or involved there, but there is a very long way between being able to add some HTML tags to a
text file and producing a website that people will actually want to visit in 2022.

O.K. This smells like an opportunity to lean into the discomfort and grow some new skills so I can hang out a shingle worthy of my brand in full tilt 2022 adaptive web style.

### Enter The Great Gatsby(JS)

On the face of it, there's a lot to like about [GatsbyJS](https://www.gatsbyjs.com/). Here are a few things I found particularly attractive going in:

* Layout will adaptively resize itself depending on the format and characteristics of the viewer's browser
* Sites written with GatsbyJS degrade gracefully and work fine even when people have JS turned off
* Site components communicate using an GraphQL back-end

So, I dove in head first and started working through the tutorial which, helpfully enough, shows the developer how to build a rather nice, feature-ful blog complete with
rich tags support and an elegant navigation system.

And I've gotta say, the tutorial was a *really* good experience! Want to build an index page? Great! Write some JSX that queries the GraphQL back-end using a fairly elegant
syntax that embeds the query right into the page. The query returns your post list which your page then renders. Hey this is pretty cool!

Here's what that first page looks like so you can get the flavor:

```
import * as React from 'react'
import { Link, useStaticQuery, graphql } from 'gatsby'
import {
  container,
  heading,
  navLinks,
  navLinkItem,
  navLinkText
} from './layout.module.css'

const Layout = ({ pageTitle, children }) => {
  const data = useStaticQuery(graphql`
    query {
      site {
        siteMetadata {
          title
        }
      }
    }
  `)

  return (
    <div className={container}>
      <title>{pageTitle} | {data.site.siteMetadata.title}</title>
      <header>{data.site.siteMetadata.title}</header>
      <nav>
        <ul className={navLinks}>
          <li className={navLinkItem}>
            <Link to="/" className={navLinkText}>
              Home
            </Link>
          </li>
          <li className={navLinkItem}>
            <Link to="/about" className={navLinkText}>
              About
            </Link>
          </li>
        </ul>
      </nav>
      <main>
        <h1 className={heading}>{pageTitle}</h1>
        {children}
      </main>
    </div>
  )
}

export default Layout
```

A couple of weeks of evening spare time (probably a couple of days of wall-clock time - bear in mind I'm teaching myself JavaScript as I do this) - I finished the tutorial
and deployed my new blog. I was elated! Mission accomplished!

### The Plot Thickens

The next day, after I'd triumphantly posted the URL for my shiny new redone blog to social media, the first fly appeared in the GatsbyJS soup manifested.

A friend rather understandably said "Hey, I use an RSS reader to keep up with blogs. You used to have an RSS feed. What's the URL for the new site?"

Uh. Woops. Truth be told I hadn't even thought about that, and the tutorial doesn't mention it. That's pretty understandable too, right? You don't want to
overwhelm people who are trying to adopt your technology with a firehose of details to master when they're just starting out.

OK. Let's bring up GatsbyJS's (up to this point) excellent documentation and see how we add an RSS feed...

### The Abstractions Begin To Crumble

Right then. I find a page describing how to add an RSS feed to your blog, Just add this handy dandy plugin to your site. This will let you do a similar GraphQL query to
the one you used for your post list, only this time you'll be generating your RSS feed. Here we go!

Add the plugin and BOOM! My site build fails with an utterly inscrutable Webpack error. Why? Ah the plugin was for a prior version of GatsbyJS and isn't compatible with
the one you used to build your site. OK, let's just use that older version of GatsbyJS instead!

Well crud. Turns out that the tutorial was written using [MDX](https://mdxjs.com/), a JSX flavored version of the popular Markdown mark-up language for React JSX pages, and 
the plugin used to provide MDX support both doesn't work with the RSS feed plugin *and* doesn't run in the prior version of GatsbyJS.

I said I wanted to learn. Let's roll up our sleeves and see about porting that plugin to the new GatsbyJS version.

Three agonizing weeks of pointless struggle later...

### The Knee Bone DOESN'T Connect To The Shin Bone

One of the things that drew me to GatsbyJS to begin with was this beautiful abstraction: pages, plugins, and components all seamlessly interpolating with a GraphQL back end.

And it *does* work that way to an extent. All the plugins do indeed communicate with the rest of your system using GraphQL queries, but because the plugin architecture
doesn't seem to enforce any interoperability rules, and also because successive GatsbyJS versions introduce radical breaking changes to the plugin API, you end up with
a programmer who was sold a glorious GraphQL future but winds up holding a rather large bucket of bolts that refuse to work together to build a meaningful whole.

### To Be Fair

I realize I'm painting a rather unappealing picture of GatsbyJS here, so I just want to say that it became a rather popular JavaScript framework a year or so back with
good reason. There are many *many* competent programmers out there deploying beautiful sites that scale using these tools.

I also recognize that building abstractions that don't leak and that seamlessly work well together is incredibly challenging. I just feel that ultimately GatsbyJS
isn't the tool for me and also that perhaps sme of the marketing should be adjusted to reflect reality on the ground.

It also needs to be said that GatsbyJS is 100% FLOSS, and as such is a gift freely given by its implementors which I very much appreciate. None of what I write here changes
that in any way.

I should also say that my inability to build with it is as much due to my own lack of JavaScript acumen as it is with the tool itself. 

These are just my opinions and personal experiences and thus should be taken with a grain (or perhaps a shaker) of salt, especially if you're a seasoned 
JavaScript developer.

### The Happy Ending (But Not With GatsbyJS!)

Ultimately, I decided that the best thing I could possibly do for myself with this blog project was to go with what I know, so I chose [Nikola](https://getnikola.com) - a
superlative Python powered static site generator, and I'm just delighted with that choice.

I'm still planning on finding something to use JavaScript for, it's just not going to be this particular task :)

