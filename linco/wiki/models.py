# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.contrib import admin
# Create your models here.
from django.conf import settings
from django.utils.timezone import now
User = settings.AUTH_USER_MODEL


class Category(models.Model):
    slug = models.SlugField()
    category_name = models.CharField(max_length=200, blank=True)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='child')

    def __unicode__(self):
        # full_path = [self.category_name]
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.category_name)
        #     k = k.parent
        # return ' -> '.join(full_path[::-1])
        return "%s" % self.category_name

    class Meta:
        verbose_name_plural = 'Categories'
        # enforcing that there can not be two categories under a parent with same slug
        unique_together = ('slug', 'parent',)
        ordering = ['category_name']

    def get_category_tree(self):
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)
        parse(self)
        return categorys

    def get_sub_categorys(self):
        categorys = []
        all_categorys = Category.objects.all()

        def parse(category):
            if category not in categorys:
                categorys.append(category)
            childs = all_categorys.filter(parent_category=category)
            for child in childs:
                if category not in categorys:
                    categorys.append(child)
                parse(child)
        parse(self)
        return categorys


class Wikientry(models.Model):

    owner = models.ForeignKey(User)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=200, blank=True)
    wiki_content = models.TextField(blank=True)
    last_edit = models.DateTimeField(auto_now=True, auto_now_add=False)
    created_time = models.DateTimeField(default=now)
    category = models.ForeignKey('Category', null=True, blank=True)

    def __unicode__(self):
        return "Subject:%s -- Content: %s" % (self.title, self.wiki_content[:20]+"...")

    def __str__(self):
        return self.title

    def get_cat_list(self):  # for now ignore this instance method,
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb)-1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]

    class Meta:
        ordering = ["-created_time", "-last_edit"]
        get_latest_by = 'last_edit'

    def get_absolute_url(self):
        return "/wiki/%s/" % self.id

    def get_category_tree(self):
        tree = self.category.get_category_tree()
