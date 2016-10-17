from django.db import models
from django.contrib.auth.models import User
from django_localflavor_us import models as us_models


class Contact(models.Model):
    user = models.OneToOneField(User)
    phone_number = us_models.PhoneNumberField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = us_models.USStateField()
    zip_code = models.CharField(max_length=255)

    class Meta:
        ordering = ('user__last_name', 'user__first_name')

    def __unicode__(self):
        return self.user.get_full_name()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def get_full_name(self):
        return self.user.get_full_name()
