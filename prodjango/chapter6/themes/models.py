from django.db import models
from django import template
from django.contrib.auth.models import User

from chapter6.themes.managers import ThemeManager


class Theme(models.Model, template.Template):
    EDITING, PENDING, APPROVED = range(3)
    STATUS_CHOICES = (
        (EDITING, u'Editing'),
        (PENDING, u'Pending Approval'),
        (APPROVED, u'Approved'),
    )
    author = models.ForeignKey(User)
    title = models.CharField(max_length=255)
    template_string = models.TextField()
    css = models.URLField(null=True, blank=True)
    status = models.SmallIntegerField(choices=STATUS_CHOICES, default=EDITING)
    is_default = models.BooleanField()

    users = models.ManyToManyField(User, through='SelectedTheme')

    objects = ThemeManager()

    def __init__(self, *args, **kwargs):
        # super() won't work here, because the two __init__()
        # method signatures accept different sets of arguments
        models.Model.__init__(self, *args, **kwargs)
        template.Template.__init__(self, self.template_string,
                                   origin=repr(self), name=unicode(self))

    def save(self):
        if self.is_default:
            # Since only one theme can be the site-wide default, any new model that
            # is defined as default must remove the default setting from any other
            # theme before committing to the database.
            self.objects.all().update(is_default=False)
        super(Theme, self).save()

    def __unicode__(self):
        return self.title


class SelectedTheme(models.Model):
    user = models.OneToOneField(User)
    theme = models.ForeignKey(Theme)
