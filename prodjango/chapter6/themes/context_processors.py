from django.conf import settings

from chapter6.themes.models import Theme


def theme(request):
    if hasattr(request, 'user') and request.user.is_authenticated():
        # A valid user is logged in, so use the manager method
        theme = Theme.objects.get_current_theme(user)
    else:
        # The user isn't logged in, so fall back to the default
        theme = Theme.objects.get(is_default=True)
    name = getattr(settings, 'THEME_CONTEXT_NAME', 'theme')
    return {name: theme}
