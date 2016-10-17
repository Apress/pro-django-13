from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from chapter10.contacts import forms, models


class EditContact(TemplateView):
    def get_objects(self, username):
        # Set up some objects if none were defined
        if username:
            user = get_object_or_404(models.User, username=username)
            try:
                contact = user.contact
            except models.Contact.DoesNotExist:
                contact = models.Contact(user=user)
        else:
            user = models.User()
            contact = models.Contact(user=user)

        return user, contact

    def get(self, request, username=None):
        user, contact = self.get_objects(username)

        return self.render_to_response({
            'username': username,
            'user_form': forms.UserEditorForm(instance=user),
            'contact_form': forms.ContactEditorForm(instance=contact),
        })

    def post(self, request, username=None):
        user, contact = self.get_objects(username)

        user_form = forms.UserEditorForm(request.POST, instance=user)
        contact_form = forms.ContactEditorForm(request.POST, instance=contact)

        if user_form.is_valid() and contact_form.is_valid():
            user = user_form.save()
            # Attach the user to the form before saving
            contact = contact_form.save(commit=False)
            contact.user = user
            contact.save()
            return HttpResponseRedirect(reverse('contact_detail',
                                                kwargs={'slug': user.username}))

        return self.render_to_response({
            'username': username,
            'user_form': user_form,
            'contact_form': contact_form,
        })
