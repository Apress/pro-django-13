from django.contrib import admin
from django import forms
from django_localflavor_us import forms as us_forms

from chapter10.properties import models


class InterestedPartyInline(admin.TabularInline):
    model = models.InterestedParty
    extra = 1


class PropertyFeatureInline(admin.TabularInline):
    model = models.PropertyFeature
    extra = 1


class PropertyForm(forms.ModelForm):
    state = us_forms.USStateField(widget=us_forms.USStateSelect)
    zip = us_forms.USZipCodeField(widget=forms.TextInput(attrs={'size': 10}))

    class Meta:
        model = models.Property


class PropertyAdmin(admin.ModelAdmin):
    form = PropertyForm
    fieldsets = (
        (None, {'fields': (('address', 'slug'),
                           ('city', 'state', 'zip'))}),
        ('Sales Information', {'fields': ('status',
                                          'price')}),
        ('Size', {'fields': ('square_feet',
                             'acreage')}),
    )
    inlines = (
        PropertyFeatureInline,
        InterestedPartyInline,
    )
    prepopulated_fields = {'slug': ('address', 'zip')}
admin.site.register(models.Property, PropertyAdmin)


class FeatureAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'definition'),
        }),
    )
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(models.Feature, FeatureAdmin)
