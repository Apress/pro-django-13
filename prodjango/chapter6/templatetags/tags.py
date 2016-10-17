from django.template import Library
from django.template import Node

register = Library()


class FirstNode(Node):
    def __init__(self, var, count):
        self.var = var
        self.count = count
    
    def render(self, context):
        value = var.resolve(context)
        return value[:self.count]


@register.tag
def first(parser, token):
    var, count = token.split_contents()[1:]
    return FirstNode(Variable(var), int(count))
