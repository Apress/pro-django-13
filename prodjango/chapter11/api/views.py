import json
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View, DetailView, ListView, FormView
from django.views.generic.edit import BaseCreateView, BaseUpdateView

from chapter11.api import serializers


class ResourceView(View):
    serializer = None
    fields = None

    def get_fields(self):
        return self.fields

    def serialize(self, value):
        return self.serializer.serialize(value, fields=self.get_fields())


class JSONFormMixin(object):
    def get_form_kwargs(self):
        kwargs = super(JSONFormMixin, self).get_form_kwargs()
        kwargs['data'] = json.loads(self.request.body or '{}')
        return kwargs

    def serialize_to_response(self, data):
        return HttpResponse(self.serialize(data), content_type='application/json')

    def form_invalid(self, form):
        return HttpResponseBadRequest(json.dumps(form.errors),
            content_type='application/json')


class ResourceCreateView(JSONFormMixin, BaseCreateView):
    def post(self, request, *args, **kwargs):
        if not self.form_class:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super(ResourceCreateView, self).post(request, *args, **kwargs)


class ResourceUpdateView(JSONFormMixin, BaseUpdateView):
    def put(self, request, *args, **kwargs):
        if not self.form_class:
            return self.http_method_not_allowed(request, *args, **kwargs)

        return super(ResourceUpdateView, self).put(request, *args, **kwargs)


class ResourceListView(ResourceView, ResourceCreateView, ListView):
    form_class = None
    serializer = serializers.QuerySetSerializer()

    http_method_names = ['GET', 'POST']

    def render_to_response(self, context):
        return self.serialize_to_response(context['object_list'])


class ResourceDetailView(ResourceView, ResourceUpdateView, DetailView):
    form_class = None
    serializer = serializers.SingleObjectSerializer()

    http_method_names = ['GET', 'PUT']

    def get_fields(self):
        fields = super(ResourceDetailView, self).get_fields()

        # Also get fields form a form if available
        if not fields and self.form_class:
            return self.form_class.base_fields.keys()
        return fields

    def render_to_response(self, context):
        return self.serialize_to_response(context['object'])

