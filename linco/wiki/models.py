# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib import admin
# Create your models here.
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Wikientry(models.Model):
	owner = models.ForeignKey(User)
	subject = models.CharField(max_length=200,blank=True)
	wiki_content=models.TextField(blank=True) 
	last_edit=models.DateField('Last Edit', default=datetime.datetime.now, editable=True)
	def __unicode__(self):
		return "Subject:%s -- Content: %s" % (self.subject, self.wiki_content[:20]+"...")
