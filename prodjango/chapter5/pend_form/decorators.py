from django import http
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils.functional import wraps


def pend_form(view):
    @wraps(view)
    def wrapper(request, form_class, template_name,
                form_hash=None, *args, **kwargs):
        if request.method == 'POST':
            form = form_class(request.POST)
            if 'pend' in request.POST:
                form_hash = form.pend()
                return http.HttpRedirect(form_hash)
            else:
                if form.is_valid():
                    return view(request, form=form, *args, **kwargs)
                else:
                    if form_hash:
                        form = form_class.resume(form_hash)
                    else:
                        form = form_class()
                return render_to_response(template_name, {'form': form},
                                          context_instance=RequestContext(request))
    return wrapper
