from django.conf.urls import *
from django.views.generic import ListView, DetailView

from chapter10.properties import models

urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(queryset=models.Property.objects.listed(),
                         template_name='properties/list.html',
                         paginate_by=25),
        name='property_list'),
    url(r'^(?P<slug>\d+-[\w-]+-\d+)/$',
        DetailView.as_view(queryset=models.Property.objects.listed(),
                           slug_field='slug',
                           template_name='properties/detail.html'),
        name='property_detail'),
)
