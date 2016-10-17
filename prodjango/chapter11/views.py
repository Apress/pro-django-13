from chapter10.contacts import models
from chapter11 import api


class ContactList(api.ResourceView):
    @api.scope('contacts:read')
    def get(self, request):
        contacts = models.Contact.objects.all()
        return self.serialize(contacts)


class Contact(api.ResourceView)
#    @api.scope('contacts:read')
    def get(self, request, username):
        contact = get_object_or_404(models.Contact, user__username=username)
        return self.serialize_one(contact)

#    @api.scope('contacts:write')
    def post(self, request, username):
        contact = get_object_or_404(models.Contact, user__username=username)
        return self.serialize(contact)
