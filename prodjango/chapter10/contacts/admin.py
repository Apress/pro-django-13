from django.contrib import admin

from chapter10.contacts import models

class ContactAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Contact, ContactAdmin)
