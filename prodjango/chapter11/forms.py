from django import forms
from chapter10.contacts import models


class ContactForm(forms.ModelForm):
    class Meta:
        model = models.Contact
        fields = ['user']
