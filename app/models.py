from __future__ import unicode_literals

from django.db import models

from django.contrib import admin
from django.contrib.auth.models import User


# Create your models here.

class Session(models.Model):
    #session_id = models.IntegerField(primary_key=True)
    selected_categories = models.CharField(max_length = 1000)
    recommended_categories = models.CharField(max_length = 1000)
    platform_used = models.CharField(max_length = 10) #could either be facebook or google
    name = models.CharField(max_length = 100, primary_key=True)
    date = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, default = None)
    #print 'model: session created'
    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.name
    def save(self, *args, **kwargs):
        super(Session, self).save(*args, **kwargs)





