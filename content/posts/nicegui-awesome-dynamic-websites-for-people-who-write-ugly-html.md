---
title: 'NiceGUI: Awesome Python Dynamic Websites For The Web Dev Impaired!'
slug: nicegui-awesome-dynamic-websites-for-people-who-write-ugly-html
date: '2025-08-03T20:11:54-04:00'
tags:
- python
- web
- website
- dynamic
- ui
---

## Confession

I have a guilty confession to make: The idea of trying to come up to speed with modern front
end web development fills me with inchoate dread.

Javascript, Typescript, React.js, advanced CSS, CORS - all of it just makes my head spin.

It's not that I don't think these are all worthy skills to have, I *do*! But the truth is I
still feel like I really want to solidify my transition from Python novice to Journeyman and
one day even with blood, sweat, tears, and a little luck ascend the lofty mountain top to
Expert!

So when the fine folks over at [Pybites](https://pybit.es/) mentioned it as a suggestion for
their "Summer of Pybites Code 2025" competition, I thought it was worth a look.

I was pleasantly surprised!

## It's Surprisingly Eaasy!
Here's how you create an input form with a prompt that lets you enter some text:

```python
  with ui.card():
        ui.input("Search for images", value="quasar").bind_value(ng, "search_text").props("outlined")
        ui.button("Search", on_click=lambda: ng.search_image_request())

    ui.run()
```

Pretty straight forward, right? The ui.card() just gives our input box a nice fancy border.

The ui.input bit is mostly self explanatory other than the .bind_value() which simply stores
the result of our input into the search_text property.

The ui.button line is what it says on the tin as well, with the addition of that lambda in
the on_click event which simply calls our search_image_request() function when we click the
Submit button.

You can see what this looks like along with the results of a search:

![An Example NiceGUI application I built showing a text
input](/images/NiceGUI_Blog_Example.png)

Needless to say, this is pretty neat! I can make very intuitive API calls to create
interactive user interface components on a dynamic web page! NiceGUI even handles creating a
server for your app, although you can deploy it other ways as well.

So until the day comes when I can devote myself to learning how to build for the modern web,
it's really "Nice" to know that there are tools out there that *are* within my reach to help
me build beautiful interactive web apps in my favorite programming language - Python!

## Potential Down Sides# Javascript All The Way Down

NiceGUI is a Python wrapper over [Quasar](https://quasar.dev) - an "Enterprise Ready"
Javascript framework written atop [Vue.js](https://vuejs.org/).

If you try to view the web pages it generates with anything other than a Javascript enabled,
modern web browser, you're out of luck. I suspect people with screen readers and the like
don't have a chance.

It's possible that Quasar implements the proper Aria roles to make the generated sites more
accessible in a modern browser, but I have no real idea honestly.

### Edge Cases Can Bite You

One of the things I really struggled with when initially trying to use NiceGUI is the fact
that if you enclose a `ui.image` inside a `ui.card` or any other container, you must either
manually style the container large enough to eocompass the image, or instead use the
`ui.interactive_image` which will apparently handle this case more smoothly.

If you don't, you'll find as I did that you get ... Nothing. Your image simply doesn't
display. This lead to a bunch of head scratching on my part, until the nice folks over at
NiceGUI pointed me in the right direction.

## Conclusion

Despite the potential issues, I think NiceGUI is a really handy tool to have in one's belt
for those moments when you just *really* need to build a quick and dirty interface for
something that renders to a web browser. The API is very approachable, and the folks behind
the project couldn't be more welcoming and helpful.

I'm very glad to have taken the time to learn NiceGUI. Give it a go and let me know what you
think!
