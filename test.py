from jinja2 import Environment, DictLoader, select_autoescape

templateDict = {
        "header.html": "<nav><a href=#>Home</a>",
        "blog_post.html": "{% include 'header.html' %}\nBlog Post"
        }

env = Environment(
        loader=DictLoader(templateDict),
        autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('blog_post.html')
print(template.render())
