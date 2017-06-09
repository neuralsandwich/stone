# stone

Yet another static website generator.

Used by half.systems


# Installation


    pip install stone-site


# Usage

To get started with `stone`:

    # Create template layout
    stone example_site init --site-name 'example.com'
    # Generate site
    stone example_site generate


## Folder Structure

Site projects can be structured as you wish.

The layout which stone was developed along side is:

* root
  * blog
  * main
  * templates
    * templated HTML for blog and main
  * site.json

As `site.json` is explicit about the location of templates and files, the
structure is flexible. You could locate separate template folder inside each
site or have one giant mess in your project root.


## Pages

The source markdown files should consist of simple markdown with a YAML header
that describe the attributes of the generated page including the page title and
the template it uses. For example:


```
template: base.html
title: TEST

# This is a header

Here is so lovely content.
```

There are additional attributes:

* date - Adds the date the page was create to the page metadata. This is
  currently used when generating indexes for blogs. Format YYYY-MM-DD


## Templates

Templates support **jinja2**, an example:

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

To generate a particular site invoke `stone` with the location of the
project's root folder.

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
