from django.template import Library

register = Library()


@register.simple_tag
def first(value, count):
    return value[:count]
