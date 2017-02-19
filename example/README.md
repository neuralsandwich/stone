page_title: stone README
template: base.html

# stone
Static website generator for half.systems

#Usage
You may define site structures within the **site.json** file. The file should contain an object that holds a list
of site definitions in the following format:

```json
    {"sites": [
      {
        "root": "root folder of current project",
        "pages": [
            {
                "source": "source markdown file",
                "target": "target html output location"
            }
        ],
        "templates": [
            "folders under the site root that contain jinja2 format template files"
        ]
      },
      ...
]}
```
## Folder Structure

Site projects should be structured as follows:
- root [project named]
    - site.json
    - templates
        - template html files
    - structured folders holding page markdown
    
## Pages
The source markdown files should consist of simple markdown with a YAML header that describe the attributes of the generated page
including the page title and the template it uses. For example:

```
page_title: TEST
template: base.html

# This is some content
```
## Templates
Templates are **jinja2**, for rendering the markdown source they should contain a content tag like:

```{{ content|safe }}```

They should also contain a title tag like:

```<title>{{ page_title }}</title>```

within the HTML head.

## Generating
To generate a particular site invoke stone.py with the location of the project's root folder. 

```python stone.py root_folder```

### Example
An example project that generates an html version of this README can be found in the example folder.

You can build it by running:

```python stone.py example```