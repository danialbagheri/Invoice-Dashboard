# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Supplier, Invoices
from django.contrib import admin

# Register your models here.
admin.site.register(Supplier)
admin.site.register(Invoices)