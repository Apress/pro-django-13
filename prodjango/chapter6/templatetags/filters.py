from django.template import Library
from django.template.defaultfilters import stringfilter

register = Library()


@register.filter
@stringfilter
def first(value, count=1):
    """
    Returns the first portion of a string, according to the count provided.
    """
    return value[:count]
