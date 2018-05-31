# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.db.models import Q

class InvoicesManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(our_ref__icontains=query) | 
                         # Q(supplier_name__icontains=query)|
                         Q(supplier_ref__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
            return qs
        else:
    		return "Didn't match"



class Supplier(models.Model):
	supplier_name = models.CharField(max_length=200,blank=True)
	vat_number = models.IntegerField(blank=True, null=True)
	def __unicode__(self):
		return "%s" % (self.supplier_name)
		
# A directory path for each supplier
# def user_directory_path(supplier, filename):
# 	return 'user_{0}/%Y/%M/{1}'.format(supplier.supplier_name, filename)

class Invoices(models.Model):
	"""docstring for ClassName"""
	supplier_name = models.ForeignKey('Supplier',on_delete=models.CASCADE)
	supplier_ref = models.CharField(max_length=100,blank=True)
	our_ref = models.CharField(max_length=100)
	invoice = models.FileField(upload_to='invoice/%Y/%M/')
	approved = models.BooleanField(default=False)
	invoice_date = models.DateTimeField('invoice date', default=datetime.datetime.now, editable=True)

	objects = InvoicesManager()
	def __unicode__(self):
		return "{} - {}".format(self.supplier_name, self.our_ref)


