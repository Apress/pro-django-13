from django.conf.urls import *

from chapter10.properties.models import Property, Feature, PropertyFeature
from chapter10.properties import forms, api_views
from chapter11 import api

api.serialize_fields(Property, forms.PropertyForm.base_fields.keys())
api.serialize_fields(Feature, ['title', 'description'])
#api.serialize_fields(PropertyFeature, ['description'])

urlpatterns = patterns('',
    url(r'^$',
        api_views.PropertyListView.as_view(
            queryset=Property.objects.all(),
            form_class=forms.PropertyForm,
        ), name='property_list_api'),
    url(r'^(?P<slug>[\w-]+)/$',
        api_views.PropertyDetailView.as_view(
            queryset=Property.objects.all(),
            form_class=forms.PropertyForm,
        ), name='property_detail_api'),
)
