# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from wiki.models import Wikientry, Category
# Register your models here.
class WikientryAdmin(admin.ModelAdmin):
	list_display = ('title', 'last_edit')

admin.site.register(Wikientry, WikientryAdmin)
admin.site.register(Category)
#@admin.register(Wikientry)