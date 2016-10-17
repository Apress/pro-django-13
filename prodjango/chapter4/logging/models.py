from datetime import datetime

from django.db import models


class Entry(models.Model):
    path = models.CharField(max_length=255)
    type = models.CharField(max_length=255, db_index=True)
    date = models.DateTimeField(default=datetime.utcnow, db_index=True)
    description = models.TextField()
