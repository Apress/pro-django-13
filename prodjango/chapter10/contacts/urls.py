from django.conf.urls import *
from django.views.generic import ListView, DetailView

from chapter10.contacts import models, views

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=models.Contact.objects.all(),
            template_name='contacts/list.html',
            paginate_by=25,
        ), name='contact_list'),
    url(r'^add/$', views.EditContact.as_view(
            template_name='contacts/editor_form.html',
        ), name='contact_add_form'),
    url(r'^(?P<slug>[\w-]+)/$',
        DetailView.as_view(queryset=models.Contact.objects.all(),
                           slug_field='user__username',
                           template_name='contacts/detail.html'),
        name='contact_detail'),
    url(r'^(?P<username>[\w-]+)/edit/$', views.EditContact.as_view(
            template_name='contacts/editor_form.html',
        ), name='contact_edit_form'),
)
