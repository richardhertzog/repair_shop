# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
# id, dropoff, pickup, mechanic, repair_type
class Service(models.Model):
    dropoff = models.CharField(max_length=100)
    pickup = models.CharField(max_length=100)
    mechanic = models.CharField(max_length=50)
    repair_type = models.CharField(max_length=10)
