# Stone

Yet another static website generator.

Used by (www|blog).half.systems


# Installation


    pip install stone-site


# Usage

To get started with `stone`:

    # Create template layout
    stone example_site init --site-name 'example.com'
    # Generate site
    stone example_site generate
    # Add a new page
    stone example_site newpage --name "About Us"


## Folder Structure

Stone is designed to generate the subdomains of half.systems. The following is
the layout of the sites:


    .
    ├── blog
    │   └── ...
    ├── main
    │   └── ...
    ├── site.json
    └── templates
        └── ...


[`site.json` is very flexiable](docs/site-json.md) about the location of
templates and files. As such your not constrained to any particular layout for
your site. You could have separate template folders inside each site or have
one giant mess in your project root.


## Pages

Pages are Markdown files with some optional YAML metadata
that describe the attributes of the generated page including the page title and
the template it uses. For example:


```
---
template: base.html
title: Hello, World

# This is a header

Here is some lovely content.
```

Stone makes all metadata available to page templates. Any data templates may use
can be embedded into a page. For exampled the data, an authors name and email,
etc.


## Templates

Templates are HTML pages with **[jinja2](http://jinja.pocoo.org)** markup.

`base.html`:

    <html>
      <head>
        {% block head %}
        <title>{{ title }}</title>
        {% endblock %}
      <head>
      <body>
      {% block body %}
        <h1>{{ title }}</title>
        <div id="post">
          <!-- Most likely we are going to pass more html here --->
          {{ content|safe }}
        </div>
      {% endblock %}
      </body>
    </html>


## Generating

To generate a particular site invoke `stone` with the location of the project's
root folder.

```
stone root_folder generate
```

### Example

An example project that generates an html version of this README can be found in
the example folder.

You can build it by running:

```
stone example generate
```
