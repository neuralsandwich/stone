
{% for post in posts %}
    <ul>
        <li><a href="{{ post.href }}">{{ post.title }}</a></li>
    </ul>
{% endfor %}
