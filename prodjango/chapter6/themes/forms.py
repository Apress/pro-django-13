from django import forms
from django import template
from django.template.loader_tags import BlockNode, ExtendsNode
from django.conf import settings

from chapter6.theme import models


class ThemeForm(forms.ModelForm):
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def clean_body(self):
        try:
            tpl = template.Template(self.cleaned_data['body'])
        except template.TemplateSyntaxError as e:
            # The template is invalid, which is an input error.
            raise forms.ValidationError(unicode(e))

        if [type(n) for n in tpl.nodelist] != [ExtendsNode] or \
            tpl.nodelist[0].parent_name != settings.THEME_EXTENDS:
                # No 'extends' tag was found
                error_msg = u"Template must extend '%s'" % settings.THEME_EXTENDS
                raise forms.ValidationError(error_msg)

        if [type(n) for n in tpl.nodelist[0].nodelist] != [BlockNode] or \
            tpl.nodelist[0].nodelist[0].name != settings.THEME_CONTAINER_BLOCK:
                # Didn't find exactly one block tag with the required name
                error_msg = u"Theme needs exactly one '%s' block " % \
                            settings.THEME_CONTAINER_BLOCK
                raise forms.ValidationError(error_msg)

            required_blocks = list(settings.THEME_BLOCKS[:])
            for node in tpl.nodelist[0].nodelist[0].nodelist:
                if type(node) is BlockNode:
                    if node.name not in required_blocks:
                        error_msg = u"'%s' is not valid for themes." % node.name
                        raise forms.ValidationError(error_msg)
                    required_blocks.remove(node.name)
                    if node.nodelist:
                        error_msg = u"'%s' block must be empty." % node.name
                        raise forms.ValidationError(error_msg)
                elif type(node) is template.TextNode:
                    # Text nodes between blocks are acceptable.
                    pass
                else:
                    # All other tags, including variables, are invalid.
                    error_msg = u"Only 'extends', 'block' and plain text are allowed."
                    raise forms.ValidationError(error_msg)

            if required_blocks:
                # Some blocks were missing from the template.
                blocks = ', '.join(map(repr, required_blocks))
                error_msg = u"The following blocks must be defined: %s" % blocks
                raise forms.ValidationError(error_msg)

        class Meta:
            model = models.Theme
