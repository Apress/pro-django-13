from django.conf.urls import *
from django.contrib.auth.models import User, Group

from chapter10.contacts.models import Contact
from chapter10.contacts import forms, api_views
from chapter11 import api

api.serialize_fields(Contact, forms.ContactEditorForm.base_fields.keys() + ['user'])
api.serialize_fields(User, forms.UserEditorForm.base_fields.keys() + ['groups'])
api.serialize_fields(Group, ['name'])

urlpatterns = patterns('',
    url(r'^$',
        api_views.ContactListView.as_view(
            queryset=Contact.objects.all(),
            form_class=forms.ContactEditorForm,
#            fields=forms.ContactEditorForm.base_fields.keys() + ['user'],
        ), name='contact_list_api'),
    url(r'^(?P<slug>[\w-]+)/$',
        api_views.ContactDetailView.as_view(
            queryset=Contact.objects.all(),
            slug_field='user__username',
            form_class=forms.ContactEditorForm,
            fields=forms.ContactEditorForm.base_fields.keys() + ['user'],
        ), name='contact_detail_api'),
)
