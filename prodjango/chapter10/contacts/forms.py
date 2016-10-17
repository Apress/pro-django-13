from itertools import chain

from django import forms
from django.forms.forms import pretty_name
from django_localflavor_us import forms as us_forms
from django.contrib.auth.models import User
from django.utils.datastructures import SortedDict

from chapter10.contacts.models import Contact


class UserEditorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ContactEditorForm(forms.ModelForm):
    phone_number = us_forms.USPhoneNumberField()
    state = us_forms.USStateField(widget=us_forms.USStateSelect)
    zip_code = us_forms.USZipCodeField(label='ZIP Code')

    class Meta:
        model = Contact
        exclude = ('user',)
