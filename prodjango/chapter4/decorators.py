from django.utils.functional import wraps
from django.shortcuts import get_object_or_404
from django.template.loader import get_template
from django.template.context import RequestContext
from django.core.serializers.json import DjangoJSONEncoder

from news.models import Article


def set_test_cookie(view):
    """
    Automatically sets the test cookie on all anonymous users,
    so that they can be logged in more easily, without having
    to hit a separate login page.
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_anonymous():
            request.session.set_test_cookie()
        return view(request, *args, **kwargs)
    return wraps(view)(wrapper)


def get_article_from_id(view):
    """
    Retrieves a specific article, passing it to the view directly
    """
    def wrapper(request, id, *args, **kwargs):
        article = get_object_or_404(Article, id=int(id))
        return view(request, article=article, *args, **kwargs)
    return wraps(view)(wrapper)


def content_type(c_type):
    """
    Overrides the Content-Type provided by the view.
    Accepts a single argument, the new Content-Type
    value to be written to the outgoing response.
    """
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            response['Content-Type'] = c_type
            return response
        return wraps(view)(wrapper)
    return decorator
