from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from chapter11 import api


class PropertyListView(api.ResourceListView):
    def form_valid(self, form):
        property = form.save()

        return HttpResponseRedirect(reverse('property_detail_api',
            kwargs={'slug': property.slug}))


class PropertyDetailView(api.ResourceDetailView):
    def form_valid(self, form):
        property = form.save()

        return self.serialize_to_response(self.object)

