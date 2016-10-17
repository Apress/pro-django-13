from django.db import models


class PendedForm(models.Model):
    form_class = models.CharField(max_length=255)
    hash = models.CharField(max_length=32)


class PendedValue(models.Model):
    form = models.ForeignKey(PendedForm, related_name='data')
    name = models.CharField(max_length=255)
    value = models.TextField()
