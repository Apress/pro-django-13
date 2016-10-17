from django.db import models
from django_localflavor_us import models as us_models

from chapter10.contacts.models import Contact


class PropertyManager(models.Manager):
    def listed(self):
        qs = super(PropertyManager, self).get_query_set()
        return qs.filter(models.Q(status=Property.LISTED) | \
                         models.Q(status=Property.PENDING))


class Property(models.Model):
    LISTED, PENDING, SOLD = range(3)
    STATUS_CHOICES = (
        (LISTED, 'Listed'),
        (PENDING, 'Pending Sale'),
        (SOLD, 'Sold'),
    )

    slug = models.SlugField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = us_models.USStateField()
    zip = models.CharField(max_length=255)
    square_feet = models.PositiveIntegerField(null=True, blank=True)
    acreage = models.FloatField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,
                                              default=LISTED,
                                              null=True, blank=True)
    price = models.PositiveIntegerField(null=True, blank=True)
    features = models.ManyToManyField('Feature', through='PropertyFeature', blank=True)
    interested_parties = models.ManyToManyField(Contact,
                                                through='InterestedParty', blank=True)

    objects = PropertyManager()

    class Meta:
        verbose_name_plural = 'properties'

    def __unicode__(self):
        return u'%s, %s' % (self.address, self.city)

class Feature(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255)
    definition = models.TextField()

    def __unicode__(self):
        return self.title

class PropertyFeature(models.Model):
    property = models.ForeignKey(Property)
    feature = models.ForeignKey(Feature)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return unicode(self.feature)

class InterestedParty(models.Model):
    BUILDER, OWNER, BUYER, AGENT, INSPECTOR = range(5)
    INTEREST_CHOICES = (
        (BUILDER, 'Builder'),
        (OWNER, 'Owner'),
        (BUYER, 'Buyer'),
        (AGENT, 'Agent'),
        (INSPECTOR, 'Inspector'),
    )
    property = models.ForeignKey(Property)
    contact = models.ForeignKey(Contact)
    interest = models.PositiveSmallIntegerField(choices=INTEREST_CHOICES)

    class Meta:
        verbose_name_plural = 'interested parties'

    def __unicode__(self):
        return u'%s, %s' % (self.contact, self.get_interest_display())
