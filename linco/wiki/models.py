# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib import admin
# Create your models here.
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Category(models.Model):
	slug = models.SlugField()
	category_name = models.CharField(max_length=200,blank=True)
	parent = models.ForeignKey('self', blank=True, null=True, related_name='child')
	
	def __unicode__(self):
		full_path = [self.category_name]
		k = self.parent
		while k is not None:
		    full_path.append(k.category_name)
		    k = k.parent
		return ' -> '.join(full_path[::-1])

	class Meta:
		verbose_name_plural = 'Categories'
		unique_together = ('slug', 'parent',) #enforcing that there can not be two categories under a parent with same slug
		ordering = ['category_name']




class Wikientry(models.Model):
	
	owner = models.ForeignKey(User)
	slug = models.SlugField(unique=True)
	title = models.CharField(max_length=200,blank=True)
	wiki_content=models.TextField(blank=True) 
	last_edit= models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	category = models.ForeignKey('Category', null=True, blank=True)
	
	def __unicode__(self):
		return "Subject:%s -- Content: %s" % (self.title, self.wiki_content[:20]+"...")
	
	def __str__(self):
		return self.title

	def get_cat_list(self):           #for now ignore this instance method,
	    k = self.category
	    breadcrumb = ["dummy"]
	    while k is not None:
	        breadcrumb.append(k.slug)
	        k = k.parent

	    for i in range(len(breadcrumb)-1):
	        breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
	    return breadcrumb[-1:0:-1]

	class Meta:
		ordering = ["-timestamp", "-last_edit"]