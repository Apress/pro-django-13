from django.forms import widgets


class PriceInput(widgets.TextInput):
    def render(self, name, value, attrs=None):
        return '$ %s' % super(PriceInput, self).render(name, value, attrs)


class PercentInput(widgets.TextInput):
    def render(self, name, value, attrs=None):
        return '%s %%' % super(PercentInput, self).render(name, value, attrs)
