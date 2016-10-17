from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect

from chapter11 import api


class ContactListView(api.ResourceListView):
    def form_valid(self, form):
        contact = form.save()

        return HttpResponseRedirect(reverse('contact_detail_api',
            slug=contact.user.username))


class ContactDetailView(api.ResourceDetailView):
    def form_valid(self, form):
        contact = form.save()
        
        return self.serialize_to_response(self.object)

