from django import template
from markdown import markdown

register = template.Library()


@register.filter
def markdownify(value):
    """Convert markdown to HTML"""
    return markdown(value, extensions=["tables", "toc"])
