from django import forms
from django.forms.forms import pretty_name
from django_localflavor_us import forms as us_forms
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict

from chapter10.properties.models import Property


class PropertyForm(forms.ModelForm):
    state = us_forms.USStateField()

    class Meta:
        model = Property
        exclude = ['interested_parties', 'features']
