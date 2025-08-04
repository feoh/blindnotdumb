<!--
.. title: NiceGUI: Awesome Python Dynamic Websites For The Web Dev Impaired!
.. slug: nicegui-awesome-dynamic-websites-for-people-who-write-ugly-html
.. date: 2025-08-03 20:11:54 UTC-04:00
.. tags: python, web, website, dynamic, ui
.. category: 
.. link: 
.. description: 
.. type: text
-->

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
