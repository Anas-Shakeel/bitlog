from django import template
import re

register = template.Library()


@register.filter
def highlight(text, query):
    """Highlight text, where query found.

    #### USAGE:
    ```
    {{ post.title|highlight:query|safe }}
    ```
    """
    if not query:
        return text

    keywords = query.split()
    for word in keywords:
        text = re.sub(
            rf"({re.escape(word)})", r"<mark>\1</mark>", text, flags=re.IGNORECASE
        )

    return text
