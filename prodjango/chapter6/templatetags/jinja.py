import jinja2
from django import template

register = template.Library()


def string_from_token(token):
    """
    Converts a lexer token back into a string for use with Jinja.
    """
    if token.token_type == template.TOKEN_TEXT:
        return token.contents

    elif token.token_type == template.TOKEN_VAR:
        return '%s %s %s' % (
            template.VARIABLE_TAG_START,
            token.contents,
            template.VARIABLE_TAG_END,
        )

    elif token.token_type == template.TOKEN_BLOCK:
        return '%s %s %s' % (
            template.BLOCK_TAG_START,
            token.contents,
            template.BLOCK_TAG_END,
        )

    elif token.token_type == template.TOKEN_COMMENT:
        return u'' # Django doesn't store the content of comments


@register.tag
def jinja(parser, token):
    """
    Define a block that gets rendered by Jinja, rather than Django's templates.
    """
    bits = token.contents.split()
    if len(bits) != 1:
        raise TemplateSyntaxError, "'%s' tag doesn't take any arguments." % bits[0]

    # Manually collect tokens for the tag's content, so Django's template
    # parser doesn't try to make sense of it.
    contents = []
    while 1:
        try:
            token = parser.next_token()
        except IndexError:
            # Reached the end of the template without finding the end tag
            raise TemplateSyntaxError("'endjinja' tag is required." % bits[0])
        if token.token_type == template.TOKEN_BLOCK and token.contents == 'endjinja':
            break
        contents.append(string_from_token(token))
    contents = ''.join(contents)

    return JinjaNode(jinja2.Template(contents))


class JinjaNode(template.Node):
    def __init__(self, template):
        self.template = template

        def render(self, django_context):
            # Jinja can't use Django's Context objects, so we have to
            # flatten it out to a single dictionary before using it.
            jinja_context = {}
            for layer in django_context:
                for key, value in layer.items():
                    if key not in jinja_context:
                        jinja_context[key] = value
            return self.template.render(jinja_context)
